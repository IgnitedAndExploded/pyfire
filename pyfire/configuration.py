# -*- coding: utf-8 -*-
"""
    pyfire.configuration
    ~~~~~~~~~~~~~~~~~~~~

    Holds and reads/writes configuration settings

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import ConfigParser
import os.path

config = ConfigParser.SafeConfigParser()

config.add_section('database')
config.set('database', 'engine', 'sqlite')
config.set('database', 'name', '')
config.set('database', 'user', '')
config.set('database', 'password', '')
config.set('database', 'host', '')
config.set('database', 'port', '')
config.set('database', 'custom_url', '')

config.add_section('listeners')
config.set('listeners', 'ip', '127.0.0.1')
config.set('listeners', 'clientport', '5222')
# TODO: Temporary item until database stored config is available
config.set('listeners', 'domains', 'localhost')

config.add_section('logging')
config.set('logging', 'global_level', 'ERROR')

config.add_section('ipc')
config.set('ipc', 'to_router', 'tcp://127.0.0.1:5556')
config.set('ipc', 'to_client', 'tcp://127.0.0.1:5557')

config.read(['pyfire.cfg', os.path.expanduser('~/.pyfire.cfg')])


def getlist(section, option, separator=','):
    """Make a list from an option. By default split on comma."""
    items = config.get(section, option)
    splits = items.split(separator)
    return [item.strip() for item in splits]

# some handy shortcuts
get = config.get
getint = config.getint
NoOptionError = ConfigParser.NoOptionError
