'''
------------------------------------------------------------------------------
BCDR += ***** (p)rett(y) (ink) TEX, RST and DOC *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ..tools.rootx import rootx

# rsme and texme import must stay out of index class
# they can be imported withoud connection to db!

from .rstme.rstme import rstme
from .texme.texme import texme

#$ class index
class index(rootx):
    #$$ __init__
    def __init__(self, dbase, mdata):

        class core:
            def __init__(self, dbase, mdata):
                self.dbase = dbase
                self.mdata = mdata

        self.core=core(dbase,mdata)
        self.sub_init('rstme', True)
        self.sub_init('texme', True)

    def sub_add_pattern(self, module):
        '''
        Return new object of submodule.
        '''
        if module=='rstme':
            return rstme(core=self.core)
        if module=='texme':
            return texme(core=self.core)
