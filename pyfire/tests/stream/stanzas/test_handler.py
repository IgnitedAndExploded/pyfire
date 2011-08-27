# -*- coding: utf-8 -*-
"""
    pyfire.tests.stream.stanzas.test_handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for Tag Handler

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import xml.etree.ElementTree as ET
import warnings

from pyfire.auth.registry import AuthHandlerRegistry, ValidationRegistry
from pyfire.auth.backends import DummyTrueValidator
from pyfire.stream.stanzas import TagHandler
from pyfire.stream import errors
from pyfire.tests import PyfireTestCase


class MockConnection(object):
    def __init__(self):

        self.last_element = None
        self.last_string = None
        self.strings = []
        self.validator_registry = ValidationRegistry()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            handler1 = DummyTrueValidator()
            self.validator_registry.register('dummy', handler1)
        self.auth_registry = AuthHandlerRegistry(self.validator_registry)

    def send_element(self, element):
        self.last_element = element
        self.strings.append(ET.tostring(element))

    def send_string(self, string):
        self.last_string = string
        self.strings.append(string)


class MockAttr(dict):
    def getValue(self, name):
        return self[name]


class TestTagHandler(PyfireTestCase):

    def setUp(self):
        self.connection = MockConnection()
        self.taghandler = TagHandler(self.connection)

    def test_stream_start(self):
        attrs = {
            'to': 'localhost',
            'xmlns': 'jabber:client',
            'xmlns:stream': 'http://etherx.jabber.org/streams',
            'version': '1.0'
        }
        attrs = MockAttr(attrs)
        self.taghandler.streamhandler(attrs)
        self.assertTrue(
            self.connection.strings[0].startswith(
                """<?xml version="1.0"?><stream:stream from="localhost" id="""))
        self.assertTrue(
            self.connection.strings[0].endswith(
                """" version="1.0" xml:lang="en" xmlns="jabber:client" """ +
                """xmlns:stream="http://etherx.jabber.org/streams" >"""
                ))

    def test_bad_stream_version(self):
        attrs = {
            'to': 'localhost',
            'xmlns': 'jabber:client',
            'xmlns:stream': 'http://etherx.jabber.org/streams',
            'version': '11.1'
        }
        attrs = MockAttr(attrs)
        with self.assertRaises(errors.UnsupportedVersionError) as cm:
            self.taghandler.streamhandler(attrs)

    def test_no_stream_version(self):
        attrs = {
            'to': 'localhost',
            'xmlns': 'jabber:client',
            'xmlns:stream': 'http://etherx.jabber.org/streams'
        }
        attrs = MockAttr(attrs)
        self.taghandler.streamhandler(attrs)
        self.assertFalse('" version="' in self.connection.strings[0])

    def test_streaminit_no_from(self):
        attrs = {
            'to': 'localhost',
            'xmlns': 'jabber:client',
            'xmlns:stream': 'http://etherx.jabber.org/streams',
            'version': '1.0'
        }
        attrs = MockAttr(attrs)
        self.taghandler.streamhandler(attrs)
        self.assertFalse('to="' in self.connection.strings[0])

    def test_streaminit_has_from(self):
        attrs = {
            'from': 'testuser@localhost',
            'to': 'localhost',
            'xmlns': 'jabber:client',
            'xmlns:stream': 'http://etherx.jabber.org/streams',
            'version': '1.0'
        }
        attrs = MockAttr(attrs)
        self.taghandler.streamhandler(attrs)
        self.assertTrue('to="' in self.connection.strings[0])

    def test_streaminit_invalid_from(self):
        attrs = {
            'from': '@localhost',
            'to': 'localhost',
            'xmlns': 'jabber:client',
            'xmlns:stream': 'http://etherx.jabber.org/streams',
            'version': '1.0'
        }
        attrs = MockAttr(attrs)
        with self.assertRaises(errors.InvalidFromError) as cm:
            self.taghandler.streamhandler(attrs)
