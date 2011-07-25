# -*- coding: utf-8 -*-
"""
    pyfire.presence
    ~~~~~~~~~~~~~

    This module handles XMPP presence packets as defined in RFC 6121 Section 4.7

    :copyright: (c) 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from base64 import b64decode
from xml.etree.ElementTree import Element, tostring

class Presence():

    def handle(self, tree):
        """handler for resence requests, returns a response that should be sent back"""
