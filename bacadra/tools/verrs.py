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

def BCDR_tools_ERROR_Translation_Not_Provided():
    erwin('e0066',
        'Please check translation, there is no one kwargs!'
    )

#$ ____ warnings ___________________________________________________________ #

def BCDR_tools_WARN_Translation_Not_Provided(language, newlang, text):
    erwin('w0066',
        f'Please check translation, there is no text in given language <{language}>. \nTip: instead of return next one avaiable <{newlang}>.'+
        (f'\nTip: returned new text -> {text}')
    )

#$ ____ infos ______________________________________________________________ #

#$ ######################################################################### #
