# -*- coding: utf-8 -*-
"""
    pyfire.tests.jid
    ~~~~~~~~~~~~~~~~

    Tests for JID

    :copyright: (c) 2011 by the pyfire Team, see AUTHORS for more details.
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

    def test_bare_jid(self):
        jid = JID("user@host/res")
        self.assertEqual(jid.bare, "user@host")

    def test_jid_compare(self):
        jid1 = JID("user1@host/res")
        jid2 = JID("user2@host/res")
        self.assertTrue(jid1 == jid1)
        self.assertFalse(jid1 == jid2)

    def test_jid_ip(self):
        JID("user@127.0.0.1/res")
        JID("user@fe80::1/res")
