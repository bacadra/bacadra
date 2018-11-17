'''
------------------------------------------------------------------------------
BCDR += ***** (root) of (cross)-multimodule concept *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ class index
class rootx:
    #$$ --init--
    def __init__(self):
        pass

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
        pass

    def sub_init(self, module, id):
        self.__dict__[f'_{module}_list'] = {'__active_id__':None}
        self.__dict__[module] = self.sub_add_pattern(module)
        self.sub_add(module, id)
        self.sub_checkout(module, id)

    def sub_add(self, module, id, checkout=False):
        self.__dict__[f'_{module}_list'].update({id:self.sub_add_pattern(module)})
        if checkout:
            self.sub_checkout(module, id)

    def sub_checkout(self, module, id, add=True):
        self.__dict__[f'_{module}_list'].update({'__active_id__':id})
        self.__dict__[module].__dict__ = self.__dict__[f'_{module}_list'][id].__dict__

    def sub_check(self, module):
        return self.__dict__[f'_{module}_list']

    def sub_check_all(self):
        import re
        npat = re.compile('_(.+)_list')
        full_list = {}
        for key,val in self.__dict__.items():
            if bool(npat.match(key)):
                full_list.update({npat.sub(r'\1', key):val['__active_id__']})
        return full_list

    def sub_get(self, module, id):
        return self.__dict__[f'_{module}_list'][id]

    def sub_get_list(self, module, pop_active=True):
        if pop_active:
            new = self.__dict__[f'_{module}_list'].copy()
            new.pop('__active_id__')
            return new
        else:
            return self.__dict__[f'_{module}_list']