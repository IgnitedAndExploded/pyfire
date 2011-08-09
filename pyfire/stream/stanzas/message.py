# -*- coding: utf-8 -*-
"""
    pyfire.stream.stanzas.message
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module handles XMPP message frames
    as defined in RFC 6121 Section 4.7

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from base64 import b64decode
from xml.etree.ElementTree import Element, tostring


class Message(object):
    """Handles <message> XMPP frames"""

    def __init__(self, tag_handler):
        super(Message, self).__init__()

        self.tag_handler = tag_handler

    def handle(self, tree):
        """handler for message requests"""

        # TODO: Implement namespaces:
        # XEP-0085 (Chat State Notifications)
        # XEP-0184 (Message Delivery Receipts)
