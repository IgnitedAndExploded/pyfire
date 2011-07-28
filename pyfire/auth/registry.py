# -*- coding: utf-8 -*-
"""
    pyfire.auth.registry
    ~~~~~~~~~~~~~~~~~~~~

    Registry for available authentication handlers

    :copyright: (c) 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from pyfire.auth.backends import InvalidAuthenticationError
from pyfire.auth.sasl import SASLAuthHandler

provided_handlers = {
    'urn:ietf:params:xml:ns:xmpp-sasl': SASLAuthHandler,
}


class UnknownAuthenticationType(Exception):
    """Raised when an unknown authentication mechanism is requested"""
    pass


class AuthHandlerRegistry(object):
    """Registry for known handlers"""

    def __init__(self, check_registry):
        self.check_registry = check_registry
        self.known_handlers = {}

        for k, v in provided_handlers.iteritems():
            self.register(k, v(self))

    def register(self, namespace, handler):
        """Registers new handler"""

        self.known_handlers[namespace] = handler
        handler.check_registry = self.check_registry

    def unregister(self, namespace):
        """Unregisters given handler"""

        try:
            del self.known_handlers[namespace]
        except KeyError:
            raise UnknownAuthenticationType(namespace)

    def request_handler(self, namespace):
        """Returns a handler for given namespace"""

        try:
            return self.known_handlers[namespace]
        except KeyError:
            raise UnknownAuthenticationType(namespace)

    @property
    def supported_namespaces(self):
        """Lists supported namespaces"""

        return frozenset([handler.namespace for handler in self.known_handlers.values()])



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
