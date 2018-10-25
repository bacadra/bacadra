
from ..cunit.ce import m

#$ ____ class pvars ________________________________________________________ #

class pvars:
    def __init__(self, dbase, pinky):
        self.dbase = dbase
        self.pinky = pinky

        self._pvars = {
            '_cates_ldef'   : None,
            '_lcase_ldef'   : None,
            '_mates_ldef'   : None,
            '_usec1_ldef'   : None,
            'nodes_fix'     : None,
            'system_dof'    : None,
            'node_tol'      : 0.01*m,
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
        Add new key to pvars. You can add new if not exists or add/mod new (also if key exists).
        '''

        if redefine:
            for key,val in ndict.items():
                self._pvars.update({key:val})
        else:
            for key,val in ndict.items():
                if key in self._pvars:
                    raise ValueError('Key does not exists!')
                else:
                    self._pvars.update({key:val})



    def set(self, ndict):
        '''
        Set new value for already exists keys. As input needed is dict.
        '''

        for key,val in ndict.items():
            if key in self._pvars:
                self._pvars.update({key:val})
            else:
                raise ValueError('Key does not exists!')

    def get(self, name=None):
        '''
        Get value of already exists keys. As input needed is string or list with strings.
        '''
        if   type(name) == str:
            return self._pvars[name]
        elif type(name) == list:
            return [self._pvars[name1] for name1 in name]
        else:
            return self._pvars


class nannex:

    def load(self, path):
        '''
        Load national annex variables from external text file.
        '''
        pass
