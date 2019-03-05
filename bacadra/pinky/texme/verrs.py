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

from ...tools.erwin  import erwin

#$ ____ errors _____________________________________________________________ #

def BCDR_pinky_texme_ERROR_General(code, text):
    erwin(code, text)

def BCDR_pinky_texme_ERROR_Header_Level(lvl,alvl):
    erwin('e0611',
        f'Typped level <{lvl}+{alvl}={lvl+alvl}> outside domain <-1,5>.'
    )

def BCDR_pinky_texme_ERROR_Type_Check(sent, correct):
    erwin('e0621',
        f'The type sent <{sent}> does not match the requirements of the attribute <{correct}>.'
    )

def BCDR_pinky_texme_ERROR_String_Selector(sent, correct):
    erwin('e0622',
        f'Unknown parameter <{sent}>, you can use a single or mix of available parameters <{correct}>.'
    )

def BCDR_pinky_texme_ERROR_Invalid_Key(sent, correct):
    erwin('e0623',
        f'The type key <{sent}> does not match current state of dict <{correct}>.'
    )

def BCDR_pinky_texme_ERROR_Path_Error(path):
    erwin('e0681',
        f'Path does not exists <{path}>'
    )

def BCDR_pinky_texme_ERROR_Evaluate(e):
    erwin('e0682',
        f'N{str(e)[1:]}.\n' # Name '..' is not defined
        'Tip: check .setts.scope atribute, may it show to wrong namespace'
    )

#$ ____ warnings ___________________________________________________________ #

def BCDR_pinky_texme_WARN_General(code, text):
    erwin(code, text)

def BCDR_pinky_texme_WARN_Path_Error(path):
    erwin('w0681',
        f'Path does not exists <{path}>'
    )

def BCDR_pinky_texme_WARN_Scope_External():
    erwin('w0631',
        'The scope is set to external project class. Dict is saving under slot 0.\n'
        'Tip: slot 0 is not external, but active is still external (check ssel)!\n'
        'Tip: If you want to set other local scope then input data as tuple\n'
        'Tip: (id, dict) where id [None,0-9] and often dict==locals()'
    )

#$ ____ infos ______________________________________________________________ #


def BCDR_pinky_texme_INFO_General(code, text):
    erwin(code, text)

def BCDR_pinky_texme_INFO_Scope(id):
    erwin('i0611',
        f'The scope selector change to new id <{id}>.'
    )

#$ ######################################################################### #
    