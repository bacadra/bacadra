'''
------------------------------------------------------------------------------
BCDR += ***** general and special (mate)rial(s) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ..tools.rootx import rootx

from .cmemb import cmemb
from .smemb import smemb
from .asect import asect

#$ class index
class index(rootx):
    #$$ __init__
    def __init__(self, core):

        from . import asect
        self.asect = asect(core=core)