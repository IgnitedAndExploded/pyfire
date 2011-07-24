# -*- coding: utf-8 -*-
"""
    pyfire.server
    ~~~~~~~~~~~~~

    This module starts the main TCP listener for XMPP client communication so far.

    :copyright: (c) 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import SocketServer
from xmpphandler import XMPPHandler

def main():
    # starts the XMPP listener...
    HOST, PORT = "0.0.0.0", 5222
    server = SocketServer.TCPServer((HOST, PORT), XMPPHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
