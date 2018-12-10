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


#$ class utile
class utile:
    #$$ def --init--
    def __init__(self, core=None):
        if core is None:
            from ..pinky import index
            self.pinky = index(dbase=None, mdata=None)
        else:
            self.pinky = core.pinky

        # data of check statment
        self.data_cs = {}

        # datas of level statment
        self.data_ls = {}

    #$$ def level
    def level(self, util, text):
        '''
        Create level's utlization statment.
        '''

        # if block
        if 0 <= util <= 1: UQ = 'OK'
        elif    util <  0: UQ = '(?)'
        elif    util >  0: UQ = '(!)'

        # add result to data contener
        self.data_ls.update({
            str(uuid.uuid4()):{
                'UQ'  :UQ,
                'Level':util,
                'Description':text,
        }})

    #$$ def check
    def check(self, util, text):
        '''
        Create check's utlization statment.
        '''

        # if block
        if util:
            UQ = 'OK'
        else:
            UQ = '(!)'

        # add result to data contener
        self.data_cs.update({
            str(uuid.uuid4()):{
                'UQ'  :UQ,
                'Description':text,
        }})

    #$$ def echo
    def echo(self, type=True, inherit=False):
        '''
        Send out generated rst-table.
        '''

        output = []

        if type in [True, 'ls']:

            data = [(v['UQ'],v['Level'],v['Description']) for v in self.data_ls.values()]

            if len(data)>0:
                i_max,i_min,u1,u2 = 0,0,0,0
                for i in range(len(data)):
                    if data[i][1] > data[i_max][1]: i_max = i
                    if data[i][1] < data[i_min][1]: i_min = i
                    if data[i][1] > 1: u1 += 1
                    if data[i][1] < 0: u2 += 1

                data.append({'h_symbol':'='})


                if u1==0:
                    text = 'All utilization statment are satisfy'
                else:
                    text = f'Few <{u1}> utilization statment are not satisfy'
                data.append(('', '', text))


                if u2==0:
                    text = 'All utilization statment were defiend correctly'
                else:
                    text = f'Few <{u2}> utilization statment were defiend uncorrectly'
                data.append(('', '', text))


                data.append(('MAX', data[i_max][1], data[i_max][2]))

                data.append(('MIN', data[i_min][1], data[i_min][2]))

                output += [self.pinky.rstme.table(
                    caption= 'Level\'s utilization statments',
                    wrap   = [False, True, True],
                    width  = [3,8,True],
                    halign = ['l','r','l'],
                    valign = ['u','u','u'],
                    dtype  = ['t','p','t'],
                    header = ['UQ', 'Level', 'Description'],
                    data   = data,
                    precision = 2,
                    inherit = inherit,
                )]

                self.pinky.rstme.table(
                    wrap   = [False, False, True],
                    width  = [15, 2, True],
                    halign = ['r','c','l'],
                    valign = ['u','u','u'],
                    dtype  = ['t','t','t'],
                    data   = [
                        ['UQ' ,'-', 'Utilization questions:\n* OK  - utilization is satisfy,\n* (!) - utilization is overhead,\n* (?) - utilization is wrong formulated.'],
                        ['Level','-', 'Level of utilization in percent scale.'],
                        ['Description', '-', 'Description of utilization level.'],

                    ],
                    border = False,
                    inherit = inherit,
                )



        if type in [True, 'cs']:

            data = [(v['UQ'],v['Description']) for v in self.data_cs.values()]

            if len(data)>0:

                u1 = 0
                for i in range(len(data)):
                    if data[i][0] is False: u1 += 1

                data.append({'h_symbol':'='})

                if u1==0:
                    text = 'All utilization statment are satisfy'
                else:
                    text = f'Few <{u1}> utilization statment are not satisfy'
                data.append(('', text))

                output += [self.pinky.rstme.table(
                    caption= 'Check\'s utilization statments',
                    wrap   = [False, True],
                    width  = [3,True],
                    halign = ['l','l'],
                    valign = ['u','u'],
                    dtype  = ['t','t'],
                    header = ['UQ', 'Description'],
                    data   = data,
                    inherit = inherit,
                )]

                self.pinky.rstme.table(
                    wrap   = [False, False, True],
                    width  = [15, 2, True],
                    halign = ['r','c','l'],
                    valign = ['u','u','u'],
                    dtype  = ['t','t','t'],
                    data   = [
                        ['UQ' ,'-', 'Utilization questions:\n* OK  - utilization is satisfy,\n* (!) - utilization is overhead.'],
                        ['Description', '-', 'Description of utilization level.'],

                    ],
                    border = False,
                    inherit = inherit,
                )


        if inherit:
            return output

    #$$ def show
    def show(self):
        '''
        Just print utilization.
        '''
        print('\n\n'.join(self.echo(inherit=True)))
