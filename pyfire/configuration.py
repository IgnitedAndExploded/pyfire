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
config.set('database', 'dburi', 'sqlite:///pyfire.db')

config.add_section('listeners')
config.set('listeners', 'ip', '127.0.0.1')
config.set('listeners', 'clientport', '5222')
# TODO: Temporary item until database stored config is available
config.set('listeners', 'domains', 'localhost')

config.add_section('logging')
config.set('logging', 'global_level', 'ERROR')

config.add_section('ipc')
config.set('ipc', 'forwarder_command_channel', 'tcp://127.0.0.1:42040')
config.set('ipc', 'forwarder', 'tcp://127.0.0.1:42042')

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
set = config.set
