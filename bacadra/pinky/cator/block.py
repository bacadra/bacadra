'''
------------------------------------------------------------------------------
****************************** report (block)s *******************************
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ____ def mates_umate_a __________________________________________________ #

def mates_umate_a(self, **kwargs):

    # get data from database
    data = self.core.dbase.get(
        mode  = 'm',
        table = ['011:mates:umate'],
        cols  = ['id','ρ_o','E_1','v_1','G_1','t_e','subcl','ttl'],
        where = kwargs['where'],
    )

    # if empty then return empty string
    if not data: return

    caption = 'General properties of materials'

    def temp(a):
        return self.core.pinky.rstme.table(
            caption = a,
            wrap    = [False,False,False,False,False,False,False,True],
            width   = [True,8,8,4,8,8,5,True],
            halign  = ['l','c','c','c','c','c','c','l'],
            valign  = ['u','u','u','u','u','u','u','u'],
            dtype   = ['t','e','e','f','e','e','t','t'],
            header  = ['id','ρ_o','E_1','v_1','G_1','t_e','subcl','ttl'],
            data    = data,
            precision = 2,
            inherit = True,
        )

    if 'r'==kwargs['out']:
        return temp(caption)

    if 't'==kwargs['out']:
        return self.core.pinky.texme.code(caption=caption, code=temp(None), rst=True, label=None, strip=False, inherit=True)


