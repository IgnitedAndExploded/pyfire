# -*- coding: utf-8 -*-
"""
    pyfire.xmppconnection
    ~~~~~~~~~~~~~

    Handles a XMPP Stream (connection)

    :copyright: (c) 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import SocketServer
import socket
from xml.sax import make_parser as sax_make_parser
import xml.etree.ElementTree as ET

from pyfire import streamprocessor
from pyfire.elements import TagHandler

class XMPPConnection(SocketServer.BaseRequestHandler):

    def handle(self):
        """Starts the handling for a new connection"""

        # create stream processor
        self.parser = sax_make_parser(['xml.sax.expatreader'])
        self.taghandler = TagHandler(self)
        self.processor = streamprocessor.XMPPContentHandler(
                                self.taghandler.streamhandler,
                                self.taghandler.contenthandler)
        self.parser.setContentHandler(self.processor)

        # TCP loop
        self.request.settimeout(0.1)
        self.running = True
        while(self.running):
            try:
                data = self.request.recv(2048)
                # if no data received, the socket seems to have closed
                # so terminate the connection
                if not data:
                    break
                self.parser.feed(data)
            except socket.timeout:
                pass

        # close client stream
        self.request.send("</stream:stream>")
        try:
            self.request.shutdown(socket.SHUT_RDWR)
        except socket.error:
            pass
        self.request.close()

    def stop_connection(self):
        self.running = False

    def send_string(self, string):
        """Send a string to client"""
        self.request.send(string)

    def send_element(self, element):
        """Serialize and send an ET Element"""

        self.request.send(ET.tostring(element))
