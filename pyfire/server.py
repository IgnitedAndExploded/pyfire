# -*- coding: utf-8 -*-
"""
    pyfire.server
    ~~~~~~~~~~~~~

    This module starts the main TCP listener for XMPP client communication so far.

    :copyright: (c) 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import SocketServer
from xmppconnection import XMPPConnection

class XMPPTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def __init__(self, sockaddr=("localhost", 5222), handler=XMPPConnection):
        SocketServer.TCPServer.__init__(self, sockaddr, handler)

def main():
    # starts the XMPP listener...
    server = XMPPTCPServer()
    print "Listening on %s:%s" % server.server_address
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()

if __name__ == '__main__':
    main()
