'''
------------------------------------------------------------------------------
***** (u)nise (math) package *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ######################################################################### #

import math
from .unise import unise
from . import udict
from . import verrs

π   = math.pi
e   = math.e

def sin(x):
    if type(x) == unise: x=x.d('')
    return math.sin(x)

def cos(x):
    if type(x) == unise: x=x.d('')
    return math.cos(x)

def tan(x):
    if type(x) == unise: x=x.d('')
    return math.tan(x)

def cot(x):
    if type(x) == unise: x=x.d('')
    return 1/math.tan(x)

def asin(x):
    if type(x) == unise: x=x.d('')
    return math.asin(x)

def acos(x):
    if type(x) == unise: x=x.d('')
    return math.acos(x)

def atan(x):
    if type(x) == unise: x=x.d('')
    return math.atan(x)

def acot(x):
    if type(x) == unise: x=x.d('')
    return 1/math.atan(x)

def sqrt(x, n=2):
    if type(x) == unise:
        return unise(x._value**(1/n), udict.vmul(x._units, 1/n))
    else:
        if n==2:
            return math.sqrt(x)
        else:
            return x**(1/n)

def floor(x, n=0, unit=None):
    if type(x) == unise:
        if unit:
            return unise(math.floor(x.c(unit)*10**n)/10**n, unit)
        else:
            return unise(math.floor(x*10**n)/10**n, x._units)
    else:
        return math.floor(x*10**n)/10**n

def exp(x):
    if type(x) == unise: x=x.d('')
    return math.exp(x)

def log(x):
    if type(x) == unise: x=x.d('')
    return math.log(x)

def ln(x):
    if type(x) == unise: x=x.d('')
    return math.log(x)

def log10(x):
    if type(x) == unise: x=x.d('')
    return math.log10(x)

#$ ######################################################################### #
