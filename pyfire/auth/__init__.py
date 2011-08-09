# -*- coding: utf-8 -*-
"""
    pyfire.auth
    ~~~~~~~~~~~

    This module handles XMPP auth packets.

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from pyfire.errors import XMPPProtocolError


class AuthenticationError(XMPPProtocolError):
    """Raised on any authentication related error"""

    def __init__(self, error_namespace, error_name=None):
        XMPPProtocolError.__init__(self,
                            "failure",
                            error_namespace,
                            error_name
                        )


class AuthenticationHandler(object):
    """Handles authentication requests"""

    namespace = "urn:ietf:params:xml:ns:xmpp-auth"
    supported_mechs = {}
    authenticated_user = ""

    check_registry = None

    def __init__(self, check_registry):
        super(AuthenticationHandler, self).__init__()
        self.check_registry = check_registry

    def process(self, auth_element):
        """Processes request for auth_element"""
        pass
