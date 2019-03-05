'''
------------------------------------------------------------------------------
***** (c)hoose (lang)uage *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ######################################################################### #

from .setts import setts_init

#$ ____ class setts ________________________________________________________ #

class setts(setts_init):

    interface = lambda self, x=None: self.tools.gst('interface', x)
    output = lambda self, x=None: self.tools.gst('output', x)

#$ ____ class clang ________________________________________________________ #

class clang:
    setts = setts()
    setts.interface('en')
    setts.output('en')

#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, core=None):

        self.core = core

        self.setts = setts(self.setts, self)

#$$ ________ def __call__ __________________________________________________ #

    def __call__(self, mode='output', en='<No english description!>', language=None, **kwargs):

        # choose output language
        if   not language and mode=='interface':
            language = self.setts.interface()
        elif not language and mode=='output':
            language = self.setts.output()

        # use default language
        if language=='en':
            text = en
        else:
            text = kwargs[language]

        return text

#$ ######################################################################### #


