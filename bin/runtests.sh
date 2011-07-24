#!/usr/bin/env bash
echo "======================"
echo "Running pyfire testkit"
echo "======================"

python -m unittest discover pyfire 'test_*.py' -v