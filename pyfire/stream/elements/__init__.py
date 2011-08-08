# -*- coding: utf-8 -*-
"""
    pyfire.stream.elements
    ~~~~~~~~~~~~~~~~~~~~~~

    Process stream events and redirect to tag handlers

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import uuid
import xml.etree.ElementTree as ET

import pyfire.configuration as config
from pyfire.jid import JID
from pyfire.stream.elements import iq, message, presence
from pyfire.stream.errors import HostUnknownError, StreamError, UnsupportedVersionError


class TagHandler(object):

    def __init__(self, connection):
        super(TagHandler, self).__init__()
        self.connection = connection
        self.server = connection.server
        self.send_element = connection.send_element
        self.send_string = connection.send_string

        self.jid = None
        self.hostname = None

        self.authenticated = False

        self.iq = iq.Iq(self)
        self.message = message.Message(self)
        self.presence = presence.Presence(self)

    def contenthandler(self, tree):
        """Handles an incomming content tree"""

        # set/replace the from attribute in stanzas as required
        # by RFC 6120 Section 8.1.2.1
        if self.authenticated:
            tree.set("from", self.jid)

        try:
            response_element = None
            if tree.tag == "auth":
                registry = self.server.auth_registry
                namespace = tree.get('xmlns')
                handler = registry.request_handler(namespace)
                handler.process(tree)
                self.connection.parser.reset()
                self.jid = JID("@".join([handler.authenticated_user,
                                         self.hostname]))
                self.authenticated = True
                response_element = ET.Element("success")
                response_element.set("xmlns", namespace)
            elif tree.tag == "iq":
                response_element = self.iq.handle(tree)
            elif tree.tag == "message":
                response_element = self.message.handle(tree)
            elif tree.tag == "presence":
                response_element = self.presence.handle(tree)

            if response_element is not None:
                self.send_element(response_element)
        except StreamError, e:
            self.send_string(unicode(e))

    def add_auth_options(self, feature_element):
        """Add supported auth mechanisms to feature element"""
        registry = self.server.auth_registry

        for mechtype in registry.supported_namespaces:
            mechtype_element = ET.SubElement(feature_element, "mechanisms")
            mechtype_element.set("xmlns", mechtype)
            handler = registry.request_handler(mechtype)
            for mech in handler.supported_mechs:
                mech_element = ET.SubElement(mechtype_element, 'mechanism')
                mech_element.text = mech
            mechanisms = ET.Element("mechanisms")

    def add_server_features(self, feature_element):
        bind = ET.SubElement(feature_element, "bind")
        bind.set("xmlns", "urn:ietf:params:xml:ns:xmpp-bind")

        # Session establishment is deprecated in RFC6121 but Appendix E
        # suggests to still advertise it as feature for compatibility.
        session = ET.SubElement(feature_element, "session")
        session.set("xmlns", "urn:ietf:params:xml:ns:xmpp-session")

    def streamhandler(self, attrs):
        """Handles a stream start"""

        if attrs == {}:
            # </stream:stream> received
            self.connection.stop_connection()
        else:
            # check if we are responsible for this stream
            self.hostname = attrs.getValue("to")
            if self.hostname not in config.getlist("listeners", "domains"):
                raise HostUnknownError

            remote_version = attrs.getValue("version")
            if remote_version is not None:
                if remote_version != "1.0":
                    raise UnsupportedVersionError

            # Stream restart
            stream = ET.Element("stream:stream")
            stream.set("xmlns", attrs.getValue("xmlns"))
            stream.set("from", self.hostname)
            stream.set("id", uuid.uuid4().hex)
            # only include version in response if client sent its max supported
            # version (RFC6120 Section 4.7.5)
            if remote_version is not None:
                stream.set("version", "1.0")
            stream.set("xml:lang", "en")
            stream.set("xmlns:stream", "http://etherx.jabber.org/streams")
            start_stream = """<?xml version="1.0"?>""" + ET.tostring(stream)
            # Element has subitems but are added later to the stream,
            # so don't mark it a single element
            self.send_string(start_stream.replace("/>", ">"))

            # Make a list of supported features
            features = ET.Element("stream:features")
            if not self.authenticated:
                self.add_auth_options(features)
            else:
                self.add_server_features(features)

            self.send_element(features)
