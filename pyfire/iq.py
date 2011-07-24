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
        if tree.find("bind") != None:
            # return dummy bind response for now
            res = tree
            res.set("type", "result")
            bind = res.find("bind")
            jid = Element("jid")
            bind.append(jid)
            if bind.find("resource") != None:
                jid.text = "test@localhost/"+bind.find("resource").text
                bind.remove(bind.find("resource"))
            else:
                jid.text = "test@localhost/blahhhhh"
            
        return res
