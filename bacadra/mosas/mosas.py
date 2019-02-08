'''
------------------------------------------------------------------------------
***** (m)echanics (o)f (s)olids and (s)tructures *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

# from ..dbase import parse
from ..tools.setts import settsmeta
from .lsoeq.lsoeq import lsoeq

#$ ____ class setts ________________________________________________________ #

class setts(settsmeta):
    pass

#$ ____ class mosas ________________________________________________________ #

class mosas:

    # class setts
    setts = setts('setts', (setts,), {})

    #$$ def __init__
    def __init__(self, core):

        # project object
        self.core = core

        # local setts
        self.setts = self.setts('setts',(),{})

    def run(self):
        lsoeq(self)