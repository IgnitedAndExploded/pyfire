"""
    pyfire.contact
    ~~~~~~~~~~

    Handles Contact ("roster item") interpretation as per RFC-6121

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from pyfire.jid import JID
import xml.etree.ElementTree as ET


class Contact(object):
    """Jabber Contact, aka roster item"""

    __slots__ = ('approved', 'ask', 'jid', 'name', 'subscription', 'group')

    def __init__(self, jid):
        super(Contact, self).__init__()

        # required
        self.jid = JID(jid)

        # optional
        self.approved = None
        self.ask = None
        self.name = None
        self.subscription = None
        self.group = []

    def to_element(self):
        """Returns the Contact as etree.ElementTree.Element object"""

        element = ET.Element("item")
        if not self.approved == None:
            element.set("approved", self.approved)
        if not self.ask == None:
            element.set("ask", self.ask)
        element.set("jid", str(self.jid.bare))
        if not self.name == None:
            element.set("name", self.name)
        if not self.subscription == None:
            element.set("subscription", self.subscription)
        for group in self.group:
            group_element = ET.Element("group")
            group_element.text = group
            element.append(group_element)
        return element
