# -*- coding: utf-8 -*-
"""
    pyfire.iq
    ~~~~~~~~~~~~~

    This module handles XMPP iq packets

    :copyright: (c) 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from base64 import b64decode
from xml.etree.ElementTree import Element, tostring


class Iq():
    """This Class handles <iq> XMPP frames"""

    def handle(self, tree):
        """<iq> handler, returns a response that should be sent back"""

        # prepare result header
        # TODO: add from attribute
        res = Element("iq")
        res.set("id", tree.get("id"))
        res.set("type", "result")
        # dispatch to the handler for the given request query
        for req in list(tree):
            if req.tag in self.handler:
                data = self.handler[req.tag](self, req)
                if data != None:
                    res.append(data)
        # return the result
        return res

    def bind(self, request):
        """Handles bind requests"""
        # return dummy bind response for now
        res = Element("bind")
        res.set("xmlns", "urn:ietf:params:xml:ns:xmpp-bind")
        jid = Element("jid")
        res.append(jid)
        if request.find("resource") != None:
            jid.text = "test@localhost/" + request.find("resource").text
        else:
            jid.text = "test@localhost/blahhhhh"
        return res

    def session(self, request):
        """Implements the session command specified in RFC3921 Chapter 3 """
        # TODO: create session
        return None

    def query(self, request):
        """Implements the query command"""
        """
            TODO: implement namespaces:
                    jabber:iq:private -> XEP-0049
                    jabber:iq:roster -> RFC 6121
        """

    handler = {
      'bind': bind,
      'session': session,
      'query': query
    }
