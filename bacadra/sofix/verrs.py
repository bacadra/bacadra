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

#$ ____ warnings ___________________________________________________________ #

#$ ____ infos ______________________________________________________________ #

def BCDR_sofix_INFO_mass_start():
    erwin('i0915',
    'Mass conversion started! Please be patient.\n'
    'Tip: if you call one wingraf several times then remember to close pdf windows after every one conversion... will be fixed in future\n',
    bott=False)

def BCDR_sofix_INFO_mass_loop(text):
    erwin('i0915',str(text),head=False, bott=False)

def BCDR_sofix_INFO_mass_end():
    erwin('i0915','\nMass conversion ended!', head=False)


#$ ######################################################################### #
