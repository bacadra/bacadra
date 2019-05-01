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

    def author(self, name=None, surname=None, company=None, logo=None, check=None):
        '''Project author's details'''

        if type(check)==str:
            return self.tools.sgc(name='author:'+check,
                value=eval(check), check=True)

        if name   !=None: self.tools.gst('author:name'   , name   )
        if surname!=None: self.tools.gst('author:surname', surname)
        if company!=None: self.tools.gst('author:company', company)
        if logo   !=None: self.tools.gst('author:logo'   , logo   )


    def scope(self, data):
        '''scope'''
        return self.tools.gst('scope', data)


    def master(self, core):
        '''Master core'''
        return self.tools.gst('master', core)



#$ ____ class core ___________________________________________________________ #


class core:
    '''
    core
    ====

    Core package represent project object. There most of bacadra object is depend core package.


    ***** Main packages *****
    -------------------------

    class tools:
        Pack of usefool tools

        class verrs:
            manage errors, warnings and infos of bacadra program

        def erwin:
            Raise bacadra error, warning or info

        module fpack:
            Pack of tools which are not connected to the core package.
            There are mdata class, float number formatter etc

        class clang:
            Manage language of bacadra interface and output.

    dbase:


    pinky:

        texme:

        docme:

        fstme:

    sofix:

        sbase:

        wgraf:

        trade:

    bapps:

    '''

    setts = setts()

    setts.author(
        name    = False,
        surname = False,
        company = False,
        logo    = False,
    )

    setts.scope({})

    setts.master(False)


    ##############################

    from .unise.unise import unise

    from .dbase.dbase import dbase

    class tools:

        from .tools.erwin import verrs

        from .tools.erwin import erwin

        from .tools import fpack

        from .tools.clang import clang

        def __init__(self, core=None):

            self.clang = self.clang(core=core)


    class pinky:

        from .pinky.docme.docme import docme

        from .pinky.texme.texme import texme

        from .pinky.fstme.fstme import fstme

        def __init__(self, core=None):

            self.docme = self.docme(core=core)

            self.texme = self.texme(core=core)

            self.fstme = self.fstme(core=core)


    class sofix:

        from .sofix.sbase import sbase

        from .sofix.wgraf import wgraf

        from .sofix.trade import trade

        def __init__(self, core=None):

            self.sbase = self.sbase(core=core)

            self.wgraf = self.wgraf(core=core)

            self.trade = self.trade(core=core)


    from .bapps.bapps import bapps


    def __init__(self):

        self.core  = self

        self.setts = setts(master=self.setts.tools, root=self)

        self.dbase = self.dbase(core=self)

        self.tools = self.tools(core=self)

        self.pinky = self.pinky(core=self)

        self.sofix = self.sofix(core=self)

        self.bapps = self.bapps(core=self)



bcdr = core

#$ ######################################################################### #
