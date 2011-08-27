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

from zmq.eventloop import ioloop
from tornado import iostream
from tornado.stack_context import StackContext

from pyfire import configuration as config
from pyfire.server import XMPPServer, XMPPConnection


def start_client_listener():
    io_loop = ioloop.IOLoop.instance()
    server = XMPPServer(io_loop)
    server.bind(config.get('listeners', 'clientport'),
                config.get('listeners', 'ip'))
    server.start()
    try:
        io_loop.start()
    except (KeyboardInterrupt, SystemExit):
        io_loop.stop()
        print "exited cleanly"

if __name__ == '__main__':
    start_client_listener()
