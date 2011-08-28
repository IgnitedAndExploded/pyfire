# -*- coding: utf-8 -*-
"""
    pyfire.auth.registry
    ~~~~~~~~~~~~~~~~~~~~

    Registry for available authentication handlers

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""




class ValidationRegistry(object):
    """Holds all active validation backends"""

    def __init__(self):
        self.handlers = {}

    def register(self, backend, handler):
        """Registers given backend handler"""

        if backend not in self.handlers:
            self.handlers[backend] = handler
        else:
            raise AttributeError("backend already known")

    def unregister(self, backend):
        """Unregisters handler for backend"""

        if backend not in self.handlers:
            raise AttributeError("backend unknown")
        self.handlers[backend].shutdown()
        del self.handlers[backend]

    def validate_userpass(self, username, password):
        """Checks username and password against all backends. Returns
           backend name where backend reported OK or raises
           InvalidAuthenticationError otherwise.
        """

        for backend, handler in self.handlers.iteritems():
            if handler.validate_userpass(username, password):
                return backend
        raise InvalidAuthenticationError("username/password invalid")

    def validate_token(self, token):
        """Validates given token against all backends. Returns
           backend name where backend reported OK or raises
           InvalidAuthenticationError otherwise.
        """

        for backend, handler in self.handlers.iteritems():
            if handler.validate_token(token):
                return backend
        raise InvalidAuthenticationError("token invalid")
