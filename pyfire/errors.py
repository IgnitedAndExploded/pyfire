# -*- coding: utf-8 -*-
"""
    pyfire.errors
    ~~~~~~~~~~~~~~~~~~~~~~

    Holds the global used base errors

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import xml.etree.ElementTree as ET


class XMPPProtocolError(Exception):
    """Base class for all errors that can be
       sent via XMPP Protocol to peer
    """

    def __init__(self, error_element, error_namespace, error_name=None):
        self.error_name = error_name
        self.element = ET.Element(error_element)
        self.element.set("xmlns", error_namespace)

    def __unicode__(self):
        if self.error_name is not None:
            self.element.append(ET.Element(self.error_name))
        return unicode(ET.tostring(self.element))
