# -*- coding: utf-8 -*-
"""
    pyfire.module
    ~~~~~~~~~~~~~

    This module implements the basic XMPP communication server-side.

    :copyright: (c) 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import SocketServer

class XMPPHandler(SocketServer.BaseRequestHandler):
  
  def handle(self):
    """ Starts the handling for a new connection """
    print "New connection from " + self.client_address[0] + ":" + str(self.client_address[1])
    
    # do some useful stuff here :)
    
    