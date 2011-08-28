# -*- coding: utf-8 -*-
"""
    pyfire.stream.stanzas.errors
    ~~~~~~~~~~~~~~~~~~~~

    Holds all Stanzas Errors/Exceptions defined in RFC6120 Section 8.3.3

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import xml.etree.ElementTree as ET
from pyfire.errors import XMPPProtocolError


class StanzaError(XMPPProtocolError):
    """Base class for all stanza errors that are
    caused while stanza processing
    """

    def __init__(self, request, error_type, error_name):
        XMPPProtocolError.__init__(self,
                                request.tag,
                                ""
                            )
        try:
            self.element.set("id", request.get("id"))
            self.element.set("to", request.get("from"))
            self.element.set("from", request.get("to"))
        except KeyError:
            pass
        self.error = ET.Element("error")
        self.error.set("type", error_type)
        self.message = ET.Element(error_name)
        self.message.set("xmlns", "urn:ietf:params:xml:ns:xmpp-stanzas")
        self.error.append(self.message)
        self.element.append(self.error)


class BadRequestError(StanzaError):
    """The sender has sent a stanza containing XML that does not conform to
       the appropriate schema or that it cannot be processed
    """

    def __init__(self, request):
        StanzaError.__init__(self, request, "modify", "bad-request")


class ConflictError(StanzaError):
    """Access cannot be granted because an existing resource exists with the
       same name or address
    """

    def __init__(self, request):
        StanzaError.__init__(self, request, "cancel", "conflict")


class FeatureNotImplementedError(StanzaError):
    """The feature represented in the XML stanza is not implemented by the
       intended recipient or an intermediate server and therefore the stanza
       cannot be processed
    """

    def __init__(self, request):
        StanzaError.__init__(self, request, "cancel",
                                "feature-not-implemented")


class ForbiddenError(StanzaError):
    """The requesting entity does not possess the necessary permissions to
       perform an action that only certain authorized roles or individuals
       are allowed to complete
    """

    def __init__(self, request):
        StanzaError.__init__(self, request, "auth", "forbidden")


class GoneError(StanzaError):
    """The recipient or server can no longer be contacted at this address"""

    def __init__(self, request, uri):
        StanzaError.__init__(self, request, "cancel", "gone")
        self.message.text = uri
        # TODO: Add "by" attribute to self.error
        #       if we can determine who we are


class InternalServerError(StanzaError):
    """The server has experienced a misconfiguration or other internal error
       that prevents it from processing the stanza
    """

    def __init__(self, request):
        StanzaError.__init__(self, request, "cancel", "internal-server-error")


class ItemNotFoundError(StanzaError):
    """The addressed JID or item requested cannot be found"""

    def __init__(self, request):
        StanzaError.__init__(self, request, "cancel", "item-not-found")


class JIDMalformedError(StanzaError):
    """Invalid JID has been set in Stanzas"""

    def __init__(self, request):
        StanzaError.__init__(self, request, "modify", "jid-malformed")


class NotAcceptableError(StanzaError):
    """The recipient or server understands the request but cannot process it
       because the request does not meet criteria defined by the recipient
       or server
    """

    def __init__(self, request):
        StanzaError.__init__(self, request, "modify", "not-acceptable")


class NotAllowedError(StanzaError):
    """The recipient or server does not allow any entity to perform the
       action
    """

    def __init__(self, request):
        StanzaError.__init__(self, request, "cancel", "not-allowed")


class NotAuthorizedError(StanzaError):
    """The sender needs to provide valid credentials before being allowed to
       perform the action
    """

    def __init__(self, request):
        StanzaError.__init__(self, request, "auth", "not-authorized")


class PolicyViolationError(StanzaError):
    """The entity has violated some local service policy"""

    def __init__(self, request, policy_text=None):
        StanzaError.__init__(self, request, "modify", "policy-violation")
        # TODO: Add "by" attribute to self.error
        #       if we can determine who we are
        if policy_text is not None:
            text = ET.Element("text")
            text.set("xmlns", "urn:ietf:params:xml:ns:xmpp-stanzas")
            text.text = policy_text
            self.message.append(text)


class RecipientUnavailableError(StanzaError):
    """The intended recipient is temporarily unavailable, undergoing
       maintenance, etc.
    """

    def __init__(self, request):
        StanzaError.__init__(self, request, "wait", "recipient-unavailable")


class RedirectError(StanzaError):
    """The recipient or server is redirecting requests for this information
       to another entity
    """

    def __init__(self, request, redirect_to):
        StanzaError.__init__(self, request, "modify", "redirect")
        self.message.text = redirect_to


class RegistrationRequiredError(StanzaError):
    """The requesting entity is not authorized to access the requested
       service because prior registration is necessary
    """

    def __init__(self, request):
        StanzaError.__init__(self, request, "auth", "registration-required")


class RemoteServerNotFoundError(StanzaError):
    """A remote server or service specified as part or all of the JID of the
       intended recipient does not exist or cannot be resolved
    """

    def __init__(self, request):
        StanzaError.__init__(self, request, "cancel",
                                        "remote-server-not-found")


class RemoteServerTimeoutError(StanzaError):
    """A remote server or service specified as part or all of the JID of the
       intended recipient (or needed to fulfill a request) was resolved but
       communications could not be established within a reasonable amount of
       time
    """

    def __init__(self, request):
        StanzaError.__init__(self, request, "wait", "remote-server-timeout")


class ResourceConstraintError(StanzaError):
    """The server or recipient is busy or lacks the system resources
       necessary to service the request
    """

    def __init__(self, request):
        StanzaError.__init__(self, request, "wait", "resource-constraint")


class ServiceUnavailableError(StanzaError):
    """The server or recipient does not currently provide the requested
        service
    """

    def __init__(self, request):
        StanzaError.__init__(self, request, "cancel", "resource-unavailable")


class SubscriptionRequiredError(StanzaError):
    """The requesting entity is not authorized to access the requested
       service because a prior subscription is necessary
    """

    def __init__(self, request):
        StanzaError.__init__(self, request, "auth", "subscription-required")


class UndefinedConditionError(StanzaError):
    """The error condition is not one of those defined by the other
       conditions
    """

    def __init__(self, request):
        StanzaError.__init__(self, request, "modify", "undefined-condition")


class UnexpectedRequestError(StanzaError):
    """The recipient or server understood the request but was not expecting
       it at this time
    """

    def __init__(self, request):
        StanzaError.__init__(self, request, "modify", "unexpected-request")
