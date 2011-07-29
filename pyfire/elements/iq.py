# -*- coding: utf-8 -*-
"""
    pyfire.iq
    ~~~~~~~~~~~~~

    This module handles XMPP iq packets

    :copyright: (c) 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import xml.etree.ElementTree as ET


class Iq(object):
    """This Class handles <iq> XMPP frames"""

    def handle(self, tree):
        """<iq> handler, returns a response that should be sent back"""

        # prepare result header
        # TODO: add from attribute
        iq = ET.Element("iq")
        iq.set("id", tree.get("id"))
        iq.set("type", "result")
        # dispatch to the handler for the given request query
        for req in list(tree):
            if req.tag in self.handler:
                data = self.handler[req.tag](self, req)
                if data != None:
                    iq.append(data)
        # return the result
        return iq

    def bind(self, request):
        """Handles bind requests"""
        # return dummy bind response for now
        bind = ET.Element("bind")
        bind.set("xmlns", "urn:ietf:params:xml:ns:xmpp-bind")
        jid = ET.SubElement(bind, "jid")
        if request.find("resource") != None:
            jid.text = "test@localhost/" + request.find("resource").text
        else:
            jid.text = "test@localhost/blahhhhh"
        return bind

    def session(self, request):
        """ No-op as suggested in RFC6121 Appendix E.
            Session establishment had been defined in RFC3921 Section 3
            and marked depricated in RFC6121.
        """
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