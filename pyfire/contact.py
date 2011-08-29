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
    """Jabber Contact, aka roster item. It has some really strict attribute
       setting mechanism as it leads to all kinds of fantastic crashes with
       clients which should be avoided really.
    """

    __slots__ = ('__approved', '__ask', 'jid', 'name', '__subscription', 'group')

    allowed_approved = frozenset([None, True, False])
    allowed_ask = frozenset([None, "subscribe"])
    allowed_subscription = frozenset([None, "none", "from", "to", "remove", "both"])

    def __init__(self, jid, **kwds):
        super(Contact, self).__init__()

        # required
        if isinstance(jid, basestring):
            self.jid = JID(jid)
        else:
            self.jid = jid
            self.jid.validate(raise_error=True)

        # optional
        self.approved = False
        self.ask = None
        self.name = None
        self.subscription = "none"
        self.group = []

        for name, value in kwds.iteritems():
            setattr(self, name, value)

    def __setattr__(self, name, value):
        hidden_name = "__%s" % name
        really_hidden_name = "_%s__%s" % (self.__class__.__name__, name)
        if hasattr(self, hidden_name) or hidden_name in self.__slots__:
            range_var = "allowed_%s" % name
            if value in getattr(self, range_var):
                object.__setattr__(self, really_hidden_name, value)
            else:
                raise ValueError("'%s' not in allowed set of values" % value)
        elif name in self.__slots__:
            object.__setattr__(self, name, value)
        else:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))

    @property
    def ask(self):
        return self.__ask

    @property
    def approved(self):
        return self.__approved

    @property
    def subscription(self):
        return self.__subscription

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
        for group in self.group:
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
                cont.group.append(group.text)
        return cont
