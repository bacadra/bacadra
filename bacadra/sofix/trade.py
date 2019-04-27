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

#$ ######################################################################### #

#$ ____ import _____________________________________________________________ #

import os
import subprocess
from ..unise import unise
from ..tools.setts import sinit
from . import verrs

#$ ____ class setts ________________________________________________________ #

class setts(sinit):

#$$ ________ def active ____________________________________________________ #

    def active(self, value=None, check=None):
        return self.tools.sgc('active', value, check)

#$$ ________ def name ______________________________________________________ #

    def name(self, value=None, check=None):
        return self.tools.sgc('name', value, check)

#$$ ________ def project ___________________________________________________ #

    def project(self, folder_path=None, cdb_name=None, check=None, mode='p'):

        if type(check)==str:
            return self.tools.sgc(name='sofistik:'+check,
                value=eval(check), check=True)


        folder_path = self.tools.sgc(name='project:folder_path', value=folder_path, check=check)

        if folder_path==True:
             folder_path=self.tools.root.core.sofix.sbase.setts.project(
                mode='p')


        cdb_name = self.tools.sgc(name='project:cdb_name', value=cdb_name, check=check)

        if cdb_name==True:
             cdb_name=self.tools.root.core.sofix.sbase.setts.project(
                mode='c')

        if folder_path and cdb_name:

            if   mode=='pc': return os.path.join(folder_path, cdb_name)

            elif mode=='p' : return folder_path

            elif mode=='c' : return cdb_name


#$ ____ class trade _______________________________________________________ #

class trade:

    setts = setts()

    setts.active(True)

    setts.name('input.dat')

    setts.project(folder_path=True, cdb_name=True)


#$$ ________ def __init __ _________________________________________________ #

    def __init__(self, core=None):

        self.core = core

        self.setts = setts(master=self.setts.tools, root=self)

        self._data_sto = []
        self._data_del = []
        self._data_def = []


#$$ ________ def sto _______________________________________________________ #

    def sto(self, name, val, comment=None, active=None):

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        if comment:
            comment = ' $ ' + comment

        else:
            comment = ''


        if type(val) == unise:
            val = val.drop()

        elif type(val) == list:
            val = str(val)[1:-1].replace(', ',' $$\n')

        self._data_del.append('del#{0}'.format(name))

        self._data_sto.append('sto#{0} {1}{2}'.format(name, val, comment))


#$$ ________ def defb ______________________________________________________ #

    def defb(self, name, val, comment=None, active=None):

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        if comment:
            comment = '$$ ' + comment + '\n'
        else:
            comment = ''
        self._data_def.append('''#define {0}\n{2}{1}\n#enddef'''.format(name, val, comment))


#$$ ________ def defi ______________________________________________________ #

    def defi(self, name, val, comment=None, active=None):

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        if comment:
            comment = '$$ ' + comment + '\n'
        else:
            comment = ''
        self._data_def.append('''#define {0}={1}'''.format(name, val))


#$$ ________ def push ______________________________________________________ #

    def push(self, active=None):

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        temp  = os.path.join(
            self.setts.project(mode='p'),
            '.'.join(os.path.splitext(self.setts.name())[:-1])
        )

        pathd = temp + '.dat' # main file
        path0 = temp + '.$d0' # plik define
        path1 = temp + '.$d1' # plik sto
        path2 = temp + '.$d2' # plik del

        data0 = '\n'.join(self._data_def)
        data1 = '\n'.join(self._data_sto)
        data2 = '\n'.join(self._data_del)
        self._data_def,self._data_sto,self._data_del = [],[],[]

        temp = self.setts.project()
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
            'name' :self.setts.name(),
            'data0':'.'.join(os.path.splitext(self.setts.name())[:-1])+'.$d0',
            'data1':'.'.join(os.path.splitext(self.setts.name())[:-1])+'.$d1',
            'data2':'.'.join(os.path.splitext(self.setts.name())[:-1])+'.$d2'})
        else:
            temp = ''

        with open(pathd, 'w') as f: f.write(temp)

#$$ ________ def make ______________________________________________________ #

    def make(self, active=None):

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        code = 'cmd /c pushd "{p0}" & "{p1}" -cdb:"{p2}" "{p3}"'.format(**{
            'p0': os.path.abspath(self.setts.project(mode='p')),
            'p1': self.core.sofix.sbase.setts.sofistik(mode='ep').replace('/', '\\'),
            'p2': self.setts.project(mode='c'),
            'p3': self.setts.name()})

        subprocess.run(code)

#$ ######################################################################### #
