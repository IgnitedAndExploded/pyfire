# -*- coding: utf-8 -*-
"""
    pyfire.stream.errors
    ~~~~~~~~~~~~~~~~~~~~

    Holds all Errors/Exceptions defined in RFC6120 Section 4.9.3

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import xml.etree.ElementTree as ET
from pyfire.errors import XMPPProtocolError


class StreamError(XMPPProtocolError):
    """Base class for all stream errors that are
       caused while document parsing
    """

    def __init__(self, error_name=None):
        XMPPProtocolError.__init__(self,
                            "stream:error",
                            "urn:ietf:params:xml:ns:xmpp-streams",
                            error_name
                            )


class BadFormatError(StreamError):
    """XML Format error"""

    def __init__(self):
        StreamError.__init__(self, "bad-format")


class BadNamespaceError(StreamError):
    """The entity has sent a namespace prefix that is unsupported, or has
       sent no namespace prefix on an element that needs such a prefix
    """

    def __init__(self):
        StreamError.__init__(self, "bad-namespace")


class StreamConflictError(StreamError):
    """Stream request conflicts with an existing stream"""

    def __init__(self):
        StreamError.__init__(self, "conflict")


class TimeoutError(StreamError):
    """Stream has timed out"""

    def __init__(self):
        StreamError.__init__(self, "connection-timeout")


class HostGoneError(StreamError):
    """Host has gone away (we dont serve this host anymore)"""

    def __init__(self):
        StreamError.__init__(self, "host-gone")


class HostUnknownError(StreamError):
    """Hostname in to attribute is unknown to this system"""

    def __init__(self):
        StreamError.__init__(self, "host-unknown")


class ImproperAddressingError(StreamError):
    """To or from attribute is missing in server-server communication"""

    def __init__(self):
        StreamError.__init__(self, "improper-addressing")


class InternalServerError(StreamError):
    """The server has experienced a misconfiguration or other internal error
       that prevents it from servicing the stream.
    """

    def __init__(self):
        StreamError.__init__(self, "internal-server-error")


class InvalidFromError(StreamError):
    """The data provided in a 'from' attribute does not match an authorized
       JID or validated domain as negotiated
    """

    def __init__(self):
        StreamError.__init__(self, "invalid-from")


class InvalidNamespaceError(StreamError):
    """The stream namespace name is something other than
       RFC6120 Section 11.2
    """

    def __init__(self):
        StreamError.__init__(self, "invalid-namespace")


class InvalidXMLError(StreamError):
    """Stream contains XML data that cannot be processed."""

    def __init__(self):
        StreamError.__init__(self, "invalid-xml")


class NotAuthorizedError(StreamError):
    """The entity has attempted to send XML stanzas or other outbound data
       before the stream has been authenticated
    """

    def __init__(self):
        StreamError.__init__(self, "not-authorized")


class NotWellFormedError(StreamError):
    """The initiating entity has sent XML that violates the well-formedness
       rules
    """

    def __init__(self):
        StreamError.__init__(self, "not-well-formed")


class PolicyViolationError(StreamError):
    """The entity has violated some local service policy (e.g., a stanza
       exceeds a configured size limit);
    """

    def __init__(self, message=None):
        StreamError.__init__(self, "policy-violation")
        if message is not None:
            body = ET.Element("body")
            body.text = message
            self.element.append(body)


class RemoteConnectionError(StreamError):
    """The server is unable to properly connect to a remote entity that is
       needed for authentication or authorization
    """

    def __init__(self):
        StreamError.__init__(self, "remote-connection-failed")


class ResetError(StreamError):
    """The server is closing the stream because it has new (typically
       security-critical) features to offer, because the keys or
       certificates used to establish a secure context for the stream have
       expired or have been revoked during the life of the stream
    """

    def __init__(self):
        StreamError.__init__(self, "reset")


class ResourceConstraintError(StreamError):
    """The server lacks the system resources necessary to service the
       stream.
    """

    def __init__(self):
        StreamError.__init__(self, "resource-constraint")


class RestrictedXMLError(StreamError):
    """The entity has attempted to send restricted XML features such as a
       comment, processing instruction, DTD subset, or XML entity reference
    """

    def __init__(self):
        StreamError.__init__(self, "invalid-xml")


class SeeOtherHostError(StreamError):
    """The server will not provide service to the initiating entity but is
       redirecting traffic to another host under the administrative control
       of the same service provider.
    """

    def __init__(self, other_host=None):
        StreamError.__init__(self, "see-other-host")
        if other_host is not None:
            self.element.text = other_host


class SystemShutdownError(StreamError):
    """The server is being shut down and all active streams are being
       closed.
    """

    def __init__(self):
        StreamError.__init__(self, "system-shutdown")


class UndefinedConditionError(StreamError):
    """The error condition is not one of those defined by the other
       conditions in RFC6121 Section 4.9.3
    """

    def __init__(self):
        StreamError.__init__(self, "undefined-condition")


class UnsupportedEncodingError(StreamError):
    """The initiating entity has encoded the stream in an encoding that is
       not supported by the server
    """

    def __init__(self):
        StreamError.__init__(self, "unsupported-encoding")


class UnsupportedFeatureError(StreamError):
    """The receiving entity has advertised a mandatory-to-negotiate stream
       feature that the initiating entity does not support, and has offered
       no other mandatory-to-negotiate feature alongside the unsupported
       feature.
    """

    def __init__(self):
        StreamError.__init__(self, "unsupported-feature")


class UnsupportedStanzaError(StreamError):
    """The initiating entity has sent a first-level child of the stream that
       is not supported by the server
    """

    def __init__(self):
        StreamError.__init__(self, "unsupported-stanza-type")


class UnsupportedVersionError(StreamError):
    """The 'version' attribute provided by the initiating entity in the
       stream header specifies a version of XMPP that is not supported by
       the server.
    """

    def __init__(self):
        StreamError.__init__(self, "unsupported-version")
