# -*- coding: utf-8 -*-
"""
    pyfire.auth
    ~~~~~~~~~~~~~

    This module handles XMPP auth pakets

    :copyright: (c) 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from base64 import b64decode

class attributeErrorException(Exception):
    """Error in required attributed detected"""
    pass

class mechanismNotSupportedException(Exception):
    """Given auth mechanism is not supported"""
    pass

class authFailedException(Exception):
    """Authentication failed"""
    pass

class Auth:
  
    def handle(self, element):
        """Handles an incomming auth request from client currently sasl-plain auth is supported"""
        if element.get("xmlns") != "urn:ietf:params:xml:ns:xmpp-sasl":
            raise attributeErrorException

        self.element = element
        
        if element.get("mechanism") == "PLAIN":
            self.authPlain()
        else:
            raise mechanismNotSupportedException

        # if we are here the authentication has succeeded...

    def authPlain(self):
        # TODO: Implement real aser authentication...
        (authzid, authcid, passwd) = b64decode( self.element.text ).split("\0")
        print b64decode( self.element.text ).split("\0")
        if authcid != "test" or passwd != "password":
            raise authFailedException
