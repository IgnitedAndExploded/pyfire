# -*- coding: utf-8 -*-
"""
    pyfire.tests.auth.test_registry
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests builtin auth handling and backends

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from base64 import b64encode
import xml.etree.ElementTree as ET
import warnings

from pyfire.tests import PyfireTestCase
from pyfire.auth.registry import ValidationRegistry
from pyfire.auth.backends import DummyTrueValidator, DummyFalseValidator, \
                                 InvalidAuthenticationError


class DummyTestValidator(DummyTrueValidator):
    def __init__(self):
        super(DummyTrueValidator, self).__init__()
        self._shutdown = False
        self._validated = False

    def validate_userpass(self, username, password):
        self._validated = True

    def validate_token(self, token):
        self._validated = True

    def shutdown(self):
        self._shutdown = True


class TestValidationRegistry(PyfireTestCase):
    def setUp(self):
        self.registry = ValidationRegistry()

    def tearDown(self):
        del self.registry

    def test_registertwice(self):
        handler = DummyFalseValidator()
        self.registry.register('dummy', handler)
        with self.assertRaises(AttributeError) as cm:
            self.registry.register('dummy', handler)

    def test_unregister_bad(self):
        with self.assertRaises(AttributeError) as cm:
            self.registry.unregister('dummy')

    def test_unregister_good(self):
        handler = DummyFalseValidator()
        self.registry.register('dummy', handler)
        self.registry.unregister('dummy')

    def test_unregister_shutdown(self):
        handler = DummyTestValidator()
        self.registry.register('dummy', handler)
        self.assertFalse(handler._shutdown)
        self.registry.unregister('dummy')
        self.assertTrue(handler._shutdown)

    def test_validation_userpass_fail(self):
        handler1 = DummyFalseValidator()
        self.registry.register('dummy', handler1)
        handler2 = DummyTestValidator()
        self.registry.register('tester', handler2)
        self.assertFalse(handler2._validated)
        with self.assertRaises(InvalidAuthenticationError) as cm:
            self.registry.validate_userpass('user', 'pass')
        self.assertTrue(handler2._validated)

    def test_validation_userpass_success(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            handler1 = DummyTrueValidator()
            self.registry.register('dummy', handler1)
            handler2 = DummyTestValidator()
            self.registry.register('tester', handler2)
            self.assertFalse(handler2._validated)
            self.assertEqual(self.registry.validate_userpass('user', 'pass'), 'dummy')
            self.assertFalse(handler2._validated)

    def test_validation_token_fail(self):
        handler1 = DummyFalseValidator()
        self.registry.register('dummy', handler1)
        handler2 = DummyTestValidator()
        self.registry.register('tester', handler2)
        self.assertFalse(handler2._validated)
        with self.assertRaises(InvalidAuthenticationError) as cm:
            self.registry.validate_token('token')
        self.assertTrue(handler2._validated)

    def test_validation_token_success(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            handler1 = DummyTrueValidator()
            self.registry.register('dummy', handler1)
            handler2 = DummyTestValidator()
            self.registry.register('tester', handler2)
            self.assertFalse(handler2._validated)
            self.assertEqual(self.registry.validate_token('token'), 'dummy')
            self.assertFalse(handler2._validated)
