# -*- coding: utf-8 -*-
"""
    pyfire.iq
    ~~~~~~~~~~~~~

    This module handles XMPP iq packets

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import xml.etree.ElementTree as ET
from pyfire.contact import Contact

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
            else:
                for elem in self.failure(req):
                    iq.append(elem)
                iq.set("type", "error")
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
        """

        response = ET.Element("query")
        if request.get("xmlns") == """http://jabber.org/protocol/disco#info""":
            features = [
                'urn:xmpp:ping', # XEP-0199
            ]

            response.set("xmlns", """http://jabber.org/protocol/disco#info""")
            for feature in features:
                feat_elem = ET.SubElement(response, "feature")
                feat_elem.set("var", feature)
        elif request.get("xmlns") == """jabber:iq:roster""":
            response.set("xmlns", """jabber:iq:roster""")
            """ TODO: return real roster """
            contact = Contact("test@localhost")
            contact.subscription = "both"
            contact.approved = "true"
            response.append(contact.to_element())
            contact = Contact("test2@localhost")
            contact.approved = "true"
            contact.subscription = "both"
            response.append(contact.to_element())
        elif request.get("xmlns") == """jabber:iq:last""":
            """XEP-0012"""
            response.set("xmlns", "jabber.iq.last")
            """ TODO: set real last activity of requested contact """
            response.set("seconds", "0")

        return response

    def ping(self, request):
        """A No-op for XEP-0199"""

    def vcard(self, request):
        """Returns the users vCard as specified by XEP-0054"""
        """ TODO: Stub - Implement real vCard storage """
        return ET.Element("vCard")

    def failure(self, requested_service):
        error = ET.Element("error")
        error.set("type", "cancel")
        service = ET.SubElement(error, "service-unavailable")
        service.set("xmlns", "urn:ietf:params:xml:ns:xmpp-stanzas")
        return [requested_service, error]

    handler = {
      'bind': bind,
      'session': session,
      'query': query,
      'ping': ping,
      'vCard': vcard
    }
