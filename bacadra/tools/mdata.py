'''
------------------------------------------------------------------------------
***** (m)apped (data)base *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''


from .color import colored

#$ ____ class mdata _________________________________________________________ #

class mdata:

    def __init__(self, obj):
        self.__keys__ = obj.keys()
        for key in self.__keys__:
            setattr(self, key, obj[key])

    def __call__(self):
        data = [colored('---------------------------------------------------------------------------\n''***** bacadra object settings *****', 'magenta')]

        for key in self.__keys__:
            val = getattr(self, key)
            if type(val) is str: val = "'" + str(val) + "'"
            data.append('> {:14s} : {}'.format(key, val))

        print ('\n'.join(data))