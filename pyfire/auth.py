# -*- coding: utf-8 -*-
"""
    pyfire.auth
    ~~~~~~~~~~~~~

    This module handles XMPP auth pakets

    :copyright: (c) 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from base64 import b64decode
from xml.etree.ElementTree import Element, tostring

class saslException(Exception):
    """generic SASL exception"""
    def __init__(self, failType = None):
        self.element = Element( "failure" )
        self.element.set("xmlns", "urn:ietf:params:xml:ns:xmpp-sasl")
        if failType:
            self.element.append( Element( failType ) )

    def __str__(self):
        return self.__unicode__()
    def __unicode__(self):
        return tostring(self.element)

class attributeErrorException(Exception):
    """Error in required attributed detected"""
    pass


class abortedException(saslException):
    """The receiving entity acknowledges that the authentication handshake
       has been aborted by the initiating entity.
    """
    def __init__(self):
        saslException.__init__(self, "aborted")

class accountDisabledException(saslException):
    """The account of the initiating entity has been temporarily disabled"""
    def __init__(self, message):
        saslException.__init__(self, "acount-disabled")
        text = Element("text")
        text.set("xml:lang", "en")
        text.text = message
        self.element.append( text )

class credentialsExpiredException(saslException):
    """The authentication failed because the initiating entity provided credentials that have expired"""
    def __init__(self):
        saslException.__init__(self, "credentials-expired")

class encryptionRequiredException(saslException):
    """The mechanism requested by the initiating entity cannot be used
       unless the confidentiality and integrity of the underlying stream are
       protected
    """
    def __init__(self):
        saslException.__init__(self, "encryption-required")

class incorrectEncodingException(saslException):
    """The data provided by the initiating entity could not be processed because the base 64 encoding is incorrect"""
    def __init__(self):
        saslException.__init__(self, "incorrect-encoding")

class invalidAuthzidException(saslException):
    """The authzid provided by the initiating entity is invalid, either
       because it is incorrectly formatted or because the initiating entity
       does not have permissions to authorize that ID
    """
    def __init__(self):
        saslException.__init__(self, "invalid-authzid")

class invalidMechanismException(saslException):
    """The initiating entity did not specify a mechanism, or requested a mechanism that is not supported by the receiving entity"""
    def __init__(self):
        saslException.__init__(self, "invalid-machnism")

class malformedRequestException():
    """The request is malformed"""
    def __init__(self):
        saslException.__init__(self, "malformed-request")

class mechanismTooWeakException(saslException):
    """The mechanism requested by the initiating entity is weaker than server policy permits for that initiating entity"""
    def __init__(self):
        saslException.__init__(self, "mechanism-too-weak")

class notAuthorizedException(saslException):
    """The authentication failed because the initiating entity did not
       provide proper credentials, or because some generic authentication
       failure has occurred but the receiving entity does not wish to
       disclose specific information about the cause of the failure
    """
    def __init__(self):
        saslException.__init__(self, "not-authorized")

class tempAuthFailureException(saslException):
    """The authentication failed because of a temporary error condition
       within the receiving entity, and it is advisable for the initiating
       entity to try again later
    """
    def __init__(self):
        saslException.__init__(self, "temporary-auth-faulire")

supportedMechs = {"PLAIN"}

class Auth:
  
    def handle(self, element):
        """Handles an incomming auth request from client currently sasl-plain auth is supported"""
        if element.get("xmlns") != "urn:ietf:params:xml:ns:xmpp-sasl":
            raise attributeErrorException

        self.element = element
        
        if element.get("mechanism") == "PLAIN":
            self.authPlain()
        else:
            raise invalidMechanismException

        # if we are here the authentication has succeeded...

    def authPlain(self):
        # TODO: Implement real aser authentication...
        (authzid, authcid, passwd) = b64decode( self.element.text ).split("\0")
        print b64decode( self.element.text ).split("\0")
        if authcid != "test" or passwd != "password":
            raise notAuthorizedException
