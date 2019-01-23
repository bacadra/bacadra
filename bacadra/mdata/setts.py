'''
------------------------------------------------------------------------------
BCDR += ***** model (sett)ing(s) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ..cunit.units import cunit

#$ ____ class setts ________________________________________________________ #

class setts:
    def __init__(self, dbase):
        self.dbase = dbase

        self._setts = {
            '_cates_ldef'   : None,
            '_lcase_ldef'   : None,
            '_mates_ldef'   : None,
            '_usec1_ldef'   : None,
            'scope'         : {},
            'nodes_fix'     : None,
            'system_space'  : None,
            'node_tol'      : cunit(0.01, 'm'),
            'xy->xz'        : True,
        }

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    def add(self, ndict, redefine=False):
        '''
        Add new key to setts. You can add new if not exists or add/mod new (also if key exists).
        '''

        if redefine:
            for key,val in ndict.items():
                self._setts.update({key:val})
        else:
            for key,val in ndict.items():
                if key in self._setts:
                    raise ValueError('Key does not exists!')
                else:
                    self._setts.update({key:val})



    def set(self, ndict):
        '''
        Set new value for already exists keys. As input needed is dict.
        '''

        for key,val in ndict.items():
            if key in self._setts:
                self._setts.update({key:val})
            else:
                raise ValueError('Key does not exists!')


    def get(self, name=None):
        '''
        Get value of already exists keys. As input needed is string or list with strings.
        '''
        if   type(name) == str:
            return self._setts[name]
        elif type(name) == list:
            return [self._setts[name1] for name1 in name]
        else:
            return self._setts



