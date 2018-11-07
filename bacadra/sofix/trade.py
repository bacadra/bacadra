import os
from . import sbase
from ..cunit import cunit


#$ ____ class trade _______________________________________________________ #

class trade:
    sbase = sbase()

    #$$ def --init--
    def __init__(self, project='sofi', dat='i_main.dat', cdb='p_main.cdb', active=True):
        self._xdata_sto = []
        self._xdata_del = []
        self._xdata_def = []
        self.active=active
        self.project = project
        self.cdb = cdb
        self.dat = dat

    #$$ def sto
    def sto(self, name, val, comment=None):
        if comment:
            comment = ' $ ' + comment
        else:
            comment = ''
        if type(val) == cunit:
            val = val.drop()
        elif type(val) == list:
            val = str(val)[1:-1].replace(' ','')
        self._xdata_del.append('del#{0}'.format(name))
        self._xdata_sto.append('sto#{0} {1}{2}'.format(name, val, comment))
        return val

    #$$ def defb
    def defb(self, name, val, comment=None):
        if comment:
            comment = '$$ ' + comment + '\n'
        else:
            comment = ''
        self._xdata_def.append('''#define {0}\n{2}{1}\n#enddef'''.format(name, val, comment))
        return val

    #$$ def defi
    def defi(self, name, val, comment=None):
        if comment:
            comment = '$$ ' + comment + '\n'
        else:
            comment = ''
        self._xdata_def.append('''#define {0}={1}'''.format(name, val))
        return val

    #$$ def push
    def push(self):
        pathd = os.path.join(self.project, self.dat)
        temp  = os.path.join(self.project, os.path.splitext(self.dat)[0])
        path0 = temp + '.$d0' # plik define
        path1 = temp + '.$d1' # plik sto
        path2 = temp + '.$d2' # plik del

        data0 = '\n'.join(self._xdata_def)
        data1 = '\n'.join(self._xdata_sto)
        data2 = '\n'.join(self._xdata_del)

        if not os.path.exists(self.project):
            os.makedirs(self.project)

        with open(path0, 'w') as f: f.write(data0)
        with open(path1, 'w') as f: f.write(data1)
        with open(path2, 'w') as f: f.write(data2)

        temp = '''
$ --------- set defines ----------------------------------------------------- $
{data0}

$ --------------------------------------------------------------------------- $
+prog template
head bcdr:pinky
dbg#2 $ debugging mode turn on

$ --------- delete variables ------------------------------------------------ $
{data2}

$ --------- set variables --------------------------------------------------- $
{data1}

$ --------------------------------------------------------------------------- $
end
'''[1:-1].format(**{
            'data0':data0,
            'data1':data1,
            'data2':data2})
        with open(pathd, 'w') as f: f.write(temp)

    #$$ def make
    def make(self):
        self.push()
        code = 'cmd /c pushd "{p0}" & "{p1}" -cdb:"{p2}" "{p3}"'.format(**{
            'p0': os.path.abspath(self.project),
            'p1': os.path.join(sofi_env, sofi_sps).replace('/', '\\'),
            'p2': self.cdb,
            'p3': self.dat})
        subprocess.run(code)
