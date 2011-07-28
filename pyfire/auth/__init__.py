# -*- coding: utf-8 -*-
"""
    pyfire.auth
    ~~~~~~~~~~~

    This module handles XMPP auth packets.

    :copyright: (c) 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""


class AuthenticationError(Exception):
    """Raised on any authentication related error"""

    def __init__(self, errorname=None):
        self.errorname = errorname


class AuthenticationHandler(object):
    """Handles authentication requests"""

    namespace = "urn:ietf:params:xml:ns:xmpp-auth"
    supported_mechs = {}

    check_registry = None

    def __init__(self, check_registry):
        super(AuthenticationHandler, self).__init__()
        self.check_registry = check_registry

    def process(self, auth_element):
        """Processes request for auth_element"""
        pass
