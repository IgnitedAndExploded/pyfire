#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Sample Server

    This module starts the main TCP listener for XMPP clients

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import sys
import os.path
# Add pyfire to namespace
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(path)

import SocketServer

from pyfire import configuration as config
from pyfire.auth.backends import DummyTrueValidator
from pyfire.auth.registry import AuthHandlerRegistry, ValidationRegistry
from pyfire.stream.sockethandler import XMPPSocketHandler


class XMPPTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def __init__(self,
                 sockaddr=(config.get('listeners', 'ip'),
                           config.getint('listeners', 'clientport')),
                 handler=XMPPSocketHandler):
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
