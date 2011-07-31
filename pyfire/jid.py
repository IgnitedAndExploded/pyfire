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

    def __init__(self, jid):
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

        self.validate(raiseerror=True)

    def __eq__(self, other):
        return self.local == other.local and \
               self.domain == other.domain and \
               self.resource == other.resource

    def __str__(self):
        if self.local and self.resource:
            return "%s@%s/%s" % (self.local, self.domain, self.resource)
        elif self.local:
            return "%s@%s" % (self.local, self.domain)
        else:
            return self.domain

    def validate(self, raiseerror=False):
        """Validate JID, either return a bool or raise :py:exc:`ValueErrors`"""

        if len(self.domain) < 1:
            if raiseerror:
                raise ValueError("A domain is required")
            else:
                return false

        if self.domain.find(".") > 1:
            if not ((RE_DOMAIN.match(self.domain) or \
                     len(self.domain) > 255) or \
                    util.is_valid_ipv4(self.domain) or \
                    util.is_valid_ipv6(self.domain)):
                if raiseerror:
                    raise ValueError("malformed domain")
                else:
                    return false
            self.real_domain = True
        else:
            if len(self.domain.encode("utf-8")) > 1024:
                if raiseerror:
                    raise ValueError("malformed domain")
                else:
                    return false

        if self.local:
            if len(self.local.encode("utf-8")) > 1024:
                if raiseerror:
                    raise ValueError("local part too long")
                else:
                    return false

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
                    if raiseerror:
                        raise ValueError("malformed local part")
                    else:
                        return false

        if self.resource:
            if len(self.resource.encode("utf-8")) > 1024:
                if raiseerror:
                    raise ValueError("resource part too long")
                else:
                    return false

            for char in self.resource:
                number = ord(char)
                if not ((number >= 0x20 and number <= 0xD7FF) or \
                        (number >= 0xE000 and number <= 0xFFFD) or \
                        (number >= 0x10000 and number <= 0x10FFFF)):
                    if raiseerror:
                        raise ValueError("malformed resource")
                    else:
                        return false

        if not raiseerror:
            return true

    @property
    def bare(self):
        """Return a bare JID (just local and domain part)"""
        if not self.local:
            raise AttributeError("JID lacks a local part")
        return "%s@%s" % (self.local, self.domain)
