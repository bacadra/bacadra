'''
------------------------------------------------------------------------------
BCDR += ***** (util)ilization (e)ngine *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

import uuid

class struct:
    pass

class utile:
    def __init__(self, core=None):
        if core is None:
            from ..pinky.rstme.rstme import rstme
            self.core = struct()
            self.core.pinky = struct()
            self.core.pinky.rstme = rstme()
        else:
            self.core = core

        self.util = {}


    def add(self, util, desc):

        if 0 <= util <= 1: qa = 'OK'
        elif    util <  0: qa = '(?)'
        elif    util >  0: qa = '(!)'

        self.util.update({
            str(uuid.uuid4()):{
                'qa'  :qa,
                'util':util,
                'desc':desc,
        }})

    def rem(self, id):
        self.util.pop(id)


    def echo(self, inherit=False):

        data = [(v['qa'],v['util'],v['desc']) for v in self.util.values()]

        i_max,i_min = 0,0
        for i in range(len(data)):
            if data[i][1] > data[i_max][1]: i_max = i
            if data[i][1] < data[i_min][1]: i_min = i

        data.append(('','',''))
        data.append(('MAX', data[i_max][1], data[i_max][2]))
        data.append(('MIN', data[i_min][1], data[i_min][2]))

        return self.core.pinky.rstme.table(
            wrap   = [False, True, True],
            width  = [3,8,True],
            halign = ['l','r','l'],
            valign = ['u','u','u'],
            dtype  = ['t','p','t'],
            header = ['QU', 'Util', 'Description'],
            data   = data,
            precision = 2,
            inherit = inherit,
        )


    def __repr__(self):
        return self.echo(inherit=True)