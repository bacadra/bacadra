'''
------------------------------------------------------------------------------
***** (v)arious (err)ors for global spac(e) *****
==============================================================================

There are three types of messages:
- errors
- warnings
- infos

Thera are class which should be inherited to all modules.

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''


from .color import colored

#$ ____ errors _____________________________________________________________ #

import sys

try:
    ipython = get_ipython() # tutaj bedzie error...

    #$ ____ def exception_handler ______________________________________________ #

    def exception_handler(exception_type, exception, traceback):
        # print("%s: %s" % (exception_type.__name__, exception), file=sys.stderr)
        if exception_type.__name__[:4]=='BCDR' and not verrs.original:
                if verrs.traceback==True:
                    print('\n'.join(traceback[:-2]))
                print('---------------------------------------------------------------------------\n'
                    '*****', exception_type.__name__,':',__exname__, '*****\n\033[1;30;1m'+str(exception),
                    file=sys.stderr)
        else:
            print(ipython.InteractiveTB.stb2text(traceback))

    ipython._showtraceback = exception_handler
except:
    pass

__exname__ = None

class __meta_1(type):
    def __call__(self,code,value=''):
        if getattr(verrs, code)==True:
            global __exname__
            __exname__ = code
            raise BCDR_ERROR(value)

class BCDR_ERROR(Exception):
    pass

class BCDR_ERRS(BCDR_ERROR,metaclass=__meta_1):
    pass


#$ ____ warnings ___________________________________________________________ #

class __meta_2(type):
    def __call__(self,code, value=''):
        if getattr(verrs, code)==True:
            print(colored('---------------------------------------------------------------------------\n''***** '+self.__name__+' : '+code+' *****\n', self.__color__) +'\033[1;30;1m'+str(value))

class BCDR_WARN(metaclass=__meta_2):
    __color__ = 'yellow'

#$ ____ infos ______________________________________________________________ #

class BCDR_INFO(metaclass=__meta_2):
    __color__ = 'green'



#$ ____ class verrs ________________________________________________________ #

class __meta_3(type):

    #$$ def __repr__
    def __repr__(self):

        data_e = [colored('---------------------------------------------------------------------------\n''***** bacadra verrs settings: errors *****', 'red')]

        data_w = [colored('\n\n---------------------------------------------------------------------------\n''***** bacadra verrs settings: warnings *****', 'yellow')]

        data_i = [colored('\n\n---------------------------------------------------------------------------\n''***** bacadra verrs settings: infos *****', 'green')]

        for key,val in verrs.__dict__.items():
            if key[0]=='e':
                data_e.append('> {:14s} : {}'.format(key, val))
            elif key[0]=='w':
                data_w.append('> {:14s} : {}'.format(key, val))
            elif key[0]=='i':
                data_i.append('> {:14s} : {}'.format(key, val))

        return str(
            '\n'.join(data_e)+'\n'.join(data_w)+'\n'.join(data_i),
        )

    #$$ def __setattr__
    def __setattr__(self, name, value):
        '''
        Method do not allow create new variable in class. It is provide more control over user correctly or spell-checker.
        '''

        if not hasattr(self, name):
            raise AttributeError(f"Creating new attributes <{name}> is not allowed!")

        type.__setattr__(self, name, value)



class verrs(metaclass=__meta_3):


#$$ ________ e- errors _____________________________________________________ #


    traceback = True # add traceback before custom exception BCDR
    original = False # add traceback before custom exception BCDR


    # 00xx - tools
    e0011 = True # BCDR_tools_ERROR_Parse_Type


    # 01xx - dbase
    e0101 = True # BCDR_dbase_ERROR_Open_Database
    e0110 = True # BCDR_dbase_ERROR_General .. transaction exe
    e0111 = True # BCDR_dbase_ERROR_General .. unsupported journal mode


    # 05xx - cunit
    e0511 = True # BCDR_cunit_ERROR_Incompatible
    e0512 = True # BCDR_cunit_ERROR_Undefined_Operator
    e0513 = True # BCDR_cunit_ERROR_System_Exists
    e0514 = True # BCDR_cunit_ERROR_Units_in_System
    e0515 = True # BCDR_cunit_ERROR_Already_Exists
    e0516 = True # BCDR_cunit_ERROR_Cover
    e0517 = True # BCDR_cunit_ERROR_General.. about power to cunit


    # 06xx - pinky texme
    e0611 = True # BCDR_pinky_texme_ERROR_Header_Level
    e0621 = True # BCDR_pinky_texme_ERROR_Type_Check
    e0622 = True # BCDR_pinky_texme_ERROR_String_Selector
    e0623 = True # BCDR_pinky_texme_ERROR_Invalid_Key
    e0624 = True # BCDR_pinky_texme_ERROR_General.. Atribute "inpath" do not set
    e0625 = True # BCDR_pinky_texme_ERROR_General.. Unknow mode of page method
    e0626 = True # BCDR_pinky_texme_ERROR_General.. Unknow float mode
    e0627 = True # BCDR_pinky_texme_ERROR_General.. Unrecognized prefix element
    e0681 = True # BCDR_pinky_texme_ERROR_Path_Error
    e0682 = True # BCDR_pinky_texme_ERROR_Evaluate, look into regme


    # 07xx - pinky rstme
    e0711 = True # BCDR_pinky_rstme_ERROR_Header_Level
    e0721 = True # BCDR_pinky_rstme_ERROR_Type_Check
    e0722 = True # BCDR_pinky_rstme_ERROR_String_Selector


    # 08xx - pinky docme


#$$ ________ w- warnings ___________________________________________________ #


    # 01xx - dbase
    w0121 = True # BCDR_dbase_WARN_Already_Closed


    # 06xx - pinky texme
    w0631 = True # BCDR_pinky_texme_WARN_Scope_External
    w0681 = True # BCDR_pinky_texme_WARN_Path_Error


#$$ ________ i- infos ______________________________________________________ #

    # 00xx - project
    i0011 = True # BCDR_pinky_texme_INFO_Scope

    # 06xx - pinky texme
    i0611 = True # BCDR_pinky_texme_INFO_Scope


