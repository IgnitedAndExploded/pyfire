# -*- coding: utf-8 -*-
"""
    pyfire.auth.backends
    ~~~~~~~~~~~~~~~~~~~~

    Credential validation backends

    :copyright: (c) 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import warnings


class InvalidAuthenticationError(Exception):
    """Raised upon fail in auth"""
    pass


class CredentialValidator(object):
    """Base class to handle credential validation"""

    def shutdown(self):
        """Shuts down needed connections and handles"""
        pass

    def validate_userpass(self, username, password):
        """Validate username and password"""
        pass

    def validate_token(self, token):
        """Validate a given token"""
        pass


class DummyTrueValidator(CredentialValidator):
    """Always returns true"""

    def __init__(self):
        warnings.warn("Do not use this validator in production",
                      RuntimeWarning)
        super(DummyTrueValidator, self).__init__()

    def validate_userpass(self, username, password):
        return True

    def validate_token(self, token):
        return True


class DummyFalseValidator(CredentialValidator):
    """Always returns false"""

    def validate_userpass(self, username, password):
        return False

    def validate_token(self, token):
        return False
