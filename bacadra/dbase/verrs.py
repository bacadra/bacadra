'''
------------------------------------------------------------------------------
***** (v)arious (err)or(s) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ######################################################################### #

#$ ____ import _____________________________________________________________ #

from ..tools.erwin  import erwin

#$ ____ errors _____________________________________________________________ #

def BCDR_dbase_ERROR_Open_Database():
    erwin('e0101',
        'Connection to database is not established.\n'
        'Tip: Open database with .connect(path=.., clear=True/False) method in dbase module.\n'
        'Tip: Database can be opened in memory, then just type path=":memory:".'
    )

def BCDR_dbase_ERROR_Parse_Type(allow_type):
    erwin('e0011',
        'Variable type is not allowed! Parse process requires correct type.\n'
        f'Tip: Correct type <{allow_type}>'
    )

#$ ____ warnings ___________________________________________________________ #

def BCDR_dbase_WARN_Already_Closed():
    erwin('w0121',
        'Databse already closed. Nothing to save.\n'
        'Tip: You can not add new data as long as database connection is close'
        )

#$ ____ infos ______________________________________________________________ #

#$ ######################################################################### #
