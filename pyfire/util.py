# -*- coding: utf-8 -*-
"""
    pyfire.util
    ~~~~~~~~~~~

    Various helper functions

    :copyright: (c) 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import socket


def is_valid_ipv4(address):
    try:
        addr = socket.inet_pton(socket.AF_INET, address)
    except socket.error:
        return False
    return True


def is_valid_ipv6(address):
    try:
        addr = socket.inet_pton(socket.AF_INET6, address)
    except socket.error:
        return False
    return True
