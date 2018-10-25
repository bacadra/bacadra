#!/usr/bin/python
# -*- coding: UTF-8 -*-
True
#$ ____ import _____________________________________________________________ #
#$$ ________ standard library ______________________________________________ #

import os
import subprocess
import glob
from ..cunit import cunit

#$$ ________ third party library ___________________________________________ #

from . import wgraf
from .simpl import simpl


# #$$ ________ local library/application _____________________________________ #
#
#
#
# #$ ____ global variables ___________________________________________________ #
#
#
# sofi_env = 'c:/Program Files/SOFiSTiK/2018/SOFiSTiK 2018/'
# sofi_wps = 'wps.exe'
# sofi_sps = 'sps.exe'
# sofi_urs = 'ursula.exe'
# magi_env = 'c:/Program Files/ImageMagick-7.0.7-Q16'
# magi_mck = 'magick.exe'
#
#
# #$ ____ class trade _______________________________________________________ #
#
# class trade:
#     #$$ def --init--
#     def __init__(self, project='sofi', dat='i_main.dat', cdb='p_main.cdb', active=True):
#         self._xdata_sto = []
#         self._xdata_del = []
#         self._xdata_def = []
#         self.active=active
#         self.project = project
#         self.cdb = cdb
#         self.dat = dat
#
#     #$$ def sto
#     def sto(self, name, val, comment=None):
#         if comment:
#             comment = ' $ ' + comment
#         else:
#             comment = ''
#         if type(val) == cunit:
#             val = val.drop()
#         elif type(val) == list:
#             val = str(val)[1:-1].replace(' ','')
#         self._xdata_del.append('del#{0}'.format(name))
#         self._xdata_sto.append('sto#{0} {1}{2}'.format(name, val, comment))
#         return val
#
#     #$$ def defb
#     def defb(self, name, val, comment=None):
#         if comment:
#             comment = '$$ ' + comment + '\n'
#         else:
#             comment = ''
#         self._xdata_def.append('''#define {0}\n{2}{1}\n#enddef'''.format(name, val, comment))
#         return val
#
#     #$$ def defi
#     def defi(self, name, val, comment=None):
#         if comment:
#             comment = '$$ ' + comment + '\n'
#         else:
#             comment = ''
#         self._xdata_def.append('''#define {0}={1}'''.format(name, val))
#         return val
#
#     #$$ def push
#     def push(self):
#         pathd = os.path.join(self.project, self.dat)
#         temp  = os.path.join(self.project, os.path.splitext(self.dat)[0])
#         path0 = temp + '.$d0' # plik define
#         path1 = temp + '.$d1' # plik sto
#         path2 = temp + '.$d2' # plik del
#
#         data0 = '\n'.join(self._xdata_def)
#         data1 = '\n'.join(self._xdata_sto)
#         data2 = '\n'.join(self._xdata_del)
#
#         if not os.path.exists(self.project):
#             os.makedirs(self.project)
#
#         with open(path0, 'w') as f: f.write(data0)
#         with open(path1, 'w') as f: f.write(data1)
#         with open(path2, 'w') as f: f.write(data2)
#
#         temp = '''
# $ --------- set defines ----------------------------------------------------- $
# {data0}
#
# $ --------------------------------------------------------------------------- $
# +prog template
# head bcdr:pinky
# dbg#2 $ debugging mode turn on
#
# $ --------- delete variables ------------------------------------------------ $
# {data2}
#
# $ --------- set variables --------------------------------------------------- $
# {data1}
#
# $ --------------------------------------------------------------------------- $
# end
# '''[1:-1].format(**{
#             'data0':data0,
#             'data1':data1,
#             'data2':data2})
#         with open(pathd, 'w') as f: f.write(temp)
#
#     #$$ def make
#     def make(self):
#         self.push()
#         code = 'cmd /c pushd "{p0}" & "{p1}" -cdb:"{p2}" "{p3}"'.format(**{
#             'p0': os.path.abspath(self.project),
#             'p1': os.path.join(sofi_env, sofi_sps).replace('/', '\\'),
#             'p2': self.cdb,
#             'p3': self.dat})
#         subprocess.run(code)
#
#
#
# #$ ____ class wgraf _______________________________________________________ #
#
# class wgraf:
#     def __init__(self, project, sinter=[], delete=True, output=None, active=False):
#         self.active = active
#         self.project = project
#         self.cdb = True
#         self.sinter = sinter
#         self.delete = True
#         self.output = project if output is None else output
#
#         self.make()
#
#     def wing(self, name):
#         code = 'cmd /c pushd "{p0}" & "{p1}" -cdb:"{p2}" "{p3}"'.format(**{
#             'p0': os.path.abspath(self.path),
#             'p1': os.path.join(sofi_env, sofi_sps).replace('/', '\\'),
#             'p2': self.cdb,
#             'p3': name})
#         subprocess.run(code)
#
#     def urs_to_pdf(self, name):
#         sofi_env_2016 = r'c:\Program Files\SOFiSTiK\2016\ANALYSIS_33_X64'
#         if os.path.exists(sofi_env_2016):
#             sofi_env_local = sofi_env_2016
#         else:
#             sofi_env_local = sofi_env
#         code = 'cmd /c pushd "{p0}" & "{p1}" "{p2}" -printto:"PDF" -picture:all'.format(**{
#             'p0': os.path.abspath(self.path),
#             'p1': os.path.join(sofi_env_local, sofi_urs).replace('/', '\\'),
#             'p2': os.path.splitext(name)[0]+'.plb'})
#         subprocess.run(code)
#
#     def pdf_to_img(self, name):
#         if not os.path.isdir(os.path.abspath(self.output)):
#             os.makedirs(self.output)
#         code = 'cmd /c pushd "{p0}" & "{p1}" -density 300 "{p2}" -quality 100 -scene 1 "{p3}-%03d.jpg"'.format(**{
#             'p0': self.path,
#             'p1': os.path.join(magi_env, magi_mck),
#             'p2': os.path.splitext(name)[0]+'.pdf',
#             'p3': os.path.join(os.path.abspath(self.output), os.path.splitext(name)[0])})
#         subprocess.run(code)
#
#     def img_convert(self, name, size):
#         if size.lower() == 'h':
#             size = '2023x1296+289+289'
#         elif size.lower() == 'v':
#             size = '2023x2668+289+289'
#         elif size.lower() == 's':
#             size = '2139x1266+229+242'
#         else:
#             raise ValueError('undefined graphic size')
#         filepattern = os.path.join(self.output, os.path.splitext(name)[0])+"-*.jpg"
#         for file in glob.glob(filepattern):
#             code = 'cmd /c pushd "{p0}" & "{p1}" "{p2}" -crop {p3} -fuzz 15% -fill white -opaque "RGB(192,192,192)" "{p2}"'.format(**{
#                 'p0': self.output,
#                 'p1': os.path.join(magi_env, magi_mck),
#                 'p2': os.path.basename(file),
#                 'p3': size})
#             subprocess.run(code)
#
#     def delete_old_files(self, name):
#         filepattern = os.path.join(self.output, os.path.splitext(name)[0])+"-*.jpg"
#         for file in glob.glob(filepattern):
#             os.remove(file)
#
#     def del_pdf(self, name):
#         os.remove(os.path.splitext(name)[0]+'.pdf')
#
#
#     def analyse(self):
#         self.cdb = os.path.basename(self.project)
#         self.path = os.path.dirname(self.project)
#
#     def make(self):
#         if self.active:
#             self.analyse()
#             for data in self.sinter:
#                 if data[0]:
#                     self.wing(data[2])
#                     self.urs_to_pdf(data[2])
#                     if self.delete:
#                         self.delete_old_files(data[2])
#                     self.pdf_to_img(data[2])
#                     self.img_convert(data[2], data[1])
#                     # self.del_pdf(data[2])
#
#
#
#
#
#
#
# # import ctypes
# #
# # dll_path = 'C:\\Program Files\\SOFiSTiK\\2018\\SOFiSTiK 2018\\interface\\64bit'
# # sys.path.append(dll_path)
# # sofi_dll = ctypes.cdll.LoadLibrary('cdb_w50_x64.dll')
# #
# # os.path.join(dll_path, 'cdb_w_edu50_x64.dll')
#
#
#
# # siio.sto('b', 5, 'test1')
# # siio.sto('a', 5)
# #
# # siio.defb('test', '0 0 0\n1 1 1', 'kom1')
# # siio.defi('test', '5', 'kom1')
