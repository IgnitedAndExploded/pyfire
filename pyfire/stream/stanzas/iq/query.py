# -*- coding: utf-8 -*-
"""
    pyfire.stream.stanzas.iq.query
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Handles XMPP iq-query sub frames

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import xml.etree.ElementTree as ET
from pyfire.contact import Contact


class Query(object):
    """Handles all iq-query xmpp frames"""

    __slots__ = ('handler', 'request', 'response')

    def handle(self, request):
        self.request = request
        self.response = ET.Element("query")

        if request.get("xmlns") in self.handler:
            self.handler[request.get("xmlns")](self)
        return self.response

    def roster(self):
        """RFC6121 Section 2"""
        self.response.set("xmlns", """jabber:iq:roster""")
        """ TODO: return real roster """
        contact = Contact("test@localhost")
        contact.subscription = "both"
        contact.approved = True
        self.response.append(contact.to_element())
        contact = Contact("test2@localhost")
        contact.approved = True
        contact.subscription = "both"
        self.response.append(contact.to_element())

    def last(self):
        """XEP-0012"""
        self.response.set("xmlns", "jabber.iq.last")
        """ TODO: set real last activity of requested contact """
        self.response.set("seconds", "0")

    def disco_info(self):
        """XEP-0030"""

        features = [
            'urn:xmpp:ping',  # XEP-0199
        ]

        self.response.set("xmlns", """http://jabber.org/protocol/disco#info""")
        for feature in features:
            feat_elem = ET.SubElement(self.response, "feature")
            feat_elem.set("var", feature)

    # TODO: implement namespaces:
    #       jabber:iq:private -> XEP-0049
    handler = {
        # 'Handled namespace': handler
        'jabber:iq:roster': roster,
        'jabber:iq:last': last,
        'http://jabber.org/protocol/disco#info': disco_info
    }
