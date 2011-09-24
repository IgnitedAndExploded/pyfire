#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    pyfire.zmq_forwarder

    This Class holds a stanza router implementation for XMPP stanzas transmitted via
    ZMQs PUSH/PULL messages.

:copyright: 2011 by the pyfire Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""

import uuid
import random
import cPickle
import zmq
from zmq.eventloop import ioloop, zmqstream

import xml.etree.ElementTree as ET

from pyfire.jid import JID
from pyfire.logger import Logger
from pyfire.stream.errors import InternalServerError

log = Logger(__name__)


class ZMQForwarder(object):
    """ZMQ Forwarder class"""

    def __init__(self, forwarder_url):
        self.loop = ioloop.IOLoop()
        self.ctx = zmq.Context()

        # Create our PULL listener to listen to the world ;)
        self.pull_sock = self.ctx.socket(zmq.PULL)
        log.debug('Listening at ' + forwarder_url)
        self.pull_sock.bind(forwarder_url)
        self.stream = zmqstream.ZMQStream(self.pull_sock, self.loop)
        self.stream.on_recv(self.handle_stanza, False)

        self.peers = dict()

    def start(self):
        """Starts the IOloop"""
        self.loop.start()

    def handle_stanza(self, zmq_messages):
        """Callback handler used for handling pulled messages"""

        # Handle all pulled ZMQ messages
        for zmq_message in zmq_messages:
            message = cPickle.loads(zmq_message.bytes)

            if isinstance(message, ZMQForwarder_message):
                self.handle_forwarder_message(message)
            else:
                self.route_stanza(message, zmq_message.bytes)

    def route_stanza(self, stanza, raw_bytes):
        """Takes care of routing stanzas supplied to their addressed destination"""

        stanza_source = JID(stanza.get('from'))
        stanza_destination = stanza.get('to')
        log.debug("received stanza from %s to %s" % (stanza_source, stanza_destination))
        if stanza_destination is None:
            destination = stanza_source.domain
            log.debug("setting to attribute to " + destination)
            stanza_destination = destination

        stanza_destination = JID(stanza_destination)
        try:
            for peer in self.peers[stanza_destination.bare]:
                # Send to peer if the stanza has a bare jid as recipient
                # or if the full jid matches
                if (stanza_destination.resource is None \
                            and stanza_source != peer[0]) \
                            or stanza_destination == peer[0]:
                    log.debug("routing stanza from %s to %s" % (stanza_source, peer[0]))
                    peer[1].send(raw_bytes)
        except KeyError:
            log.debug("Unknown message destination..")
            # Do not send errors if we cant deliver error messages
            if stanza.find('error') is None:
                # import error here on demand to prevent import loop
                from pyfire.stream.stanzas.errors import ServiceUnavailableError
                error_message = ServiceUnavailableError(stanza)
                self.route_stanza(error_message.element, cPickle.dumps(error_message.element))

    def handle_forwarder_message(self, msg):
        """Handles incoming command requests from peer"""

        if msg.command == 'REGISTER':
            (push_url, jids) = msg.attributes
            log.info('registering new peer at ' + push_url)
            peer = self.ctx.socket(zmq.PUSH)
            peer.connect(push_url)
            if isinstance(jids, JID):
                jids = [jids, ]
            for jid in jids:
                log.info('adding routing entry for ' + unicode(jid))
                jid = JID(jid)
                try:
                    # append to bare jids list of existing connections
                    self.peers[jid.bare].append((jid, peer))
                except KeyError:
                    # create new entry
                    self.peers[jid.bare] = [(jid, peer), ]
        else:
            raise InternalServerError()


class ZMQForwarder_message(object):
    """ZMQ Forwarder message class is used to control the forwarder from other parts of the software"""

    __slots__ = ('command', 'attributes')

    def __init__(self, command='', attributes=()):
        self.command = command
        self.attributes = attributes
