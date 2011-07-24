# -*- coding: utf-8 -*-
"""
    pyfire.module
    ~~~~~~~~~~~~~

    This module implements the basic XMPP communication server-side.

    :copyright: (c) 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import SocketServer
from socket import SHUT_RDWR, timeout
from time import sleep

class XMPPHandler(SocketServer.BaseRequestHandler):
  
  def handle(self):
    """ Starts the handling for a new connection """
    print "New connection from %s:%i" % self.client_address

    self.request.settimeout(0.1)
    
    try:
      while( 1 ):
	## main loop
	try:
	  data = self.request.recv( 2048 )
	  # if not data received the socket seems to have closed so terminate the connection
	  if not data:
	    break	  
	except timeout:
	  pass

	  # do some useful stuff here :)

    except:
      raise
    finally:
      self.request.shutdown(SHUT_RDWR)
      self.request.close()

  def finish(self):
    """ called upon socket shutdown either from client- or severside """
    print "Connection closed...\n"
    