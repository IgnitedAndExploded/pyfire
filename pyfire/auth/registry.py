# -*- coding: utf-8 -*-
"""
    pyfire.auth.registry
    ~~~~~~~~~~~~~~~~~~~~

    Registry for available authentication handlers

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from _thread import allocate_lock

from pyfire.auth.backends import InvalidAuthenticationError


class ValidationRegistry(object):
    """Holds all active validation backends"""

    def __init__(self):
        self.handlers = {}
        self._lock = allocate_lock()

    def register(self, backend, handler):
        """Registers given backend handler"""

        success = False
        with self._lock:
            if backend not in self.handlers:
                self.handlers[backend] = handler
                success = True
        if not success:
            raise AttributeError("backend already known")

    def unregister(self, backend):
        """Unregisters handler for backend"""

        success = False
        with self._lock:
            if backend in self.handlers:
                self.handlers[backend].shutdown()
                del self.handlers[backend]
                success = True
        if not success:
            raise AttributeError("backend unknown")

    def validate_userpass(self, username, password):
        """Checks username and password against all backends. Returns
           backend name where backend reported OK or raises
           InvalidAuthenticationError otherwise.
        """

        result = ""
        with self._lock:
            for backend, handler in self.handlers.iteritems():
                if handler.validate_userpass(username, password):
                    result = backend
                    break
        if result == "":
            raise InvalidAuthenticationError("username/password invalid")
        return result

    def validate_token(self, token):
        """Validates given token against all backends. Returns
           backend name where backend reported OK or raises
           InvalidAuthenticationError otherwise.
        """

        result = ""
        with self._lock:
            for backend, handler in self.handlers.iteritems():
                if handler.validate_token(token):
                    result = backend
                    break
        if result == "":
            raise InvalidAuthenticationError("token invalid")
        return result
