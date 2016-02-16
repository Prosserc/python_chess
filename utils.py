#!/usr/bin/env python
"""
General utility functions / constants for python_chess
"""
from enum import Enum


class DebugLevel(Enum):
    """Debug messages will be printed if classified as less than or equal to
    the level the program is running in.
    """
    none = 0
    low = 1
    mid = 2
    high = 3


LOG_FILE_PATH = 'log.json'
ASCII_OFFSET = 64  # used to convert numbers to ascii letter codes
WRONG_ENTRY_POINT_MSG = "This module is not intended to be the main entry point for the" + \
                        "program, call python_chess.game to start a new game."
DEFAULT_DEBUG_LEVEL = DebugLevel.low

verbose = False ## todo replace with DEBUG_LEVEL when ready
current_debug_level = DebugLevel.low


def debug(msg, level=DebugLevel.low, print_func=print()):
    """Use like the print function, messages will only be printed if debug_level
    is less than or equal to the constant DEBUG_LEVEL.
    """
    if level.value <= current_debug_level.value:
        print_func(msg)


def set_debugging_level(level, feedback_required=False):
    """
    Set the current debug level. Use a DebugLevel or a string.
    """
    if isinstance(level, DebugLevel):
        current_debug_level = level

    if not level:
        print("debug level not provided, setting to low")
        current_debug_level = DebugLevel.low

    debug_code  = level[0].lower()

    if debug_code == 'h':
        current_debug_level = DebugLevel.high
    elif debug_code == 'm':
        current_debug_level = DebugLevel.mid
    elif debug_code == 'l':
        current_debug_level = DebugLevel.low
    else:
        print("unable to interpret debug level requested ({0}), setting to low".format(level))
        current_debug_level = DebugLevel.low

    if feedback_required:
        return "Debugging  level set to {0}".format(current_debug_level.name)


def pos_to_cell_ref(pos):
    """
    Converts a [row, col] list into a cell reference where the
    cell is described as a letter for the column followed by a number 
    for the row e.g. [1, 1] becomes 'A1' or [4, 8] becomes 'H4'.
    """
    return "{0}{1}".format(col_no_to_letter(pos[1]), str(pos[0]))


def col_no_to_letter(col_no):
    return chr(col_no + ASCII_OFFSET)


def cell_ref_to_pos(cell_ref):
    """
    Converts a cell_ref as given by the user (e.g. 'B6' to describe
    column B, row 6) into a [row, col] list e.g. 'E2' => [2, 5].
    """
    return [int(cell_ref[1]), col_letter_to_no(cell_ref[0])]


def col_letter_to_no(col_letter):
    return ord(col_letter.upper()) - ASCII_OFFSET


def write_log(log):
    """
    Write json log data to a file.
    """
    file_obj = open(LOG_FILE_PATH, 'w')
    print('\nLogging game data...')
    file_obj.writelines(log)
    file_obj.close()


def list_agg(operator='+', *args):
    """
    Perform an aggregation of lists by the operator supplied e.g.
    list_agg('+'. [3, 6], [2, 2]) would return [5, 7]. The number of
    lists supplied is arbitrary, but each list must have the same 
    number of elements.
    """
    l = len(args[1])
    res = args[0]
    for i, arg in enumerate(args[1:]):
        if len(arg) != l:
            raise Exception("The length of all arguments must be the same")
        for j, item in enumerate(arg):
            cmd = "res[j] " + operator + "= " + str(item)
            exec(cmd)
    return res


def shout(msg, suffix=' !!!', print_output=True, return_output=False):
    """
    Output message in all caps with spaces between and a suffix.
    """
    adj_msg = ' '.join([str(i).upper() for i in str(msg) + str(suffix)])
    if print_output:
        print(adj_msg)
    if return_output:
        return adj_msg


def format_msg(msg, line_width=80):
    """
    Formats a message into chunks to avoid splitting words.
    """
    line_pos, result = 0, ""
    for word in msg.split(' '):
        line_pos += len(word) + 1
        if line_pos < line_width:
            result += word + ' '
        else:
            result += '\n' + word + ' '
            line_pos = len(word) + 1
    return result


if __name__ == '__main__':
    print(WRONG_ENTRY_POINT_MSG)
