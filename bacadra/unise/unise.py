'''
------------------------------------------------------------------------------
***** (uni)ts for (s)tructural (e)ngineering *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ######################################################################### #

#$ ____ import _____________________________________________________________ #

import math
import numpy as np
from ..tools.setts import setts_init
from ..tools.fpack import nprec
from . import udict, verrs


#$ ____ class setts ________________________________________________________ #

class setts(setts_init):

    def system(self, value=None, check=None, reset=None):
        '''
        system of units.
        '''
        return self.tools.gst('system', value, check, reset)

    def syspro(self, value=None, check=None, reset=None):
        '''
        Convert units to other system inplace. Can be localy changed in primary method.
        '''
        return self.tools.gst('syspro', value, check, reset)

    def sysadd(self, value=None, check=None, reset=None):
        '''
        sysadd convert units.
        '''
        return self.tools.gst('sysadd', value, check, reset)

    def style(self, value=None, check=None, reset=None):
        return self.tools.gst('style', value, check, reset)

    def notation(self, value=None, check=None, reset=None):
        return self.tools.gst('notation', value, check, reset)

    def trail(self, value=None, check=None, reset=None):
        return self.tools.gst('trail', value, check, reset)

    def significant(self, value=None, check=None, reset=None):
        return self.tools.gst('significant', value, check, reset)

    def decimal(self, value=None, check=None, reset=None):
        return self.tools.gst('decimal', value, check, reset)

    def exp_width(self, value=None, check=None, reset=None):
        return self.tools.gst('exp_width', value, check, reset)

    def echo(self, value=None, check=None, reset=None):
        return self.tools.gst('echo', value, check, reset)



#$ ____ class unise ________________________________________________________ #

class unise:

#$$ ________ setts _________________________________________________________ #

    setts = setts()
    setts.system('si')
    setts.syspro(True)
    setts.sysadd(False)
    setts.style('short')
    setts.notation('f')
    setts.trail(False)
    setts.significant(False)
    setts.decimal(False)
    setts.exp_width(1)
    setts.echo(True)

#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, value=1, units=None, system=None):

        self.setts = setts(self.setts, self)

        if system==None: system = unise.setts.system()

        self.setts.system(system)

        # save value
        self._value  = value

        # call to convert methods
        if type(units) == str: units = udict.str2dict(self, units)

        # save units as dict
        self._units  = units



#$$ ________ systems _______________________________________________________ #

#$$$ ____________ base_si __________________________________________________ #


    # si prefixes
    base_si_prefix = {
        'Y'  : 10**24 , # yotta
        'Z'  : 10**21 , # zetta
        'E'  : 10**18 , # exa
        'P'  : 10**15 , # peta
        'T'  : 10**12 , # tera
        'G'  : 10**9  , # giga
        'M'  : 10**6  , # mega
        'k'  : 10**3  , # kilo
        'h'  : 10**2  , # hecto
        'da' : 10**1  , # deca
        'd'  : 10**-1 , # deci
        'c'  : 10**-2 , # centi
        'm'  : 10**-3 , # milli
        'μ'  : 10**-6 , # micro
        'n'  : 10**-9 , # nano
        'p'  : 10**-12, # piko
        'f'  : 10**-15, # femto
        'a'  : 10**-18, # atto
        'z'  : 10**-21, # zepto
        'y'  : 10**-24, # yocto
    }

    # system SI
    base_si = {
        # base units
        'm'  : None, # metre
        'kg' : None, # kilogram
        's'  : None, # second
        'A'  : None, # ampere
        'K'  : None, # kelvin
        'mol': None, # mole
        'cd' : None, # candela

        # derived units
        'Hz' : (1, {'s'  :-1                               }),
        'rad': (1, {                                       }),
        'sr' : (1, {                                       }),
        'N'  : (1, {'kg' : 1, 'm'  : 1, 's'  :-2           }),
        'Pa' : (1, {'kg' : 1, 'm'  :-1, 's'  :-2           }),
        'J'  : (1, {'kg' : 1, 'm'  : 2, 's'  :-2           }),
        'W'  : (1, {'kg' : 1, 'm'  : 2, 's'  :-3           }),
        'C'  : (1, {'s'  : 1, 'A'  : 1                     }),
        'V'  : (1, {'kg' : 1, 'm'  : 2, 's'  :-3, 'A'  :-1 }),
        'F'  : (1, {'kg' :-1, 'm'  :-2, 's'  : 4, 'A'  : 2 }),
        'Ω'  : (1, {'kg' : 1, 'm'  : 2, 's'  :-3, 'A'  :-2 }),
        'S'  : (1, {'kg' :-1, 'm'  :-2, 's'  : 3, 'A'  : 2 }),
        'Wb' : (1, {'kg' : 1, 'm'  : 2, 's'  :-2, 'A'  :-1 }),
        'T'  : (1, {'kg' : 1, 's'  :-2, 'A'  :-1           }),
        'H'  : (1, {'kg' : 1, 'm'  : 2, 's'  :-2, 'A'  :-2 }),
        '°C' : (1, {'K'  : 1                               }),
        'lm' : (1, {'cd' : 1                               }),
        'lx' : (1, {'m'  :-2, 'cd' : 1                     }),
        'Bq' : (1, {'s'  :-1                               }),
        'Gy' : (1, {'m'  : 2, 's'  :-2                     }),
        'Sv' : (1, {'m'  : 2, 's'  :-2                     }),
        'kat': (1, {'s'  :-1, 'mol': 1                     }),

        # derived with prefix
        'μm'  : (base_si_prefix['μ'], {'m' : 1                 }),
        'mm'  : (base_si_prefix['m'], {'m' : 1                 }),
        'cm'  : (base_si_prefix['c'], {'m' : 1                 }),
        'dm'  : (base_si_prefix['d'], {'m' : 1                 }),
        'km'  : (base_si_prefix['k'], {'m' : 1                 }),
        'mrad': (base_si_prefix['m'], {                        }),
        'kN'  : (base_si_prefix['k'], {'kg': 1, 'm': 1, 's':-2 }),
        'MN'  : (base_si_prefix['M'], {'kg': 1, 'm': 1, 's':-2 }),
        'kPa' : (base_si_prefix['k'], {'kg': 1, 'm':-1, 's':-2 }),
        'MPa' : (base_si_prefix['M'], {'kg': 1, 'm':-1, 's':-2 }),
        'GPa' : (base_si_prefix['G'], {'kg': 1, 'm':-1, 's':-2 }),

        # addictional
        '%'  : (0.01, {}),
        'yr' : (60*60*24*365,  {'s' : 1}),
        'day': (60*60*24,      {'s' : 1}),
        'hr' : (60*60,         {'s' : 1}),
        'min': (60,            {'s' : 1}),
        'deg': (math.pi/180,   {       }),
        '°'  : (math.pi/180,   {       }),
        't'  : (1000,          {'kg': 1}),

        # shortcuts
        'Length'     : (1,     {'m' : 1}),
        'Mass'       : (1,     {'kg': 1}),
        'Time'       : (1,     {'s' : 1}),
        'Temperature': (1,     {'K' : 1}),
        'Force'      : (1,     {'N' : 1}),
        'Pressure'   : (1,     {'Pa': 1}),
    }

    # system sysadd for Stucture Engineering, kN, m, °C, s
    base_si_ce = {
        'kg'  : (0.001 , {'kN': 1, 'm':-1, 's': 2         }),
        'K'   : (1     , {'°C': 1                         }),
    }



#$$ ________ base operations _______________________________________________ #

#$$$ ____________ def base _________________________________________________ #

    def base(self=None, system=True, sysadd=True):
        '''
        The system atribute type must be dictonary. Inside them we need include the fallowing type:
        {'<name>' : (<numerical object>,
                     <dictonary with unit power>)}
        if unit should be base unit, then just type {'<name>':(None)}
        '''

        # class and object method in one
        if self==None: self=unise

        if system==True:
            system = self.setts.system()

        if sysadd==True:
            sysadd = self.setts.sysadd()

        if sysadd!=False:
            sysadd = '_' + sysadd
        else:
            sysadd = ''

        return getattr(self, 'base_'+system+sysadd)


#$$$ ____________ def add __________________________________________________ #

    @staticmethod
    def add(name, value, units, overwrite=False):
        '''
        Add child unit to current system. Current system can be check under self.system atribute. As input method want:
        - name - new name of unit, like "m" or "kN",
        - value - multiply number,
        - units - dictonary with basic unit, basic and only basic!
        If overwrite is True, then if definition of unit alredy exists, then it will be overwriten! If overwrite is False, if same case method return errror.
        '''

        # check overwrite flag
        if (not overwrite) and (name in unise.base()):

            # if flag if False and name alredy exists, then raise error
            verrs.BCDR_unise_ERROR_Already_Exists(unise.setts.system(), name)

        # extend base dict
        unise.base(sysadd=False).update({name:(value, units)})

        # retur unise object
        # return unise.get(name)

#$$$ ____________ def rem __________________________________________________ #

    @staticmethod
    def rem(name, silent=True):
        '''
        Delete unit from current system. If silent is True, then no error occur if name not occur in self.base too.
        '''

        # first check if name is exists in self.base
        if name in unise.base():

            # the fastest method of delete key is del statment
            del unise.base()[name]

        # if not exists, then check silent flag
        elif not silent:

            # if silent if False, then raise error
            verrs.BCDR_cunit_ERROR_Units_in_System(unise.setts.system(), name)






#$$$ ____________ def get __________________________________________________ #

    @classmethod
    def get(self, units, system=None, sysadd=False):
        '''
        User input units as string type. This must be checked explicit, link in __init__(...). The set up _value and _units as copy from system definition if it exists, else return unisesystemERROR.
        This method must set up _value and _units or raise error!
        '''

        system = self.setts.system(system, check=True)
        base = self.base(system=system, sysadd=sysadd)

        if units in base:
        # get value and unit from system defintion
            base_value = base[units]
            # base_value = unise.base[units]

            # if returned was base unit (value is equal to None), then prepare object value and unit by hand
            if base_value == None:
                return unise(1, {units:1}, system)
            # else get value and unit
            else:
                return unise(base_value[0], base_value[1], system)

        # if unit does not exist in base system, then raise error
        else:
            verrs.BCDR_unise_ERROR_Units_in_System(system, units)







#$$ ________ basis operations ______________________________________________ #

#$$$ ____________ def primary ______________________________________________ #

    def primary(self, system=True, sysadd=True, inplace=False, scheck=True, key_prefix=''):

        if type(self)!=unise:
            if type(self)==list:
                return [unise.primary(obj, system, sysadd, inplace) for obj in self]
            elif type(self)==tuple:
                return tuple(unise.primary(obj, system, sysadd, inplace) for obj in self)
            elif type(self)==np.ndarray:
                return np.array([unise.primary(obj, system, sysadd, inplace) for obj in self])
            else:
                return self


        # othe = cunit(self._value, self._units, self.setts.system())
        if self.setts.syspro()==True:
            othe = self
        else:
            othe = self.copy()

        if system in [None, True]: system = unise.setts.system()

        # if current system of variable is diffrent than specyfied system and scheck flags is True, then go and convert unit
        if (othe.setts.system() != system) and scheck:

            print('system convert! syspro:',self.setts.syspro())
            print('old system:', othe.setts.system())
            print('new system:', system)

            # if old system is other than si
            # then go and first convert it to si
            if othe.setts.system() != 'si':

                # convert self to primary units in old system
                othe.primary(
                    system       = othe.setts.system(),
                    scheck       = False,
                    inplace      = True,
                    key_prefix   = '',
                )

                # now convert othe to new system
                othe.primary(
                    system       = othe.setts.system(),
                    scheck       = False,
                    inplace      = True,
                    key_prefix   = 'me->si:',
                )

                # change self system variable
                othe.setts.system('si')

                # just use self primary to full convert variable
                othe.primary(
                    system       = othe.setts.system(),
                    scheck       = False,
                    inplace      = True,
                    key_prefix   = '',
                )

                # now the variable is full ready in si system

            # if new system is other than si, then convert it
            # please notice, that variable must be already in si system
            if system != 'si':

                # convert self to primary units in old system
                othe.primary(
                    system       = othe.setts.system(),
                    scheck       = False,
                    inplace      = True,
                    key_prefix   = '',
                )

                # now convert othe to new system
                othe.primary(
                    system       = system,
                    scheck       = False,
                    inplace      = True,
                    key_prefix   = 'si->me:',
                )

                # change othe system variable
                othe.setts.system(system)

                # just use self primary to full convert variable
                othe.primary(
                    system       = othe.setts.system(),
                    scheck       = False,
                    inplace      = True,
                    key_prefix   = '',
                )


        base = othe.base(system=system, sysadd=False)

        # get value
        cv  = othe._value

        if cv == 0:
            return unise(cv, {})

        # copy unit dictonary
        cd, od = othe._units.copy(), {}

        # loop over keys in unit dictonary
        while cd!=od:

            od = cd.copy()

            for key,val in od.items():

                # get base key
                base_value = base[key_prefix+key]

                # if unit is not primary then convert it to primary
                if base_value!=None:

                    # multiply value by unit value
                    cv *= base_value[0] ** val

                    # delete key from dictonary
                    cd.pop(key, None)

                    # sum unit's power, which need to consider actual power
                    cd = udict.dsum(cd, udict.vmul(base_value[1], val))

        if sysadd!=None and scheck:

            base = othe.base(system=system, sysadd=sysadd)

            od = {}

            # loop over keys in unit dictonary
            while cd!=od:

                od = cd.copy()

                for key,val in od.items():

                    # if unit is not primary then convert it to primary
                    if key in base and base[key]!=None:

                        # multiply value by unit value
                        cv *= base[key][0] ** val

                        # delete key from dictonary
                        cd.pop(key, None)

                        # sum unit's power, which need to consider actual power
                        cd = udict.dsum(cd, udict.vmul(base[key][1], val))

        # convert self inplace
        if inplace:
            self._value = cv
            self._units = cd
            if system!=True:
                self.setts.system(system)
            return self

        # return new unise, does not convert old!
        else:
            othe = unise(cv, cd)
            if system!=True:
                othe.setts.system(system)
            return othe


#$$$ ____________ def convert ______________________________________________ #

    def convert(self, units, cover=False, inplace=False):
        '''
        Convert unit to other one. Convert as defualt return new one object of unise, but inplace flag can convert inplace.

        If cover flags==True, then units must full cover old unit stack. New units can be input as dict, as string or as unise.
        '''

        if type(self)!=unise:
            if type(self)==list:
                return [unise.convert(obj, units, cover, inplace) for obj in self]
            elif type(self)==tuple:
                return tuple(unise.convert(obj, units, cover, inplace) for obj in self)
            elif type(self)==np.ndarray:
                return np.array([unise.convert(obj, units, cover, inplace) for obj in self])
            else:
                return self


        # check type of new units
        # if is typed as string then convert string to dict
        if type(units) == str:
            units = udict.str2dict(self, units)

        # if it is type as unise then get _units from them
        elif type(units) == unise:
            units = units._units

        # create copy of self and run primary
        self = self.primary()

        # create other value and run primary
        othe = unise(1, units).primary(inplace=True)

        # divide number and sub units
        ve = self._value / othe._value
        ue = udict.dsub(self._units, othe._units)

        # if cover==True then convert must be fully
        if cover in [True,'True','T'] and ue!={}:
            # if result of divide is not empty unit then raise error
            verrs.BCDR_unise_ERROR_Cover(
                old  = self._units,
                new  = units,
                diff = ue,
            )

        # check inplace flag, hmm, dont work inplace?
        if inplace:
            self._value = ve
            self._units = udict.dsum(units, ue)
            return self

        # return new unise
        else:
            return unise(ve, udict.dsum(units, ue))



#$$$ ____________ def copy _________________________________________________ #

    def copy(self):
        '''
        Return copy of self. Needed in show function etc.
        '''

        if type(self)!=unise:
            if type(self)==list:
                return [unise.copy(obj) for obj in self]
            elif type(self)==tuple:
                return tuple(unise.copy(obj) for obj in self)
            elif type(self)==np.ndarray:
                return np.array([unise.copy(obj) for obj in self])
            else:
                return self


        othe = unise(self._value, self._units)
        othe.setts = self.setts
        return othe


#$$$ ____________ def drop _________________________________________________ #

    def drop(self, units=None, cover=True, system=True, sysadd=True):
        '''
        Drop unit and return value alone. If dropped pattern unit is not explicit defined, then drop as system base. Is system is not explicited defined then use current system.
        '''

        if type(self)!=unise:
            if type(self)==list:
                return [unise.drop(obj, units, cover, system, sysadd) for obj in self]
            elif type(self)==tuple:
                return tuple(unise.drop(obj, units, cover, system, sysadd) for obj in self)
            elif type(self)==np.ndarray:
                return np.array([unise.drop(obj, units, cover, system, sysadd) for obj in self])
            else:
                return self

        self = self.primary(system=system, sysadd=sysadd)

        # if units is defined explicity
        # so if it is typed as string
        if type(units)==str:
            # then convert string to dictonary
            units = udict.str2dict(self, units)

        # else is not defined
        elif units==None:
            # get primary unit and extract _units from it
            units = self._units

        # create other value and run primary
        othe = unise(1, units).primary(system=system, sysadd=sysadd, inplace=True)

        # divide number and sub units
        ve = self._value / othe._value
        ue = udict.dsub(self._units, othe._units)

        # if cover==True then convert must be fully
        if cover in [True, 'True','T'] and ue!={}:
            # if result of divide is not empty unit then raise error
            verrs.BCDR_unise_ERROR_Cover(
                old  = self._units,
                new  = units,
                diff = ue,
            )

        return ve




#$$$ ____________ def gdim _________________________________________________ #

    def gdim(self, primary=True, system=True):
        '''
        Get dimension of unise.
        '''

        if type(self)!=unise:
            if type(self)==list:
                return [unise.units(obj, primary, system) for obj in self]
            elif type(self)==tuple:
                return tuple(unise.units(obj, primary, system) for obj in self)
            elif type(self)==np.ndarray:
                return np.array([unise.units(obj, primary, system) for obj in self])
            else:
                return self

        if primary==True:
            self = self.copy()
            self.primary(inplace=True)

        return unise(1, self._units)



#$$$ ____________ def call _________________________________________________ #

    def call(self, code=None, units=None, decimal=None, significant=None, style=None, notation=None, trail=None, exp_width=None, cover=None, system=None, sysadd=None, inplace=None,

    u=None, d=None, s=None, y=None, n=None, t=None, e=None, c=None, b=None, p=None, i=None):
        '''
        Now call replace old method edit and show.
        '''

        if code:
            return self.format(code, style2ltx=False, out2repr=False)

        if units       == None: units       = u
        if decimal     == None: decimal     = d
        if significant == None: significant = s
        if style       == None: style       = y
        if notation    == None: notation    = n
        if trail       == None: trail       = t
        if exp_width   == None: exp_width   = e
        if cover       == None: cover       = c
        if system      == None: system      = b
        if inplace     == None: inplace     = i

        if type(self)!=unise:
            if type(self)==list:
                return [unise.call(obj, units,decimal,significant,style ,notation,trail,exp_width ,cover,system,inplace) for obj in self]
            elif type(self)==tuple:
                return tuple(unise.call(obj, units,decimal,significant,style ,notation,trail,exp_width ,cover,system,inplace) for obj in self)
            elif type(self)==np.ndarray:
                return np.array([unise.call(obj, units,decimal,significant,style ,notation,trail,exp_width ,cover,system,inplace) for obj in self])
            else:
                return self


        if inplace==True:
            othe = self
        else:
            othe = self.copy()

        if system or sysadd:
            othe.primary(system=system, sysadd=sysadd, inplace=True)
        elif system:
            othe.primary(system=system,            inplace=True)
        elif system:
            othe.primary(               sysadd=sysadd, inplace=True)

        if units:
            othe = othe.convert(units=units, cover=cover, inplace=True)

        if decimal     != None: othe.setts.decimal     ( int(decimal     ))
        if significant != None: othe.setts.significant ( int(significant ))
        if style       != None: othe.setts.style       ( style            )
        if notation    != None: othe.setts.notation    ( notation         )
        if trail       != None: othe.setts.trail       ( trail            )
        if exp_width   != None: othe.setts.exp_width   ( int(exp_width   ))

        # return new object as self or other
        return othe

#$$$ ____________ def format _______________________________________________ #

    def format(self, code='', style2ltx=True, out2repr=True):

        if type(self)!=unise:
            if type(self)==list:
                return [unise.format(obj, code, style2ltx) for obj in self]
            elif type(self)==tuple:
                return tuple(unise.format(obj, code, style2ltx) for obj in self)
            elif type(self)==np.ndarray:
                return np.array([unise.format(obj,code, style2ltx) for obj in self])
            else:
                return self

        out = {}

        # loop over code
        if len(code)>0:
            for key in code.split(':'):

                add = 1 if key[1]=='=' else 0

                # add it into dict
                out.update({key[0]:key[1+add:]})

        if style2ltx and 'y' not in out:
            out['y'] = 'latex'

        if out2repr:
            return repr(self.call(**out))
        else:
            return self.call(**out)


#$$$ ____________ def __call__ _____________________________________________ #

    __call__ = call

#$$$ ____________ def __format__ ___________________________________________ #

    __format__ = format

#$$$ ____________ def __rshift__ ___________________________________________ #

    __rshift__ = call


#$$ ________ decorators ____________________________________________________ #

#$$$ ____________ def ufree ________________________________________________ #

    @staticmethod
    def ufree(**p2d):
        def check_types(func, p2d = p2d):
            def modified(*args, **kw):
                arg_names = func.__code__.co_varnames
                kw.update(zip(arg_names, args))
                _ous    = p2d['_ous']    if '_ous'    in p2d else None
                _ouc    = p2d['_ouc']    if '_ouc'    in p2d else None
                _system = p2d['_system'] if '_system' in p2d else None
                for name, category in p2d.items():
                    if name in ['_ous', '_ouc', '_system']:
                        continue
                    if name in kw and type(kw[name])==unise:
                        kw[name] = unise.drop(
                            kw[name], category, system=_system)
                if _ous and not _ouc:
                    return unise(func(**kw), _ous).primary()
                elif _ous and _ouc:
                    return unise(func(**kw), _ous).call(_ouc)
                else:
                    return func(**kw)
            modified.__name__ = func.__name__
            modified.__doc__  = func.__doc__
            return modified
        return check_types






#$$ ________ magic behaviour _______________________________________________ #

#$$$ ____________ def __add__ ______________________________________________ #

    def __add__(self, othe):
        '''
        Python Magic Method: self + othe
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # now if-block of data type
        # if second variable is also unise
        if othe_type == unise:
            # then primary units self and othe
            s = self.primary()
            o = othe.primary()

            # below if-block is neccesary, because we want that 0*m**3 + 0*kN shoud work correctly. fix-zero value
            if s._value == 0: return o
            if o._value == 0: return s

            # check compability and else raise error
            verrs.BCDR_unise_ERROR_Units_Incompatible(s, o, 'add')

            v = s._value + o._value
            if v==0:
                u = {}
            else:
                u = s._units

            # return new instant of unise, get s or o units, they are the same
            return unise(v,u)

        # if second variable is given as list, so we want add variable to list or list to variable (we want 2-dir the same method)
        elif othe_type == list:
            # loop over all value in list and call recurive
            return [self.__add__(val) for val in othe]

        # if second variable is numpy array, again, loop over
        elif othe_type == np.ndarray:
            return np.array([self.__add__(val) for val in othe])

        # if type is zero, then just return self
        elif othe == 0:
            return self

        # if self units is empty, again, just return self without unit
        elif self._units in [{}, {'%':1}]:
            val = self._value if self._units == {} else self._value / 100
            return unise(val + othe, {})

        # else raise error
        else:
            verrs.BCDR_unise_ERROR_Undefined_Operator(self, othe, 'add')

#$$$ ____________ def __radd__ _____________________________________________ #

    def __radd__(self, othe):
        '''
        Python Magic Method: othe + self
        '''
        return self.__add__(othe)


#$$$ ____________ def __iadd__ _____________________________________________ #

    def __iadd__(self, othe):
        '''
        Python Magic Method: self += othe
        '''
        return self.__add__(othe)

#$$$ ____________ def __pos__ ______________________________________________ #

    def __pos__(self):
        '''
        Python Magic Method: +self
        '''
        return self


#$$$ ____________ def __sub__ ______________________________________________ #

    def __sub__(self, othe):
        '''
        Python Magic Method: self - othe
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # now if-block of data type
        # if second variable is also unise
        if othe_type == unise:
            # then primary units self and othe
            s = self.primary()
            o = othe.primary()

            # below if-block is neccesary, because we want that 0*m**3 + 0*kN shoud work correctly. fix-zero value
            if s._value == 0: return -o
            if o._value == 0: return s

            # check compability
            verrs.BCDR_unise_ERROR_Units_Incompatible(s, o, 'sub')

            v = s._value - o._value
            if v==0:
                u = {}
            else:
                u = s._units

            # return new instant of unise, get s or o units, they are the same
            return unise(v,u)

        # if second variable is given as list, so we want add variable to list or list to variable (we want 2-dir the same method)
        elif othe_type == list:
            # loop over all value in list and call recurive
            return [self.__sub__(val) for val in othe]

        # if second variable is numpy array, again, loop over
        elif othe_type == np.ndarray:
            return np.array([self.__sub__(val) for val in othe])

        # if type is zero, then just return self
        elif othe == 0:
            return self

        # if self units is empty, again, just return self without unit
        elif self._units in [{}, {'%':1}]:
            val = self._value if self._units == {} else self._value / 100
            return unise(val - othe, {})

        # else raise error
        else:
            verrs.BCDR_unise_ERROR_Undefined_Operator(self, othe, 'sub')


#$$$ ____________ def __rsub__ _____________________________________________ #

    def __rsub__(self, othe):
        '''
        Python Magic Method: othe - self
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # now if-block of data type
        # if second variable is also unise
        if othe_type == unise:
            # then primary units self and othe
            s = self.primary()
            o = othe.primary()

            # below if-block is neccesary, because we want that 0*m**3 + 0*kN shoud work correctly. fix-zero value
            if s._value == 0: return o
            if o._value == 0: return -s

            # check compability
            verrs.BCDR_unise_ERROR_Units_Incompatible(s, o, 'rsub')

            v = o._value - s._value
            if v==0:
                u = {}
            else:
                u = s._units

            # return new instant of unise, get s or o units, they are the same
            return unise(v,u)

        # if second variable is given as list, so we want add variable to list or list to variable (we want 2-dir the same method)
        elif othe_type == list:
            # loop over all value in list and call recurive
            return [self.__rsub__(val) for val in othe]

        # if second variable is numpy array, again, loop over
        elif othe_type == np.ndarray:
            return np.array([self.__rsub__(val) for val in othe])

        # if type is zero, then just return self
        elif othe == 0:
            return -self

        # if self units is empty
        elif self._units in [{}, {'%':1}]:
            val = self._value if self._units == {} else self._value / 100
            return unise(othe - val, {})

        # else raise error
        else:
            verrs.BCDR_unise_ERROR_Undefined_Operator(self, othe, 'rsub')

#$$$ ____________ def __isub__ _____________________________________________ #

    def __isub__(self, othe):
        '''
        Python Magic Method: self -= othe
        '''
        return self.__sub__(othe)

#$$$ ____________ def __neg__ ______________________________________________ #

    def __neg__(self):
        '''
        Python Magic Method: -self
        '''
        return unise(-self._value, self._units)


#$$$ ____________ def __pow__ ______________________________________________ #

    def __pow__(self, othe):
        '''
        Python Magic Method: self**othe
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # if type othe is unise withou unit, then convert it to number data
        if othe_type== unise and othe._units == {}:
            othe = othe._value
        elif othe_type==unise:
            verrs.BCDR_unise_ERROR_Power2unise(othe)

        # convert self to primary unit
        s = self.primary()

        # return powered unise
        return unise(s._value**othe, udict.vmul(s._units, othe))

#$$$ ____________ def __rpow__ _____________________________________________ #

    def __rpow__(self, othe):
        '''
        Python Magic Method: othe**self
        '''

        # if self._units is not empty, then exception must occur, the unise in power zone is not implemented and probably will not be
        if self._units != {}:
            verrs.BCDR_unise_ERROR_Power2unise(self)

        # but if _units is empty, then i can treat it as clean self._value and return result
        # if othe will be unise, then by recurency __pow__ will start
        return othe ** self._value

#$$$ ____________ def __ipow__ _____________________________________________ #

    def __ipow__(self, othe):
        '''
        Python Magic Method: self **= othe
        '''
        return self.__pow__(othe)


#$$$ ____________ def __mul__ ______________________________________________ #

    def __mul__(self, othe):
        '''
        Python Magic Method: self * othe
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # now if-block of data type
        # if second variable is also unise
        if othe_type == unise:
            if self._value == 0 or othe._value == 0:
                return unise(0, {})

            # then primary units self and othe
            # note: we do not need to check compability units, we can multiply any two units
            s = self.primary()
            o = othe.primary()

            v = s._value * o._value
            if v==0:
                u = {}
            else:
                u = udict.dsum(s._units, o._units)

            # return new unise, with multipled value and summed units
            return unise(v, u)

        # if second variable is given as list, so we want add variable to list or list to variable (we want 2-dir the same method)
        elif othe_type == list:
            # loop over all value in list and call recurive
            return [self.__mul__(val) for val in othe]

        # if second variable is numpy array, again, loop over
        elif othe_type == np.ndarray:
            return np.array([self.__mul__(val) for val in othe])

        # else just try to multiply value with othe and pase units
        else:
            return unise(self._value * othe, self._units)

#$$$ ____________ def __rmul__ _____________________________________________ #

    def __rmul__(self, othe):
        '''
        Python Magic Method: othe * self
        '''
        return self.__mul__(othe)

#$$$ ____________ def __imul__ _____________________________________________ #

    def __imul__(self, othe):
        '''
        Python Magic Method: self *= othe
        '''
        return self.__mul__(othe)


#$$$ ____________ def __truediv__ __________________________________________ #

    def __truediv__(self, othe):
        '''
        Python Magic Method: self / othe
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # now if-block of data type
        # if second variable is also unise
        if othe_type == unise:
            if self._value == 0:
                return unise(0, {})

            # then primary units self and othe
            # note: we do not need to check compability units, we can multiply any two units
            s = self.primary()
            o = othe.primary()

            v = s._value / o._value
            if v==0:
                u = {}
            else:
                u = udict.dsub(s._units, o._units)

            # return new unise, with multipled value and summed units
            return unise(v,u)

        # if second variable is given as list, so we want add variable to list or list to variable (we want 2-dir the same method)
        elif othe_type == list:
            # loop over all value in list and call recurive
            return [self.__truediv__(val) for val in othe]

        # if second variable is numpy array, again, loop over
        elif othe_type == np.ndarray:
            return np.array([self.__truediv__(val) for val in othe])

        # else just try to multiply value with othe and pase units
        else:
            return unise(self._value / othe, self._units)

#$$$ ____________ def __rtruediv__ _________________________________________ #

    def __rtruediv__(self, othe):
        '''
        Python Magic Method: othe / self
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # now if-block of data type
        # if second variable is also unise
        if othe_type == unise:
            if othe._value == 0:
                return unise(0, {})

            # then primary units self and othe
            # note: we do not need to check compability units, we can multiply any two units
            s = self.primary()
            o = othe.primary()

            # return new unise, with multipled value and summed units
            return unise(o._value / s._value, udict.dsub(o._units, s._units))

        # if second variable is given as list, so we want add variable to list or list to variable (we want 2-dir the same method)
        elif othe_type == list:
            # loop over all value in list and call recurive
            return [self.__rtruediv__(val) for val in othe]

        # if second variable is numpy array, again, loop over
        elif othe_type == np.ndarray:
            return np.array([self.__rtruediv__(val) for val in othe])

        # else just try to multiply value with othe and pase units
        else:
            return unise(othe / self._value, udict.vmul(self._units, -1))

#$$$ ____________ def __itruediv__ _________________________________________ #

    def __itruediv__(self, othe):
        '''
        Python Magic Method: self /= othe
        '''
        return self.__truediv__(othe)



#$$$ ____________ def __round__ ____________________________________________ #

    def __round__(self, acc=0):
        '''
        Python function: round(self, acc)
        '''
        return unise(round(self._value, acc), self._units)

#$$$ ____________ def __ceil__ _____________________________________________ #

    def __ceil__(self):
        '''
        Python function: ceil(self)
        '''
        return unise(math.ceil(self._value), self._units)

#$$$ ____________ def __trunc__ ____________________________________________ #

    def __trunc__(self):
        '''
        Python function: trunc(self)
        '''
        return unise(math.trunc(self._value), self._units)

#$$$ ____________ def __lt__ _______________________________________________ #

    def __lt__(self, othe):
        '''
        Python Magic Method: self < othe
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # now if-block of data type
        # if second variable is also unise
        if othe_type == unise:
            if othe._value == 0 or self._value == 0:
                return self._value < othe._value

            # then primary units self and othe
            s = self.primary()
            o = othe.primary()

            # check compability
            verrs.BCDR_unise_ERROR_Incompatible(s, o, '__lt__')

            if s._value < o._value:
                return True
            else:
                 return False

        # if type is zero
        elif othe == 0:
            return self._value < 0

        # if self units is empty, again, just return self without unit
        elif self._units in [{}, {'%':1}]:
            val = self._value if self._units == {} else self._value / 100
            return val < othe

        # else raise error
        else:
            verrs.BCDR_unise_ERROR_Undefined_Operator('__lt__', self, othe)



#$$$ ____________ def __le__ _______________________________________________ #

    def __le__(self, othe):
        '''
        Python Magic Method: self <= othe
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # now if-block of data type
        # if second variable is also unise
        if othe_type == unise:
            if othe._value == 0 or self._value == 0:
                return self._value <= othe._value

            # then primary units self and othe
            s = self.primary()
            o = othe.primary()

            # check compability
            verrs.BCDR_unise_ERROR_Incompatible(s, o, '__le__')

            if s._value <= o._value:
                return True
            else:
                 return False

        # if type is zero
        elif othe == 0:
            return self._value <= 0

        # if self units is empty, again, just return self without unit
        elif self._units in [{}, {'%':1}]:
            val = self._value if self._units == {} else self._value / 100
            return val <= othe

        # else raise error
        else:
            verrs.BCDR_unise_ERROR_Undefined_Operator('__le__', self, othe)

#$$$ ____________ def __gt__ _______________________________________________ #

    def __gt__(self, othe):
        '''
        Python Magic Method: self > othe
        '''
        return unise.__lt__(-self,-othe)

#$$$ ____________ def __ge__ _______________________________________________ #

    def __ge__(self, othe):
        '''
        Python Magic Method: self >= othe
        '''
        return unise.__le__(-self,-othe)


#$$$ ____________ def __eq__ _______________________________________________ #

    def __eq__(self, othe):
        '''
        Python Magic Method: self == othe
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # now if-block of data type
        # if second variable is also unise
        if othe_type == unise:
            if othe._value == 0 or self._value == 0:
                return self._value == othe._value

            # then primary units self and othe
            s = self.primary()
            o = othe.primary()

            # check compability
            verrs.BCDR_unise_ERROR_Incompatible(s, o, '__eq__')

            if s._value == o._value:
                return True
            else:
                 return False

        # if type is zero
        elif othe == 0:
            return self._value == 0

        # if self units is empty, again, just return self without unit
        elif self._units in [{}, {'%':1}]:
            val = self._value if self._units == {} else self._value / 100
            return val == othe

        # treat bool and None types
        elif othe in [True, False, None]:
            return self._value == othe

        elif othe_type in [str, dict, list]:
            return False

        # else raise error
        else:
            verrs.BCDR_unise_ERROR_Undefined_Operator('__eq__', self, othe)



#$$$ ____________ def __ne__ _______________________________________________ #

    def __ne__(self, othe):
        '''
        Python Magic Method: self != othe
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # now if-block of data type
        # if second variable is also unise
        if othe_type == unise:
            if othe._value == 0 or self._value == 0:
                return self._value != othe._value

            # then primary units self and othe
            s = self.primary()
            o = othe.primary()

            # check compability
            verrs.BCDR_unise_ERROR_Incompatible(s, o, '__ne__')

            if s._value != o._value:
                return True
            else:
                 return False

        # if type is zero
        elif othe == 0:
            return self._value != 0

        # if self units is empty, again, just return self without unit
        elif self._units in [{}, {'%':1}]:
            val = self._value if self._units == {} else self._value / 100
            return val != othe

        # treat bool and None types
        elif othe in [True, False, None]:
            return self._value != othe

        elif othe_type in [str, dict, list]:
            return True

        # else raise error
        else:
            verrs.BCDR_unise_ERROR_Undefined_Operator('__ne__', self, othe)


#$$$ ____________ def __is__ _______________________________________________ #

    def __is__(self, othe):
        '''
        Python Magic Method: self is othe
        '''
        return self.__eq__(self, othe)

#$$$ ____________ def is_not _______________________________________________ #

    def is_not(self, othe):
        '''
        Python Magic Method: self is not othe
        '''
        return self.__ne__(self, othe)

#$$$ ____________ def __and__ ______________________________________________ #

    def __and__(self, othe):
        '''
        Python Magic Method: self and othe
        '''
        if bool(self._value) and othe:
            return True
        else:
            return False

#$$$ ____________ def __rand__ _____________________________________________ #

    def __rand__(self, othe):
        '''
        Python Magic Method: othe and self
        '''
        return self.__and__(self, othe)



#$$$ ____________ def __xor__  _____________________________________________ #

    def __xor__(self, othe):
        '''
        Python Magic Method: self or othe
        '''
        if bool(self._value) or othe:
            return True
        else:
            return False

#$$$ ____________ def __rxor__  ____________________________________________ #

    def __rxor__(self, othe):
        '''
        Python Magic Method: othe or self
        '''
        return self.__xor__(self, othe)


#$$$ ____________ def __abs__  _____________________________________________ #

    def __abs__(self):
        '''
        Python function: abs(self)
        '''
        return unise(abs(self._value), self._units)


#$$$ ____________ def __mod__  _____________________________________________ #

    def __mod__(self, val):
        '''
        Python function: mod(self)
        '''
        return unise(self._value % val, self._units)


#$$$ ____________ def __float__ ____________________________________________ #

    def __float__(self):
        '''
        Python function: float(self)
        '''
        return float(self._value)


#$$$ ____________ def __int__ ______________________________________________ #

    def __int__(self):
        '''
        Python function: int(self)
        '''
        return int(self._value)


#$$$ ____________ def __bool__ _____________________________________________ #

    def __bool__(self):
        return bool(self._value)


#$$$ ____________ def __repr__ _____________________________________________ #

    def __repr__(self):
        '''
        Representation of unise. The methods provide few styles.
        '''

        # prepare numeric data
        value = nprec(
            value       = self._value,
            notation    = self.setts.notation(),
            trail       = self.setts.trail(),
            significant = self.setts.significant(),
            decimal     = self.setts.decimal(),
            exp_width   = self.setts.exp_width(),
        )

        # convert style to lowercase
        style = self.setts.style().lower()

        if   style == 'pretty': return self.__repr__pretty(self, value)
        elif style == 'python': return self.__repr__python(self, value)
        elif style == 'latex' : return self.__repr__latex(self, value)
        elif style == 'short' : return self.__repr__short(self, value)

#$$$ ____________ def __repr__pretty _______________________________________ #

    @staticmethod
    def __repr__pretty(self, value):
        # denominator - d - mianownik
        # counter - u - licznik

        # init counter and donominator
        u,d = '',''

        # loop over units row in dictonary
        for u_str, u_val in self._units.items():

            u_str = u_str[u_str.rfind('/')+1:]

            # if-block depend on power
            # if power is zero, then pass
            if   u_val==0 : pass

            # if power is one, then expand counter
            elif u_val==1 : u += '[' + u_str + ']'

            # if power is more than one, then expand counter with "^" symbol
            # elif u_val>0  : u += '[' + u_str + '^' + str(u_val)  + ']'
            elif u_val>0  : u += '[' + u_str + str(u_val)  + ']'

            # if power is one, then expand denominator
            elif u_val==-1: d += '[' + u_str + ']'

            # if power is less than one, then expand denominator with "^" symbol
            # elif u_val<0  : d += '[' + u_str + '^' + str(-u_val) + ']'
            elif u_val<0  : d += '[' + u_str + str(-u_val) + ']'


        # if-block depend on counter and denominator empty's
        # if all is empty
        if u=='' and d=='':
            return value + ' [1]'
        elif u=='':
            return value + ' [1]/' + d
        elif d=='':
            return value + ' ' + u
        else:
            return value + ' ' + u + '/' + d


#$$$ ____________ def __repr__short ________________________________________ #

    @staticmethod
    def __repr__short(self, value):
        # denominator - d - mianownik
        # counter - u - licznik

        # init counter and donominator
        u, d = [], []

        # loop over units row in dictonary
        for u_str, u_val in self._units.items():

            u_str = u_str[u_str.rfind('/')+1:]

            # if-block depend on power
            # if power is zero, then pass
            if   u_val==0 : pass

            # if power is one, then expand counter
            elif u_val==1 : u.append(u_str)

            # if power is more than one, then expand counter with "^" symbol
            elif u_val>0 : u.append(u_str+ '^'+str(u_val))

            # if power is one, then expand denominator
            elif u_val==-1: d.append(u_str)

            # if power is less than one, then expand denominator with "^" symbol
            # elif u_val<0  : d += '[' + u_str + '^' + str(-u_val) + ']'
            elif u_val<0  : d.append(u_str+ '^'+ str(-u_val))


        # if-block depend on counter and denominator empty's
        # if all is empty
        if u==[] and d==[]:
            return value + ' [1]'
        elif u==[]:
            return value + ' [1]/' + '[' + ' '.join(d) + ']'
        elif d==[]:
            return value + ' [' + ' '.join(u) + ']'
        else:
            return value + ' [' + ' '.join(u) + ']/[' + ' '.join(d) + ']'



#$$$ ____________ def __repr__python _______________________________________ #

    @staticmethod
    def __repr__python(self, value):
        # denominator - d - mianownik
        # counter - u - licznik

        # init counter and donominator
        u,d = '',''

        # loop over units row in dictonary
        for u_str, u_val in self._units.items():

            u_str = u_str[u_str.rfind('/')+1:]

            # if-block depend on power
            # if power is zero, then pass
            if   u_val==0 : pass

            # if power is one, then expand counter
            elif u_val==1 : u += '*' + u_str

            # if power is more than one, then expand counter with "^" symbol
            elif u_val>0  : u += '*' + u_str + '**' + str(u_val)

            # if power is one, then expand denominator
            elif u_val==-1: d += '*' + u_str

            # if power is less than one, then expand denominator with "^" symbol
            elif u_val<0  : d += '*' + u_str + '**' + str(-u_val)

        # if-block depend on counter and denominator empty's
        # if all is empty
        if u=='' and d=='':
            return value
        elif u=='':
            return value + '*(1)/(' + d[1:] + ')'
        elif d=='':
            return value + '*(' + u[1:] + ')'
        else:
            return value + '*(' + u[1:] + ')/(' + d[1:] + ')'


#$$$ ____________ def __repr__latex ________________________________________ #

    @staticmethod
    def __repr__latex(self, value):
        # denominator - d - mianownik
        # counter - u - licznik

        # init counter and donominator
        u,d = '',''

        # loop over units row in dictonary
        for u_str, u_val in self._units.items():

            u_str = u_str[u_str.rfind('/')+1:]

            u_str = u_str.replace(r'°C',r'^{\circ}C')

            if u_str=='%':
                u_str = r'\%'

            # if-block depend on power
            # if power is zero, then pass
            if   u_val==0 : pass

            # if power is one, then expand counter
            elif u_val==1 : u += r'\,\mathrm{' + u_str + '}'

            # if power is more than one, then expand counter with "^" symbol
            elif u_val>0  : u += r'\,\mathrm{' +u_str + '}^{' + str(u_val) + '}'

            # if power is one, then expand denominator
            elif u_val==-1: d += r'\,\mathrm{' + u_str + '}'

            # if power is less than one, then expand denominator with "^" symbol
            elif u_val<0  : d += r'\,\mathrm{' +u_str + '}^{' + str(-u_val) + '}'

        # u = u.replace(r'\,^',r'^')

        # if-block depend on counter and denominator empty's
        # if all is empty
        if u=='' and d=='':
            return value
        elif u=='':
            return value + r'\,(1)/(' + d[2:] + ')'
        elif d=='':
            return value + u
        else:
            return value + r'\,\cfrac{' + u[2:] + '}{' + d[2:] + '}'



#$$ ________ class crange __________________________________________________ #

    class crange:

        def __init__(self, units=1, val1=None, val2=None, val3=None):
            if type(val1) is unise: val1 = int(val1.d(units))
            if type(val2) is unise: val2 = int(val2.d(units))
            if type(val3) is unise: val3 = int(val3.d(units))

            if type(units) == str:
                # call to convert methods
                units = udict.str2dict(unise, units)

            if val1 is not None and val2 is not None and val3 is not None:
                data = range(val1, val2, val3)
                self.name = f"crange('{units}', {val1}, {val2}, {val3})"
            elif val1 is not None and val2 is not None:
                data = range(val1, val2)
                self.name = f"crange('{units}', {val1}, {val2})"
            elif val1 is not None:
                data = range(val1)
                self.name = f"crange('{units}', {val1})"

            self.value = [unise(val, units) for val in data]

        def __iter__(self):
            return (x for x in self.value)

        def __repr__(self):
            return self.name



#$ ######################################################################### #
