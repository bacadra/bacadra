#!/usr/bin/python
#-*-coding: UTF-8-*-
#$ ____ import _____________________________________________________________ #

import math

import numpy as np

from .ndict import ndict

from . import verrs

#$ ____ metaclass cunitmeta ________________________________________________ #

class cunitmeta(type):
    @property
    def system(cls):
        return cls._system

    @system.setter
    def system(cls, value):
        cls.base = eval('cls.base_'+value)
        cls._system = value



#$ ____ class cunit ________________________________________________________ #

class cunit(object, metaclass=cunitmeta):

    # accuracy of printed value
    acc = (None,None)

    # print style, style of print
    style = 'pretty'

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
        'rad' : (1,             {}                          ),
        'mrad': (0.001,         {}                          ),
        'deg' : (math.pi/180,   {}                          ),
        'C'   : (273.15,        {'K':1}                     ),
        'Hz'  : (1,             {'s':-1}                    ),
        't'   : (1000,          {'kg':1}                    ),
        'kNm' : (10**2,         {'kg':1,'m':2, 's':-2}      ),
        'MNm' : (10**5,         {'kg':1,'m':2, 's':-2}      ),
        'N'   : (0.1,           {'kg':1,'m':1, 's':-2}      ),
        'cm'  : (0.01,          {'m':1}                     ),
        'mm'  : (0.001,         {'m':1}                     ),
        'km'  : (1000,          {'m':1}                     ),
        'dm'  : (0.1,           {'m':1}                     ),
        'kN'  : (10**2,         {'kg':1, 'm':1,  's':-2}    ),
        'MN'  : (10**5,         {'kg':1, 'm':1,  's':-2}    ),
        'GN'  : (10**8,         {'kg':1, 'm':1,  's':-2}    ),
        'Pa'  : (1,             {'kg':1, 'm':-1, 's':-2}    ),
        'kPa' : (10**2,         {'kg':1, 'm':-1, 's':-2}    ),
        'MPa' : (10**5,         {'kg':1, 'm':-1, 's':-2}    ),
        'GPa' : (10**8,         {'kg':1, 'm':-1, 's':-2}    ),
        'yr'  : (60*60*24*365,  {'s':1}                     ),
        'day' : (60*60*24,      {'s':1}                     ),
        'hr'  : (60*60,         {'s':1}                     ),
        'min' : (60,            {'s':1}                     ),
    }

    # system Civil Engineering
    base_ce = {
        'kN'  : (None                                       ),
        'm'   : (None                                       ),
        'C'   : (None                                       ),
        's'   : (None                                       ),
        'rad' : (1,             {}                          ),
        'mrad': (0.001,         {}                          ),
        'deg' : (math.pi/180,   {}                          ),
        'Hz'  : (1,             {'s':-1}                    ),
        'kNm' : (1,             {'kN':1, 'm':1}             ),
        'MNm' : (1000,          {'kN':1, 'm':1}             ),
        'kg'  : (0.01,          {'kN':1, 'm':-1, 's':2}     ),
        't'   : (10,            {'kN':1}                    ),
        'K'   : (-273.15,       {'C':1}                     ),
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


    # system default
    _system = 'ce'    # system -> metaclass setter
    base  = base_ce # non-dynamicly so 2x definitions


#$$ ________ def --init-- __________________________________________________ #

    def __init__(self, value=1, units={}):
        '''
        Called class return cunit object. It have two arguments: value and units. The value can be numeric type data, while units accept only dictonary and string.
        '''

        # if user input units as string, then convert it to dictonary type
        if type(units) == str:
            # call to convert methods
            units = ndict.str2dict(units)

        # if value's type is string, then try to get unit definition from base_{x}.
        if type(value) == str:
            self._get(value)
        else:
            # else set up atributes for value and units as user input
            self._value = value
            self._units = units


#$$ ________ def -get ______________________________________________________ #

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
            verrs.f3CunitSystemError(cunit._system, name)

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
                cval *= base_value[0]

                # delete key from dictonary
                cdict.pop(key, None)

                # sum unit's power, which need to consider actual power
                cdict = ndict.dsum(cdict, ndict.vmul(base_value[1], val))

        # return new cunit, does not convert old!
        return cunit(cval, cdict)


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



#$$ ________ def drop ______________________________________________________ #

    def drop(self, units=None, fcover=False, system=None):
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



#$$ ________ def copy ______________________________________________________ #

    def copy(self):
        '''
        Return copy of self. Needed in show function etc.
        '''
        return cunit(self._value, self._units)


#$$ ________ def edit ______________________________________________________ #

    def edit(self, units=None, acc=None, style=None, fcover=False, post=True):
        '''
        Change self in-place like acc, style or units.
        '''
        if units: self.convert(
            units=units, fcover=fcover, inplace=True)
        if acc  : self.acc   = acc
        if style: self.style = style
        return self
    e = edit

#$$ ________ def show ______________________________________________________ #

    def show(self, units=None, acc=None, style=None, fcover=False, post=True):
        '''
        Change self only to print, like acc, style or units.
        '''
        if units: othe = self.convert(
            units=units, fcover=fcover, inplace=False)
        if acc  : othe.acc   = acc
        if style: othe.style = style
        return othe
    s = show

#$$ ________ magic behaviour _______________________________________________ #
#$$$ ____________ def --add-- / --radd-- / --iadd-- / --pos-- ______________ #

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
        elif self._units=={}:
            return cunit(self._value + othe, {})

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


#$$$ ____________ def --sub-- / --rsub-- / --isub-- / --neg-- ______________ #

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
        elif self._units=={}:
                return cunit(self._value - othe, {})

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
        elif self._units=={}:
                return cunit(othe - self._value, {})

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



#$$$ ____________ def --pow-- / --rpow-- / --ipow-- ________________________ #

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


#$$$ ____________ def --mul-- / --rmul-- / --imul-- ________________________ #

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



#$$$ ____________ def --truediv-- / --rtruediv-- / --itruediv-- ____________ #

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



#$$$ ____________ def --round-- ____________________________________________ #

    def __round__(self, acc=0):
        '''
        Python function: round(self, acc)
        '''
        return cunit(round(self._value, acc), self._units)

#$$$ ____________ def --ceil-- _____________________________________________ #

    def __ceil__(self):
        '''
        Python function: ceil(self)
        '''
        return cunit(math.ceil(self._value), self._units)

#$$$ ____________ def --trunc-- ____________________________________________ #

    def __trunc__(self):
        '''
        Python function: trunc(self)
        '''
        return cunit(math.trunc(self._value), self._units)

#$$$ ____________ def --nstyle-- ___________________________________________ #

    def __nstyle__(self, acc):
        '''
        Prepare numeric type data to print it.
        '''

        # save self value
        value = self._value

        # if self value type is numeric type then round and sign value
        if type(value) in [int,float]:

            # decimal places
            if acc[0]:
                value = round(value, acc[0])

                # loop over units and round unit's power
                for key,val in self._units.items():
                    self._units[key] = round(val, acc[0])

            # significant numbers
            if acc[1]:
                # TODO: verify how numbers are rounded, ceil, floor or what?
                if value != 0:
                    value = round(value, -int(math.floor(math.log10(abs(value)))) + (acc[1]-1))

            if int(value) == value:
                value = int(value)

        # return new units, with acc deci and prec
        return cunit(value, self._units)



#$$$ ____________ def --repr-- _____________________________________________ #

    def __repr__(self):
        '''
        Representation of cunit. The methods provide few styles.
        '''

        # prepare numeric data
        new = self.__nstyle__(self.acc)

        # convert style to lowercase
        self.style = cunit.style.lower()

        # if-block depend on presentation style
        if   self.style == 'pretty': return self.__repr__pretty(new)
        elif self.style == 'python': return self.__repr__python(new)
        elif self.style == 'latex' : return self.__repr__latex(new)


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
        val = str(self._value)

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
        val = str(self._value)

        # if-block depend on counter and denominator empty's
        # if all is empty
        if u=='' and d=='':
            return val + '*(1)'
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

            # if-block depend on power
            # if power is zero, then pass
            if   u_val==0 : pass

            # if power is one, then expand counter
            elif u_val==1 : u += r'~\textrm{' + u_str + '}'

            # if power is more than one, then expand counter with "^" symbol
            elif u_val>0  : u += r'~\textrm{' +u_str + '}^{' + str(u_val) + '}'

            # if power is one, then expand denominator
            elif u_val==-1: d += r'~\textrm{' + u_str + '}'

            # if power is less than one, then expand denominator with "^" symbol
            elif u_val<0  : d += r'~\textrm{' +u_str + '}^{' + str(-u_val) + '}'

        # convert self value to string
        val = str(self._value)

        # if-block depend on counter and denominator empty's
        # if all is empty
        if u=='' and d=='':
            return val
        elif u=='':
            return val + '~(1)/(' + d[1:] + ')'
        elif d=='':
            return val + u
        else:
            return val + r'~\cfrac{' + u[1:] + '}{' + d[1:] + '}'




#$$$ ____________ def --lt-- / --le-- ______________________________________ #

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
        elif self._units=={}:
            return self._value < othe

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
        elif self._units=={}:
            return self._value <= othe

        # else raise error
        else:
            verrs.fCunitUndefinedOperationError('__le__', self, othe)


#$$$ ____________ def --gt-- / --ge-- ______________________________________ #

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


#$$$ ____________ def --eq-- / --ne-- ______________________________________ #

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
        elif self._units=={}:
            return self._value == othe

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
        elif self._units=={}:
            return self._value != othe

        # treat bool and None types
        elif othe in [True, False, None]:
            return self._value != othe

        # else raise error
        else:
            verrs.fCunitUndefinedOperationError('__ne__', self, othe)



#$$$ ____________ def --is-- / is-not ______________________________________ #

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

#$$$ ____________ def --and-- / --rand-- ___________________________________ #

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


#$$$ ____________ def --xor-- / --rxor-- ___________________________________ #


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


#$$$ ____________ def --abs-- / --mod-- ____________________________________ #

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


#$$$ ____________ def --float-- / --int-- __________________________________ #

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


#$$$ ____________ def --bool-- _____________________________________________ #

    def __bool__(self):
        return bool(self._value)


#$$$ ____________ def --iter-- _____________________________________________ #

    # def __iter__(self):
    #     if type(self._value)==list or type(self._value)==tuple:
    #         return (x for x in self._value)
    #
    # def __call__(self):
    #     print(
    #           'style  = ', self.style,
    #         '\nacc   = ', self.acc,
    #         '\nvalue = ', self._value,
    #         '\nunits = ', self._units)



#$$ ________ @property convert _______________________________________________ #

    # for key,val in base.items():
    #     command = ("@property\n"
    #                "def  _" + str(key) + "(self):\n"
    #                "   return self.convert({'" + str(key) + "':1})")
    #     exec(command)
