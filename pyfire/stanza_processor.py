#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Stanza Processor

    This module starts a stanza processor that is responsible for
    processing all stanzas addressed to the local domain(s)

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
 
import zmq
from zmq.eventloop import ioloop, zmqstream
import xml.etree.ElementTree as ET

from pyfire.logger import Logger
from pyfire import configuration as config

log = Logger(__name__)

class StanzaProcessor(object):
    """Holds a stanza handler for local domains"""

    def __init__(self, local_domains = ("localhost")):
        self.local_domains = local_domains
        self.loop = ioloop.IOLoop.instance()
        self.ctx = zmq.Context()

        log.debug('Registering StanzaProcessor at forwarder..')
        router = self.ctx.socket(zmq.REQ)
        router.connect(config.get('ipc', 'forwarder_command_channel'))

        # TODO: add auth for authenticating us at the forwarder when it supports it
        router.send(' ')
        self.pub_url, self.sub_url = router.recv_json()
        router.close()

        self.pub_socket = self.ctx.socket(zmq.PUB)
        self.pub_socket.bind(self.pub_url)
        sub_socket = self.ctx.socket(zmq.SUB)
        sub_socket.connect(self.sub_url)
        # TODO: only subscribe to local domains
        sub_socket.setsockopt(zmq.SUBSCRIBE, '')
        substream = zmqstream.ZMQStream(sub_socket, self.loop)
        substream.on_recv(self.handle_stanza)

    def start(self):
        """Starts the handling of the bundles IOLoop"""
        self.loop.start()

    def handle_stanza(self, msg_list):
        """This actually handles the incomming stamzas"""
        for msg in msg_list:
            log.debug("Received stanza: "+msg)
