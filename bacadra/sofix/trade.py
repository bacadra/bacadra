import os
import subprocess

from . import sbase
from ..cunit import cunit


#$ ____ class trade _______________________________________________________ #

class trade:
    sbase = sbase()

    #$$ def --init--
    def __init__(self, cdb='c_main.cdb', name='x_main.dat', active=True):
        self.active    = active
        self.cdb       = cdb
        self.name      = name

        self._data_sto = []
        self._data_del = []
        self._data_def = []


    #$$ def sto
    def sto(self, name, val, comment=None):
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
        return val

    #$$ def defb
    def defb(self, name, val, comment=None):
        if comment:
            comment = '$$ ' + comment + '\n'
        else:
            comment = ''
        self._data_def.append('''#define {0}\n{2}{1}\n#enddef'''.format(name, val, comment))
        return val

    #$$ def defi
    def defi(self, name, val, comment=None):
        if comment:
            comment = '$$ ' + comment + '\n'
        else:
            comment = ''
        self._data_def.append('''#define {0}={1}'''.format(name, val))
        return val

    #$$ def push
    def push(self):

        temp  = os.path.join(
            os.path.dirname(self.cdb),
            os.path.splitext(self.name)[0]
        )

        pathd = temp + '.dat' # main file
        path0 = temp + '.$d0' # plik define
        path1 = temp + '.$d1' # plik sto
        path2 = temp + '.$d2' # plik del

        data0 = '\n'.join(self._data_def)
        data1 = '\n'.join(self._data_sto)
        data2 = '\n'.join(self._data_del)

        if not os.path.exists(os.path.dirname(self.cdb)):
            os.makedirs(os.path.dirname(self.cdb))

        with open(path0, 'w') as f: f.write(data0)
        with open(path1, 'w') as f: f.write(data1)
        with open(path2, 'w') as f: f.write(data2)

        temp = '''
$ --------- set defines ----------------------------------------------------- $
#include "{data0}"

$ --------------------------------------------------------------------------- $
+prog template
head bcdr:pinky
dbg#2 $ debugging mode turn on

$ --------- delete variables ------------------------------------------------ $
#include "{data2}"

$ --------- set variables --------------------------------------------------- $
#include "{data1}"

$ --------------------------------------------------------------------------- $
end
'''[1:-1].format(**{
            'data0':os.path.splitext(self.name)[0]+'.$d0',
            'data1':os.path.splitext(self.name)[0]+'.$d1',
            'data2':os.path.splitext(self.name)[0]+'.$d2'})
        with open(pathd, 'w') as f: f.write(temp)

    #$$ def make
    def make(self):
        self.push()
        code = 'cmd /c pushd "{p0}" & "{p1}" -cdb:"{p2}" "{p3}"'.format(**{
            'p0': os.path.abspath(os.path.dirname(self.cdb)),
            'p1': os.path.join(
                self.sbase._sofi_env,
                self.sbase._sofi_run,
            ).replace('/', '\\'),
            'p2': os.path.basename(self.cdb),
            'p3': self.name})
        subprocess.run(code)
