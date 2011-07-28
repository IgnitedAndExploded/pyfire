# -*- coding: utf-8 -*-
"""
    pyfire.tests.auth.test_sasl
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests builtin sasl interface

    :copyright: (c) 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from base64 import b64encode
import xml.etree.ElementTree as ET

from pyfire.auth.sasl import SASLAuthHandler, MalformedRequestError, NotAuthorizedError
from pyfire.auth.backends import InvalidAuthenticationError
from pyfire.tests import PyfireTestCase


class MockValidatorRegistry(object):

    success = True

    def validate_userpass(self, *args, **kwds):
        if self.success:
            return "dummy"
        else:
            raise InvalidAuthenticationError

    def validate_token(self, *args, **kwds):
        if self.success:
            return "dummy"
        else:
            raise InvalidAuthenticationError


class TestSASLAuthHandler(PyfireTestCase):

    def test_plain_auth_good(self):
        MockValidatorRegistry.success = True
        handler = SASLAuthHandler(MockValidatorRegistry())
        auth_element = ET.Element("auth")
        auth_element.set("mechanism", "PLAIN")
        auth_element.text = b64encode(unichr(0).join(["zid", "user", "pass"]))
        handler.process(auth_element)

    def test_plain_auth_bad(self):
        MockValidatorRegistry.success = False
        registry = MockValidatorRegistry()
        handler = SASLAuthHandler(MockValidatorRegistry())
        auth_element = ET.Element("auth")
        auth_element.set("mechanism", "PLAIN")
        auth_element.text = b64encode(unichr(0).join(["zid", "user", "pass"]))
        with self.assertRaises(NotAuthorizedError) as cm:
            handler.process(auth_element)

    def test_plain_auth_baddata(self):
        handler = SASLAuthHandler(MockValidatorRegistry())
        auth_element = ET.Element("auth")
        auth_element.set("mechanism", "PLAIN")
        auth_element.text = "something\0totallywronghere"
        with self.assertRaises(MalformedRequestError) as cm:
            handler.process(auth_element)
