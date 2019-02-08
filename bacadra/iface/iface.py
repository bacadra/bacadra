'''
------------------------------------------------------------------------------
***** bacadra (i)nter(face) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from ..tools.setts import settsmeta
from . import verrs

#$ ____ class setts ________________________________________________________ #

class setts(settsmeta):

    nodes_fix = None

#$$ ________ def scope _____________________________________________________ #

    _scope = [{}]*10 # turn off it to printng, to long...
    __ssel  = 0   # select scope bank

    @property
    def scope(self):
        return self._scope[self.__ssel]

    @scope.setter
    def scope(self, value):
        '''
        There is 11 slots for scope dictonary.

        0    -- base dictonary, can be selected by value=True
        1..9 -- other scopes

        to change dictonary <var> = n, {..}; where n is dictonary name
        if {..} is empty, then dict will be only changed, but not replace
        if {..} is not empty, then slot will be replaced with new one dict

        Remember!
        The scope atribute is simpler than in child class. e.g. texme can set __ssel=None to get scope from project class. Project class is the main, so None is unnecessary.
        '''

        # simple given dict
        if type(value)==dict:

            if self.__save__: self._scope[self.__ssel] = value
            else:             self.__temp__ = value

        # if given as number,dict
        elif type(value)==tuple:
            id,value = value

            if self.__save__:
                self.__ssel = id
                verrs.BCDR_project_INFO_Scope(id)
                if value:
                    self._scope[id] = value
            else:
                if value:
                    self.__temp__ = value
                else:
                    self.__temp__ = self._scope[id]

        elif value==True:
            self.__ssel = 0
            verrs.BCDR_project_INFO_Scope(0)



#$$ ________ def active ____________________________________________________ #

    __active = False

    @property
    def active(self): return self.__active

    @active.setter
    def active(self, value):

        if self.__save__: self.__active = value
        else:             self.__temp__ = value








#$ ____ class iface __________________________________________________________ #

class iface:

    # class setts
    setts = setts('setts', (setts,), {})

    from .bapps import bapps

    from .cunit import cunit

    from .pinky import pinky

    from .sofix import sofix

    from .solve import solve

    from .tools import tools

    from ..dbase.dbase import dbase

    class mates:

        from ..mates.umate.umate import umate

        from ..mates.steea.steea import steea

        def __init__(self, core=None):

            self.umate = self.umate(core=core)

            self.steea = self.steea(core=core)


    class usecp:

        from ..usect.usecp.value import value

        from ..usect.usecp.tsect import tsect

        from ..usect.usecp.point import point

        def __init__(self, core=None):

            self.value = self.value(core=core)

            self.tsect = self.tsect(core=core)

            self.point = self.point(core=core)

    class geomf:

        from ..geomx.geomf.nodes import nodes

        from ..geomx.geomf.truss import truss

        def __init__(self, core=None):

            self.nodes = self.nodes(core=core)

            self.truss = self.truss(core=core)

    class loads:

        from ..loads.cates import cates

        from ..loads.lcase import lcase

        def __init__(self, core=None):

            self.cates = self.cates(core=core)

            self.lcase = self.lcase(core=core)

    from ..mosas.mosas import mosas

    def __init__(self):

        # object setts
        self.setts = self.setts('setts',(),{})

        self.pinky = self.pinky(core=self)

        self.sofix = self.sofix(core=self)

        self.tools = self.tools(core=self)

        self.dbase = self.dbase(core=self)

        self.mates = self.mates(core=self)

        self.usecp = self.usecp(core=self)

        self.geomf = self.geomf(core=self)

        self.loads = self.loads(core=self)

        self.mosas = self.mosas(core=self)


