# -*- coding: utf-8 -*-
"""
    pyfire.xmppconnection
    ~~~~~~~~~~~~~

    This module implements the basic XMPP communication server-side.

    :copyright: (c) 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import SocketServer
from socket import SHUT_RDWR, timeout
from time import sleep

from xml import sax
from xml.etree.ElementTree import Element, tostring
import streamprocessor

import uuid
import auth, iq, presence


class XMPPConnection(SocketServer.BaseRequestHandler):

    def streamhandler(self, attrs):
        """ handles an incomming stream start """
        print "Detected stream handlerattr.."
        if attrs == {}:
            self.running = 0;
        else:
            # FIXME: set real from attribute based on config
            self.request.send("""<?xml version='1.0'?><stream:stream xmlns="%s" from="%s" id="%s" version="1.0" xml:lang="en" xmlns:stream="http://etherx.jabber.org/streams">""" % (attrs.getValue("xmlns"), attrs.getValue("to"), uuid.uuid4().hex ) )
            self.sendElement( self.features )

    def contenthandler(self, tree):
        """ handles an incomming content tree """
        print "Detected stream content data.."

        if tree.tag == "auth":
            try:
                req = auth.Auth()
                req.handle( tree )
                self.authenticated = 1
                self.parser.reset()

                # reset features to announce we have bind support
                bind = Element( "bind" )
                bind.set("xmlns", "urn:ietf:params:xml:ns:xmpp-bind")
                session = Element( "session" )
                session.set("xmlns", "urn:ietf:params:xml:ns:xmpp-session")
                self.features = Element( "stream:features" )
                self.features.append( bind )
                self.features.append( session )

                # Tell client, the auth has succeted
                resp = Element("success")
                resp.set("xmlns", "urn:ietf:params:xml:ns:xmpp-sasl")
                self.sendElement( resp )

            except auth.saslException, e:
                self.request.send( str(e) )
        elif tree.tag == "iq":
            req = iq.Iq()
            resp = req.handle( tree )
            self.sendElement( resp )
        elif tree.tag == "presence":
            req = presence.Presence()
            resp = req.handle( tree )
            self.sendElement( resp )

    def handle(self):
        """ Starts the handling for a new connection """
        print "New connection from %s:%i" % self.client_address

        # fetch supported mechanisms from auth module
        self.features = Element("stream:features")
        mechanisms = Element("mechanisms")
        mechanisms.set("xmlns", "urn:ietf:params:xml:ns:xmpp-sasl")
        for mech in auth.supportedMechs:
            elm = Element("mechanism")
            elm.text = mech
            mechanisms.append( elm )
        self.features.append(mechanisms)

        self.request.settimeout(0.1)
        self.running = 1
        self.authenticated = 0

        self.parser = sax.make_parser(['xml.sax.expatreader'])
        self.handler = streamprocessor.XMPPContentHandler( self.streamhandler, self.contenthandler )
        self.parser.setContentHandler( self.handler )

        while( self.running ):
            ## main loop
            try:
                data = self.request.recv( 2048 )
                # if not data received the socket seems to have closed so terminate the connection
                if not data:
                    break
                self.parser.feed( data )
            except timeout:
                pass

        # close client stream
        self.request.send("""</stream:stream>""")
        self.request.shutdown(SHUT_RDWR)
        self.request.close()

    def finish(self):
        """ called upon socket shutdown either from client- or severside """
        print "Connection closed..."

    def sendElement(self, element):
        """ Function to send out and Element() object """
        self.request.send( tostring( element ) )
