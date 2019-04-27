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

from . import fpack

from .setts import sinit, tools

#$ ____ class setts ________________________________________________________ #

class setts(sinit):

    def __init__(self):
        self.tools = tools()

    def new(name, doc):
        '''
        name -- code of error/warning/info like e0051
        mname -- method name, like small description
        '''

        setattr(setts, name, lambda self, x=None: self.tools.gst(name, x))
        getattr(setts, name).__doc__ = doc

#$$ ________ general _______________________________________________________ #

    def original(self, value=None):
        '''Show original error menu'''
        return self.tools.gst('original', value)

    def traceback(self, value=None):
        '''Show traceback; work only with custom error msg'''
        return self.tools.gst('traceback', value)



#$$ ________ x0000 tools ___________________________________________________ #

setts.new('e0000', 'bacadra error')

setts.new('e0001', 'setts: Unknow setting')





#$$ ________ x0100 unise ___________________________________________________ #

#$$ ________ x0200 dbase ___________________________________________________ #




#$$ ________ make verrs ____________________________________________________ #

verrs = setts()
verrs.original(False)
verrs.traceback(True)

for key in dir(verrs):
    if key[0] in 'ewi':
        getattr(verrs, key)(True)


#$ ____ errors _____________________________________________________________ #


try:

    from IPython import get_ipython
    ipython = get_ipython()

    def exception_handler(exception_type, exception, traceback):

        if exception_type.__name__[:4]=='BCDR' and not verrs.original():

                if verrs.traceback()==True:
                    print('\n'.join(traceback[:-2]))

                id, exception = str(exception).split('$$!$!$$')

                print(fpack.berwin(
                    mode = exception_type.__name__,
                    code = id,
                    info = exception,
                ))

        else:
            print(ipython.InteractiveTB.stb2text(traceback))

    ipython._showtraceback = exception_handler

except:
    pass

class BCDR(Exception):
    pass

#$ ____ warnings ___________________________________________________________ #

def BCDR_WARN(id, value=''):

    if getattr(verrs.setts, id)():

        print(fpack.berwin(
            mode = 'BCDR',
            code = id,
            info = value,
        ))

#$ ____ infos ______________________________________________________________ #

def BCDR_INFO(id, value=''):

    if getattr(verrs.setts, id)():

        print(fpack.berwin(
            mode = 'BCDR',
            code = id,
            info = value,
        ))

#$ ____ erwin ______________________________________________________________ #

def erwin(id, value=''):
    if id[0]=='e':
        if hasattr(verrs, id):
            if getattr(verrs, id)():
                raise BCDR(id + '$$!$!$$' + value)
        else:
                raise BCDR(id+' (unknow!)' + '$$!$!$$' + value)


    elif id[0]=='w':
        return BCDR_WARN(id, value)

    elif id[0]=='i':
        return BCDR_INFO(id, value)

#$ ######################################################################### #
