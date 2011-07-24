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

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def main():
    # starts the XMPP listener...
    HOST, PORT = "0.0.0.0", 5222
    server = ThreadedTCPServer((HOST, PORT), XMPPConnection)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()

if __name__ == '__main__':
    main()
