# -*- coding: utf-8 -*-
"""
    pyfire.services.localdomain
    ~~~~~~~~~~~~~~~~~~~~~~

    Provides all services required to serve a local domain

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from pyfire.jid import JID
from pyfire.services import XMPPService
from pyfire.stream.stanzas import iq, message, presence


class LocalDomainService(XMPPService):
    """Provides services required to serve a local domain"""

    def __init__(self, domainpart=None, router=None):
        super(LocalDomainService, self).__init__(domainpart, router)

        self.iq = iq.Iq()
        self.message = message.Message()
        self.presence = presence.Presence()

    def process(self, element_tree):
        """Processes the element_tree according to the implemented service"""

        # TODO: implement local service here which includes handling of stanzas addressed
        #       to local domain and route stanzas addressed to JIDs to their connections
        to_jid = JID(element_tree.get("to"))
        response_element = None
        if element_tree.tag == "iq":
            response_element = self.iq.handle(element_tree)
        elif element_tree.tag == "message":
            response_element = self.message.handle(element_tree)
        elif element_tree.tag == "presence":
            response_element = self.presence.handle(element_tree)

        # always add from attribute
        if response_element is not None:
            if response_element.get("from") is None:
                response_element.set("from", to_jid.domain)

        return response_element
