# -*- coding: utf-8 -*-
"""
    pyfire.auth.sasl
    ~~~~~~~~~~~~~~~~

    SASL authentication implementation

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from base64 import b64decode
import xml.etree.ElementTree as ET

from pyfire.auth import AuthenticationHandler, AuthenticationError
from pyfire.auth.backends import InvalidAuthenticationError


class SASLError(AuthenticationError):
    """generic SASL exception"""

    def __init__(self, error_name=None):
        AuthenticationError.__init__(self,
                                "urn:ietf:params:xml:ns:xmpp-sasl",
                                error_name
                            )


class AbortedError(SASLError):
    """The receiving entity acknowledges that the authentication handshake
       has been aborted by the initiating entity.
    """

    def __init__(self):
        SASLError.__init__(self, "aborted")


class AccountDisabledError(SASLError):
    """The account of the initiating entity has been temporarily disabled"""

    def __init__(self, message):
        SASLError.__init__(self, "acount-disabled")
        text = ET.Element("text")
        text.set("xml:lang", "en")
        text.text = message
        self.element.append(text)


class CredentialsExpiredError(SASLError):
    """The authentication failed because the initiating entity provided
       credentials that have expired
    """

    def __init__(self):
        SASLError.__init__(self, "credentials-expired")


class EncryptionRequiredError(SASLError):
    """The mechanism requested by the initiating entity cannot be used
       unless the confidentiality and integrity of the underlying stream are
       protected
    """

    def __init__(self):
        SASLError.__init__(self, "encryption-required")


class IncorrectEncodingError(SASLError):
    """The data provided by the initiating entity could not be processed
       because the base 64 encoding is incorrect
    """

    def __init__(self):
        SASLError.__init__(self, "incorrect-encoding")


class InvalidAuthzidError(SASLError):
    """The authzid provided by the initiating entity is invalid, either
       because it is incorrectly formatted or because the initiating entity
       does not have permissions to authorize that ID
    """

    def __init__(self):
        SASLError.__init__(self, "invalid-authzid")


class InvalidMechanismError(SASLError):
    """The initiating entity did not specify a mechanism, or requested a
       mechanism that is not supported by the receiving entity
    """

    def __init__(self):
        SASLError.__init__(self, "invalid-machnism")


class MalformedRequestError(SASLError):
    """The request is malformed"""

    def __init__(self):
        SASLError.__init__(self, "malformed-request")


class MechanismTooWeakError(SASLError):
    """The mechanism requested by the initiating entity is weaker than server
       policy permits for that initiating entity
    """

    def __init__(self):
        SASLError.__init__(self, "mechanism-too-weak")


class NotAuthorizedError(SASLError):
    """The authentication failed because the initiating entity did not
       provide proper credentials, or because some generic authentication
       failure has occurred but the receiving entity does not wish to
       disclose specific information about the cause of the failure
    """

    def __init__(self):
        SASLError.__init__(self, "not-authorized")


class TempAuthFailureError(SASLError):
    """The authentication failed because of a temporary error condition
       within the receiving entity, and it is advisable for the initiating
       entity to try again later
    """

    def __init__(self):
        SASLError.__init__(self, "temporary-auth-faulire")


class SASLAuthHandler(AuthenticationHandler):
    """Handle SASL authentication requests"""

    namespace = "urn:ietf:params:xml:ns:xmpp-sasl"

    def process(self, auth_element):
        """Processes one auth element"""

        self.auth_element = auth_element
        try:
            self.supported_mechs[auth_element.get("mechanism")](self)
        except KeyError:
            raise InvalidMechanismError

    def auth_plain(self):
        try:
            splits = b64decode(self.auth_element.text).split(unichr(0))
            if len(splits) != 3:
                raise InvalidAuthenticationError

            authzid, authcid, password = splits
            try:
                self.check_registry.validate_userpass(authcid, password)
                self.authenticated_user = authcid
            except InvalidAuthenticationError:
                raise NotAuthorizedError
        except (TypeError, InvalidAuthenticationError):
            raise MalformedRequestError

    supported_mechs = {
        'PLAIN': auth_plain
    }
