# -*- coding: utf-8 -*-
"""
    pyfire.tests.stream.test_streamprocessor
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Unittests for streamprocessor

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import xml.etree.ElementTree as ET

from pyfire.tests import PyfireTestCase

from pyfire.stream import processor, errors

STREAMSTART = """<?xml version='1.0'?><stream:stream xmlns="jabber:client" to="localhost" version="1.0" xmlns:stream="http://etherx.jabber.org/streams">"""


class TestContentHandler(PyfireTestCase):

    def fakestreamhandler(self, attrs):
        self.lastattrs = attrs

    def fakecontenthandler(self, tree):
        self.lasttree = tree

    def setUp(self):
        self.lastattrs = None
        self.lasttree = None
        self.parser = processor.StreamProcessor(self.fakestreamhandler, self.fakecontenthandler)

    def tearDown(self):
        self.parser.close()

    def test_client_streamstart(self):
        self.parser.feed(STREAMSTART)
        self.assertEqual(len(self.lastattrs.keys()), 4)

    def test_bad_start(self):
        teststring = """<?xml version='1.0'?><hello>"""
        with self.assertRaises(errors.BadFormatError) as cm:
            self.parser.feed(teststring)

    def test_treeparse(self):
        teststring = """<iq id="yhc13a95" type="set"><bind xmlns="urn:ietf:params:xml:ns:xmpp-bind"><resource>balcony</resource></bind></iq>"""
        self.parser.feed(STREAMSTART)
        self.parser.feed(teststring)
        self.assertEqual(ET.tostring(self.lasttree), teststring)

    def test_partial_treeparse(self):
        teststring1 = """<iq id="yhc13a95" type="set"><bind xmlns="urn:ietf:params:xml:ns:xmpp-bi"""
        teststring2 = """nd"><resource>balcony</resource></bind></iq>"""
        self.parser.feed(STREAMSTART)
        self.assertEqual(self.lasttree, None)
        self.parser.feed(teststring1)
        self.assertEqual(self.lasttree, None)
        self.parser.feed(teststring2)
        self.assertEqual(ET.tostring(self.lasttree), teststring1 + teststring2)

    def test_badxml_no_closing_tag(self):
        teststring = """<message><body>No closing tag!</message>"""
        self.parser.feed(STREAMSTART)
        with self.assertRaises(errors.BadFormatError) as cm:
            self.parser.feed(teststring)
