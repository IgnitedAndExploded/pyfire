# -*- coding: utf-8 -*-
"""
    pyfire.stream.socket
    ~~~~~~~~~~~~~~~~~~~~

    Handles a XMPP Stream (connection)

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import SocketServer
import socket
import xml.etree.ElementTree as ET

from pyfire.logger import Logger
from pyfire.stream import processor
from pyfire.stream.stanzas import TagHandler
from pyfire.stream.errors import StreamError

log = Logger(__name__)


class XMPPSocketHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        """Starts the handling for a new connection"""

        # init StreamProcessor
        self.taghandler = TagHandler(self)
        self.parser = processor.StreamProcessor(
                            self.taghandler.streamhandler,
                            self.taghandler.contenthandler)

        # TCP loop
        self.request.settimeout(0.1)
        self.running = True
        log.debug("Entering Stream Loop")
        while(self.running):
            try:
                data = self.request.recv(2048)
                # if no data received, the socket seems to have closed
                # so terminate the connection
                if not data:
                    break
                log.debug("Received data from client:" + data)
                self.parser.feed(data)
            except StreamError, e:
                self.send_string(unicode(e))
                # Stream errors are unrecoverable so terminate the connection
                self.stop_connection()
            except socket.timeout:
                pass

        # close client stream
        log.debug("Sending stream end")
        self.request.send("</stream:stream>")
        try:
            self.request.shutdown(socket.SHUT_RDWR)
        except socket.error:
            pass
        log.debug("Shutting request down")
        self.request.close()

    def stop_connection(self):
        self.running = False

    def send_string(self, string):
        """Send a string to client"""
        log.debug("Sending string to client:" + string)
        self.request.send(string)

    def send_element(self, element):
        """Serialize and send an ET Element"""
        string = ET.tostring(element)
        log.debug("Sending element to client:" + string)
        self.request.send(string)
