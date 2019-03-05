'''
------------------------------------------------------------------------------
***** bacadra (init) package *****
==============================================================================

There are definition for the most important class of bcdr env -- core.

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ######################################################################### #

from .tools.setts import setts_init
from .tools import verrs

#$ ____ class setts ________________________________________________________ #

class setts(setts_init):

#$$ ________ def scope _____________________________________________________ #

    def scope(self, id=None, value=None, check=None, reset=None):
        if id!=None:
            if check==True:
                id = self.tools.set('scope', id, check)
            else:
                self.tools.set('scope', id, check)
        else:
            id = self.tools.get('scope')

        if value==None:
            if self.tools.exists('_scope_'+str(id)):
                return self.tools.get('_scope_'+str(id), reset)
            else:
                return
        else:
            return self.tools.set('_scope_'+str(id), value, check)

#$ ____ class core ___________________________________________________________ #

class core:

    setts = setts()
    setts.scope(True, {})

    from .dbase.dbase import dbase

    from .unise.unise import unise

    class tools:

        from .tools.clang import clang

        from .tools.erwin import verrs

        from .tools import fpack

        from .tools import bsver

        def __init__(self, core=None):

            self.clang = self.clang(core=core)

            self.verrs = self.verrs(core=core)

    class pinky:

        from .pinky.texme.texme import texme

        def __init__(self, core=None):

            self.texme = self.texme(core=core)


    class sofix:

        from .sofix.sbase import sbase

        from .sofix.trade import trade

        from .sofix.wgraf import wgraf

        def __init__(self, core=None):

            self.sbase = self.sbase(core=core)

            self.trade = self.trade(core=core)

            self.wgraf = self.wgraf(core=core)


    class mates:

        from .mates.umate.umate import umate

        from .mates.steea.steea import steea

        def __init__(self, core=None):

            self.umate = self.umate(core=core)

            self.steea = self.steea(core=core)


    def __init__(self):

        self.setts = setts(self.setts, self)

        self.dbase = self.dbase(core=self)

        self.tools = self.tools(core=self)

        self.pinky = self.pinky(core=self)

        self.sofix = self.sofix(core=self)

        self.mates = self.mates(core=self)

#$ ######################################################################### #
