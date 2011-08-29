# -*- coding: utf-8 -*-
"""
    pyfire.tests
    ~~~~~~~~~~~~

    All unittests live here

    :copyright: 2011 by the pyfire Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""

import unittest

# Disable logging if we run unit tests
import pyfire.logger
pyfire.logger.global_disable = True


class PyfireTestCase(unittest.TestCase):
    """All our unittests are based on this class"""
    pass
