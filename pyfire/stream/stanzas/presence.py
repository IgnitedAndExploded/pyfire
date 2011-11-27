# -*- coding: utf-8 -*-
"""
    pyfire.stream.stanzas.presence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module handles XMPP presence packets
    as defined in RFC 6121 Section 4

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import copy
from base64 import b64decode
from xml.etree.ElementTree import Element, tostring

from pyfire.contact import Contact, Roster
from pyfire.jid import JID
from pyfire.storage import Session

from pyfire.logger import Logger
log = Logger(__name__)

class Presence(object):
    """This Class handles <resence> XMPP frames"""

    def __init__(self):
        super(Presence, self).__init__()

    def handle(self, tree):
        """handler for resence requests,
           returns a response that should be sent back"""
        log.debug('loading roster to broadcast presence to subscribers..')
        session = Session()
        response = list()
        senderjid = JID(tree.get("from"))
        roster = session.query(Roster).filter_by(jid=senderjid.bare).first()
        if roster is not None:
            for contact in roster.contacts:
                # only broadcast to contacts having from or both subscription to brodcasting contact..
                if contact.subscription not in ['from', 'both']:
                    continue
                log.debug('broadcasting presence to ' + contact.jid.bare)
                brd_element = copy.deepcopy(tree)
                brd_element.set('to', contact.jid.bare )
                response.append(brd_element)

        # also broadcast presence to bare JID so all resources gets it
        brd_element = copy.deepcopy(tree)
        brd_element.set('to', JID(tree.get('from')).bare )
        response.append(brd_element)

        return response
