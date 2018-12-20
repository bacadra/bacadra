'''
------------------------------------------------------------------------------
BCDR += ***** (b)acadra (datas) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

class bdata:
    #$$ def __item__
    def __init__(self, ndict):
        self.__dict__.update(ndict)

    #$$ def __repr__
    def __repr__(self):
        data = []
        for key,val in self.__dict__.items():
            data.append('> {:14s} : {}'.format(key, val))

        return '\n'.join(data)
