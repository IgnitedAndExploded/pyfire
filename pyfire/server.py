from datetime import datetime
import errno
import fcntl
import os
import socket
import sys
import traceback
import xml.etree.ElementTree as ET

from zmq.eventloop import ioloop
from tornado import iostream
from tornado import stack_context

from pyfire import configuration as config
from pyfire.auth.backends import DummyTrueValidator
from pyfire.auth.registry import AuthHandlerRegistry, ValidationRegistry
from pyfire.errors import XMPPProtocolError
from pyfire.logger import Logger
from pyfire.stream import processor
from pyfire.stream.stanzas import TagHandler

log = Logger(__name__)


class XMPPServer(object):
    """A non-blocking, single-threaded XMPP server."""

    def __init__(self, io_loop=None):

        self.io_loop = io_loop
        self._sockets = {}  # fd -> socket object
        self._started = False
        self._connections = {}
        self.checker = ioloop.PeriodicCallback(
            self.check_for_closed_connections, 30000)

    def listen(self, port, address=""):
        """Binds to the given port and starts the server in a single process.

        This method is a shortcut for:

            server.bind(port, address)
            server.start()

        """
        self.bind(port, address)
        self.start()

    def bind(self, port, address=None, family=socket.AF_UNSPEC):
        """Binds this server to the given port on the given address.

        To start the server, call start(). You can call listen() as
        a shortcut to the sequence of bind() and start() calls.

        Address may be either an IP address or hostname.  If it's a hostname,
        the server will listen on all IP addresses associated with the
        name.  Address may be an empty string or None to listen on all
        available interfaces.  Family may be set to either socket.AF_INET
        or socket.AF_INET6 to restrict to ipv4 or ipv6 addresses, otherwise
        both will be used if available.

        This method may be called multiple times prior to start() to listen
        on multiple ports or interfaces.
        """
        if address == "":
            address = None
        for res in socket.getaddrinfo(address, port, family,
                                      socket.SOCK_STREAM, 0,
                                      socket.AI_PASSIVE | socket.AI_ADDRCONFIG):
            af, socktype, proto, canonname, sockaddr = res
            sock = socket.socket(af, socktype, proto)
            flags = fcntl.fcntl(sock.fileno(), fcntl.F_GETFD)
            flags |= fcntl.FD_CLOEXEC
            fcntl.fcntl(sock.fileno(), fcntl.F_SETFD, flags)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if af == socket.AF_INET6:
                # On linux, ipv6 sockets accept ipv4 too by default,
                # but this makes it impossible to bind to both
                # 0.0.0.0 in ipv4 and :: in ipv6.  On other systems,
                # separate sockets *must* be used to listen for both ipv4
                # and ipv6.  For consistency, always disable ipv4 on our
                # ipv6 sockets and use a separate ipv4 socket when needed.
                if hasattr(socket, "IPPROTO_IPV6"):
                    sock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
            sock.setblocking(0)
            sock.bind(sockaddr)
            sock.listen(128)
            log.info("Starting to listen on IP %s Port %s for connections" % sockaddr)
            self._sockets[sock.fileno()] = sock
            if self._started:
                self.io_loop.add_handler(sock.fileno(), self._handle_events,
                                         ioloop.IOLoop.READ)

    def start(self):
        """Starts this server in the IOLoop."""

        assert not self._started
        if not self.io_loop:
            self.io_loop = ioloop.IOLoop.instance()
        for fd in self._sockets.keys():
            self.io_loop.add_handler(fd, self._handle_events,
                                     ioloop.IOLoop.READ)

    def stop(self):
        """Stops listening for new connections.

        Streams currently running may still continue after the
        server is stopped.
        """
        for fd, sock in self._sockets.iteritems():
            self.io_loop.remove_handler(fd)
            sock.close()

    def _handle_events(self, fd, events):
        while True:
            try:
                connection, address = self._sockets[fd].accept()
            except socket.error, e:
                if e.args[0] in (errno.EWOULDBLOCK, errno.EAGAIN):
                    return
                raise
            try:
                #import pdb;pdb.set_trace()
                stream = iostream.IOStream(connection, io_loop=self.io_loop)
                log.info("Starting new connection for client connection from %s:%s" % address)
                self._connections[address] = XMPPConnection(stream, address)
                if not self.checker._running:
                    self.checker.start()
            except Exception, e:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                log.error("Error in connection callback, %s" % str(e))
                for line in traceback.format_tb(exc_traceback):
                    if line.find("\n") >= 0:
                        for subline in line.split("\n"):
                            log.error(subline)
                    else:
                        log.error(line.rstrip("\n"))

    def check_for_closed_connections(self):
        log.debug("checking for closed connections")
        for address in self._connections.keys():
            connection = self._connections[address]
            if connection.closed():
                log.debug("detected dead stream/connection: %s:%s" % connection.address)
                del self._connections[address]
                if len(self._connections) == 0:
                    log.debug("stopping checker")
                    self.checker.stop()


class XMPPConnection(object):
    """One XMPP connection initiated by class:`XMPPServer`"""

    def __init__(self, stream, address):
        self.stream = stream
        self.address = address
        self.connectiontime = self.last_seen = datetime.now()

        self.taghandler = TagHandler(self)
        self.parser = processor.StreamProcessor(
                            self.taghandler.streamhandler,
                            self.taghandler.contenthandler)

        # TODO: Find a better place for this
        validation_registry = ValidationRegistry()
        self.auth_registry = AuthHandlerRegistry(validation_registry)

        validator = DummyTrueValidator()
        validation_registry.register('dummy', validator)
        self.stream.read_bytes(1, self._read_char)

    def _read_char(self, data):
        """Reads from client in byte mode"""

        try:
            if data == " ":
                log.debug("Found whitespace keepalive")
                self.stream.read_bytes(1, self._read_char)
            else:
                log.debug("Processing byte: %s" % data)
                self.parser.feed(data)
                self.stream.read_until(">", self._read_xml)
            self.last_seen = datetime.now()
        except IOError:
            self.done()

    def _read_xml(self, data):
        """Reads from client until closing tag for xml is found"""

        try:
            self.last_seen = datetime.now()
            log.debug("Processing chunk: %s" % data)
            self.parser.feed(data)
            if self.parser.depth >= 2:
                self.stream.read_until(">", self._read_xml)
            else:
                self.stream.read_bytes(1, self._read_char)
        except IOError:
            self.done()

    def send_string(self, string):
        """Sends a string to client"""

        log.debug("Sending string to client:" + string)
        self.stream.write(string)

    def send_element(self, element):
        """Serializes and send an ET Element"""

        string = ET.tostring(element)
        log.debug("Sending element to client:" + string)
        self.stream.write(string)

    def stop_connection(self):
        """Sends stream close, discards stream closed errors"""

        try:
            self.stream.write("</stream:stream>")
        except IOError:
            pass

    def done(self):
        """Does cleanup work"""

        self.stream.close()

    def closed(self):
        """Checks if underlying stream is closed"""

        return self.stream.closed()
