'''
------------------------------------------------------------------------------
***** (trade) variable sofi x bcdr *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ____ import _____________________________________________________________ #

import os
import subprocess
from ..cunit import cunit
from ..tools.setts import settsmeta
from . import verrs

#$ ____ class setts ________________________________________________________ #

class setts(settsmeta):

    _self = None # here will be placed self instance

#$$ ________ def active ____________________________________________________ #

    __active = True

    @property
    def active(self):
            return self.__active

    @active.setter
    def active(self, value):
        '''
        User can deactive all methods, then methods will exit at the begging.
        '''

        if type(value) is not bool:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'bool')

        if self.__save__: self.__active = value
        else:             self.__temp__ = value


#$$ ________ def name ______________________________________________________ #

    __name = 'x_main.dat'

    @property
    def name(self):
            return self.__name

    @name.setter
    def name(self, value):

        if self.__save__: self.__name = value
        else:             self.__temp__ = value

#$$ ________ def project ___________________________________________________ #

    __project = None

    @property
    def project(self):
        if self._self.core and not self.__project:
            return self._self.core.sofix.sbase.setts.project
        else:
            return self.__project

    @project.setter
    def project(self, value):
        if self.__save__: self.__project = value
        else:             self.__temp__ = value


#$$ ________ def cdb_name __________________________________________________ #

    __cdb_name = None

    @property
    def cdb_name(self):
        if self._self.core and not self.__cdb_name:
            return self._self.core.sofix.sbase.setts.cdb_name
        else:
            return self.__cdb_name

    @cdb_name.setter
    def cdb_name(self, value):

        if self.__save__: self.__cdb_name = value
        else:             self.__temp__ = value



#$ ____ class trade _______________________________________________________ #

class trade:

    # class setts
    setts = setts('setts', (setts,), {})

#$$ ________ def __init __ _________________________________________________ #

    def __init__(self, core=None):

        self.core = core

        # object setts
        self.setts = self.setts('setts',(),{'_self':self})

        self._data_sto = []
        self._data_del = []
        self._data_def = []


#$$ ________ def sto _______________________________________________________ #

    def sto(self, name, val, comment=None, active=None):

        # if user want to overwrite global active atribute
        if not self.setts.check_loc('active', active): return

        if comment:
            comment = ' $ ' + comment
        else:
            comment = ''
        if type(val) == cunit:
            val = val.drop()
        elif type(val) == list:
            val = str(val)[1:-1].replace(', ',' $$\n')
        self._data_del.append('del#{0}'.format(name))
        self._data_sto.append('sto#{0} {1}{2}'.format(name, val, comment))


#$$ ________ def defb ______________________________________________________ #

    def defb(self, name, val, comment=None, active=None):

        # if user want to overwrite global active atribute
        if not self.setts.check_loc('active', active): return

        if comment:
            comment = '$$ ' + comment + '\n'
        else:
            comment = ''
        self._data_def.append('''#define {0}\n{2}{1}\n#enddef'''.format(name, val, comment))


#$$ ________ def defi ______________________________________________________ #

    def defi(self, name, val, comment=None, active=None):

        # if user want to overwrite global active atribute
        if not self.setts.check_loc('active', active): return

        if comment:
            comment = '$$ ' + comment + '\n'
        else:
            comment = ''
        self._data_def.append('''#define {0}={1}'''.format(name, val))


#$$ ________ def push ______________________________________________________ #

    def push(self, active=None):

        # if user want to overwrite global active atribute
        if not self.setts.check_loc('active', active): return

        temp  = os.path.join(
            self.core.sofix.sbase.setts.project,
            '.'.join(os.path.splitext(self.setts.name)[:-1])
        )

        pathd = temp + '.dat' # main file
        path0 = temp + '.$d0' # plik define
        path1 = temp + '.$d1' # plik sto
        path2 = temp + '.$d2' # plik del

        data0 = '\n'.join(self._data_def)
        data1 = '\n'.join(self._data_sto)
        data2 = '\n'.join(self._data_del)
        self._data_def,self._data_sto,self._data_del = [],[],[]

        temp = self.core.sofix.sbase.setts.project
        if not os.path.exists(temp):
            os.makedirs(temp)

        with open(path0, 'w') as f: f.write(data0)
        with open(path1, 'w') as f: f.write(data1)
        with open(path2, 'w') as f: f.write(data2)

        if len(data0)>0 or len(data1)>0 or len(data2)>0:
            temp = '''
$ --------- set defines ----------------------------------------------------- $
#include "{data0}"

$ --------------------------------------------------------------------------- $
+prog template
head bcdr : {name}
dbg#2 $ debugging mode turn on

$ --------- delete variables ------------------------------------------------ $
#include "{data2}"

$ --------- set variables --------------------------------------------------- $
#include "{data1}"

$ --------------------------------------------------------------------------- $
end
'''[1:-1].format(**{
            'name' :self.setts.name,
            'data0':'.'.join(os.path.splitext(self.setts.name)[:-1])+'.$d0',
            'data1':'.'.join(os.path.splitext(self.setts.name)[:-1])+'.$d1',
            'data2':'.'.join(os.path.splitext(self.setts.name)[:-1])+'.$d2'})
        else:
            temp = ''

        with open(pathd, 'w') as f: f.write(temp)

#$$ ________ def make ______________________________________________________ #

    def make(self, active=None):

        # if user want to overwrite global active atribute
        if not self.setts.check_loc('active', active): return

        code = 'cmd /c pushd "{p0}" & "{p1}" -cdb:"{p2}" "{p3}"'.format(**{
            'p0': os.path.abspath(self.core.sofix.sbase.setts.project),
            'p1': os.path.join(
                    self.core.sofix.sbase.setts.sofi_env,
                    self.core.sofix.sbase.setts.sofi_run,
                  ).replace('/', '\\'),
            'p2': self.core.sofix.sbase.setts.cdb_name,
            'p3': self.setts.name})

        subprocess.run(code)