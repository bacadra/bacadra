'''
------------------------------------------------------------------------------
***** (T)-(sect)ions one dim unit-sections *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''


from ...dbase import parse
from ...cunit.cunit import cunit
from ...tools.setts import settsmeta

#$ ____ class setts ________________________________________________________ #

class setts(settsmeta):
    pass

#$ ____ class tsect ________________________________________________________ #

class tsect:

    # class setts
    setts = setts('setts', (setts,), {})


    #$$ def __init__
    def __init__(self, core):

        # project object
        self.core = core

        # local setts
        self.setts = self.setts('setts',(),{})


    #$$ def add
    def add(self, id=None, mate=None, h=None, h_w=None, t_w=None, t_f_l=None, b_f_l=None, t_f_u=None, b_f_u=None, ttl=None):

        id    = parse.chdr('setts.id'         , id   )
        h     = parse.chdr('usect.tsect.h'    , h    )
        h_w   = parse.chdr('usect.tsect.h_w'  , h_w  )
        t_w   = parse.chdr('usect.tsect.t_w'  , t_w  )
        t_f_l = parse.chdr('usect.tsect.t_f_l', t_f_l)
        b_f_l = parse.chdr('usect.tsect.b_f_l', b_f_l)
        t_f_u = parse.chdr('usect.tsect.t_f_u', t_f_u)
        b_f_u = parse.chdr('usect.tsect.b_f_u', b_f_u)

        # fullfill dimension
        h,h_w,t_f_l,t_f_u=self._us_height(h,h_w,t_f_l,t_f_u)

        data = self._calc(h,h_w,t_w,t_f_l,b_f_l,t_f_u,b_f_u)

        # parse universal units section 1d data
        self.core.usecp.value.add(**{**data, **{
                'id'   : id,
                'mate' : mate,
                'ttl'  : ttl,
                'subcl': 'tsect',
            }}
        )

        data = self._sspt(h,h_w,t_w,t_f_l,b_f_l,t_f_u,b_f_u)

        self.core.dbase.add(
            mode  = 'r',
            table = '[025:usecp:tsect]',
            cols  = ['id','h','h_w','t_w','t_f_u','b_f_u','t_f_l','b_f_l'],
            data  = [ id , h , h_w , t_w , t_f_u , b_f_u , t_f_l , b_f_l ],
        )

        self.core.usecp.point.adm(
            cols = ['id','y','z','ttl','sect','mate'],
            defs = {'sect+d':id, 'mate+d':mate},
            data = data,
        )


    def _calc(self,h,h_w,t_w,t_f_l,b_f_l,t_f_u,b_f_u):
        '''
        Calculate geometric characteristic and few other section parameters.
        '''

        if h    ==None: h     = 0
        if h_w  ==None: h_w   = 0
        if t_w  ==None: t_w   = 0
        if t_f_l==None: t_f_l = 0
        if b_f_l==None: b_f_l = 0
        if t_f_u==None: t_f_u = 0
        if b_f_u==None: b_f_u = 0

        A = h_w * t_w + t_f_l * b_f_l + t_f_u * b_f_u

        S_y = (
            (h_w * t_w) * (t_f_u + 0.5*h_w) +
            (t_f_l * b_f_l) * (t_f_u + h_w + 0.5*t_f_l) +
            (t_f_u * b_f_u) * (0.5*t_f_u)
        )

        z_0 = S_y/A

        I_y = (
            (  h_w**3*t_w  /12)+(  h_w*t_w  )*(t_f_u+0.5*h_w-z_0)**2 +
            (t_f_l**3*b_f_l/12)+(t_f_l*b_f_l)*(t_f_u+h_w+ 0.5*t_f_l-z_0)**2 +
            (t_f_u**3*b_f_u/12)+(t_f_u*b_f_u)*(0.5*t_f_u-z_0)**2
        )

        I_z = (
            t_w**3 * h_w / 12 +
            b_f_l**3 * t_f_l / 12 +
            b_f_u**3 * t_f_u / 12
        )

        u = (
            b_f_l * 2 - t_w + 2* t_f_l +
            b_f_u * 2 - t_w + 2* t_f_u +
            h_w * 2
        )

        A_y,A_z,A_1,A_2,I_t,z_sc,y_sc,C_m,C_ms=[None]*9

        y_c,z_c=0,0
        I_1 = max([I_y,I_z])
        I_2 = min([I_y,I_z])
        z_min = -z_0
        z_max = (h_w+t_f_l+t_f_u)-z_0
        y_max = max(b_f_l, b_f_u, t_w)/2
        y_min = -y_max
        α = 0 if I_y>I_z else 1.5708

        return {
            'A_y'  : A_y   ,
            'A_z'  : A_z   ,
            'A_1'  : A_1   ,
            'A_2'  : A_2   ,
            'I_t'  : I_t   ,
            'z_sc' : z_sc  ,
            'y_sc' : y_sc  ,
            'C_m'  : C_m   ,
            'C_ms' : C_ms  ,
            'A'    : A     ,
            'I_y'  : I_y   ,
            'I_z'  : I_z   ,
            'u'    : u     ,
            'y_c'  : y_c   ,
            'z_c'  : z_c   ,
            'I_1'  : I_1   ,
            'I_2'  : I_2   ,
            'z_min': z_min ,
            'z_max': z_max ,
            'y_max': y_max ,
            'y_min': y_min ,
            'α'    : α     ,
        }


    def _sspt(self,h,h_w,t_w,t_f_l,b_f_l,t_f_u,b_f_u):
        '''
        Create stress points.
        '''

        data = [] # id, y, z, ttl

        if h_w and t_w:
            data.append(['ax' , 0,     0,  'stress in gravity center'])
            data.append(['zh+', 0,  h_w/2, 'clear bending My in z+'])
            data.append(['zh-', 0, -h_w/2, 'clear bending My in z-'])

        return data


    def _us_height(self, h, h_w, t_f_l, t_f_u):
        '''
        _us_height(h=1, h_w=0.5, t_f_l=True, t_f_u=True)
            {'h': 1, 'h_w': 0.5, 't_f_l': 0.25, 't_f_u': 0.25}
        _us_height(h=1, h_w=0.5, t_f_l=True, t_f_u=None)
            {'h': 1, 'h_w': 0.5, 't_f_l': 0.5, 't_f_u': None}
        _us_height(h=1, h_w=0.5, t_f_l=None, t_f_u=True)
            {'h': 1, 'h_w': 0.5, 't_f_l': None, 't_f_u': 0.5}
        _us_height(h=1, h_w=0.5, t_f_l=None, t_f_u=None)
            ValueError!

        _us_height(h=1, h_w=None, t_f_l=0.2, t_f_u=0.3)
            {'h': 1, 'h_w': 0.5, 't_f_l': 0.2, 't_f_u': 0.3}
        _us_height(h=1, h_w=None, t_f_l=0.2, t_f_u=None)
            {'h': 1, 'h_w': 0.8, 't_f_l': 0.2, 't_f_u': None}
        _us_height(h=1, h_w=None, t_f_l=None, t_f_u=0.3)
            {'h': 1, 'h_w': 0.7, 't_f_l': None, 't_f_u': 0.3}

        _us_height(h=None, h_w=0.5, t_f_l=0.2, t_f_u=0.3)
            {'h': 1.0, 'h_w': 0.5, 't_f_l': 0.2, 't_f_u': 0.3}
        _us_height(h=None, h_w=0.5, t_f_l=0.2, t_f_u=None)
            {'h': 0.7, 'h_w': 0.5, 't_f_l': 0.2, 't_f_u': None}
        _us_height(h=None, h_w=0.5, t_f_l=None, t_f_u=0.3)
            {'h': 0.8, 'h_w': 0.5, 't_f_l': None, 't_f_u': 0.3}
        '''

        if h and h_w and t_f_l==True and t_f_u==True:
            t_f_l = (h-h_w)/2
            t_f_u = t_f_l

        elif h and h_w and t_f_l==True and t_f_u==None:
            t_f_l = h-h_w

        elif h and h_w and t_f_l==None and t_f_u==True:
            t_f_u = h-h_w

        elif h and t_f_l and t_f_u:
            h_w = h - t_f_l - t_f_u

        elif h and t_f_l and t_f_u==None:
            h_w = h - t_f_l

        elif h and t_f_l==None and t_f_u:
            h_w = h - t_f_u


        elif h_w and t_f_l and t_f_u:
            h = h_w + t_f_l + t_f_u

        elif h_w and t_f_l and t_f_u==None:
            h = h_w + t_f_l

        elif h_w and t_f_l==None and t_f_u:
            h = h_w + t_f_u

        else:
            raise ValueError('Inshape data')

        return h, h_w, t_f_l, t_f_u


    def echo(self, mode='a+', where=None):

        if 'a' in mode:
            data = self.core.dbase.get(
                mode  = 'm',
                table = '[025:usecp:tsect]',
                cols  = ['id','h','h_w','t_w','t_f_u','b_f_u','t_f_l','b_f_l'],
                where = where,
            )

            if not data: return

            self.core.pinky.rstme.table(
                caption= 'T-section one dimmensional',
                wrap   = [False,False,False,False,False,False,False],
                width  = [True,8,8,8,8,8,8],
                halign = ['l','c','c','c','c','c','c'],
                valign = ['m','u','u','u','u','u','u'],
                dtype  = ['t','e','e','e','e','e','e'],
                header = ['id',['h','h_w'],'t_w','t_f_u',
                          'b_f_u','t_f_l','b_f_l'],
                data   = [[
                    row['id'],
                    [row['h'], row['h_w']],
                    row['t_w'],
                    row['t_f_u'],
                    row['b_f_u'],
                    row['t_f_l'],
                    row['b_f_l'],

                ] for row in data],
                precision = 2,
            )

            if not '+' in mode: return
            
            self.core.pinky.rstme.table(
                wrap   = [False, False, False, True],
                width  = [23, 3, 2,True],
                halign = ['r','l','c','l'],
                valign = ['u','u','u','u'],
                dtype  = ['t','t','t','t'],
                data   = [
                    ['id','','-','identificator'],
                    ['h','[m]','-','total height of section'],
                    ['h_w','[m]','-','section web height'],
                    ['t_w','[m]','-','thickness of web'],
                    ['t_f_u','[m]','-','thickness of upper flange'],
                    ['b_f_u','[m]','-','width of upper flange'],
                    ['t_f_l','[m]','-','thickness of lower flange'],
                    ['b_f_l','[m]','-','width of lower flange'],
                ],
                border = False,
            )