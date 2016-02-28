#!/usr/bin/env python3
"""
Base class for all move validation checks.
"""
from abc import ABCMeta, abstractmethod
import utils
from move import Move


class BaseMoveValidationStep(metaclass=ABCMeta):


    def __init__(self, move_obj):
        """
        :param move_obj: The move object to be validated
        :return: None
        """
        if isinstance(move_obj, Move):
            self.move_obj = move_obj
        else:
            raise TypeError("A move object is required to initialise this class")

        self._is_valid = False
        self._invalid_reason = "{0} - Validation not yet performed".format(self.__doc__)


    @abstractmethod
    def perform_check(self):
        """
        Performs the check and sets up is_valid and invalid_reason properties
        :return: None
        """
        raise NotImplementedError("This is an abstract base class")


    def debug(self, msg, debug_level=utils.DebugLevel.mid):
        utils.debug(msg, level=debug_level, filter_func=not self.move_obj.theoretical_move)


    @property
    def is_valid(self):
        return self._is_valid


    @property
    def invalid_reason(self):
        return None if self.is_valid else self._invalid_reason