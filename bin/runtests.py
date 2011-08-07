#!/usr/bin/env python
import argparse
import unittest

import sys
import os.path

# Add pyfire to namespace
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run pyfire testsuite')
    parser.add_argument('-v', '--verbosity', dest='verbosity', type=int,
                        default=2, help="Test runner verbosity", choices="012")
    parser.add_mutually_exclusive_group()
    parser.add_argument('--coverage', dest='coverage',
                        action='store_true',
                        help="Enable tracking of code coverage")
    parser.add_argument('--full-coverage', dest="fullcoverage",
                        action='store_true',
                        help="Enable tracking of code coverage and" +
                             "do not exclude tests dir")

    args = parser.parse_args(sys.argv[1:])
    testpath = os.path.join(path, 'pyfire', 'tests')
    # Load all tests from pyfire.tests path whose filenames start with test
    if args.coverage or args.fullcoverage:
        from coverage import coverage
        if args.coverage:
            omit = "pyfire/tests/*"
        else:
            omit = None
        cov = coverage(omit=omit)
        cov.start()
        suite = unittest.TestLoader().discover(testpath)
        unittest.TextTestRunner(verbosity=args.verbosity).run(suite)
        cov.stop()
        cov.html_report(directory='coveragereport')
    else:
        suite = unittest.TestLoader().discover(testpath)
        unittest.TextTestRunner(verbosity=args.verbosity).run(suite)
