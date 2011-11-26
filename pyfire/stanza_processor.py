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
from pyfire.zmq_forwarder import ZMQForwarder_message
from pyfire import configuration as config
from pyfire.stream.stanzas import iq, message, presence
from pyfire.stream.stanzas.errors import StanzaError, FeatureNotImplementedError

log = Logger(__name__)


class StanzaProcessor(object):
    """Holds a stanza handler for local domains"""

    def __init__(self, local_domains=("localhost")):
        self.local_domains = local_domains
        self.loop = ioloop.IOLoop()
        self.ctx = zmq.Context()

        log.debug('Registering StanzaProcessor at forwarder..')
        # connect push socket to forwarder
        self.forwarder = self.ctx.socket(zmq.PUSH)
        self.forwarder.connect(config.get('ipc', 'forwarder'))

        pull_socket = self.ctx.socket(zmq.PULL)
        stream = zmqstream.ZMQStream(pull_socket, self.loop)
        stream.on_recv(self.handle_stanza, False)
        port = pull_socket.bind_to_random_port('tcp://127.0.0.1')

        # register connection at forwarder
        reg_msg = ZMQForwarder_message('REGISTER')
        reg_msg.attributes = (config.get('ipc', 'password'), 'tcp://127.0.0.1:' + str(port), local_domains)
        self.forwarder.send_pyobj(reg_msg)

        # init the handlers
        self.stanza_handlers = {
                'iq': iq.Iq(),
                'message': message.Message(),
                'presence': presence.Presence()
            }

    def start(self):
        """Starts the handling of the bundles IOLoop"""
        self.loop.start()

    def handle_stanza(self, msgs):
        """This actually handles the incomming stamzas"""
        for msg in msgs:
            tree = cPickle.loads(msg.bytes)
            if tree.get("to") is None or tree.get("to") in self.local_domains:
                log.debug("Received stanza to handle: " + ET.tostring(tree))

                try:
                    if tree.tag not in self.stanza_handlers:
                        raise FeatureNotImplementedError(tree)

                    response = self.stanza_handlers[tree.tag].handle(tree)
                    if response is not None:
                        if isinstance(response, (list, tuple)):
                            for resp in response:
                                self.forwarder.send(cPickle.dumps(resp))
                        else:
                            self.forwarder.send(cPickle.dumps(response))
                except StanzaError, e:
                    # send caught errors back to sender
                    self.forwarder.send(cPickle.dumps(e.element))
