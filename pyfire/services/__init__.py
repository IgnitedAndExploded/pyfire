# -*- coding: utf-8 -*-
"""
    pyfire.services
    ~~~~~~~~~~~~~~~~~~~~~~

    Defines a base XMPP service

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""


class XMPPService(object):
    """Defines a XMPP Service"""

    def __init__(self, domainpart=None, router=None):
        super(XMPPService, self).__init__()

        # Autoregister in router if given
        if domainpart is not None and router is not None:
            router.register_service(domainpart, self)

    def process(self, element_tree):
        """Processes the element_tree according to the implemented service"""
        pass
