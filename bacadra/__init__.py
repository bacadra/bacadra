'''
------------------------------------------------------------------------------
***** bacadra (core) package *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ######################################################################### #

from .tools.setts import sinit


#$ ____ class setts ________________________________________________________ #

class setts(sinit):

    pass

#$ ____ class core ___________________________________________________________ #


class core:

    setts = setts()


    from .unise.unise import unise


    class tools:

        from .tools.erwin import verrs

        from .tools import fpack

        def __init__(self, core=None):

            pass

    class pinky:

        from .pinky.docme.docme import docme

        from .pinky.texme.texme import texme

        from .pinky.fstme.fstme import fstme

        def __init__(self, core=None):

            self.docme = self.docme(core=core)

            self.texme = self.texme(core=core)

            self.fstme = self.fstme(core=core)

    from .bapps.bapps import bapps


    def __init__(self):

        self.setts = setts(master=self.setts.tools, root=self)

        self.tools = self.tools(core=self)

        self.pinky = self.pinky(core=self)

        self.bapps = self.bapps(core=self)



#$ ######################################################################### #
