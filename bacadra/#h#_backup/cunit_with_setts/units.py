'''
------------------------------------------------------------------------------
***** bacadra (c)arefree (unit)s package *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ____ import _____________________________________________________________ #

import math

import numpy as np
import sympy as sp

from ..tools.setts import settsmeta

from .ndict import ndict
from . import verrs
from . import nprec


#$ ____ class crange _______________________________________________________ #

class crange:

    #$$ def __init__
    def __init__(self, unit=1, val1=None, val2=None, val3=None):
        if type(val1) is cunit: val1 = int(val1.d(unit))
        if type(val2) is cunit: val2 = int(val2.d(unit))
        if type(val3) is cunit: val3 = int(val3.d(unit))

        if val1 is not None and val2 is not None and val3 is not None:
            data = range(val1, val2, val3)
            self.name = f"crange('{unit}', {val1}, {val2}, {val3})"
        elif val1 is not None and val2 is not None:
            data = range(val1, val2)
            self.name = f"crange('{unit}', {val1}, {val2})"
        elif val1 is not None:
            data = range(val1)
            self.name = f"crange('{unit}', {val1})"

        self.value = [cunit(val, unit) for val in data]

    #$$ def __iter__
    def __iter__(self):
        return (x for x in self.value)

    #$$ def __repr__
    def __repr__(self):
        return self.name





#$ ____ class setts ________________________________________________________ #

class setts(settsmeta):
    __addp__ = {}

#$$ ________ def acc _______________________________________________________ #

    # TODO: add acc type checks, it must be list, not tuple!
    # accuracy of printed value
    acc = [None,None]
    __addp__.update({'acc':acc})

#$$ ________ def eacc ______________________________________________________ #

    # exponent round point
    eacc = 5
    __addp__.update({'eacc':eacc})

#$$ ________ def style _____________________________________________________ #

    # print style, style of print
    style = 'pretty'
    __addp__.update({'style':style})

#$$ ________ def trail _____________________________________________________ #

    # trailing zero print's flag (True|False)
    trail = False
    __addp__.update({'trail':trail})

#$$ ________ def nnot ______________________________________________________ #

    # number notations (a|f|e|E)
    nnot = 'f'
    __addp__.update({'nnot':nnot})


#$$ ________ def system ____________________________________________________ #

    __system = None
    base = None

    @property
    def system(self): return self.__system

    @system.setter
    def system(self, value):

        # if 'base_'+value in self.__dict__:
            self.base = getattr(self, 'base_'+value)
            self.__system = value
        # else:
            # raise verrs.BCDR_cunit_Error_System_Exists(value)


#$$ ________ system base_ce ________________________________________________ #

    # system definition
    # the system atribute type must be dictonary. Inside them we need include the fallowing type:
    # {'<name>' : (<numerical object with value>,
    #              <dictonary object with unit def>)}
    # if unit should be base unit, then just type {'<name>':(None)}

    # system SI
    base_si = {

        # base units
        'm'          : (None                                       ),
        'kg'         : (None                                       ),
        's'          : (None                                       ),
        'K'          : (None                                       ),

        # deriative units
        '%'          : (0.01,          {}                          ),
        'rad'        : (1,             {}                          ),
        'mrad'       : (0.001,         {}                          ),
        'deg'        : (math.pi/180,   {}                          ),
        '°'          : (math.pi/180,   {}                          ),
        '°C'         : (1,             {'K':1}                     ),
        'Hz'         : (1,             {'s':-1}                    ),
        't'          : (1000,          {'kg':1}                    ),
        'cm'         : (0.01,          {'m':1}                     ),
        'mm'         : (0.001,         {'m':1}                     ),
        'km'         : (1000,          {'m':1}                     ),
        'dm'         : (0.1,           {'m':1}                     ),
        'N'          : (1,             {'kg':1, 'm':1,  's':-2}    ),
        'kN'         : (10**3,         {'kg':1, 'm':1,  's':-2}    ),
        'MN'         : (10**6,         {'kg':1, 'm':1,  's':-2}    ),
        'GN'         : (10**9,         {'kg':1, 'm':1,  's':-2}    ),
        'Pa'         : (1,             {'kg':1, 'm':-1, 's':-2}    ),
        'kPa'        : (10**3,         {'kg':1, 'm':-1, 's':-2}    ),
        'MPa'        : (10**6,         {'kg':1, 'm':-1, 's':-2}    ),
        'GPa'        : (10**9,         {'kg':1, 'm':-1, 's':-2}    ),
        'yr'         : (60*60*24*365,  {'s':1}                     ),
        'day'        : (60*60*24,      {'s':1}                     ),
        'hr'         : (60*60,         {'s':1}                     ),
        'min'        : (60,            {'s':1}                     ),

        # shortcuts
        'Length'     : (1,             {'m':1 }                    ),
        'Mass'       : (1,             {'kg':1}                    ),
        'Time'       : (1,             {'s':1}                     ),
        'Temperature': (1,             {'K':1}                     ),
        'Force'      : (1,             {'kg':1, 'm':1,  's':-2}    ),
        'Pressure'   : (1,             {'kg':1, 'm':-1, 's':-2}    ),
    }



#$$ ________ system base_ce ________________________________________________ #


    # system Civil Engineering
    base_ce = {

        # translate si_base_units to self_base_units
        'si->me:m'   : (None                                       ),
        'si->me:kg'  : (0.001,         {'kN':1, 'm':-1, 's':2}     ),
        'si->me:s'   : (None                                       ),
        'si->me:K'   : (1,             {'°C':1}                    ),

        # translate self_base_units to si_base_units
        'me->si:kN'  : (1,             {'kN':1}                    ),
        'me->si:m'   : (1,             {'m':1}                     ),
        'me->si:°C'  : (1,             {'°C':1}                    ),
        'me->si:s'   : (1,             {'s':1}                     ),

        # base units
        'kN'         : (None                                       ),
        'm'          : (None                                       ),
        '°C'         : (None                                       ),
        's'          : (None                                       ),

        # deriative units
        '%'          : (0.01,          {}                          ),
        'rad'        : (1,             {}                          ),
        'mrad'       : (0.001,         {}                          ),
        'deg'        : (math.pi/180,   {}                          ),
        '°'          : (math.pi/180,   {}                          ),
        'Hz'         : (1,             {'s':-1}                    ),
        'kg'         : (0.001,         {'kN':1, 'm':-1, 's':2}     ),
        't'          : (10,            {'kN':1}                    ),
        'K'          : (1,             {'°C':1}                    ),
        'km'         : (1000,          {'m':1}                     ),
        'dm'         : (0.1,           {'m':1}                     ),
        'cm'         : (0.01,          {'m':1}                     ),
        'mm'         : (0.001,         {'m':1}                     ),
        'GN'         : (1000000,       {'kN':1}                    ),
        'MN'         : (1000,          {'kN':1}                    ),
        'N'          : (0.001,         {'kN':1}                    ),
        'yr'         : (60*60*24*365,  {'s':1}                     ),
        'day'        : (60*60*24,      {'s':1}                     ),
        'hr'         : (60*60,         {'s':1}                     ),
        'min'        : (60,            {'s':1}                     ),
        'GPa'        : (1000000,       {'m':-2, 'kN':1}            ),
        'MPa'        : (1000,          {'m':-2, 'kN':1}            ),
        'kPa'        : (1,             {'m':-2, 'kN':1}            ),
        'Pa'         : (0.001,         {'m':-2, 'kN':1}            ),
    }


#$$ ________ system base_ci ________________________________________________ #


    # TODO: good idea, extend system by other one

    # # small system to test simplier method of base untis definition
    # base_ci = {
    #     # translate si_base_units to self_base_units
    #     'si->me:m'   : (None),
    #     'si->me:kg'  : (0.001,         {'kN':1, 'm':-1, 's':2}     ),
    #     'si->me:s'   : (None),
    #     'si->me:K'   : (1,             {'°C':1}                    ),
    #
    #     # translate self_base_units to si_base_units
    #     'me->si:kN'  : (1,             {'kN':1}                    ),
    #     'me->si:m'   : (1,             {'m':1}                     ),
    #     'me->si:°C'  : (1,             {'°C':1}                    ),
    #     'me->si:s'   : (1,             {'s':1}                     ),
    #
    #     # base units
    #     'kN'         : (None                                       ),
    #     'm'          : (None                                       ),
    #     '°C'         : (None                                       ),
    #     's'          : (None                                       ),
    # }

#$$ ________ def create_system _____________________________________________ #

    # def create_system(self, name={}):
        # eval('self.setts.base_'+name+'='+str(name))


#$ ____ class cunit ________________________________________________________ #

class cunit:

    # class setts
    setts = setts('setts', (setts,), {})


#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, value=1, units=None, system=None):
        '''
        Called class return cunit object. It have two arguments: value and units. The value can be numeric type data, while units accept only dictonary and string.
        '''

        # if value's type is string, then try to get unit definition from base_{x}.
        if type(value)==str and units==None:
            self._get(value)

        # else set up atributes for value and units as user input
        else:
            # !!!remember!!!
            # do not check here if units exists in system.setts.base
            # 1. time, 2. convinient, 3. if you want create in place variable use cc methods

            # if user input units as string, then convert it to dictonary type
            if type(units) == str:
                # call to convert methods
                units = ndict.str2dict(units)

            self._value = value
            self._units = units

        self._system = cunit.setts.system if system is None else system


    # dziala w porzadku, ale jakos mega spowalania prace...
    # zeby dzialalo to trzeba dodac pretypowanie na poczatku inita

    # #$$ def __setattr__
    # def __setattr__(self, name, value):
    #     '''
    #     Method do not allow create new variable in class. It is provide more control over user correctly or simply spell-checker.
    #     '''
    #
    #     if not hasattr(self, name) and inspect.stack()[1][3] != '__init__':
    #         raise AttributeError(f"Creating new attributes <{name}> is not allowed!")
    #
    #     object.__setattr__(self, name, value)


    @classmethod
    def cc(self, value, units):
        '''
        Create cunit in place without convert it. It also check if all key in units exists in base attribute.

        If it often used in texme math methods, wher variable is not defined in python system, but should be printed in report.
        eg. texme.m('a=@cc(15, "MPa")@'))
        '''

        if type(units) == str:
            # call to convert methods
            units = ndict.str2dict(units)

        for key,val in units.items():
            if not key in cunit.setts.base:
                verrs.BCDR_cunit_Error_Units_in_System(cunit.setts.system, units)

        return cunit(value, units)


#$$ ________ def _get ______________________________________________________ #

    def _get(self, units):
        '''
        User input units as string type. This must be checked explicit, link in __init__(...). The set up _value and _units as copy from system definition if it exists, else return CunitSystemError.
        This method must set up _value and _units or raise error!
        '''
        try:
        # get value and unit from system defintion
            base_value = cunit.setts.base[units]

            # if returned was base unit (value is equal to None), then prepare object value and unit by hand
            if base_value == None:
                self._value = 1
                self._units = {units:1}
            # else get value and unit
            else:
                self._value = base_value[0]
                self._units = base_value[1]

        # if unit does not exist in base system, then raise error
        except:
            verrs.BCDR_cunit_Error_Units_in_System(cunit.setts.system, units)


#$$ ________ def add _______________________________________________________ #

    @staticmethod
    def add(name, value, units, overwrite=False):
        '''
        Add child unit to current system. Current system can be check under self.setts.system atribute. As input method want:
        - name - new name of unit, like "m" or "kN",
        - value - multiply number,
        - units - dictonary with basic unit, basic and only basic!
        If overwrite is True, then if definition of unit alredy exists, then it will be overwriten! If overwrite is False, if same case method return errror.
        '''

        # check overwrite flag
        if (not overwrite) and (name in cunit.setts.base):

            # if flag if False and name alredy exists, then raise error
            verrs.BCDR_cunit_Error_Already_Exists(cunit.setts.system, name)

        # extend base dict
        cunit.setts.base.update({name:(value, units)})

        # retur cunit object
        return cunit(name)


#$$ ________ def rem _______________________________________________________ #

    @staticmethod
    def rem(name, silent=True):
        '''
        Delete unit from current system. If silent is True, then no error occur if name not occur in self.setts.base too.
        '''

        # first check if name is exists in self.setts.base
        if name in cunit.setts.base:

            # the fastest method of delete key is del statment
            del cunit.setts.base[name]

        # if not exists, then check silent flag
        elif not silent:

            # if silent if False, then raise error
            verrs.BCDR_cunit_Error_Units_in_System(cunit.setts.system, name)


#$$ ________ def primary ___________________________________________________ #

    def primary(self, system=None, check_system=True, inplace=False, key_prefix=''):
        '''
        Convert unit to current base system. Method loop over _units and convert each row to base line. Method reutnr new one units and does not convert old!

        system can be input as None (get current system) or string (get one of alredy defined systems).

        check_system can be turned off, then unit are not converted automaticly to new system.

        inplace flags can be change to True, then variable itself will be changed

        key_prefix is needed only to system changes.
        '''

        # if user do not input system, then get default
        if system is None: system = cunit.setts.system

        # if current system of variable is diffrent than specyfied system and check_system flags is True, then go and convert unit
        if (self._system != system) and check_system:

            # if old system is other than si
            # then go and first convert it to si
            if self._system != 'si':

                # convert self to primary units in old system
                self.primary(
                    system       = self._system,
                    check_system = False,
                    inplace      = True,
                    key_prefix   = '',
                )

                # now convert self to new system
                self.primary(
                    system       = self._system,
                    check_system = False,
                    inplace      = True,
                    key_prefix   = 'me->si:',
                )

                # change self system variable
                self._system = 'si'

                # just use self primary to full convert variable
                self.primary(
                    system       = self._system,
                    check_system = False,
                    inplace      = True,
                    key_prefix   = '',
                )

                # now the variable is full ready in si system

            # if new system is other than si, then convert it
            # please notice, that variable must be already in si system
            if system != 'si':


                # convert self to primary units in old system
                self.primary(
                    system       = self._system,
                    check_system = False,
                    inplace      = True,
                    key_prefix   = '',
                )


                # now convert self to new system
                self.primary(
                    system       = system,
                    check_system = False,
                    inplace      = True,
                    key_prefix   = 'si->me:',
                )


                # change self system variable
                self._system = system

                # just use self primary to full convert variable
                self.primary(
                    system       = self._system,
                    check_system = False,
                    inplace      = True,
                    key_prefix   = '',
                )


        # then get one of already exists system
        base = eval('self.setts.base_'+system)

        # get value
        cval  = self._value

        if cval == 0:
            return cunit(cval, {})

        # copy unit dictonary
        cdict = self._units.copy()

        # loop over keys in unit dictonary
        for key,val in self._units.items():

            # TODO: good idea, extend system by other one
            # # get base key, extend base by si system
            # if key_prefix+key in base:
            #     base_value = base[key_prefix+key]
            # elif key_prefix+key in self.setts.base_si:
            #     base_value = self.setts.base_si[key_prefix+key]
            # else:
            #     raise ValueError('Unit does not find:',key_prefix+key)

            # get base key
            base_value = base[key_prefix+key]

            # if unit is not primary then convert it to primary
            if base_value:

                # multiply value by unit value
                cval *= base_value[0] ** val

                # delete key from dictonary
                cdict.pop(key, None)

                # sum unit's power, which need to consider actual power
                cdict = ndict.dsum(cdict, ndict.vmul(base_value[1], val))

        # convert self inplace
        if inplace:
            self._value = cval
            self._units = cdict

        # return new cunit, does not convert old!
        else:
            return cunit(cval, cdict, system=self._system)
    p = primary




#$$ ________ def convert ___________________________________________________ #

    def convert(self, units, fcover=False, post=True, inplace=False):
        '''
        Convert unit to other one. Convert is not in-place method!. If fcover flags is True, then units must cover in all current _units. New units can be input as dict, as string or as cunit. Be aware! if you have units "MPa" it is high risk that is defined by base value, so the convert will not work then!
        '''

        # check type of new units
        # if is typed as string then convert string to dict
        if type(units) == str:
            units = ndict.str2dict(txt=units, othe=self)
        # if it is type as cunit then get _units from them
        elif type(units) == cunit:
            units = units._units

        # divide value
        # this is best work, because if divide mechanism is already define for lots types, then convert work too.
        val = self/cunit(1, units)

        # if fcover flag is types as True
        if fcover:
            # if result of divide is not empty unit then raise error
            if val._units != {}:

                # prepare val for better print error
                val = cunit(1, val._units)

                # raise error
                verrs.BCDR_cunit_Error_Cover(val)


        # check inplace flag
        if inplace:
            self._value = val._value
            self._units = ndict.dsum(units, val._units)
            return self

        else:
            # if anythink is ok then return NEW cunit
            return cunit(val._value, ndict.dsum(units, val._units))
    c = convert


#$$ ________ def drop ______________________________________________________ #

    def drop(self, units=None, fcover=True, system=None):
        '''
        Drop unit and return value alone. If dropped pattern unit is not explicit defined, then drop as system base. Is system is not explicited defined then use current system.
        '''

        # if units is defined explicity
        # so if it is typed as string
        if type(units) == str:
            # then convert string to dictonary
            units = ndict.str2dict(units)

        # else is not defined
        elif units==None:
            # get primary unit and extract _units from it
            units = self.primary(system=system)._units

        # divide by new unit - its convert value in good way
        # val = self/(cunit(1, units)).primary(system=system)
        val = self/cunit(1, units)

        #
        if fcover:
            if len(val._units) != 0:
                verrs.BCDR_cunit_Error_Cover(str(val._units))

        return val._value
    d = drop


#$$ ________ def drop_external _____________________________________________ #

    @staticmethod
    def drop_external(self, units=None):

        if type(self) in [list, np.ndarray]:
            return [cunit.drop_external(obj, units) for obj in self]

        elif type(self) is cunit:
            return cunit.drop(self, units)

        else:
            return self
    de = drop_external



#$$ ________ def copy ______________________________________________________ #

    def copy(self):
        '''
        Return copy of self. Needed in show function etc.
        '''
        return cunit(self._value, self._units)


#$$ ________ def edit ______________________________________________________ #

    # def edit(self, units=None, acc=None, style=None, fcover=False, post=True, trail=None, nnot=None):
    #     '''
    #     Change self in-place like acc, style or units.
    #     '''
    #     if units: self.convert(
    #         units=units, fcover=fcover, inplace=True)
    #     if acc  : self.setts.acc   = acc
    #     if style: self.setts.style = style
    #     if trail: self.setts.trail = trail
    #     if nnot : self.setts.nnot  = nnot
    #     return self

    def edit(self, **kwargs):
        self.show(inplace=True, **kwargs)

    e = edit

#$$ ________ def show ______________________________________________________ #

    def show(self,
        # log names
        units=None, acc=None, style=None, fcover=False, trail=None, nnot=None, system=None,

        # short names
        u=None, a=None, ad=None, ai=None, s=None, f=None, t=None, n=None,

        inplace=False):
        '''
        Change self only to print, like acc, style or units.
        units  - print as new units, it must be valid in current system
        acc    - accuracy of results cunit, [0]- decimal, [1]- precision
        style  - style of printed results
        fcover - new units must full replace old one,
        trail  - show trailing zero
        nnot   - notations of value in printed results
        '''

        try:
            if system:
                _system_old = cunit.setts.system
                cunit.setts.system = system
                # print(self.setts.base)

            # convert short name to long name
            if u  and not units : units  = u
            if a  and not acc   : acc    = a
            if (acc is None) and ((ad is not None) or (ai is not None)):
                acc = [None, None]
                if ad is not None: acc[0] = ad
                if ai is not None: acc[1] = ai
            if s  and not style : style  = s
            if f  and not fcover: fcover = f
            if t  and not trail : trail  = t
            if n  and not nnot  : nnot   = n

            # create copy of self
            if inplace:
                othe = self
            else:
                othe = self.copy()

            if system: othe.primary(
                system=system,
                inplace=True,
            )

            # convert units and fcover checks
            if units: othe.convert(
                units=units, fcover=fcover, inplace=True)

            # change acc
            if acc  : othe.setts.acc   = acc

            # change style
            if style: othe.setts.style = style

            # change trail settings
            if trail: othe.setts.trail = trail

            # change notations settings
            if nnot : othe.setts.nnot  = nnot

        finally:
            if system:
                cunit.setts.system = _system_old

        return othe
    s = show


#$$ ________ def __call__ __________________________________________________ #

    __call__ = show


#$$ ________ def show-external _____________________________________________ #

    @staticmethod
    def show_external(self, units=None, acc=None, style=None, fcover=False, trail=None, nnot=None):

        if type(self) in [list, np.ndarray]:
            return [cunit.show_external(obj, units, acc, style, fcover, trail, nnot) for obj in self]

        elif type(self) is cunit:
            return cunit.show(self, units, acc, style, fcover, trail, nnot)

        else:
            return self
    se = show_external


#$$ ________ def units _____________________________________________________ #

    def units(self):
        '''
        Return cunit with actual units and value equal to 1.
        '''

        return cunit(1, self._units)
    u = units

#$$ ________ def range _____________________________________________________ #

    @staticmethod
    def range(unit={}, val1=None, val2=None, val3=None):
        return crange(unit=unit, val1=val1, val2=val2, val3=val3)
    crange = crange

#$$ ________ magic behaviour _______________________________________________ #
#$$$ ____________ def __add__ / __radd__ / __iadd__ / __pos__ ______________ #

    def __add__(self, othe):
        '''
        Python Magic Method: self + othe
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # now if-block of data type
        # if second variable is also cunit
        if othe_type == cunit:
            # then primary units self and othe
            s = self.primary()
            o = othe.primary()

            # below if-block is neccesary, because we want that 0*m**3 + 0*kN shoud work correctly. fix-zero value
            if s._value == 0: return o
            if o._value == 0: return s

            # check compability
            verrs.BCDR_cunit_Error_Incompatible(s, o, '__(ri)add__')

            # return new instant of cunit, get s or o units, they are the same
            return cunit(s._value + o._value, s._units)

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
            return cunit(val + othe, {})

        # else raise error
        else:
            verrs.BCDR_cunit_Error_Undefined_Operator('__add__', self, othe)


    def __radd__(self, othe):
        '''
        Python Magic Method: othe + self
        '''
        return self.__add__(othe)


    def __iadd__(self, othe):
        '''
        Python Magic Method: self += othe
        '''
        return self.__add__(othe)


    def __pos__(self):
        '''
        Python Magic Method: +self
        '''
        return self


#$$$ ____________ def __sub__ / __rsub__ / __isub__ / __neg__ ______________ #

    def __sub__(self, othe):
        '''
        Python Magic Method: self - othe
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # now if-block of data type
        # if second variable is also cunit
        if othe_type == cunit:
            # then primary units self and othe
            s = self.primary()
            o = othe.primary()

            # below if-block is neccesary, because we want that 0*m**3 + 0*kN shoud work correctly. fix-zero value
            if s._value == 0: return -o
            if o._value == 0: return s

            # check compability
            verrs.BCDR_cunit_Error_Incompatible(s, o, '__sub__')

            # return new instant of cunit, get s or o units, they are the same
            return cunit(s._value - o._value, s._units)

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
            return cunit(val - othe, {})

        # else raise error
        else:
            verrs.BCDR_cunit_Error_Undefined_Operator('__sub__', self, othe)


    def __rsub__(self, othe):
        '''
        Python Magic Method: othe - self
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # now if-block of data type
        # if second variable is also cunit
        if othe_type == cunit:
            # then primary units self and othe
            s = self.primary()
            o = othe.primary()

            # below if-block is neccesary, because we want that 0*m**3 + 0*kN shoud work correctly. fix-zero value
            if s._value == 0: return o
            if o._value == 0: return -s

            # check compability
            verrs.BCDR_cunit_Error_Incompatible(s, o, '__rsub__')

            # return new instant of cunit, get s or o units, they are the same
            return cunit(o._value - s._value, s._units)

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
            return cunit(othe - val, {})

        # else raise error
        else:
            verrs.BCDR_cunit_Error_Undefined_Operator('__rsub__', self, othe)


    def __isub__(self, othe):
        '''
        Python Magic Method: self -= othe
        '''
        return self.__sub__(othe)


    def __neg__(self):
        '''
        Python Magic Method: -self
        '''
        return cunit(-self._value, self._units)


    # def __invert__(self):
    #     '''
    #     Python Magic Method: ~self
    #     '''
    #     return cunit(self._value**(-1), ndict.dsub({},self._units))



#$$$ ____________ def __pow__ / __rpow__ / __ipow__ ________________________ #

    def __pow__(self, othe):
        '''
        Python Magic Method: self**othe
        '''

        # if type othe is cunit withou unit, then convert it to number data
        if type(othe) == cunit and othe._units == {}:
            othe = othe._value

        # convert self to primary unit
        s = self.primary()

        # return powered cunit
        return cunit(s._value**othe, ndict.vmul(s._units, othe))


    def __rpow__(self, othe):
        '''
        Python Magic Method: othe**self
        '''

        # if self._units is not empty, then exception must occur, the cunit in power zone is not implemented and probably will not be
        if self._units != {}:
            verrs.BCDR_cunit_Error_General('Power cunit type is not implemented')

        # but if _units is empty, then i can treat it as clean self._value and return result
        # if othe will be cunit, then by recurency __pow__ will start
        return othe ** self._value


    def __ipow__(self, othe):
        '''
        Python Magic Method: self **= othe
        '''
        return self.__pow__(othe)


#$$$ ____________ def __mul__ / __rmul__ / __imul__ ________________________ #

    def __mul__(self, othe):
        '''
        Python Magic Method: self * othe
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # now if-block of data type
        # if second variable is also cunit
        if othe_type == cunit:
            if self._value == 0 or othe._value == 0:
                return cunit(0, {})

            # then primary units self and othe
            # note: we do not need to check compability units, we can multiply any two units
            s = self.primary()
            o = othe.primary()

            # return new cunit, with multipled value and summed units
            return cunit(s._value * o._value, ndict.dsum(s._units, o._units))

        # if second variable is given as list, so we want add variable to list or list to variable (we want 2-dir the same method)
        elif othe_type == list:
            # loop over all value in list and call recurive
            return [self.__mul__(val) for val in othe]

        # if second variable is numpy array, again, loop over
        elif othe_type == np.ndarray:
            return np.array([self.__mul__(val) for val in othe])

        # else just try to multiply value with othe and pase units
        else:
            return cunit(self._value * othe, self._units)


    def __rmul__(self, othe):
        '''
        Python Magic Method: othe * self
        '''
        return self.__mul__(othe)


    def __imul__(self, othe):
        '''
        Python Magic Method: self *= othe
        '''
        return self.__mul__(othe)



#$$$ ____________ def __truediv__ / __rtruediv__ / __itruediv__ ____________ #

    def __truediv__(self, othe):
        '''
        Python Magic Method: self / othe
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # now if-block of data type
        # if second variable is also cunit
        if othe_type == cunit:
            if self._value == 0:
                return cunit(0, {})

            # then primary units self and othe
            # note: we do not need to check compability units, we can multiply any two units
            s = self.primary()
            o = othe.primary()

            # return new cunit, with multipled value and summed units
            return cunit(s._value / o._value, ndict.dsub(s._units, o._units))

        # if second variable is given as list, so we want add variable to list or list to variable (we want 2-dir the same method)
        elif othe_type == list:
            # loop over all value in list and call recurive
            return [self.__truediv__(val) for val in othe]

        # if second variable is numpy array, again, loop over
        elif othe_type == np.ndarray:
            return np.array([self.__truediv__(val) for val in othe])

        # else just try to multiply value with othe and pase units
        else:
            return cunit(self._value / othe, self._units)


    def __rtruediv__(self, othe):
        '''
        Python Magic Method: othe / self
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # now if-block of data type
        # if second variable is also cunit
        if othe_type == cunit:
            if othe._value == 0:
                return cunit(0, {})

            # then primary units self and othe
            # note: we do not need to check compability units, we can multiply any two units
            s = self.primary()
            o = othe.primary()

            # return new cunit, with multipled value and summed units
            return cunit(o._value / s._value, ndict.dsub(o._units, s._units))

        # if second variable is given as list, so we want add variable to list or list to variable (we want 2-dir the same method)
        elif othe_type == list:
            # loop over all value in list and call recurive
            return [self.__rtruediv__(val) for val in othe]

        # if second variable is numpy array, again, loop over
        elif othe_type == np.ndarray:
            return np.array([self.__rtruediv__(val) for val in othe])

        # else just try to multiply value with othe and pase units
        else:
            return cunit(othe / self._value, ndict.vmul(self._units, -1))


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
        return cunit(round(self._value, acc), self._units)

#$$$ ____________ def __ceil__ _____________________________________________ #

    def __ceil__(self):
        '''
        Python function: ceil(self)
        '''
        return cunit(math.ceil(self._value), self._units)

#$$$ ____________ def __trunc__ ____________________________________________ #

    def __trunc__(self):
        '''
        Python function: trunc(self)
        '''
        return cunit(math.trunc(self._value), self._units)

#$$$ ____________ def __nstyle__ ___________________________________________ #

    def __nstyle__(self):
        '''
        Prepare numeric type data to print it.
        '''

        # save self value
        value = self._value

        # if self value type is numeric type then round and sign value
        if type(value) in [int, float, np.float64, sp.Expr]:

            value = nprec.to_precision(
                value       = value,
                nround      = self.setts.acc[0],
                precision   = self.setts.acc[1],
                notation    = self.setts.nnot,
                strip_zeros = not self.setts.trail,
            )

            for key,val in self._units.items():
                self._units[key] = round(val, self.setts.eacc)

        else:
            value = str(value)


        # return new units, with acc deci and prec
        return cunit(value, self._units)



#$$$ ____________ def __repr__ _____________________________________________ #

    def __repr__(self):
        '''
        Representation of cunit. The methods provide few styles.
        '''

        # prepare numeric data
        new = self.__nstyle__()

        # convert style to lowercase
        style = self.setts.style.lower()

        # if-block depend on presentation style
        if   style == 'pretty': return self.__repr__pretty(new)
        elif style == 'python': return self.__repr__python(new)
        elif style == 'latex' : return self.__repr__latex(new)


    @staticmethod
    def __repr__pretty(self):
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
            elif u_val>0  : u += '[' + u_str + '^' + str(u_val)  + ']'

            # if power is one, then expand denominator
            elif u_val==-1: d += '[' + u_str + ']'

            # if power is less than one, then expand denominator with "^" symbol
            elif u_val<0  : d += '[' + u_str + '^' + str(-u_val) + ']'

        # convert self value to string
        val = self._value

        # if-block depend on counter and denominator empty's
        # if all is empty
        if u=='' and d=='':
            return val + ' [1]'
        elif u=='':
            return val + ' [1]/' + d
        elif d=='':
            return val + ' ' + u
        else:
            return val + ' ' + u + '/' + d



    @staticmethod
    def __repr__python(self):
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

        # convert self value to string
        val = self._value

        # if-block depend on counter and denominator empty's
        # if all is empty
        if u=='' and d=='':
            return val
        elif u=='':
            return val + '*(1)/(' + d[1:] + ')'
        elif d=='':
            return val + '*(' + u[1:] + ')'
        else:
            return val + '*(' + u[1:] + ')/(' + d[1:] + ')'



    @staticmethod
    def __repr__latex(self):
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

        # convert self value to string
        val = self._value

        # if-block depend on counter and denominator empty's
        # if all is empty
        if u=='' and d=='':
            return val
        elif u=='':
            return val + r'\,(1)/(' + d[2:] + ')'
        elif d=='':
            return val + u
        else:
            return val + r'\,\cfrac{' + u[2:] + '}{' + d[2:] + '}'




#$$$ ____________ def __lt__ / __le__ ______________________________________ #

    def __lt__(self, othe):
        '''
        Python Magic Method: self < othe
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # now if-block of data type
        # if second variable is also cunit
        if othe_type == cunit:
            if othe._value == 0 or self._value == 0:
                return self._value < othe._value

            # then primary units self and othe
            s = self.primary()
            o = othe.primary()

            # check compability
            verrs.BCDR_cunit_Error_Incompatible(s, o, '__lt__')

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
            verrs.BCDR_cunit_Error_Undefined_Operator('__lt__', self, othe)




    def __le__(self, othe):
        '''
        Python Magic Method: self <= othe
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # now if-block of data type
        # if second variable is also cunit
        if othe_type == cunit:
            if othe._value == 0 or self._value == 0:
                return self._value <= othe._value

            # then primary units self and othe
            s = self.primary()
            o = othe.primary()

            # check compability
            verrs.BCDR_cunit_Error_Incompatible(s, o, '__le__')

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
            verrs.BCDR_cunit_Error_Undefined_Operator('__le__', self, othe)


#$$$ ____________ def __gt__ / __ge__ ______________________________________ #

    def __gt__(self, othe):
        '''
        Python Magic Method: self > othe
        '''
        return cunit.__lt__(-self,-othe)


    def __ge__(self, othe):
        '''
        Python Magic Method: self >= othe
        '''
        return cunit.__le__(-self,-othe)


#$$$ ____________ def __eq__ / __ne__ ______________________________________ #

    def __eq__(self, othe):
        '''
        Python Magic Method: self == othe
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # now if-block of data type
        # if second variable is also cunit
        if othe_type == cunit:
            if othe._value == 0 or self._value == 0:
                return self._value == othe._value

            # then primary units self and othe
            s = self.primary()
            o = othe.primary()

            # check compability
            verrs.BCDR_cunit_Error_Incompatible(s, o, '__eq__')

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

        # else raise error
        else:
            verrs.BCDR_cunit_Error_Undefined_Operator('__eq__', self, othe)




    def __ne__(self, othe):
        '''
        Python Magic Method: self != othe
        '''

        # save othe type as hard variable
        othe_type = type(othe)

        # now if-block of data type
        # if second variable is also cunit
        if othe_type == cunit:
            if othe._value == 0 or self._value == 0:
                return self._value != othe._value

            # then primary units self and othe
            s = self.primary()
            o = othe.primary()

            # check compability
            verrs.BCDR_cunit_Error_Incompatible(s, o, '__ne__')

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

        # else raise error
        else:
            verrs.BCDR_cunit_Error_Undefined_Operator('__ne__', self, othe)



#$$$ ____________ def __is__ / is-not ______________________________________ #

    def __is__(self, othe):
        '''
        Python Magic Method: self is othe
        '''
        return self.__eq__(self, othe)


    def is_not(self, othe):
        '''
        Python Magic Method: self is not othe
        '''
        return self.__ne__(self, othe)

#$$$ ____________ def __and__ / __rand__ ___________________________________ #

    def __and__(self, othe):
        '''
        Python Magic Method: self and othe
        '''
        if bool(self._value) and othe:
            return True
        else:
            return False


    def __rand__(self, othe):
        '''
        Python Magic Method: othe and self
        '''
        return self.__and__(self, othe)


#$$$ ____________ def __xor__ / __rxor__ ___________________________________ #


    def __xor__(self, othe):
        '''
        Python Magic Method: self or othe
        '''
        if bool(self._value) or othe:
            return True
        else:
            return False


    def __rxor__(self, othe):
        '''
        Python Magic Method: othe or self
        '''
        return self.__xor__(self, othe)


#$$$ ____________ def __abs__ / __mod__ ____________________________________ #

    def __abs__(self):
        '''
        Python function: abs(self)
        '''
        return cunit(abs(self._value), self._units)

    def __mod__(self, val):
        '''
        Python function: mod(self)
        '''
        return cunit(self._value % val, self._units)


#$$$ ____________ def __float__ / __int__ __________________________________ #

    def __float__(self):
        '''
        Python function: float(self)
        '''
        return float(self._value)


    def __int__(self):
        '''
        Python function: int(self)
        '''
        return int(self._value)


#$$$ ____________ def __bool__ _____________________________________________ #

    def __bool__(self):
        return bool(self._value)

