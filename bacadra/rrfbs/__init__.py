'''
***** (r)ailway-, (r)oad- and (f)oot- (b)ridge(s) *****
'''

from ..tools.rootx import rootx

from . import railb
from . import roadb
from . import footb

#$ class index
class index(rootx):
    def __init__(self, core):

        self.railb = railb.index(core=core)
        self.roadb = roadb.index(core=core)
        self.footb = footb.index(core=core)