# -*- coding: utf-8 -*-
"""
    pyfire.tests.jid
    ~~~~~~~~~~~~~~~~

    Tests for JID

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from pyfire.tests import PyfireTestCase

from pyfire.jid import JID


class TestJID(PyfireTestCase):

    def test_parse_full_jid(self):
        jid = JID("user@host/res")
        self.assertEqual(jid.local, "user")
        self.assertEqual(jid.domain, "host")
        self.assertEqual(jid.resource, "res")

    def test_parse_domain_partial_jid(self):
        jid = JID("host/res")
        self.assertEqual(jid.local, None)
        self.assertEqual(jid.domain, "host")
        self.assertEqual(jid.resource, "res")

    def test_parse_domain_jid(self):
        jid = JID("host")
        self.assertEqual(jid.local, None)
        self.assertEqual(jid.domain, "host")
        self.assertEqual(jid.resource, None)

    def test_jid_compare(self):
        jid1 = JID("user1@host/res")
        jid2 = JID("user2@host/res")
        self.assertTrue(jid1 == jid1)
        self.assertFalse(jid1 == jid2)

    def test_jid_ip(self):
        JID("user@127.0.0.1/res")
        JID("user@fe80::1/res")

    def test_bare_jid(self):
        jid = JID("user@host/res")
        self.assertEqual(jid.bare, "user@host")
        jid = JID("host/res")
        self.assertEqual(jid.bare, "host")

    def test_jid_operators(self):
        a = JID("user@host/res")
        b = JID("user@host/res")
        self.assertTrue(a == b)
        self.assertFalse(a != b)
        self.assertTrue(a is not b)
        self.assertFalse(a is b)

    def test_str(self):
        jids = [
            "host",
            "user@host",
            "host/res",
            "user@host/res"
        ]

        for testjid in jids:
            jid = JID(testjid)
            self.assertEqual(str(jid), testjid)

    def test_jid_true(self):
        jid = JID("user@host/res")
        self.assertTrue(jid.validate())

    badjids = [
        "",
        "1.2.3.256",
        "a" * 128 + "." + "a" * 128,
        unichr(0x100) * 512 + "a",  # results in 1025 byte
        "fg::",  # looks like ipv6 but is invalid
        "test/",
        unichr(0x100) * 512 + "a@testhost",
        "@testhost",
        unichr(0xD800) + "@testhost",
        "testhost/" + unichr(0x100) * 512 + "a",
        "testhost/" + unichr(0xD800)
    ]

    def test_bad_jids_raise(self):
        for testjid in self.badjids:
            try:
                with self.assertRaises(ValueError) as cm:
                    jid = JID(testjid)
            except AssertionError:
                raise AssertionError("ValueError not raised for JID '%s'" % testjid)

    def test_bad_jids_false(self):
        for testjid in self.badjids:
            jid = JID(testjid, validate_on_init=False)
            self.assertFalse(jid.validate())

    def test_bad_jid_inject(self):
        jid = JID('test')
        jid.domain = None
        with self.assertRaises(ValueError) as cm:
            jid.validate(True)
