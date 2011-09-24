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
import zmq
import thread
import time


class TestZMQForwarder(PyfireTestCase):

    def setUp(self):
        self.forwarder_url = "tcp://127.0.0.1:42050"
        self.forwarder = zmq_forwarder.ZMQForwarder(self.forwarder_url)
        #thread.start_new_thread(self.forwarder.start, ())

        #self.ctx = zmq.Context()

    def tearDown(self):
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

