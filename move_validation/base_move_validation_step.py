#!/usr/bin/env python3
"""
Base class for all move validation checks.
"""
from abc import ABCMeta, abstractmethod, abstractproperty
from utils import debug, DebugLevel


class BaseMoveValidationStep(metaclass=ABCMeta):


    @abstractmethod
    def __init__(self, move_obj):
        """
        :param move_obj: The move object to be validated
        :return: None
        """
        raise NotImplementedError("This is an abstract base class")


    @abstractmethod
    def perform_check(self):
        """
        Performs the check and sets up is_valid and invalid_reason properties
        :return: None
        """
        raise NotImplementedError("This is an abstract base class")


    @abstractproperty
    def is_valid(self):
        return self._is_valid


    @abstractproperty
    def invalid_reason(self):
        return None if self.is_valid else self._invalid_reason
