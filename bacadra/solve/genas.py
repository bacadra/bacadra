'''
------------------------------------------------------------------------------
***** (gen)etic (a)lgorithm (s)olver *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

import random
from ..cunit.units import cunit

class sman:

    # init data, init limits etc.
    init = {}

    def __init__(self, kwargs):

        # type()=dict, generic data
        self.d = kwargs

        # type()=list, constraint
        self.c = []

        # type()=float, adjustment function
        self.f = None

        # run body
        self.body()


    def __repr__(self):
        return str({'f':self.f, 'c':self.c, 'd':self.d,})

    def body(self):
        '''
        Function will be overwritten by user.
        '''
        pass


    @classmethod
    def new(self):

        # create dict for new objects
        gdata = {}

        # loop over all generic data
        for key,val in self.init.items():

            # if user specified genetic by dictonary
            if type(val)==dict:

                # if value is int or float
                if type(val['min']) in [int,float]:
                    x = random.randrange(val['min'], val['max'], val['step'])

                # if vakue is csman
            elif type(val['min'])==cunit:
                    cc  = val['min'].smans().primary()
                    min = val['min'].d()
                    max = val['max'].d()
                    step = val['step'].d()
                    x = random.randrange(min,max,step)*cc

            # add parameter to dict
            gdata.update({key:x})

        # create object, it will be calculated now
        obj = sman(gdata)

        # if not fullfill all requitments
        if all(obj.c) is False:

            obj = self.new()

        # then add it to data
        return obj


    @staticmethod
    def mut(self, value, gd=True):
        if gd is True:
            for key in self.d.keys():
                self.d[key] *= 1+(random.random()*2-1)*value
        elif type(gd) is str:
            self.d[gd] *= 1+(random.random()*2-1)*value

        self.body()


    @staticmethod
    def crx(self, othe, times=1):
        for i in range(times):
            key,val = random.choice(list(self.d.items()))
            self.d[key] = othe.d[key]
            othe.d[key] = val

        self.body()



class line:
    def __init__(self, mode='min'):
        self.data = []
        self.mode = mode


    def __repr__(self):
        return repr(self.data)


    def add(self, n, inherit=False):
        '''
        Create new object in line. Their are base only on generic data constrain.
        '''

        # create n instance
        for i in range(n):
                self.data += [sman.new()]


    def rem(self, i, rest=0):
        if self.mode is None:
            self.data.remove(i)
        elif self.mode in ['max', 'min']:
            self.data = self.data[:-i-rest]+self.data[-rest:]


    def sort(self):

        self.data = [sman if all(sman.c)==True else sman.new() for sman in self.data]

        if self.mode=='max':
            self.data.sort(key=lambda x: x.f, reverse=True)
        elif self.mode=='min':
            self.data.sort(key=lambda x: x.f)


    def mut(self, value, gd=True):
        for obj in self.data:
            sman.mut(obj, value, gd)

    def crx(self, n, times=1):
        for i in range(n):
            a = random.choice(self.data)
            b = random.choice(self.data)
            sman.crx(a,b, times)