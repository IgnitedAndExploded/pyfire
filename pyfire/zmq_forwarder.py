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

from pyfire.jid import JID
import pyfire.configuration as config
from pyfire.logger import Logger

log = Logger(__name__)


class ZMQForwarder(object):
    """ZMQ Forwarder class"""

    def __init__(self):
        self.loop = ioloop.IOLoop()
        self.ctx = zmq.Context()

        # Init command channel
        comm_sock = self.ctx.socket(zmq.REP)
        comm_sock.bind(config.get('ipc', 'forwarder_command_channel'))
        self.command_channel = zmqstream.ZMQStream(comm_sock, self.loop)
        self.command_channel.on_recv(self.register_peer, False)

        self.pull_sock = self.ctx.socket(zmq.PULL)
        self.pull_sock.bind(config.get('ipc', 'forwarder'))
        self.stream = zmqstream.ZMQStream(self.pull_sock, self.loop)
        self.stream.on_recv(self.handle_stanza, False)

        self.peers = dict()

    def start(self):
        """Starts the IOloop"""
        self.loop.start()

    def handle_stanza(self, msg):
        """Callback handler used for forwarding received stanzas"""

        for message in msg:
            stanza = cPickle.loads(message.bytes)
            stanza_source = stanza.get('from')
            stanza_destination = stanza.get('to')
            log.debug("received stanza from %s to %s" % (stanza_source, stanza_destination))
            if stanza_destination is None:
                destination = JID(stanza_source).domain
                log.debug("setting to attribute to " + destination)
                stanza_destination = destination

            stanza_destination = JID(stanza_destination)
            if stanza_destination.bare in self.peers:
                log.debug("routing stanza from %s to %s" % (stanza_source, stanza_destination))
                self.peers[stanza_destination.bare][1].send(message.bytes)
            else:
                log.debug("Unknown message destination..")

    def register_peer(self, msg):
        """Callback for command channel that registeres a new peer"""

        # TODO: Add auth
        for me in list(msg):
            (push_url, jids) = cPickle.loads(me.bytes)
            log.info('registering new peer at '+push_url)
            peer = self.ctx.socket(zmq.PUSH)
            peer.connect(push_url)
            if isinstance(jids, JID):
                jids = [jids,]
            for jid in jids:
                log.info('adding routing entry for '+unicode(jid))
                jid = JID(jid)
                self.peers[jid.bare] = (jid, peer)
        self.command_channel.send('OK')
