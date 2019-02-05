'''
------------------------------------------------------------------------------
***** bacadra (project) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from .tools.setts import settsmeta
from .tools.verre import BCDR_ERRS,BCDR_WARN,BCDR_INFO


#$ ____ errors _____________________________________________________________ #

class BCDR_project_ERROR(BCDR_ERRS):
    pass

#$ ____ warnings ___________________________________________________________ #

class BCDR_project_WARN(BCDR_WARN):
    pass

#$ ____ infos ______________________________________________________________ #

class BCDR_project_INFO(BCDR_INFO):
    pass

def BCDR_project_INFO_Scope(id):
    BCDR_project_INFO('i0011',
        f'The scope selector change to new id <{id}>.'
    )






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
                BCDR_project_INFO_Scope(id)
                if value:
                    self._scope[id] = value
            else:
                if value:
                    self.__temp__ = value
                else:
                    self.__temp__ = self._scope[id]

        elif value==True:
            self.__ssel = 0
            BCDR_project_INFO_Scope(0)








#$ ____ class project ______________________________________________________ #

class project:

    # class setts
    setts = setts('setts', (setts,), {})


    from .dbase.dbase import dbase

    class pinky:

        from .pinky.texme.texme import texme

        from .pinky.texme.texpj import texpj

        from .pinky.rstme.rstme import rstme

    class mates:

        from .mates.umate.umate import umate

    class usecp:

        from .usect.usecp.value import value

        from .usect.usecp.tsect import tsect

        from .usect.usecp.point import point

    class geomf:

        from .geomx.geomf.nodes import nodes

        from .geomx.geomf.truss import truss

    class loads:

        from .loads.cates import cates

        from .loads.lcase import lcase

    from .mosas.mosas import mosas



    def __init__(self):

        # object setts
        self.setts = self.setts('setts',(),{})

        self.dbase = self.dbase(core=self)

        class pinky:

            texme = self.pinky.texme(core=self)

            texpj = self.pinky.texpj(core=self, tex=texme)

            rstme = self.pinky.rstme(core=self)

        self.pinky = pinky()

        class mates:

            umate = self.mates.umate(core=self)

        self.mates = mates()

        class usecp:

            value = self.usecp.value(core=self)

            tsect = self.usecp.tsect(core=self)

            point = self.usecp.point(core=self)

        self.usecp = usecp()

        class geomf:

            nodes = self.geomf.nodes(core=self)

            truss = self.geomf.truss(core=self)

        self.geomf = geomf()

        class loads:

            cates = self.loads.cates(core=self)

            lcase = self.loads.lcase(core=self)

        self.loads = loads()

        self.mosas = self.mosas(core=self)
