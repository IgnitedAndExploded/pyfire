#!/usr/bin/env python
import argparse
import unittest

import sys
import os.path
from os.path import join as pjoin

# Add pyfire to namespace
path = os.path.abspath(pjoin(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run pyfire testsuite')
    parser.add_argument('-v', '--verbosity', dest='verbosity', type=int,
                        default=2, help="Test runner verbosity",
                        choices=[0, 1, 2])
    parser.add_argument('--coverage', dest='coverage',
                        action='store_true',
                        help="Enable tracking of code coverage")
    parser.add_argument('--full-coverage', dest="fullcoverage",
                        action='store_true',
                        help="Enable tracking of code coverage and" +
                             "do not exclude tests dir")

    args = parser.parse_args()
    testpath = pjoin(path, 'pyfire', 'tests')
    # Load all tests from pyfire.tests path whose filenames start with test
    if args.coverage or args.fullcoverage:
        from coverage import coverage
        if args.fullcoverage:
            omit = None
        else:
            omit = "pyfire/tests/*"
        cov = coverage(omit=omit)
        cov.start()
        suite = unittest.TestLoader().discover(testpath)
        unittest.TextTestRunner(verbosity=args.verbosity).run(suite)
        cov.stop()
        cov.html_report(directory=pjoin(path, '_build', 'coveragereport'))
    else:
        suite = unittest.TestLoader().discover(testpath)
        unittest.TextTestRunner(verbosity=args.verbosity).run(suite)
