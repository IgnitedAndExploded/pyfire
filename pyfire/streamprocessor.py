# -*- coding: utf-8 -*-
"""
    pyfire.streamprocessor
    ~~~~~~~~~~~~~~~~~~~~~~

    Implementation of XMPP Stream processing

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

try:
    from collections import OrderedDict
except ImportError:
    from sqlalchemy.util import OrderedDict

import xml.etree.ElementTree as ET
from xml.sax.handler import ContentHandler


class UnknownStreamException(Exception):
    """Stream starts with something other than XMPP control"""
    pass


class XMPPContentHandler(ContentHandler):
    """Process content from parser, tracking parsing depths

       Passes a streamhandler attributes from stream start and
       :class:`ET.Element` nodes to the provided content handler
    """

    def __init__(self, streamhandler, contenthandler):
        self.streamhandler = streamhandler
        self.contenthandler = contenthandler
        self.treebuilder = ET.TreeBuilder()

    def startDocument(self):
        self.depth = 0

    def endDocument(self):
        self.depth = 0

    def startElement(self, name, attrs):
        """map element stream to ET elements as they occur"""
        # first level, stream starts
        if self.depth == 0:
            if name != "stream:stream":
                raise UnknownStreamException
            self.streamhandler(attrs)
            self.depth = 1
        # second level creates element tree
        else:
            self.treebuilder.start(name, self.makedictfromattrs(attrs))
            self.depth += 1

    def endElement(self, name):
        if self.depth == 1:
            self.streamhandler({})
            self.depth = 0
        elif self.depth >= 2:
            self.treebuilder.end(name)
            self.depth -= 1
            if self.depth == 1:
                tree = self.treebuilder.close()
                self.contenthandler(tree)

    def characters(self, content):
        self.treebuilder.data(content)

    def makedictfromattrs(self, attrs):
        """Attributes from sax are not dictionaries. ElementTree doesn't
           copy automatically, so do it here and convert to ordered dict."""
        retdict = OrderedDict()
        for k, v in attrs.items():
            retdict[k] = v
        return retdict
