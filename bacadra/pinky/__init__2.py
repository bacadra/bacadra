from .rstme import rstme
from .texme import texme

#$ class index
class index:
    #$$ --init--
    def __init__(self, dbase, mdata):
        class core:
            def __init__(self, dbase, mdata):
                self.dbase = dbase
                self.mdata = mdata
        self.core=core(dbase,mdata)
        self.init('rstme', True)
        self.init('texme', True)


    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    def _add_patt(self, module):
        '''
        Return new object of submodule.
        '''
        if module=='rstme':
            return rstme.rstme(core=self.core)
        if module=='texme':
            return texme.texme(core=self.core)

    def init(self, module, id):
        self.__dict__[f'_{module}_list'] = {'__active_id__':None}
        self.__dict__[module] = self._add_patt(module)
        self.add(module, id)
        self.checkout(module, id)

    def add(self, module, id, checkout=False):
        self.__dict__[f'_{module}_list'].update({id:self._add_patt(module)})
        if checkout:
            self.checkout(module, id)

    def checkout(self, module, id, add=True):
        self.__dict__[f'_{module}_list'].update({'__active_id__':id})
        self.__dict__[module].__dict__ = self.__dict__[f'_{module}_list'][id].__dict__

    def check(self, module):
        return self.__dict__[f'_{module}_list']