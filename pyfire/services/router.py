# -*- coding: utf-8 -*-
"""
    pyfire.services.router
    ~~~~~~~~~~~~~~~~~~~~~~

    Routes a given stanza to the right service provider

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from pyfire.jid import JID
from pyfire.logger import Logger
import pyfire.configuration as config

log = Logger(__name__)


class DuplicatedEntryError(Exception):
    """An entry can not be added to the routing table as the given domainpart
       already exists in the routing table
    """
    pass


class Router(object):
    """Handles the Stanza routing to service providers"""

    def __init__(self):
        super(Router, self).__init__()
        self.routing_table = {}

    def register_service(self, domainpart, service):
        """Registers a new service at the given domainpart"""

        if domainpart in self.routing_table:
            raise DuplicatedEntryError

        log.info("registering new %s service at %s" %
                            (service.__class__.__name__, domainpart))
        self.routing_table[domainpart] = service

    def unregister_service(self, domainpart):
        """Unregisters the service from the given domainpart"""

        log.info("unregistering service at " + domainpart)
        del self.routing_table[domainpart]

    def route_stanza(self, element_tree):
        """Routes the given stanza to the service provider it is addressed to
           and let the service provider process it.
        """
        to = element_tree.get("to")
        # if no to is given its localdomain
        if to is None:
            log.debug("no to specified, routing to first local domain")
            to = config.getlist("listeners", "domains")[0]
            element_tree.set("to", to)

        destination_domain = JID(to).domain

        destination = self.routing_table[destination_domain]

        log.debug("routing stanza to domain %s (%s)" %
                    (destination_domain, destination.__class__.__name__))
        return destination.process(element_tree)
