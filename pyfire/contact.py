"""
    pyfire.contact
    ~~~~~~~~~~

    Handles Contact ("roster item") interpretation as per RFC-6121

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import xml.etree.ElementTree as ET

from sqlalchemy import Table, Column, Boolean, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship, backref

from pyfire.jid import JID
from pyfire.storage import Base, JIDString


contacts_groups = Table('contacts_groups', Base.metadata,
    Column('contact_id', Integer, ForeignKey('contacts.id')),
    Column('group_id', Integer, ForeignKey('groups.id'))
)

class Roster(Base):
    """List of contacts for a given jid"""

    __tablename__ = 'rosters'

    id = Column(Integer, primary_key=True)
    jid = Column(JIDString, nullable=False)

    def __init__(self, jid):
        self.jid = JID(jid)


class Group(Base):
    """Simple group, only providing a name for now"""

    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))


class Contact(Base):
    """Jabber Contact, aka roster item. It has some really strict attribute
       setting mechanism as it leads to all kinds of fantastic crashes with
       clients which should be avoided in any case.
    """

    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    approved = Column(Boolean)
    ask = Column(Enum('subscribe'))
    jid = Column(JIDString, nullable=False)
    name = Column(String(255))
    subscription = Column(Enum("none", "from", "to", "remove", "both"))
    groups = relationship(Group, secondary=contacts_groups)
    roster = relationship(Roster, backref=backref('contacts'))
    roster_id = Column(Integer, ForeignKey('rosters.id'), nullable=False)

    def __init__(self, jid, **kwds):
        super(Contact, self).__init__()

        # required
        if isinstance(jid, basestring):
            self.jid = JID(jid)
        elif isinstance(jid, JID):
            self.jid = jid
            self.jid.validate(raise_error=True)
        else:
            raise AttributeError("Needs valid jid either as string or JID instance")

        # optional
        self.approved = False
        self.ask = None
        self.name = None
        self.subscription = "none"
        self.groups = []

        for k, v in kwds.iteritems():
            setattr(self, k, v)

    def to_element(self):
        """Formats contact as `class`:ET.Element object"""

        element = ET.Element("item")
        if self.approved is not None:
            element.set("approved", 'true' if self.approved else 'false')
        if self.ask is not None:
            element.set("ask", self.ask)
        element.set("jid", str(self.jid))
        if self.name is not None:
            element.set("name", self.name)
        if self.subscription is not None:
            element.set("subscription", self.subscription)
        for group in self.groups:
            group_element = ET.SubElement(element, "group")
            group_element.text = group
        return element

    @staticmethod
    def from_element(element):
        """Creates contact instance from `class`:ET.Element"""

        if element.tag != "item":
            raise ValueError("Invalid element with tag %s" % element.tag)

        cont = Contact(element.get('jid'))
        cont.ask = element.get('ask')
        cont.subscription = element.get('subscription')
        approved = element.get('approved')
        if approved == 'true':
            cont.approved = True
        elif approved == 'false':
            cont.approved = False
        else:
            cont.approved = approved
        for group in list(element):
            if group.tag == "group":
                cont.groups.append(group.text)
        return cont
