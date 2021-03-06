# -*- coding: utf-8 -*-
"""
    pyfire.stream.stanzas.iq
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Handles XMPP iq packets

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from pyfire.jid import JID
import xml.etree.ElementTree as ET
from pyfire.stream.stanzas.iq.query import Query


class Iq(object):
    """This Class handles <iq> XMPP frames"""

    def __init__(self):
        super(Iq, self).__init__()
        self.from_jid = None

    def create_response(self, content, iq_id=None):
        """Set up an iq response"""
        # prepare result header
        iq = ET.Element("iq")
        iq.set("id", iq_id or self.tree.get("id"))
        iq.set("type", "result")
        iq.set("from", self.from_jid.domain)
        iq.set("to", self.tree.get("from"))
        iq.append(content)
        return iq

    def handle(self, tree):
        """<iq> handler, returns one or more <iq> tags with results and new ones if required"""

        self.from_jid = JID(tree.get("from"))
        self.tree = tree

        responses = []
        # dispatch to the handler for the given request query
        for req in list(tree):
            if tree.get("type") == "get":
                try:
                    data = self.get_handler[req.tag](self, req)
                    if data != None:
                        responses.append(self.create_response(data))
                except KeyError as e:
                    for elem in self.failure(req):
                        iq.append(elem)
                    iq.set("type", "error")
        # return the result
        return responses

    def bind(self, request):
        """Handles bind requests"""
        bind = ET.Element("bind")
        bind.set("xmlns", "urn:ietf:params:xml:ns:xmpp-bind")
        jid = ET.SubElement(bind, "jid")
        # add resource to JID if provided
        if request.find("resource") != None:
            self.from_jid.resource = request.find("resource").text
            if not self.from_jid.validate():
                self.from_jid.resource = None

        jid.text = unicode(self.from_jid)
        return bind

    def session(self, request):
        """ No-op as suggested in RFC6121 Appendix E.
            Session establishment had been defined in RFC3921 Section 3
            and marked depricated in RFC6121.
        """
        return None

    def query(self, request):
        """Implements the query command"""
        handler = Query()
        return handler.handle(request, self.tree.get("from"))

    def ping(self, request):
        """A No-op for XEP-0199"""

    def vcard(self, request):
        """Returns the users vCard as specified by XEP-0054"""

        # TODO: Stub - Implement real vCard storage
        return ET.Element("vCard")

    def failure(self, requested_service):
        error = ET.Element("error")
        error.set("type", "cancel")
        service = ET.SubElement(error, "service-unavailable")
        service.set("xmlns", "urn:ietf:params:xml:ns:xmpp-stanzas")
        return [requested_service, error]

    get_handler = {
      'bind': bind,
      'session': session,
      'query': query,
      'ping': ping,
      'vCard': vcard
    }
