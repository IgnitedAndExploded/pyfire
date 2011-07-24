# -*- coding: utf-8 -*-
"""
    pyfire.tests.test_streamprocessor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Unittests for streamprocessor

    :copyright: (c) 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from xml import sax
import xml.etree.ElementTree as ET

from pyfire.tests import PyfireTestCase

from pyfire import streamprocessor

STREAMSTART = """<?xml version='1.0'?><stream:stream xmlns="jabber:client" to="localhost" version="1.0" xmlns:stream="http://etherx.jabber.org/streams">"""

class Test_contenthandler(PyfireTestCase):

    def fakestreamhandler(self, attrs):
        self.lastattrs = attrs

    def fakecontenthandler(self, tree):
        self.lasttree = tree

    def setUp(self):
        self.lastattrs = None
        self.lasttree = None
        self.parser = sax.make_parser(['xml.sax.expatreader'])
        self.handler = streamprocessor.XMPPContentHandler(self.fakestreamhandler, self.fakecontenthandler)
        self.parser.setContentHandler(self.handler)

    def tearDown(self):
        try:
            self.parser.close()
        except sax.SAXParseException:
            pass

    def test_client_streamstart(self):
        self.parser.feed(STREAMSTART)
        self.assertEqual(len(self.lastattrs.keys()), 4)

    def test_bad_start(self):
        teststring = """<?xml version='1.0'?><hello>"""
        with self.assertRaises(streamprocessor.UnknownStreamException) as cm:
            self.parser.feed(teststring)

    def test_treeparse(self):
        teststring = """<iq id="yhc13a95" type="set"><bind xmlns="urn:ietf:params:xml:ns:xmpp-bind"><resource>balcony</resource></bind></iq>"""
        self.parser.feed(STREAMSTART)
        self.parser.feed(teststring)
        self.assertEqual(ET.tostring(self.lasttree), teststring)