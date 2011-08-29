"""
    pyfire.jid
    ~~~~~~~~~~

    Handle JID parsing and interpretation as per RFC-6122

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import re

from pyfire import util

RE_DOMAIN = re.compile("^(([a-zA-Z0-9]|[a-zA-Z][a-zA-Z0-9\-]" +
                       "*[a-zA-Z0-9])\.)*([A-Za-z]|" +
                       "[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$")


class JID(object):
    """Jabber ID"""

    __slots__ = ('local', 'domain', 'resource', 'real_domain')

    def __init__(self, jid, validate_on_init=True):
        super(JID, self).__init__()

        self.real_domain = False

        parts = unicode(jid).split('@', 1)
        if len(parts) == 2:
            self.local = parts[0]
            jid = parts[1]
        else:
            self.local = None
            jid = parts[0]

        parts = jid.split('/', 1)
        if len(parts) == 2:
            self.domain = parts[0]
            self.resource = parts[1]
        else:
            self.domain = parts[0]
            self.resource = None

        if validate_on_init:
            self.validate(raise_error=True)

    def __eq__(self, other):
        return self.local == other.local and \
               self.domain == other.domain and \
               self.resource == other.resource

    def __str__(self):
        if self.local is not None and \
           self.resource is not None:
            return "%s@%s/%s" % (self.local, self.domain, self.resource)
        elif self.local is not None:
            return "%s@%s" % (self.local, self.domain)
        elif self.resource is not None:
            return "%s/%s" % (self.domain, self.resource)
        else:
            return self.domain

    def validate(self, raise_error=False):
        """Validate JID, either return a bool or raise :py:exc:`ValueErrors`"""

        if self.domain is None or len(self.domain) < 1:
            if raise_error:
                raise ValueError("A domain is required")
            else:
                return False

        if self.domain.find(".") >= 0 or self.domain.find(":") >= 0:
            if not ((len(self.domain) < 256 and \
                     RE_DOMAIN.match(self.domain) is not None) or \
                    util.is_valid_ipv4(self.domain) or \
                    util.is_valid_ipv6(self.domain)):
                if raise_error:
                    raise ValueError("malformed domain")
                else:
                    return False
            self.real_domain = True
        else:
            if len(self.domain.encode("utf-8")) > 1024:
                if raise_error:
                    raise ValueError("malformed domain")
                else:
                    return False

        if self.local is not None:
            if len(self.local) < 1:
                if raise_error:
                    raise ValueError("local part too short")
                else:
                    return False

            if len(self.local.encode("utf-8")) > 1024:
                if raise_error:
                    raise ValueError("local part too long")
                else:
                    return False

            for char in self.local:
                number = ord(char)
                if not ((number in [0x21, 0x3B, 0x3D, 0x3F]) or \
                        (number >= 0x23 and number <= 0x25) or \
                        (number >= 0x28 and number <= 0x2E) or \
                        (number >= 0x30 and number <= 0x39) or \
                        (number >= 0x41 and number <= 0x7E) or \
                        (number >= 0x80 and number <= 0xD7FF) or \
                        (number >= 0xE000 and number <= 0xFFFD) or \
                        (number >= 0x10000 and number <= 0x10FFFF)
                        ):
                    if raise_error:
                        raise ValueError("malformed local part")
                    else:
                        return False

        if self.resource is not None:
            if len(self.resource) < 1:
                if raise_error:
                    raise ValueError("resource part too short")
                else:
                    return False

            if len(self.resource.encode("utf-8")) > 1024:
                if raise_error:
                    raise ValueError("resource part too long")
                else:
                    return False

            for char in self.resource:
                number = ord(char)
                if not ((number >= 0x20 and number <= 0xD7FF) or \
                        (number >= 0xE000 and number <= 0xFFFD) or \
                        (number >= 0x10000 and number <= 0x10FFFF)):
                    if raise_error:
                        raise ValueError("malformed resource")
                    else:
                        return False

        if not raise_error:
            return True

    @property
    def bare(self):
        """Return a bare JID (just local and domain part)"""

        if self.local is not None:
            return "%s@%s" % (self.local, self.domain)
        else:
            return self.domain
