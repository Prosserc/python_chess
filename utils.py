#!/usr/bin/python
"""General utility functions / constants for python_chess"""
LOG_FILE_PATH = 'log.json'
ASCII_OFFSET = 64 # used to convert numbers to ascii letter codes
VERBOSE = False 

def pos_to_cell_ref(pos):
    """converts a [row, col] list into a cell reference where the
    cell is described as a letter for the column followed by a number 
    for the row e.g. [1, 1] becomes 'A1' or [4, 8] becomes 'H4'."""
    return chr(pos[1]+ ASCII_OFFSET)+str(pos[0])

def cell_ref_to_pos(cell_ref):
    """converts a cell_ref as given by the user (e.g. 'B6' to describe
    column B, row 6) into a [row, col] list e.g. 'E2' => [2, 5]."""
    return [int(cell_ref[1]), ord(cell_ref[0].upper())-ASCII_OFFSET]

def write_log(log):
    """write json log data to a file."""
    file_obj = open(LOG_FILE_PATH, 'wb')
    print('\nLogging game data...')
    file_obj.writelines(log)
    file_obj.close()

def listagg(opperator='+', *args):
    """Perform an aggregation of lists by the opperator supplied e.g. 
    listagg('+'. [3, 6], [2, 2]) would return [5, 7]. The number of 
    lists supplied is arbitrary, but each list must have the same 
    number of elements."""
    l = len(args[1])
    res = args[0]
    for i, arg in enumerate(args[1:]):
        if len(arg) != l:
            raise Exception("The length of all arguements must be the same")
        for j, item in enumerate(arg):
            cmd = "res[j] " + opperator + "= " + str(item)
            exec(cmd)
    return res

def shout(msg, suffix=' !!!', print_output=True, return_output=False):
    """Output message in all caps with spaces between and a suffix."""
    adj_msg = ' '.join([str(i).upper() for i in str(msg)+str(suffix)])
    if print_output:
        print(adj_msg)
    if return_output:
        return adj_msg

def format_msg(msg, line_width=80):
    """Formats a message into chuncks to avoid splitting words."""
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
    print("This module is not intended to be the main entry point for the " +
          "program, call python_chess.game to start a new game.")
