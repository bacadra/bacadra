'''
------------------------------------------------------------------------------
***** unise (si) package *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ######################################################################### #

from .unise import unise
unise.setts.system('si')
cu   = unise(1, {        }, 'si')
kN   = unise(1, {'kN'  :1}, 'si')
m    = unise(1, {'m'   :1}, 'si')
rad  = unise(1, {'rad' :1}, 'si')
mrad = unise(1, {'mrad':1}, 'si')
C    = unise(1, {'C'   :1}, 'si')
s    = unise(1, {'s'   :1}, 'si')
deg  = unise(1, {'deg' :1}, 'si')
kg   = unise(1, {'kg'  :1}, 'si')
ton  = unise(1, {'ton' :1}, 'si')
K    = unise(1, {'K'   :1}, 'si')
km   = unise(1, {'km'  :1}, 'si')
dm   = unise(1, {'dm'  :1}, 'si')
cm   = unise(1, {'cm'  :1}, 'si')
mm   = unise(1, {'mm'  :1}, 'si')
MN   = unise(1, {'MN'  :1}, 'si')
N    = unise(1, {'N'   :1}, 'si')
yr   = unise(1, {'yr'  :1}, 'si')
day  = unise(1, {'day' :1}, 'si')
hr   = unise(1, {'hr'  :1}, 'si')
mn   = unise(1, {'mn'  :1}, 'si')
GPa  = unise(1, {'GPa' :1}, 'si')
MPa  = unise(1, {'MPa' :1}, 'si')
kPa  = unise(1, {'kPa' :1}, 'si')
Pa   = unise(1, {'Pa'  :1}, 'si')
Hz   = unise(1, {'Hz'  :1}, 'si')
t    = unise(1, {'t'   :1}, 'si')
kNm  = kN*m
MNm  = MN*m

#$ ######################################################################### #
