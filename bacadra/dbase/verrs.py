'''
------------------------------------------------------------------------------
BCDR += ***** (v)arious (err)ors *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''


class DatabaseError(Exception):
    pass

def openDatabaseError():
    raise DatabaseError('Connection to database is not established.\nTip1: Open database with .connect(path=.., clear=True/False) method in dbase module.\nTip2: Database can be opened in memory, then just type path=":memory:".')

class ParseError(Exception):
    '''
    General parser exception.
    '''
    pass

def f1ParseErorr(mode):
    '''
    Function raise error with info, that parse_mode is unrecocnized. Look at parse module for list of current parsing modes.
    '''
    raise ParseError(f'Unrecognized parse mode <{mode}>. Look at parse chapter for more informations.')


class ParseMultiError(Exception):
    '''
    Exception for multiparser.
    '''
    pass

def f1ParseMultiError(l1, l2, row):
    '''
    Data length is not equal to col length, please fix it!
    '''
    raise ParseMultiError(f'Data list length <{l1}> is not equal to col list length <{l2}>, please fix the row <{row}>')