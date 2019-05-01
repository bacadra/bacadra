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

from .setts import sinit

#$ ____ class setts ________________________________________________________ #

class setts(sinit):

    _default_mode = {}

    def new(name, mode, doc):
        '''
        name -- code of error/warning/info like e0051
        mname -- method name, like small description
        '''

        setattr(setts, name, lambda self, x=None: self.tools.gst(name, x))
        getattr(setts, name).__doc__ = doc

        setts._default_mode[name] = mode

#$$ ________ general _______________________________________________________ #

    def original(self, value=None):
        '''Show original error menu'''
        return self.tools.gst('original', value)

    def traceback(self, value=None):
        '''Show traceback; work only with custom error msg'''
        return self.tools.gst('traceback', value)



#$$ ________ x0000 tools ___________________________________________________ #

setts.new('e0000', True,  'bacadra error')

setts.new('w0000', True,  'bacadra warning')

setts.new('i0000', True,  'bacadra info')


setts.new('e0001', True, 'BCDR_tools_ERROR_setts_get_unknow')

setts.new('e0066', True, 'BCDR_tools_ERROR_Translation_Not_Provided')

setts.new('e0071', False, 'BCDR_tools_ERROR_Letters_not_occur')


setts.new('w0066', True, 'BCDR_tools_WARN_Translation_Not_Provided')

setts.new('w0071', True, 'BCDR_tools_WARN_Letters_not_occur')


#$$ ________ x0100 unise ___________________________________________________ #

#$$ ________ x0200 dbase ___________________________________________________ #

setts.new('e0201', True, 'BCDR_dbase_ERROR_Open_Database')

setts.new('e0211', True, 'BCDR_dbase_ERROR_Parse_Type')


setts.new('w0202', True, 'BCDR_dbase_WARN_Already_Closed')

#$$ ________ x0600 pinky:texme _____________________________________________ #

setts.new('e0611', True, 'BCDR_pinky_texme_ERROR_Header_Level')

setts.new('e0621', True, 'BCDR_pinky_texme_ERROR_Type_Check')

setts.new('e0622', True, 'BCDR_pinky_texme_ERROR_String_Selector')

setts.new('e0623', True, 'BCDR_pinky_texme_ERROR_Invalid_Key')

setts.new('e0625', True, 'BCDR_pinky_texme_ERROR_unknow_mode_page')

setts.new('e0681', True, 'BCDR_pinky_texme_ERROR_Path_Error')

setts.new('e0682', True, 'BCDR_pinky_texme_ERROR_Evaluate')


setts.new('w0681', True, 'BCDR_pinky_texme_WARN_Path_Error')

setts.new('w0631', True, 'BCDR_pinky_texme_WARN_Scope_External')

#$$ ________ x0900 sofix ___________________________________________________ #

setts.new('i0915', True, 'BCDR_sofix_INFO_mass')


#$$ ________ make verrs ____________________________________________________ #

verrs = setts()
verrs.original(False)
verrs.traceback(True)

for key in dir(verrs):
    if key[0] in 'ewi':
        getattr(verrs, key)(setts._default_mode[key])


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

#$ ____ erwin ______________________________________________________________ #

def erwin(id, value='', head=True, bott=True):

    if id[0]=='e':
        if hasattr(verrs, id):
            if getattr(verrs, id)():
                raise BCDR(id + '$$!$!$$' + value)
        else:
                raise BCDR(id+' (unknow!)' + '$$!$!$$' + value)

    elif id[0]=='w' or id[0]=='i':
        if hasattr(verrs, id):
            if getattr(verrs, id)():
                print(fpack.berwin(
                    mode = 'BCDR',
                    code = id,
                    info = value,
                    head = head,
                    bott = bott,
                ))

        else:
            print(fpack.berwin(
                mode = 'BCDR',
                code = id+' (unknow!)',
                info = value,
                head = head,
                bott = bott,
            ))

    else:
        raise BCDR('e0000'+'$$!$!$$' +
            "Unknow erwin mode!\nTip: Please use only 'e', 'w' or 'i'")




#$ ######################################################################### #
