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

from .setts import sinit

from . import verrs

#$ ____ class setts ________________________________________________________ #

class setts(sinit):

    def interface(self, language=None, check=None):
        return self.tools.gst('interface', language)
    i = interface

    def messages(self, language=None, check=None):
        return self.tools.gst('output', language)
    m = messages

#$ ____ class clang ________________________________________________________ #

class clang:

    setts = setts()

    setts.interface('en')

    setts.messages('en')

#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, core=None):

        self.core = core

        self.setts = setts(master=self.setts.tools, root=self)

#$$ ________ def choose ____________________________________________________ #

    def choose(self, mode='m', language=None, **kwargs):

        # choose output language
        if not language and mode in ['interface', 'i']:
            language = self.setts.interface()

        elif not language and mode in ['messages', 'm']:
            language = self.setts.messages()


        if language in kwargs:
            text = kwargs[language]

        elif 'en' in kwargs:
            text = kwargs['en']
            verrs.BCDR_tools_WARN_Translation_Not_Provided(
                language, 'en', text)

        elif 'pl' in kwargs:
            text = kwargs['pl']
            verrs.BCDR_tools_WARN_Translation_Not_Provided(
                language, 'pl', text)

        elif len(kwargs)>0:
            newlang=kwargs.keys()[0]
            text = kwargs[newlang]
            verrs.BCDR_tools_WARN_Translation_Not_Provided(
                language, newlang, text)

        else:
            verrs.BCDR_tools_ERROR_Translation_Not_Provided()

        return text


#$ ######################################################################### #


