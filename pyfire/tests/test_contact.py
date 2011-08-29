# -*- coding: utf-8 -*-
"""
    pyfire.tests.test_contact
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Tests for Contact

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import xml.etree.ElementTree as ET

from pyfire.contact import Contact
from pyfire.jid import JID
from pyfire.tests import PyfireTestCase



class TestContact(PyfireTestCase):

    def test_init_required_attrs(self):
        with self.assertRaises(TypeError) as cm:
            cont = Contact()
        cont = Contact('test')
        cont = Contact(JID('test'))

    def test_init_optional_attrs(self):
        cont = Contact('test', subscription="both")
        self.assertEqual(cont.subscription, "both")

    def test_init_invalid_attr(self):
        with self.assertRaises(ValueError):
            cont = Contact('test', subscription="fail")

    def test_invalid_value(self):
        cont = Contact('test')
        with self.assertRaises(ValueError):
            cont.subscription = "fail"

    def test_invalid_attr(self):
        cont = Contact('test')
        with self.assertRaises(AttributeError):
            cont.fail = "fail"

    def test_tostring(self):
        cont = Contact('test')
        result = '<item approved="false" jid="test" subscription="none" />'
        self.assertEqual(ET.tostring(cont.to_element()), result)
        result = '<item approved="false" jid="test" />'
        cont.subscription = None
        self.assertEqual(ET.tostring(cont.to_element()), result)
        result = '<item jid="test" />'
        cont.approved = None
        self.assertEqual(ET.tostring(cont.to_element()), result)
        result = '<item ask="subscribe" jid="test" name="Joe" />'
        cont.ask = 'subscribe'
        cont.name = "Joe"
        self.assertEqual(ET.tostring(cont.to_element()), result)

    def test_fromstring(self):
        result = '<item approved="false" jid="test" subscription="none" />'
        in_element = ET.fromstring(result)
        cont = Contact.from_element(in_element)
        out_element = cont.to_element()
        self.assertEqual(ET.tostring(out_element), result)

        result = '<item approved="true" jid="test" subscription="none"><group>test1</group></item>'
        in_element = ET.fromstring(result)
        cont = Contact.from_element(in_element)
        out_element = cont.to_element()
        self.assertEqual(ET.tostring(out_element), result)

    def test_bad_fromstring(self):
        result = '<item approved="peng" jid="test" subscription="none" />'
        in_element = ET.fromstring(result)
        with self.assertRaises(ValueError):
            cont = Contact.from_element(in_element)

        result = '<failitem approved="true" jid="test" subscription="none" />'
        in_element = ET.fromstring(result)
        with self.assertRaises(ValueError):
            cont = Contact.from_element(in_element)

    def test_bad_jid(self):
        jid = JID('test')
        jid.domain = ''
        with self.assertRaises(ValueError):
            cont = Contact(jid)
