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

    def handle(self, tree):
        """handler for iq requests, returns a response that should be sent back"""

        # prepare result header
        res = Element("iq")
        res.set("id", tree.get("id"))
        res.set("type", "result")
        # dispatch to the handler for the given request query
        for req in list(tree):
            if req.tag in handler:
                res.append(handler[req.tag](self, req))
        # return the result
        return res

    def bind(self, request):
        """handles bind requests"""
        # return dummy bind response for now
        res = Element("bind")
        res.set("xmlns", "urn:ietf:params:xml:ns:xmpp-bind")
        jid = Element("jid")
        res.append(jid)
        if request.find("resource") != None:
            jid.text = "test@localhost/"+request.find("resource").text
        else:
            jid.text = "test@localhost/blahhhhh"
        return res

handler = {'bind': Iq.bind}
