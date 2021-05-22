# -*- coding: utf-8 -*-
"""
    pyfire.stream.stanzas.iq.query
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Handles XMPP iq-query sub frames

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import xml.etree.ElementTree as ET

from pyfire.contact import Contact, Roster
from pyfire.jid import JID
from pyfire.storage import Session


class Query(object):
    """Handles all iq-query xmpp frames"""

    __slots__ = ( 'request', 'response', 'sender')

    def handle(self, request, sender):
        self.request = request
        self.sender = sender
        self.response = ET.Element("query")

        if request.get("xmlns") in self.handler:
            self.handler[request.get("xmlns")](self)
        return self.response

    def roster(self):
        """RFC6121 Section 2"""

        session = Session()
        senderjid = JID(self.sender)
        roster = session.query(Roster).filter_by(jid=senderjid.bare).first()
        if roster is None:
            roster = Roster(jid=senderjid.bare)
            session.add(roster)
            session.commit()

        for contact in roster.contacts:
            self.response.append(contact.to_element())
        self.response.set("xmlns", """jabber:iq:roster""")

    def last(self):
        """XEP-0012"""

        self.response.set("xmlns", "jabber.iq.last")
        """ TODO: set real last activity of requested contact """
        self.response.set("seconds", "0")

    def disco_info(self):
        """XEP-0030"""

        features = [
            """http://jabber.org/protocol/disco#info""", # XEP-0030 (myself)
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
