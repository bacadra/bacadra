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
    erwin('e0201',
        'Connection to database is not established\n'
        'Tip: Open database with .connect() method\n'
        'Tip: Database can be opened in memory, then just type path=":memory:"'
        'Tip: Default path is set as ":memory:" :)'
    )

def BCDR_dbase_ERROR_Parse_Type(allow_type, type_value):
    erwin('e0211',
        'Variable type is not allowed! Parse process requires correct type.\n'
        f'Tip: Given variable type <{type_value}>\n'
        f'Tip: Correct type <{allow_type}>'
    )

def BCDR_dbase_ERROR_undefined_transaction_mode(command, mode, allow):
    erwin('e0203',
        f'Undefined transaction mode <{mode}>!\n'
        f'Tip: caller command <{command}>'
        f"Tip: you can use {allow}"

    )


#$ ____ warnings ___________________________________________________________ #

def BCDR_dbase_WARN_Already_Closed():
    erwin('w0202',
        'Databse already closed. Nothing to save.\n'
        'Tip: You can not add new data as long as database connection is close'
        )

#$ ____ infos ______________________________________________________________ #

#$ ######################################################################### #
