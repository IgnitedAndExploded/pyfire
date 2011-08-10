# -*- coding: utf-8 -*-
"""
    pyfire.services.localdomain
    ~~~~~~~~~~~~~~~~~~~~~~

    Provides all services required to serve a local domain

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from pyfire.services import XMPPService


class LocalDomainService(XMPPService):
    """Provides services required to serve a local domain"""

    def __init__(self, domainpart=None, router=None):
        super(LocalDomainService, self).__init__(domainpart, router)

    def process(self, element_tree):
        """Processes the element_tree according to the implemented service"""

        # TODO: implement local service here which includes handling of stanzas addressed
        #       to local domain and route stanzas addressed to JIDs to their connections
