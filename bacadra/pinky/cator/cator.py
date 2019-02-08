'''
------------------------------------------------------------------------------
********************** (c)reate (a)u(to)matic (r)eport ***********************
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ____ import _____________________________________________________________ #

from ...tools.setts import settsmeta
from . import block

#$ ____ class setts ________________________________________________________ #

class setts(settsmeta):
    pass


#$ ____ class cator ________________________________________________________ #

class cator:

    # class setts
    setts = setts('setts', (setts,), {})

#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, core=None):

        # project object
        self.core = core

        # local setts
        self.setts = self.setts('setts',(),{})

#$$ ________ def add _______________________________________________________ #

    def add(self, out='r', name=None, sub='a', mode='r', where=None, label=None):
        '''
        '''

        if name==None: return

        for outi in out:
            for modei in mode:
                code = getattr(block, name+'_'+sub)(
                    self  = self,
                    out   = outi,
                    mode  = modei,
                    where = where,
                    label = label
                )

                if   outi=='r': self.core.pinky.rstme.add(code)
                elif outi=='t': self.core.pinky.texme.add(code)
                elif outi=='d': self.core.pinky.docme.add(code)


#$$ ________ def rst________________________________________________________ #

    def rst(self, sub='a', data={}):

        othe = self.core.pinky.rstme
        out  = 'r'
        mode = 'm'


        othe.h(1, 'General information')

        othe.h(1, 'Model data')

        othe.h(2, 'Materials')

        self.add(out, 'mates_umate', sub, mode)

        othe.h(1, 'General information')

        othe.h(1, 'Model data')

        othe.h(2, 'Materials')

        othe.h(2, 'Unit sections')

        othe.h(3, 'Unit sections 1d')

        othe.h(2, 'Nodes') #$$#

        othe.h(2, 'Truss elements') #$$#

        othe.h(1, 'Loads')

        othe.h(1, 'Combinations')

        othe.h(1, 'Static analysis')

        othe.h(1, 'Dynamic analysis')

        othe.h(1, 'Design analysis')

        othe.h(1, 'Summary')

        othe.toc('b')
