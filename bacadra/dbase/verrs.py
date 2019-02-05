'''
------------------------------------------------------------------------------
***** (v)arious (err)or(s) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ..tools.verre  import BCDR_ERRS,BCDR_WARN,BCDR_INFO

#$ ____ errors _____________________________________________________________ #

class BCDR_dbase_ERROR(BCDR_ERRS):
    pass

def BCDR_dbase_ERROR_General(code, text):
    BCDR_dbase_ERROR(code, text)

def BCDR_dbase_ERROR_Open_Database():
    BCDR_dbase_ERROR('e0101',
        'Connection to database is not established.\n'
        'Tip: Open database with .connect(path=.., clear=True/False) method in dbase module.\n'
        'Tip: Database can be opened in memory, then just type path=":memory:".'
    )

def BCDR_dbase_ERROR_Parse_Type(allow_type):
    BCDR_dbase_ERROR('e0011',
        'Variable type is not allowed! Parse process requires correct type.\n'
        f'Tip: Correct type <{allow_type}>'
    )

#$ ____ warnings ___________________________________________________________ #

class BCDR_dbase_WARN(BCDR_WARN):
    pass

def BCDR_dbase_WARN_Already_Closed():
    BCDR_dbase_WARN('w0121',
        'Databse already closed. Nothing to save.\n'
        'Tip: You can not add new data as long as database connection is close'
        )

#$ ____ infos ______________________________________________________________ #

class BCDR_dbase_INFO(BCDR_INFO):
    pass


