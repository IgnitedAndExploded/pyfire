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

global_disable = False

try:
    import logbook
    import logbook.more

    class Logger(logbook.Logger):
        def __init__(self, name):
            classname = name.replace('.', '_').lower()
            if classname.startswith("pyfire_"):
                classname = classname[7:]

            try:
                level = config.get('logging', classname).upper()
            except config.NoOptionError:
                level = ''

            if not level:
                level = config.get('logging', 'global_level').upper()

            if level not in frozenset(['CRITICAL', 'ERROR', 'WARNING',
                                       'INFO', 'DEBUG', 'NOTSET']):
                warnings.warn("No such loglevel %s" % level, RuntimeWarning)
                level = 'ERROR'
            super(Logger, self).__init__(classname, getattr(logbook, level))
            self.handlers.append(logbook.more.ColorizedStderrHandler())
            self._disabled = False

        def _set_disabled(self, value):
            self._disabled = value

        def _get_disabled(self):
            return global_disable or self.disabled

        disabled = property(_get_disabled, _set_disabled)

except ImportError:
    class Logger(object):
        def __init__(self, name, level=0):
            self.name = name
            self.level = level
        debug = info = warn = warning = notice = error = exception = \
            critical = log = lambda *a, **kw: None
