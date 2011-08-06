# -*- coding: utf-8 -*-
"""
    pyfire.logger
    ~~~~~~~~~~~~~

    Use pocoo's logbook or a simple no-op fallback

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import warnings
import pyfire.configuration as config

try:
    import logbook

    class Logger(logbook.Logger):
        def __init__(self, name):
            try:
                level = config.get('logging', name.replace('.', '_')).upper()
            except config.NoOptionError:
                level = ''

            if not level:
                level = config.get('logging', 'global_level').upper()

            if level not in frozenset(['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']):
                warnings.warn("No such loglevel %s" % level, RuntimeWarning)
                level = 'ERROR'

            super(Logger, self).__init__(name, getattr(logbook, level))

except ImportError:
    class Logger(object):
        def __init__(self, name, level=0):
            self.name = name
            self.level = level
        debug = info = warn = warning = notice = error = exception = \
            critical = log = lambda *a, **kw: None
