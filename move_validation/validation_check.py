#!/usr/bin/env python3
"""
Base class for all move validation checks.
"""


class ValidationCheck(object):


    def __init__(self):
        self.valid = False
        self.invalid_reason = "Validation not performed yet"


    def perform_check(self):
        self.invalid_reason = "You must use a subclass of ValidationCheck"
