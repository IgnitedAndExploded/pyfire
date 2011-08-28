#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    pyfire.zmq_forwarder

    This Class holds a forwarder implementation for ZMQs PUB/SUB messages as
    the included forwarder device does not work as espected.

:copyright: 2011 by the pyfire Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import random
import zmq
from zmq.eventloop import ioloop, zmqstream

import pyfire.configuration as config
from pyfire.logger import Logger

log = Logger(__name__)


class ZMQForwarder(object):
    """ZMQ Forwarder class"""

    def __init__(self):
        self.loop = ioloop.IOLoop.instance()
        self.ctx = zmq.Context()

        # Init command channel
        comm_sock = self.ctx.socket(zmq.REP)
        comm_sock.bind(config.get('ipc', 'forwarder_command_channel'))
        self.command_channel = zmqstream.ZMQStream(comm_sock, self.loop)
        self.command_channel.on_recv(self.register_peer)

        self.output_url = 'tcp://127.0.0.1:%i' % ( random.randint(15000,15500) )
        self.output = self.ctx.socket(zmq.PUB)
        self.output.bind(self.output_url)

    def start(self):
        """Starts the IOloop"""
        self.loop.start()

    def handle_stanza(self, msg):
        """Callback handler used for forwarding received stanzas"""

        for line in msg:
            self.output.send(line)

    def register_peer(self, msg):
        """Callback for command channel that registeres a new peer"""

        subscriber = 'tcp://127.0.0.1:%i' % ( random.randint(5600,5700) )
        log.info('registering new subscriber at '+subscriber)
        new_sub = self.ctx.socket(zmq.SUB)
        new_sub.connect(subscriber)
        new_sub.setsockopt(zmq.SUBSCRIBE, '')
        substream = zmqstream.ZMQStream(new_sub, self.loop)
        substream.on_recv(self.handle_stanza)
        self.command_channel.send_json((subscriber, self.output_url))
