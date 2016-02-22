#!/usr/bin/env python3
"""
Run all of the unit tests
"""
import unittest


def main():
    loader = unittest.TestLoader()
    tests = loader.discover('.')
    runner = unittest.runner.TextTestRunner()
    runner.run(tests)


if __name__ == '__main__':
    main()