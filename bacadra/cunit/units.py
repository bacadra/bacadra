#!/usr/bin/python
#-*-coding: UTF-8-*-
#$ ____ import _____________________________________________________________ #

import math

import numpy as np
import sympy as sp

from .ndict import ndict

from . import verrs
from . import nprec

#$ ____ metaclass cunitmeta ________________________________________________ #

class cunitmeta(type):

#$$ ________ def system ____________________________________________________ #

    @property
    def system(cls):
        return cls._system

    @system.setter
    def system(cls, value):
        cls.base = eval('cls.base_'+value)
        cls._system = value

#$$ ________ def create-system _____________________________________________ #

    def create_system(cls, name={}):
        eval('cls.base_'+name+'='+str(name))

#$ ____ class crange _______________________________________________________ #

class crange:

    #$$ def __init__
    def __init__(self, unit=1, val1=None, val2=None, val3=None):
        if type(val1) is cunit: val1 = int(val1.d(unit))
        if type(val2) is cunit: val2 = int(val2.d(unit))
        if type(val3) is cunit: val3 = int(val3.d(unit))

        if val1 is not None and val2 is not None and val3 is not None:
            data = range(val1, val2, val3)
        elif val1 is not None and val2 is not None:
            data = range(val1, val2)
        elif val1 is not None:
            data = range(val1)

        self.value = [cunit(val, unit) for val in data]

    #$$ def __iter__
    def __iter__(self):
        return (x for x in self.value)


#$ ____ class cunit ________________________________________________________ #

class cunit(object, metaclass=cunitmeta):

    # accuracy of printed value
    acc = (None,None)

    # exponent round point
    eacc = 5

    # print style, style of print
    style = 'pretty'

    # trailing zero print's flag (True|False)
    trail = False

    # number notations (a|f|e|E)
    nnot = 'f'

    # system definition
    # the system atribute type must be dictonary. Inside them we need include the fallowing type:
    # {'<name>' : (<numerical object with value>,
    #              <dictonary object with unit def>)}
    # if unit should be base unit, then just type {'<name>':(None)}

    # system SI
    base_si = {
        'm'   : (None                                       ),
        'kg'  : (None                                       ),
        's'   : (None                                       ),
        'K'   : (None                                       ),
        's'   : (None                                       ),
        '%'   : (0.01,          {}                          ),
        'rad' : (1,             {}                          ),
        'mrad': (0.001,         {}                          ),
        'deg' : (math.pi/180,   {}                          ),
        '°'   : (math.pi/180,   {}                          ),
        '°C'  : (1,             {'K':1}                     ),
        'Hz'  : (1,             {'s':-1}                    ),
        't'   : (1000,          {'kg':1}                    ),
        'cm'  : (0.01,          {'m':1}                     ),
        'mm'  : (0.001,         {'m':1}                     ),
        'km'  : (1000,          {'m':1}                     ),
        'dm'  : (0.1,           {'m':1}                     ),
        'N'   : (1,             {'kg':1, 'm':1,  's':-2}    ),
        'kN'  : (10**3,         {'kg':1, 'm':1,  's':-2}    ),
        'MN'  : (10**6,         {'kg':1, 'm':1,  's':-2}    ),
        'GN'  : (10**9,         {'kg':1, 'm':1,  's':-2}    ),
        'Pa'  : (1,             {'kg':1, 'm':-1, 's':-2}    ),
        'kPa' : (10**3,         {'kg':1, 'm':-1, 's':-2}    ),
        'MPa' : (10**6,         {'kg':1, 'm':-1, 's':-2}    ),
        'GPa' : (10**9,         {'kg':1, 'm':-1, 's':-2}    ),
        'yr'  : (60*60*24*365,  {'s':1}                     ),
        'day' : (60*60*24,      {'s':1}                     ),
        'hr'  : (60*60,         {'s':1}                     ),
        'min' : (60,            {'s':1}                     ),
    }

    # system Civil Engineering
    base_ce = {
        'kN'  : (None                                       ),
        'm'   : (None                                       ),
        '°C'  : (None                                       ),
        's'   : (None                                       ),
        '%'   : (0.01,          {}                          ),
        'rad' : (1,             {}                          ),
        'mrad': (0.001,         {}                          ),
        'deg' : (math.pi/180,   {}                          ),
        '°'   : (math.pi/180,   {}                          ),
        'Hz'  : (1,             {'s':-1}                    ),
        'kg'  : (0.001,         {'kN':1, 'm':-1, 's':2}     ),
        't'   : (10,            {'kN':1}                    ),
        'K'   : (1,             {'°C':1}                    ),
        'km'  : (1000,          {'m':1}                     ),
        'dm'  : (0.1,           {'m':1}                     ),
        'cm'  : (0.01,          {'m':1}                     ),
        'mm'  : (0.001,         {'m':1}                     ),
        'GN'  : (1000000,       {'kN':1}                    ),
        'MN'  : (1000,          {'kN':1}                    ),
        'N'   : (0.001,         {'kN':1}                    ),
        'yr'  : (60*60*24*365,  {'s':1}                     ),
        'day' : (60*60*24,      {'s':1}                     ),
        'hr'  : (60*60,         {'s':1}                     ),
        'min' : (60,            {'s':1}                     ),
        'GPa' : (1000000,       {'m':-2, 'kN':1}            ),
        'MPa' : (1000,          {'m':-2, 'kN':1}            ),
        'kPa' : (1,             {'m':-2, 'kN':1}            ),
        'Pa'  : (0.001,         {'m':-2, 'kN':1}            ),
    }

    _system = 'ce'


#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, value=1, units=None):
        '''
        Called class return cunit object. It have two arguments: value and units. The value can be numeric type data, while units accept only dictonary and string.
        '''

        # if user input units as string, then convert it to dictonary type
        if type(units) == str:
            # call to convert methods
            units = ndict.str2dict(units)

        # if value's type is string, then try to get unit definition from base_{x}.
        if type(value)==str and units==None:
            self._get(value)
        else:
            # else set up atributes for value and units as user input
            self._value = value
            self._units = units


#$$ ________ def _get ______________________________________________________ #

    def _get(self, units):
        '''
        User input units as string type. This must be checked explicit, link in __init__(...). The set up _value and _units as copy from system definition if it exists, else return CunitSystemError.
        This method must set up _value and _units or raise error!
        '''
        try:
            # get value and unit from system defintion
            base_value = cunit.base[units]

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
            verrs.f1CunitSystemError(self._system, units)


#$$ ________ def add _______________________________________________________ #

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
        if (not overwrite) and (name in cunit.base):

            # if flag if False and name alredy exists, then raise error
            verrs.f3CunitSystemError(cunit.system, name)

        # extend base dict
        cunit.base.update({name:(value, units)})

        # retur cunit object
        return cunit(name)


#$$ ________ def rem _______________________________________________________ #

    @staticmethod
    def rem(name, silent=True):
        '''
        Delete unit from current system. If silent is True, then no error occur if name not occur in self.base too.
        '''

        # first check if name is exists in self.base
        if name in cunit.base:

            # the fastest method of delete key is del statment
            del cunit.base[name]

        # if not exists, then check silent flag
        elif not silent:

            # if silent if False, then raise error
            raise ValueError('name not in base')


#$$ ________ def primary ___________________________________________________ #

    def primary(self, system=None):
        '''
        Convert unit to current base system. Method loop over _units and convert each row to base line. Method reutnr new one units and does not convert old!

        system can be input as None (get current system), dict (input full sytem dictonary) or string (get one of alredy defined systems).
        '''

        # base type is dict, but user can input in other types
        # if system is not definex explicited
        if system is None:
            # then get current base
            system = self.base
        # else input type is string
        elif type(system) is str:
            # then get one of already exists system
            system = eval('self.base_'+system)
        # else it it dict
        elif type(system) is dict:
            pass
        # if type is other, i dont now what do with that
        else:
            verrs.f2CunitSystemError(system)

        # get value
        cval  = self._value

        if cval == 0:
            return cunit(cval, {})

        # copy unit dictonary
        cdict = self._units.copy()

        # loop over keys in unit dictonary
        for key,val in self._units.items():

            # get base key
            base_value = system[key]

            # if unit is not primary then convert it to primary
            if base_value:

                # multiply value by unit value
                cval *= base_value[0] ** val

                # delete key from dictonary
                cdict.pop(key, None)

                # sum unit's power, which need to consider actual power
                cdict = ndict.dsum(cdict, ndict.vmul(base_value[1], val))

        # return new cunit, does not convert old!
        return cunit(cval, cdict)
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
                verrs.f1CunitCoverError(val)

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
        val = self/cunit(1, units)

        #
        if fcover:
            if len(val._units) != 0:
                verrs.f1CunitCoverError(str(val._units))

        return val._value
    d = drop


#$$ ________ def drop-external _____________________________________________ #

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

    def edit(self, units=None, acc=None, style=None, fcover=False, post=True, trail=None, nnot=None):
        '''
        Change self in-place like acc, style or units.
        '''
        if units: self.convert(
            units=units, fcover=fcover, inplace=True)
        if acc  : self.acc   = acc
        if style: self.style = style
        if trail: self.trail = trail
        if nnot : self.nnot  = nnot
        return self
    e = edit

#$$ ________ def show ______________________________________________________ #

    def show(self, units=None, acc=None, style=None, fcover=False, post=True, trail=None, nnot=None):
        '''
        Change self only to print, like acc, style or units.
        '''
        othe = self.copy()
        if units: othe.convert(
            units=units, fcover=fcover, inplace=True)
        if acc  : othe.acc   = acc
        if style: othe.style = style
        if trail: othe.trail = trail
        if nnot : othe.nnot  = nnot
        return othe
    s = show

#$$ ________ def show-external _____________________________________________ #

    @staticmethod
    def show_external(self, units=None, acc=None, style=None, fcover=False, post=True, trail=None, nnot=None):

        if type(self) in [list, np.ndarray]:
            return [cunit.show_external(obj, units, acc, style, fcover, post, trail, nnot) for obj in self]

        elif type(self) is cunit:
            return cunit.show(self, units, acc, style, fcover, post, trail, nnot)

        else:
            return self
    se = show_external


#$$ ________ def units _____________________________________________________ #

    def units(self):
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
            verrs.fCunitIncompatibleErorr(s, o, '__(ri)add__')

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
            verrs.fCunitUndefinedOperationError('__add__', self, othe)


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
            verrs.fCunitIncompatibleErorr(s, o, '__sub__')

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
            verrs.fCunitUndefinedOperationError('__sub__', self, othe)


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
            verrs.fCunitIncompatibleErorr(s, o, '__rsub__')

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
            verrs.fCunitUndefinedOperationError('__rsub__', self, othe)


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
            verrs.f0CunitSystemError('Power cunit type is not implemented')

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
                nround      = self.acc[0],
                precision   = self.acc[1],
                notation    = self.nnot,
                strip_zeros = not self.trail,
            )

            for key,val in self._units.items():
                self._units[key] = round(val, self.eacc)

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
        style = self.style.lower()

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
            verrs.fCunitIncompatibleErorr(s, o, '__lt__')

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
            verrs.fCunitUndefinedOperationError('__lt__', self, othe)




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
            verrs.fCunitIncompatibleErorr(s, o, '__le__')

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
            verrs.fCunitUndefinedOperationError('__le__', self, othe)


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
            verrs.fCunitIncompatibleErorr(s, o, '__eq__')

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
            verrs.fCunitUndefinedOperationError('__eq__', self, othe)




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
            verrs.fCunitIncompatibleErorr(s, o, '__ne__')

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
            verrs.fCunitUndefinedOperationError('__ne__', self, othe)



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

