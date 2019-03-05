'''
------------------------------------------------------------------------------
***** (er)rrors, (w)arnings, (in)fos *****
==============================================================================

There are three types of messages:
- errors
- warnings
- infos

Thera are class which should be inherited to all modules.

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ######################################################################### #

import textwrap

from .fpack import color
from .setts import setts_init


#$ ____ class setts ________________________________________________________ #

class setts(setts_init):

#$$ ________ general _______________________________________________________ #

    original = lambda self, x=None: self.tools.gst('original', x)
    traceback = lambda self, x=None: self.tools.gst('traceback', x)

#$$ ________ def new _______________________________________________________ #

def new(name, mname):
    '''
    name -- code of error/warning/info like e0051
    mname -- method name, like small description
    '''
    setattr(setts, name, lambda self, x=None: self.tools.gst(name, x))

#$$ ________ x0000 tools ___________________________________________________ #

new('e0011', 'BCDR_tools_ERROR_Parse_Type')

#$$ ________ x0100 unise ___________________________________________________ #

new('e0111', 'BCDR_unise_ERROR_Incompatible')
new('e0112', 'BCDR_unise_ERROR_Undefined_Operator')
new('e0114', 'BCDR_unise_ERROR_Units_in_System')
new('e0115', 'BCDR_unise_ERROR_Already_Exists')
new('e0116', 'BCDR_unise_ERROR_Cover')
new('e0117', 'BCDR_unise_ERROR_Power2unise')

#$$ ________ x0600 pinky:texme _____________________________________________ #

new('e0611', 'BCDR_pinky_texme_ERROR_Header_Level')
new('e0621', 'BCDR_pinky_texme_ERROR_Type_Check')
new('e0622', 'BCDR_pinky_texme_ERROR_String_Selector')
new('e0623', 'BCDR_pinky_texme_ERROR_Invalid_Key')
new('e0681', 'BCDR_pinky_texme_ERROR_Path_Error')
new('e0682', 'BCDR_pinky_texme_ERROR_Evaluate')

new('w0681', 'BCDR_pinky_texme_WARN_Path_Error')
new('w0631', 'BCDR_pinky_texme_WARN_Scope_External')

new('i0611', 'BCDR_pinky_texme_INFO_Scope')






#$$ ________ x0700 pinky:rstme _____________________________________________ #

#$$ ________ x0800 pinky:docme _____________________________________________ #



#$ ____ class verrs ________________________________________________________ #

class verrs:
    setts = setts()
    setts.original(False)
    setts.traceback(True)

    # activate all errors, warning and infos
    for key in dir(setts):
        if key[0] in 'ewi':
            getattr(setts, key)(True)


    def __init__(self, core=None):

        self.core = core

        self.setts = setts(self.setts, self)



#$ ____ errors _____________________________________________________________ #

try:

    from IPython import get_ipython
    ipython = get_ipython()

    def exception_handler(exception_type, exception, traceback):

        if exception_type.__name__[:4]=='BCDR' and not verrs.setts.original():

                if verrs.setts.traceback()==True:
                    print('\n'.join(traceback[:-2]))

                title = exception_type.__name__
                width = 75
                len1 = int((width - len(title) - 6 - 10)/2)
                len2 = (width - len(title) - 6- 10) - len1

                print(color(len1*'-' + ' ' + '*'*5 + ' '*2 + title + ' '*2  + '*'*5 + ' '  + len2*'*', 'c'))

                # divide text by new line symbol
                exception = str(exception).split('\n')
                for i in range(len(exception)):
                    exception[i] = textwrap.fill(str(exception[i]), width=width)
                exception = '\n'.join(exception)

                print(exception)

        else:
            print(ipython.InteractiveTB.stb2text(traceback))

    ipython._showtraceback = exception_handler

except:
    pass


class BCDR_ERROR(Exception):
    pass

def BCDR_ERRO(id, value=''):
    if getattr(verrs.setts, id)():
        raise BCDR_ERROR(value)

#$ ____ warnings ___________________________________________________________ #

def BCDR_WARN(id, value=''):

    if getattr(verrs.setts, id)():

        title = 'BCDR_WARN'
        width = 75
        len1 = int((width - len(title) - 6 - 10)/2)
        len2 = (width - len(title) - 6- 10) - len1

        print(color(len1*'-' + ' ' + '*'*5 + ' '*2 + title + ' '*2  + '*'*5 + ' '  + len2*'*', 'y'))

        # divide text by new line symbol
        value = str(value).split('\n')
        for i in range(len(value)):
            value[i] = textwrap.fill(str(value[i]), width=width)
        value = '\n'.join(value)

        print(value)

#$ ____ infos ______________________________________________________________ #


def BCDR_INFO(id, value=''):

    if getattr(verrs.setts, id)():

        title = 'BCDR_INFO'
        width = 75
        len1 = int((width - len(title) - 6 - 10)/2)
        len2 = (width - len(title) - 6- 10) - len1

        print(color(len1*'-' + ' ' + '*'*5 + ' '*2 + title + ' '*2  + '*'*5 + ' '  + len2*'*', 'g'))

        # divide text by new line symbol
        value = str(value).split('\n')
        for i in range(len(value)):
            value[i] = textwrap.fill(str(value[i]), width=width)
        value = '\n'.join(value)

        print(value)


#$ ____ geenral erwin ______________________________________________________ #

def erwin(id, value=''):
    if   id[0]=='e': return BCDR_ERRO(id, value)
    elif id[0]=='w': return BCDR_WARN(id, value)
    elif id[0]=='i': return BCDR_INFO(id, value)

#$ ######################################################################### #
