from ..tools.index import root_index

from .rstme import rstme
from .texme import texme

#$ class index
class index(root_index):
    #$$ --init--
    def __init__(self, dbase, mdata):
        class core:
            def __init__(self, dbase, mdata):
                self.dbase = dbase
                self.mdata = mdata
        self.core=core(dbase,mdata)
        self.sub_init('rstme', True)
        self.sub_init('texme', True)


    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    def sub_add_pattern(self, module):
        '''
        Return new object of submodule.
        '''
        if module=='rstme':
            return rstme.rstme(core=self.core)
        if module=='texme':
            return texme.texme(core=self.core)