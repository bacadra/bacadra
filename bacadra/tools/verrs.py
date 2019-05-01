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

from .erwin  import erwin

#$ ____ errors _____________________________________________________________ #

def BCDR_tools_ERROR_setts_get_unknow(name):
    erwin('e0001',
    f'Unknow setting <{name}>\n'
    'Tip: please check that init method set'
    )

def BCDR_tools_ERROR_Translation_Not_Provided():
    erwin('e0066',
        'Please check translation, there is no one kwargs!'
    )

def BCDR_tools_ERROR_Letters_check(driver, letters):
    erwin('e0071',
        'Letter do not occur in driver string!\n'
        f'Tip: valid string <{driver}>\n'
        f'Tip: given string <{letters}>'
    )

def BCDR_tools_WARN_Letters_check(driver, letters):
    erwin('w0071',
        'Letter do not occur in driver string!\n'
        f'Tip: valid string <{driver}>\n'
        f'Tip: given string <{letters}>'
    )

#$ ____ warnings ___________________________________________________________ #

def BCDR_tools_WARN_Translation_Not_Provided(language, newlang, text):
    erwin('w0066',
        f'Please check translation, there is no text in given language <{language}>. \nTip: instead of return next one avaiable <{newlang}>.'+
        (f'\nTip: returned new text -> {text}')
    )

#$ ____ infos ______________________________________________________________ #

#$ ######################################################################### #
