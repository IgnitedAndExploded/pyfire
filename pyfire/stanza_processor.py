#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Stanza Processor

    This module starts a stanza processor that is responsible for
    processing all stanzas addressed to the local domain(s)

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import cPickle
import zmq
from zmq.eventloop import ioloop, zmqstream
import xml.etree.ElementTree as ET

from pyfire.logger import Logger
from pyfire import configuration as config
from pyfire.stream.stanzas import iq, message, presence
from pyfire.stream.stanzas.errors import StanzaError, FeatureNotImplementedError

log = Logger(__name__)


class StanzaProcessor(object):
    """Holds a stanza handler for local domains"""

    def __init__(self, local_domains=("localhost")):
        self.local_domains = local_domains
        self.current_topic = None
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
        for domain in self.local_domains:
            sub_socket.setsockopt(zmq.SUBSCRIBE, domain)
        substream = zmqstream.ZMQStream(sub_socket, self.loop)
        substream.on_recv(self.handle_stanza)

        # init the handlers
        self.stanza_handlers = {
                'iq': iq.Iq(),
                'message': message.Message(),
                'presence': presence.Presence()
            }

    def start(self):
        """Starts the handling of the bundles IOLoop"""
        self.loop.start()

    def handle_stanza(self, msg):
        """This actually handles the incomming stamzas"""
        if self.current_topic is None:
            self.current_topic = msg[0]
            return

        # TODO: check if we really want to handle the topis set..
        tree = cPickle.loads(msg[0].split('\n'))
        log.debug("Received stanza to handle: " + ET.tostring(tree))

        try:
            if tree.tag not in self.stanza_handlers:
                raise FeatureNotImplementedError(tree)

            response = self.stanza_handlers[tree.tag].handle(tree)
            if response is not None:
                self.pub_socket.send_multipart((tree.get("from"), cPickle.dumps(response)))
        except StanzaError, e:
            # send cought errors back to sender
            self.pub_socket.send_multipart((tree.get("from"), unicode(e)))

        # reset topic when we handled it..
        self.current_topic = None
