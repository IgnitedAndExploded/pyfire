# -*- coding: utf-8 -*-
"""
    pyfire.logger
    ~~~~~~~~~~~~~

    Use pocoo's logbook or a simple no-op fallback

    :copyright: (c) 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

try:
    from logbook import Logger
except ImportError:
    class Logger(object):
        def __init__(self, name, level=0):
            self.name = name
            self.level = level
        debug = info = warn = warning = notice = error = exception = \
            critical = log = lambda *a, **kw: None
