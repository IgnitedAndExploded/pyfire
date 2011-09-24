# -*- coding: utf-8 -*-
"""
    pyfire.tests.stream.test_zmqforwarder
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Unittests for ZMQ Forwarder/router

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import xml.etree.ElementTree as ET

from pyfire.tests import PyfireTestCase

from pyfire import zmq_forwarder
from pyfire.stream.errors import InternalServerError
from pyfire.stream.stanzas.errors import ServiceUnavailableError
import zmq
import thread
import time


class TestZMQForwarder(PyfireTestCase):

    def setUp(self):
        self.forwarder_url = "tcp://127.0.0.1:42050"
        self.forwarder = zmq_forwarder.ZMQForwarder(self.forwarder_url)
        thread.start_new_thread(self.forwarder.start, ())

        self.ctx = zmq.Context()

    def tearDown(self):
        self.forwarder.loop.stop()
        self.forwarder.pull_sock.close()

    def test_register_peer(self):
        reg_cmd = zmq_forwarder.ZMQForwarder_message('REGISTER')
        reg_cmd.attributes = ('tcp://127.0.0.1:1234', ['localhost',])
        self.forwarder.handle_forwarder_message(reg_cmd)
        self.assertEqual( len(self.forwarder.peers), 1)

    def test_unknown_command(self):
        reg_cmd = zmq_forwarder.ZMQForwarder_message('NOT_IMPLEMENTED')
        reg_cmd.attributes = ('tcp://127.0.0.1:1234', ['localhost',])
        with self.assertRaises(InternalServerError):
            self.forwarder.handle_forwarder_message(reg_cmd)

    def test_route_message(self):
        forwarder = self.ctx.socket(zmq.PUSH)
        forwarder.connect(self.forwarder_url)

        pull_socket = self.ctx.socket(zmq.PULL)
        test_port = pull_socket.bind_to_random_port('tcp://127.0.0.1')

        reg_cmd = zmq_forwarder.ZMQForwarder_message('REGISTER')
        reg_cmd.attributes = ('tcp://127.0.0.1:' + str(test_port), ['testhost',])
        forwarder.send_pyobj(reg_cmd)

        test_stanza = ET.Element('Iq')
        test_stanza.set('id', '1')
        test_stanza.set('from', 'testhost')
        test_stanza.set('to', 'testhost')
        forwarder.send_pyobj(test_stanza)

        received_stanza = pull_socket.recv_pyobj()
        self.assertEqual(ET.tostring(test_stanza), ET.tostring(received_stanza))

    def test_route_unknownrecipient(self):
        forwarder = self.ctx.socket(zmq.PUSH)
        forwarder.connect(self.forwarder_url)

        pull_socket = self.ctx.socket(zmq.PULL)
        test_port = pull_socket.bind_to_random_port('tcp://127.0.0.1')

        reg_cmd = zmq_forwarder.ZMQForwarder_message('REGISTER')
        reg_cmd.attributes = ('tcp://127.0.0.1:' + str(test_port), ['testsender',])
        forwarder.send_pyobj(reg_cmd)

        test_stanza = ET.Element('Iq')
        test_stanza.set('id', '1')
        test_stanza.set('from', 'testsender')
        test_stanza.set('to', 'unknown')
        expected_stanza = ServiceUnavailableError(test_stanza).element

        forwarder.send_pyobj(test_stanza)
        received_stanza = pull_socket.recv_pyobj()

        self.assertEqual(ET.tostring(expected_stanza), ET.tostring(received_stanza))
