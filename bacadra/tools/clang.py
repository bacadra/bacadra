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


class clangmeta(type):

    propme = (
    "__face = 'en'              \n"

    "@property                  \n"
    "def face(self):            \n"
    "    return self.__face     \n"

    "@face.setter               \n"
    "def face(self, value):     \n"
    "    self.__face = value    \n"

    "__out = 'en'               \n"

    "@property                  \n"
    "def out(self):             \n"
    "    return self.__out      \n"

    "@out.setter                \n"
    "def out(self, value):      \n"
    "    self.__out = value     \n"
    )

    exec(propme)


class clang(metaclass=clangmeta):

    exec(clangmeta.propme)

    def __init__(self, core=None):

        self.core = core

#$ ____ def __call__ ________________________________________________________ #

    def __call__(self, mode='out', en='<No english description!>', language=None, l=None, **kwargs):
        '''
        (c)hoose (lang)uage
        '''

        # resolve shortcuts...
        if l: language = l

        # choose output language
        if   not language and mode=='out' : language = self.out
        elif not language and mode=='face': language = self.face
        if language==None: language='en'

        # join dict
        data = {**{'en':en}, **kwargs}

        # send correct data
        if language in data:
            return data[language]
        else:
            return data['en']



# from .setts import settsmeta
#
#
# #$ ____ class setts ________________________________________________________ #
#
# class setts(settsmeta):
#
# #$$ ________ def face ______________________________________________________ #
#
#     __face = 'en'
#
#     @property
#     def face(self): return self.__face
#
#     @face.setter
#     def face(self, value):
#         '''
#         Language of syste, interface.
#         '''
#
#         if self.__save__: self.__face   = value
#         else:             self.__temp__ = value
#
#
# #$$ ________ def out _______________________________________________________ #
#
#     __out = 'en'
#
#     @property
#     def out(self): return self.__out
#
#     @out.setter
#     def out(self, value):
#         '''
#         Language of project output.
#         '''
#
#         if self.__save__: self.__out    = value
#         else:             self.__temp__ = value
#
#
# class clang:
#
#     # class setts
#     setts = setts('setts', (setts,), {})
#
#     def __init__(self, core=None):
#
#         self.core = core
#
#         # object setts
#         self.setts = self.setts('setts',(),{})
#
# #$ ____ def __call__ ________________________________________________________ #
#
#     def __call__(self, mode, en='<No english description!>', language=None, l=None, **kwargs):
#         '''
#         (c)hoose (lang)uage
#         '''
#
#         # resolve shortcuts...
#         if l: language = l
#
#         # choose output language
#         if   not language and mode=='out' : language = self.setts.out
#         elif not language and mode=='face': language = self.setts.face
#         if language==None: language='en'
#
#         # join dict
#         data = {**{'en':en}, **kwargs}
#
#         # send correct data
#         if language in data:
#             return data[language]
#         else:
#             return data['en']






# class clang:
#
# #$$ ________ def face ______________________________________________________ #
#
#     __face = 'en'
#
#     @property
#     def face(self): return self.__face
#
#     @face.setter
#     def face(self, value):
#         '''
#         Language of syste, interface.
#         '''
#
#         if self.__save__: self.__face   = value
#         else:             self.__temp__ = value
#
#
# #$$ ________ def out _______________________________________________________ #
#
#     __out = 'en'
#
#     @property
#     def out(self): return self.__out
#
#     @out.setter
#     def out(self, value):
#         '''
#         Language of project output.
#         '''
#
#         if self.__save__: self.__out    = value
#         else:             self.__temp__ = value
#
#     def __init__(self, core=None):
#
#         self.core = core
#
#
#
# #$ ____ def __call__ ________________________________________________________ #
#
#     def __call__(self, mode='out', en='<No english description!>', language=None, l=None, **kwargs):
#         '''
#         (c)hoose (lang)uage
#         '''
#
#         # resolve shortcuts...
#         if l: language = l
#
#         # choose output language
#         if   not language and mode=='out' : language = self.out
#         elif not language and mode=='face': language = self.face
#         if language==None: language='en'
#
#         # join dict
#         data = {**{'en':en}, **kwargs}
#
#         # send correct data
#         if language in data:
#             return data[language]
#         else:
#             return data['en']









