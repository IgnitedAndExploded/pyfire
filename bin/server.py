#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Sample Server

    This module starts the main TCP listener for XMPP clients

    :copyright: (c) 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import SocketServer
from pyfire.xmppconnection import XMPPConnection
from pyfire.auth.backends import DummyTrueValidator
from pyfire.auth.registry import AuthHandlerRegistry, ValidationRegistry


class XMPPTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def __init__(self, sockaddr=("localhost", 5222), handler=XMPPConnection):
        SocketServer.TCPServer.__init__(self, sockaddr, handler)

        # init auth backends
        validation_registry = ValidationRegistry()
        self.auth_registry = AuthHandlerRegistry(validation_registry)

        validator = DummyTrueValidator()
        validation_registry.register('dummy', validator)


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
