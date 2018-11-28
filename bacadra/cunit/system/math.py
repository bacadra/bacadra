import math
from ..units import cunit
from ..ndict import ndict
from .. import verrs

π   = math.pi
e   = math.e
g   = cunit(10, {'m':1, 's':-2})

def sin(x):
    if type(x) == cunit:
        verrs.f2CunitIncompatibleErorr(x, 'sin(x)')
    return math.sin(x)

def cos(x):
    if type(x) == cunit:
        verrs.f2CunitIncompatibleErorr(x, 'cos(x)')

    return math.cos(x)

def tan(x):
    if type(x) == cunit:
        verrs.f2CunitIncompatibleErorr(x, 'tan(x)')
    return math.tan(x)

def cot(x):
    if type(x) == cunit:
        verrs.f2CunitIncompatibleErorr(x, 'cot(x)')
    return 1/math.tan(x)

def asin(x):
    if type(x) == cunit:
        verrs.f2CunitIncompatibleErorr(x, 'asin(x)')
    return math.asin(x)

def acos(x):
    if type(x) == cunit:
        verrs.f2CunitIncompatibleErorr(x, 'acos(x)')
    return math.acos(x)

def atan(x):
    if type(x) == cunit:
        verrs.f2CunitIncompatibleErorr(x, 'atan(x)')
    return math.atan(x)

def acot(x):
    if type(x) == cunit:
        verrs.f2CunitIncompatibleErorr(x, 'acot(x)')
    return 1/math.atan(x)

def sqrt(x, n=2):
    if type(x) == cunit:
        return cunit(x._value**(1/n), ndict.vmul(x._units, 1/n))
    else:
        if n==2:
            return math.sqrt(x)
        else:
            return x**(1/n)

def floor(x, n=0, unit=None):
    if type(x) == cunit:
        if unit:
            return cunit(math.floor(x.c(unit)*10**n)/10**n, unit)
        else:
            return cunit(math.floor(x*10**n)/10**n, x._units)
    else:
        return math.floor(x*10**n)/10**n

exp   = math.exp
log   = math.log
ln    = math.log
log10 = math.log10
