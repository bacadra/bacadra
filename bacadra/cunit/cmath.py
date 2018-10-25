import math
from .units import cunit
from .ndict import ndict

def sin(x):
    if type(x) == cunit:
        if x._units != {}:
            raise ValueError('IncomapitibleUnitsError')
    return math.sin(x)

def cos(x):
    if type(x) == cunit:
        if x._units != {}:
            raise ValueError('IncomapitibleUnitsError')
    return math.cos(x)

def tan(x):
    if type(x) == cunit:
        if x._units != {}:
            raise ValueError('IncomapitibleUnitsError')
    return math.tan(x)

def cot(x):
    if type(x) == cunit:
        if x._units != {}:
            raise ValueError('IncomapitibleUnitsError')
    return 1/math.tan(x)

def asin(x):
    if type(x) == cunit:
        if x._units != {}:
            raise ValueError('IncomapitibleUnitsError')
    return math.asin(x)

def acos(x):
    if type(x) == cunit:
        if x._units == {}:
            raise ValueError('IncomapitibleUnitsError')
    return math.acos(x)

def atan(x):
    if type(x) == cunit:
        if x._units != {}:
            raise ValueError('IncomapitibleUnitsError')
    return math.atan(x)

def acot(x):
    if type(x) == cunit:
        if x._units != {}:
            raise ValueError('IncomapitibleUnitsError')
    return 1/math.atan(x)

def sqrt(x, n=2):
    if type(x) == cunit:
        return cunit(x._value**(1/n), ndict.vmul(x._units, 1/n))
    else:
        return 1/math.atan(x)
