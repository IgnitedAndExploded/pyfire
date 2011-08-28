# -*- coding: utf-8 -*-
"""
    pyfire.singletons
    ~~~~~~~~~~~~~~~~~

    Contains all singleton classes we use

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

from thread import allocate_lock

import zmq

from pyfire.auth.registry import ValidationRegistry
import pyfire.configuration as config
from pyfire.logger import Logger

log = Logger(__name__)

_known_jids = None
_known_jids_lock = allocate_lock()

def get_known_jids():
    """Returns the list with known jids"""
    global _known_jids
    _known_jids_lock.acquire()
    if _known_jids == None:
        _known_jids = ThreadSafeList()
    _known_jids_lock.release()
    return _known_jids

class ThreadSafeList(list):
    """List implementation with threadsafe append and remove methods"""

    def append(self, content):
        with _known_jids_lock:
            super(ThreadSafeList, self).append(content)

    def remove(self, content):
        with _known_jids_lock:
            super(ThreadSafeList, self).remove(content)


_publisher = None
_publisher_lock = allocate_lock()

def get_publisher():
    """Returns the application publish socket"""
    global _publisher
    _publisher_lock.acquire()
    if _publisher == None:
        _publisher = StanzaPublisher()
    _publisher_lock.release()
    return _publisher


class StanzaPublisher(object):
    """Handles the publish socket"""

    def __init__(self):
        self.zmq_context = zmq.Context()

        # connect to forwarder/router
        log.debug('Registering StanzaPublisher at forwarder..')
        router = self.zmq_context.socket(zmq.REQ)
        router.connect(config.get('ipc', 'forwarder_command_channel'))

        # TODO: add auth for authenticating us at the forwarder when it supports it
        router.send(' ')
        self.pub_url, self.sub_url = router.recv_json()
        router.close()

        self.pub_socket = self.zmq_context.socket(zmq.PUB)
        self.pub_socket.bind(self.pub_url)

    def send(self, msg):
        with _publisher_lock:
            self.pub_socket.send(msg)

_validation_registry = None
_validation_registry_lock = allocate_lock()

def get_validation_registry():
    """Returns the jid auth validation registry"""
    global _validation_registry
    with _validation_registry_lock:
        if _validation_registry == None:
            _validation_registry = ValidationRegistry()
    return _validation_registry