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


import errno
import functools
import contextlib
import socket
import thread

from zmq.eventloop import ioloop
from tornado import iostream
from tornado.stack_context import StackContext

from pyfire import configuration as config
from pyfire import zmq_forwarder
from pyfire.auth.backends import DummyTrueValidator
from pyfire.server import XMPPServer, XMPPConnection
from pyfire.singletons import get_validation_registry

def start_client_listener(io_loop):
    server = XMPPServer(io_loop)
    server.bind(config.get('listeners', 'clientport'),
                config.get('listeners', 'ip'))
    server.start()

if __name__ == '__main__':
    validation_registry = get_validation_registry()
    validator = DummyTrueValidator()
    validation_registry.register('dummy', validator)

    io_loop = ioloop.IOLoop.instance()
    # create a forwader/router for internal communication
    fwd = zmq_forwarder.ZMQForwarder()
    thread.start_new_thread(fwd.start, ())

    start_client_listener(io_loop)
    try:
        io_loop.start()
    except (KeyboardInterrupt, SystemExit):
        io_loop.stop()
        print "exited cleanly"
