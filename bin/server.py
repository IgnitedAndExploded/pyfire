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


# TODO: move to Server!!
def check_for_closed_connections():
    print "checking for closed connections"
    streamlist = connections.keys()
    for stream in streamlist:
        if stream.closed():
            print "detected dead stream"
            del connections[stream]
            if len(connections) == 0:
                print "stopping checker"
                checker.stop()

checker = ioloop.PeriodicCallback(check_for_closed_connections,5000)

connections = {}
def connection_ready(sock, fd, events):
    i=1
    while True:
        try:
            connection, address = sock.accept()
        except socket.error, e:
            if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                raise
            return
        connection.setblocking(0)
        io_loop = ioloop.IOLoop.instance()
        stream = iostream.IOStream(connection, io_loop=io_loop)
        connections[stream] = XMPPConnection(stream)
        if not checker._running:
            checker.start()

if __name__ == '__main__':
    io_loop = ioloop.IOLoop.instance()
    server = XMPPServer(connection_ready, io_loop)
    server.bind(config.get('listeners', 'clientport'), config.get('listeners', 'ip'))
    server.start()
    try:
        io_loop.start()
    except (KeyboardInterrupt, SystemExit):
        io_loop.stop()
        print "exited cleanly"
