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

from pyfire import configuration as config
from pyfire import zmq_forwarder, stanza_processor
from pyfire.auth.backends import DummyTrueValidator
from pyfire.server import XMPPServer, XMPPConnection
from pyfire.singletons import get_validation_registry, get_publisher

def start_client_listener():
    publisher = get_publisher()
    validation_registry = get_validation_registry()
    validator = DummyTrueValidator()
    validation_registry.register('dummy', validator)

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

def fire_up():
    import pyfire.storage
    import pyfire.contact
    pyfire.storage.Base.metadata.create_all(pyfire.storage.engine)

    # create a forwader/router for internal communication
    fwd = zmq_forwarder.ZMQForwarder(config.get('ipc', 'forwarder'))
    thread.start_new_thread(fwd.start, ())

    # create a stamza processor for local domains
    stanza_proc = stanza_processor.StanzaProcessor(config.getlist('listeners', 'domains'))
    thread.start_new_thread(stanza_proc.start, ())

    # start listener for incomming Connections
    start_client_listener()

if __name__ == '__main__':
    fire_up()
