'''
------------------------------------------------------------------------------
***** create La(TeX) (m)assive (e)nvelope *****
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
import inspect
import shutil
import subprocess
import importlib.util

from IPython.display import Image, Latex, HTML, Markdown, display

from ...tools.fpack import translate
from ...tools.setts import sinit

from . import verrs
from .regme import regme



#$ ____ class setts ________________________________________________________ #

class setts(sinit):

#$$ ________ def force_copy ________________________________________________ #

    def force_copy(self, value=None, check=None):
        '''
        Force update of template, if true new files will be copy indepened of existsing .tex.bak file.
        '''

        return self.tools.sgc('force_copy', value, check)


#$$ ________ def path ______________________________________________________ #

    def path(self, folder_path=None, check=None):
        '''
        Output path related to actual state of kernel. In mostly case it refer to input file. The existing of folder will be checked during template coping.
        '''

        return self.tools.sgc('path', folder_path, check)



#$$ ________ def source ____________________________________________________ #

    def source(self, folder_path=None, filename=None, check=None, mode='pn'):
        '''

        eg.

        folder_path==None, filename==None, check==None, mode==pn:
            return joined path

        folder_path==None, filename==None, check==None, mode==p or n:
            return path or name

        folder_path!=None, filename!=None, check==None, mode...
            set path, set name

        folder_path!=None, filename!=None, check==True, mode==pn:
            return joined path with new value

        '''


        folder_path = self.tools.sgc('source:folder_path', folder_path, check)

        filename    = self.tools.sgc('source:filename'   , filename, check)

        if folder_path and filename:

            if   mode=='pn': return os.path.join(folder_path, filename)

            elif mode=='p' : return folder_path

            elif mode=='n' : return filename



#$$ ________ def template __________________________________________________ #

    def template(self, name=None, cave=None, filename=None, check=None):

        cave = self.tools.sgc('template:cave', cave, check)

        if name:

            self.source(folder_path=os.path.join(
                cave, name), filename=filename)


            # load external methods depend on template

            path = self.source(filename='main.py', check=True)

            spec = importlib.util.spec_from_file_location("external", path)

            external = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(external)

            if self.tools.root==None:
                obj = texme

            else:
                obj = self.tools.root

            obj.tmp = external.tmp(obj)



#$$ ________ def keys ______________________________________________________ #

    def keys(self, data={}, check=None, **kwargs):

        if check==None: check=self.tools.check

        kwargs.update(data) ; data = kwargs

        if check==False:

            if 'keys' not in self.tools.data: self.tools.data['keys'] = {}

            self.tools.data['keys'].update(data)

        elif check==True:

            return {**self.tools.get('keys'), **data}

        elif check in data:

            return data[check]

        else:

            return self.tools.get('keys')[check]


#$$ ________ def echo ______________________________________________________ #

    def echo(self, code=None, check=None):
        '''
        Atribute <echo> set the output of base methods in texme class. It provide letters interface "hmpt" which can turn on/off

        > "h" -- colorful html header,
        > "m" -- rendered latex math equation,
        > "p" -- rendered picture with constant width,
        > "t" -- rendered tables (don't work yet),
        > "c" -- code cell (don't work yet),
        > "x" -- plain tex code which will be included into tex document.

        User can type value as True then will be set "hmp" configuration or False then no output will be produced.
        '''

        if   code==True : code='hmp'
        elif code==False: code=''

        return self.tools.sgc(name='echo', value=code, check=check)


#$$ ________ def inherit ________________________________________________ #

    def inherit(self, value=None, check=None):
        '''
        If true then code is returned, if false code is added to buffer.
        '''

        return self.tools.sgc('inherit', value, check)


#$$ ________ def active ____________________________________________________ #

    def active(self, value=None, check=None):
        return self.tools.sgc('active', value, check)


#$$ ________ def autolabel _________________________________________________ #

    def autolabel(self, code=None, check=None):
        '''
        label is dict with dew substitute labels types.
        h -- header
        p -- picture
        f -- file
        c -- code
        '''

        if   code==True : code='p'
        elif code==False: code=''

        return self.tools.sgc(name='autolabel', value=code, check=check)


#$$ ________ def re ________________________________________________________ #

    def re(self, xt=None, ht=None, pc=None, mt=None, me=None, mo=None, tc=None, td=None, ce=None, cc=None, fc=None, check=None):
        '''
        xt  - text    + text             | item + text
        ht  - head    + text
        pc  - picture + caption
        mt  - math    + text             | item + math
        me  - math    + equation         | item + math
        mo  - math    + echo             | item + math
        tc  - table   + caption
        td  - table   + data & header
        ce  - code    + code
        cc  - code    + caption
        fc  - file    + caption
        '''

        if type(check)==str:
            return self.tools.sgc(name='re:'+check,
                value=eval(check), check=True)

        if xt!=None: self.tools.sgc(name='re:xt', value=xt, check=False)
        if ht!=None: self.tools.sgc(name='re:ht', value=ht, check=False)
        if pc!=None: self.tools.sgc(name='re:pc', value=pc, check=False)
        if mt!=None: self.tools.sgc(name='re:mt', value=mt, check=False)
        if me!=None: self.tools.sgc(name='re:me', value=me, check=False)
        if mo!=None: self.tools.sgc(name='re:mo', value=mo, check=False)
        if tc!=None: self.tools.sgc(name='re:tc', value=tc, check=False)
        if td!=None: self.tools.sgc(name='re:td', value=td, check=False)
        if ce!=None: self.tools.sgc(name='re:ce', value=ce, check=False)
        if cc!=None: self.tools.sgc(name='re:cc', value=cc, check=False)
        if fc!=None: self.tools.sgc(name='re:fc', value=fc, check=False)

#$$ ________ def float _____________________________________________________ #

    def float(self, pic=None, tab=None, check=None):
        '''
        p -- picture
        t -- table
        '''

        if type(check)==str:
            return self.tools.sgc(name='float:'+check,
                value=eval(check), check=True)

        if pic!=None: self.tools.sgc(name='float:pic', value=pic, check=False)
        if tab!=None: self.tools.sgc(name='float:tab', value=tab, check=False)



#$$ ________ def picset ____________________________________________________ #

    def picset(self, root=None, display_width=None, check=None):

        if type(check)==str:
            return self.tools.sgc(name='picset:'+check,
                value=eval(check), check=True)

        if root !=None: self.tools.sgc(name='picset:root' , value=root , check=False)
        if display_width!=None: self.tools.sgc(name='picset:display_width', value=display_width, check=False)

#$$ ________ def headset ___________________________________________________ #

    def headset(self, inc=None, check=None):

        if type(check)==str:
            return self.tools.sgc(name='headset:'+check,
                value=eval(check), check=True)

        if inc!=None: self.tools.sgc(name='headset:inc' , value=inc , check=False)

#$$ ________ def itemset ___________________________________________________ #

    def itemset(self, lvl=None, width=None, check=None):

        if type(check)==str:
            return self.tools.sgc(name='itemset:'+check,
                value=eval(check), check=True)

        if lvl!=None  : self.tools.sgc(name='itemset:lvl'  , value=lvl  , check=False)
        if width!=None: self.tools.sgc(name='itemset:width', value=width, check=False)



#$$ ________ def fclib _____________________________________________________ #

    def fclib(self, name=None, id=None, cave=None, check=None):
        '''
        File of main tex document in inpath folder.
        '''

        cave = self.tools.sgc('fclib:cave', cave, check)

        if name:

            path = os.path.join(cave, name+'.py')

            spec = importlib.util.spec_from_file_location("fclib", path)

            external = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(external)

            if self.tools.root==None:
                obj = texme

            else:
                obj = self.tools.root


            # simple load single lib
            if id==None:
                obj.lib = external.lib(obj)

            # create dict of libs
            else:
                if type(obj.lib)!=dict: obj.lib = {}

                obj.lib[id] = external.lib(obj)












# #$$ ________ def lststyle ________________________________________________ #
#
#     def lststyle(self, value=None, check=None, reset=None):
#         if value!=None and not type(value)==str:
#             verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'str')
#         return self.tools.gst('lststyle', value, check, reset)
#
#     __lststyle = 'bcdr1'


# #$$ ________ def lib _______________________________________________________ #
#
#     def fclib(self, id, path=None, root=True):
#         '''
#         File of main tex document in inpath folder.
#         '''
#
#         path = path+'.py'
#         if root:
#             path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fclib', path)
#
#         spec = importlib.util.spec_from_file_location("fclib", path)
#
#         external = importlib.util.module_from_spec(spec)
#
#         spec.loader.exec_module(external)
#
#         if self.tools.other==None:
#             obj = texme
#         else:
#             obj = self.tools.other
#
#         if id==None:
#             obj.lib = external.lib(obj)
#         else:
#             if type(obj.lib)!=dict:
#                 obj.lib = {}
#             obj.lib[id] = external.lib(obj)





#$ ____ class texme ________________________________________________________ #

class texme:

    setts = setts()

    setts.force_copy(False)

    setts.path(r'.\tex')

    setts.source(folder_path=r'.\src', filename='main.tex')

    setts.template(cave=os.path.join(
        os.path.dirname(os.path.realpath(__file__)),'temps'))

    setts.tools.data['keys'] = {}

    setts.echo(True)

    setts.inherit(False)

    setts.active(True)

    setts.autolabel(False)

    setts.re(
        xt ='e$fcbuilsyr$hgo',
        ht ='e$fcbuilsyr$hgo',
        pc ='e$fcbuilsyr$hgo',
        mt ='e$fcbuilsyr$hrgo',
        me ='efcpbuilsyhrgo',
        mo ='mt',
        tc ='e$fcbuilsyr$hgo',
        td ='e$fcbuilsyr$hgo',
        ce ='',
        cc ='e$fcbuilsyr$hgo',
    )

    setts.float(
        pic = False,
        tab = False,
    )

    setts.picset(
        root = '.',
        display_width=500,
    )


    setts.headset(
        inc = 0,
    )

    setts.itemset(
        lvl = 1,
        width = 80,
    )

    setts.fclib(cave=os.path.join(
        os.path.dirname(os.path.realpath(__file__)),'fclib'))


    tmp = None

    lib = None



#$$ ________ def __init __ _________________________________________________ #

    def __init__(self, core=None, **kwargs):

        self.core = core

        self.setts = setts(master=self.setts.tools, root=self)

        # list with generated and ready-to-insert code
        self.buffer = []

        for key,val in kwargs.items():
            getattr(self.setts, key)(val)

        self.ldef = {'type':None, 'head':{}}

        self.slave = slave(self, core)

        self.lib = {}


#$$ ________ process methods _______________________________________________ #

#$$$ ____________ def add __________________________________________________ #

    def add(self, code, inherit=None, submodule=None, echo=None, presymbol='', postsymbol='\n%'):
        '''
        Append code to buffer. Method offer adding symbol at the end of statment, inherit base if-block and print block. It is add clear code into buffer (with additional pre- and post- symbol, but only if inherit is False, more, never in echo).
        '''

        # get default parametrs by test if None
        # do not test it in every generate method!!!
        inherit = self.setts.inherit(inherit, check=True)

        # base on iherit methods then return or add code
        if inherit is True: return code

        elif inherit is False:
            self.ldef['type'] = submodule

            # else:
            self.buffer += [presymbol + code + postsymbol]

            self.slave.add(presymbol + code + postsymbol)

        # depend on setting echo in "t" print code or not
        # do not test it in every generate method!!!
        if 'x' in self.setts.echo(echo, check=True):
            print(f'[pinky.texme.{submodule}]\n{code}')


#$$$ ____________ def clear _________________________________________ #

    def clear(self):
        '''
        Clear buffer.
        '''

        self.buffer = []


#$$$ ____________ def bib_update ___________________________________________ #

    def bib_update(self):
        '''
        Update biblography files in depend templates. It run bat script which provide copy methods.
        It should be run only before template copy, if user return calculation on already copied - then no updating prefered.
        '''

        basepath = os.path.dirname(os.path.realpath(__file__))
        os.system(os.path.join(basepath, r'temps\bibme.bat'))


#$$$ ____________ def _copy_template ______________________________________ #

    def _copy_template(self):
        '''
        Copy template tree from input to output dir. It working in two mode: force and inteligent (.force_copy is cotroler).
        '''

        # if force copy is True or folder does not exists
        if self.setts.force_copy() or not os.path.exists(self.setts.path()):

            # first, if output dir exists, then delete is
            if os.path.isdir(self.setts.path()):

                # by full tree
                shutil.rmtree(self.setts.path())

            # then update bibliography by central data
            self.bib_update()

            # at least copy dir from input to output
            shutil.copytree(self.setts.source(mode='p'), self.setts.path())


        # if force mode is deactive
        else:
            # exists of path is alredy done
            # save base path
            path = self.setts.source()

            # if output folder exists, then check if bak folder exists
            if os.path.exists(path):
                os.remove(path)

            if not os.path.exists(path + '.bak'):
                pathT = self.setts.source() + '.bak'
                shutil.copyfile(pathT, path)

#$$$ ____________ def _dictonary ___________________________________________ #

    def _dictonary(self):
        '''
        Create diconary pattern. If buffer is list, then treat it as normal object, so glue list and insert it in 0001 position.
        On the other hand, if buffer is dict, then its mind that object is super object, and place text in special cells.
        '''

        # if buffer is list, then self is normal texme object
        if type(self.buffer) is list:
            # create basis pattern
            sdict = {'%<0001>%': '\n'.join(map(str, self.buffer))}

        # if buffer is dict, then treat self as super object
        elif type(self.buffer) is dict:

            sdict = {}

            for key, val in self.buffer.items():
                sdict.update({'%<'+key+'>%': '\n'.join(map(str, val.buffer))})

        for key, val in self.setts.keys(check=True).items():
            sdict.update({'%<'+key+'>%': val})

        return sdict


#$$$ ____________ def _substitution_via ______________________________________ #

    def _substitution_via(self, ndict, mode):
        '''
        Copy .tex.bak file to .tex with substitution variables.
        '''

        # output main tex file path
        path1 = os.path.join(
            self.setts.path(),
            self.setts.source(mode='n'),
        )

        # output main tex file path bak file
        path2 = path1 + '.bak'

        # copy and substituion
        with open(path2, encoding='utf-8') as infile, open(path1, mode, encoding='utf-8') as outfile:
            # copy line by line
            for line in infile:
                outfile.write(translate(line, ndict))

    # TODO: latex run methods should be rewrite, bib dont work corretly etc


#$$$ ____________ def _pdf_maker ___________________________________________ #

    def _pdf_maker(self, force_mode=True, shell_escape=False, synctex=True, output=False):
        '''Start TeX compilating. There is needed pdflatex software. The sheel-escepe and forcecopy can be activated.'''
        sett = ''
        if synctex:      sett += ' -synctex=1'
        if force_mode:   sett += ' -interaction=nonstopmode -file-line-error'
        if shell_escape: sett += '--shell-escape'

        code = 'cd "{0}" & pdflatex {1} "{2}"'.format(
            self.setts.source(mode='p'), sett, self.setts.source(mode='n'))
        p = subprocess.Popen(code, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)

        if output:
            out = p.stdout.read().decode('UTF-8')
            out = out.split('\n')
            for line in out:
                print(line)

#$$$ ____________ def _bib_loader __________________________________________ #

    def _bib_loader(self, mode='biber', output=False):
        '''Start BiB compilating. There are needed bibtex software. BiB root must have the extension .bib.'''

        name_noext = os.path.basename(os.path.splitext(self.setts.source(mode='n'))[0])

        # if bibtex:
        if mode=='bibtex':
            code = 'cd "{0}" & bibtex "{1}"'.format(
                self.setts.path(), name_noext + '.aux')

        elif mode=='biber':
            code = 'cd "{0}" & biber "{1}"'.format(
            self.setts.path(), name_noext + '.bcf')

        elif mode=='bibtex8':
            code = 'cd "{0}" & bibtex8 "{1}"'.format(
            self.setts.path(), name_noext + '.bcf')

        p = subprocess.run(code, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)

        if output:
            out = p.stdout.decode('UTF-8')
            out = out.split('\n')
            for line in out:
                print(line)


#$$$ ____________ def _tex_clear ___________________________________________ #

    def _tex_clear(self):
        '''fclear folder after TeX compiling. There are lots file deleted, so please use it carefully.'''

        ext_list = ['.aux', '.bcf', '.fdb_latexmk', '.fls', '.run.xml', '.lof', '.lot', '.toc',
                    '.bbl', '.blg', '.lol', '.maf', '.mtc', '.out']

        for i in range(30):
            ext_list.append('.mlf' + str(i))
            ext_list.append('.mlt' + str(i))
            ext_list.append('.mtc' + str(i))

        name_noext = os.path.basename(os.path.splitext(self.setts.source(mode='n'))[0])

        for ext in ext_list:
            if os.path.exists(os.path.join(self.setts.source(mode='p'), name_noext) + ext):
                os.remove(os.path.join(self.setts.source(mode='p'), name_noext) + ext)

#$$$ ____________ def make _________________________________________________ #

    def make(self, active=None, fclear=True, times=4, force_mode=True, shell_escape=False, synctex=True, output=False):

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # if times is more than zero, then start loop making pdf
        for i in range(times):
            self._pdf_maker(force_mode, shell_escape, synctex, output)
            if i == 1: self._bib_loader(output=output)

        # after all you can clean output dir
        if fclear: self._tex_clear()



    # #$$$ def -pdf-maker
    # def _pdf_maker(self, force_mode, shell_escape, synctex):
    #     '''Start TeX compilating. There is needed pdflatex software. The sheel-escepe and forcecopy can be activated.'''
    #     sett = ''
    #     if synctex:      sett += ' -synctex=1'
    #     if force_mode:   sett += ' -interaction=nonstopmode -file-line-error'
    #     if shell_escape: sett += '--shell-escape'
    #
    #     code = 'cd "{0}" & pdflatex {1} "{2}"'.format(
    #         self.setts.path, sett, self.inname)
    #     subprocess.run(code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #
    # #$$$ def -bib-loader
    # def _bib_loader(self, mode='biber'):
    #     '''Start BiB compilating. There are needed bibtex software. BiB root must have the extension .bib.'''
    #     name_noext = os.path.basename(os.path.splitext(self.inname)[0])
    #
    #     # if bibtex:
    #     if mode=='bibtex':
    #         code = 'cd "{0}" & bibtex "{1}"'.format(
    #             self.setts.path, name_noext + '.aux')
    #     elif mode=='biber':
    #         code = 'cd "{0}" & biber "{1}"'.format(
    #         self.setts.path, name_noext + '.bcf')
    #     elif mode=='bibtex8':
    #         code = 'cd "{0}" & bibtex8 "{1}"'.format(
    #         self.setts.path, name_noext + '.bcf')
    #
    #     subprocess.run(code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #
    #
    # #$$$ def -tex-clear
    # def _tex_clear(self):
    #     '''fclear folder after TeX compiling. There are lots file deleted, so please use it carefully.'''
    #
    #     ext_list = ['.aux', '.bcf', '.fdb_latexmk', '.fls', '.run.xml', '.lof', '.lot', '.toc',
    #                 '.bbl', '.blg', '.lol', '.maf', '.mtc', '.out']
    #
    #     for i in range(30):
    #         ext_list.append('.mlf' + str(i))
    #         ext_list.append('.mlt' + str(i))
    #         ext_list.append('.mtc' + str(i))
    #
    #     name_noext = os.path.basename(os.path.splitext(self.inname)[0])
    #
    #     for ext in ext_list:
    #         if os.path.exists(os.path.join(self.setts.path, name_noext) + ext):
    #             os.remove(os.path.join(self.setts.path, name_noext) + ext)



#$$$ ____________ def save _________________________________________________ #

    def save(self, mode='w', active=None):
        '''
        Save buffer to file, copy and substitute into inpath+inname file.
        '''

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # prepare template to replace blocks
        self._copy_template()

        # replace in file
        self._substitution_via(self._dictonary(), mode)


#$$$ ____________ def push _________________________________________________ #

    def push(self, active=None):
        '''
        Push method is connection of save and clear methods.
        '''

        if len(self.buffer) > 0:
            self.save(active=active)
        self.clear()








#$$ ________ generate methods ______________________________________________ #

#$$$ ____________ def page _________________________________________________ #

    def page(self, mode, val1=None, active=None, inherit=None, echo=None):
        '''
        Check reference:

        https://tex.stackexchange.com/questions/45609/is-it-wrong-to-use-clearpage-instead-of-newpage

        https://tex.stackexchange.com/questions/9852/what-is-the-difference-between-page-break-and-new-page

        '''

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        if inherit in ['beg','end']:
            if type(mode) in [tuple, list]:
                if len>1: val1 = mode[1]
                if len>2: val2 = mode[2]
                mode = mode[0]

        if mode in [None]:
            code=None

        elif mode in ['clearpage', 'cp']:
            '''
            Clearpage statment break page and block range for float items.
            '''
            code = r'\clearpage'

        elif mode in ['cleardoublepage', 'cdp']:
            '''
            Clearpage statment break page and block range for float items.
            '''
            code = r'\cleardoublepage'

        elif mode in ['npage','np','newpage']:
            '''
            Clearpage statment break page and don't block range for float items.
            '''
            code = r'\newpage'

        elif mode in ['pagebreak', 'pb']:
            code = r'\pagebreak'

        elif mode in ['goodbreak', 'gp']:
            code = r'\goodbreak'

        elif mode in ['absolutelynopagebreak-b', 'anpbb', 'ab']:
            code = r'\begin{absolutelynopagebreak}'

        elif mode in ['absolutelynopagebreak-e', 'anpbe', 'ae']:
            code = r'\end{absolutelynopagebreak}'

        elif mode in ['vspace', 'vs']:
            code = r'\vspace*{'+val1+'}'

        elif mode in ['newline', 'nl']:
            code = r'\newline'

        elif mode in ['appendices-b', 'apb']:
            code = r'\begin{appendices}'

        elif mode in ['appendices-e', 'ape']:
            code = r'\end{appendices}'

        else:
            verrs.BCDR_pinky_texme_ERROR_General(
                'e0625', 'Unknow mode of page method!\n'
                'Tip: look into manual...'
            )

        if inherit=='beg':
            inherit = True
            code    = (code + '\n' if code else '')

        elif inherit=='end':
            inherit = True
            code    = ('\n'+ code if code else '')

        return self.add(
            submodule = 'page',
            code      = code,
            inherit   = inherit,
            echo      = echo,
        )







#$$$ ____________ def text _________________________________________________ #

    def text(self, text, re_xt=None, strip=True, active=None, inherit=None, echo=None, pbeg=None, pend=None):
        '''
        Add formated text to tex document. Text can be striped and filter regme changed.
        '''

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # if page is typed
        pbeg = self.page(pbeg, inherit='beg')
        pend = self.page(pend, inherit='end')

        # use global settings
        self.setts.tools.check = True
        re_xt = self.setts.re(xt=re_xt)
        self.setts.tools.check = False

        # use filter regme
        code = regme(text, re_xt)

        # strip begind and end of text
        if strip: code = code.strip()

        return self.add(
            submodule = 'x',
            code      = pbeg+code+pend,
            inherit   = inherit,
            echo      = echo,
        )


    x = text


#$$$ ____________ def head _________________________________________________ #

    def head(self, lvl, text, label=None, text2=None, re_ht=None, without_number=False, minitoc=None, active=None, inherit=None, echo=None, pbeg=None, pend=None):
        '''
        '''

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # if page is typed
        pbeg = self.page(pbeg, inherit='beg')
        pend = self.page(pend, inherit='end')

        # use global settings
        self.setts.tools.check = True
        echo  = self.setts.echo(echo)
        re_ht = self.setts.re(re_ht)
        minitoc = False
        self.setts.tools.check = False

        # use filter regme
        texo = text
        text = regme(text, re_ht)

        if label:
            lab = '\\hedlab{' + label + '}'

        elif 'p' in self.setts.autolabel(check='p'):

            firstletters = ''.join([i[0].lower() for i in texo.split()])

            lab = '\\hedlab{h'+str(lvl)+':' + firstletters + '}'

        else:
            lab = ''

        if without_number:
            without_number = '*'
        else:
            without_number = ''

        nlvl = lvl+self.setts.headset(check='inc')

        if nlvl == -1:
            tex = '\\part' + without_number + '%2{%1} ' + lab
            if minitoc:
                tex += '\n\\minitoc'

        elif nlvl == 0:
            tex = '\\chapter' + without_number + '%2{%1} ' + lab
            if minitoc:
                tex += '\n\\minitoc'

        elif nlvl == 1:
            tex = '\\section' + without_number + '%2{%1} ' + lab

        elif nlvl == 2:
            tex = '\\subsection' + without_number + '%2{%1} ' + lab

        elif nlvl == 3:
            tex = '\\subsubsection' + without_number + '%2{%1} ' + lab

        elif nlvl == 4:
            tex = '\\paragraph' + without_number + '%2{%1} ' + lab

        elif nlvl == 5:
            tex = '\\subparagraph' + without_number + '%2{%1} ' + lab

        else:
            verrs.BCDR_pinky_texme_ERROR_Header_Level(
                nlvl,self.setts.headset(check='inc'))

        if text2:
            text2 = '[' + regme(text2, re_ht) + ']'
        else:
            text2 = ''

        code = tex.replace('%1', text.strip())
        code = code.replace('%2', text2)

        if 'h' in echo:

            if   lvl==1: color = "255,127,80"
            elif lvl==2: color = "165,127,80"
            elif lvl==3: color = "125,127,80"
            elif lvl==4: color = "125,177,80"
            else       : color = "255,255,255"

            source = "<h{2} style='color: rgb({0})'>{1}</h1>".format(
                color,text,lvl)

            display(HTML(source.strip().replace('~', ' ')))

        self.ldef['head'].update(
            {lvl: {'texo': texo}, 'last':{'lvl': lvl, 'texo': texo}}
        )

        return self.add(
            submodule = 'h',
            code      = pbeg+code+pend,
            inherit   = inherit,
            echo      = echo,
        )

    h = head


#$$$ ____________ def pic __________________________________________________ #

    def pic(self, path, caption=False, label=None, float=None, abs_path=False, frame=True, grey_scale=False, caption2=False, re_pc=None, width_factor=1, height_factor=0.95, mode='fig', root=None, pic_error=True, active=None, inherit=None, echo=None, pbeg=None, pend=None):
        '''
        '''

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # if page is typed
        pbeg = self.page(pbeg, inherit='beg')
        pend = self.page(pend, inherit='end')

        # use global settings
        self.setts.tools.check = True
        echo     = self.setts.echo     ( echo               )
        re_pc    = self.setts.re       ( re_pc                 )
        pic_root = self.setts.picset(root, check= 'root')
        # label    = self.setts.label    (p=label , check='p')
        float    = self.setts.float    (pic=float , check='pic')
        self.setts.tools.check = False

        # save inputed path
        user_path = path

        # user can define prepath for picture
        path = os.path.join(pic_root, path).replace('/', '\\')

        # first check if file is exists
        if not os.path.exists(path):
            if pic_error:
                verrs.BCDR_pinky_texme_ERROR_Path_Error(path)
                verrs.BCDR_pinky_texme_WARN_Path_Error(path)
            else:
                verrs.BCDR_pinky_texme_WARN_Path_Error(path)
            return

        # create absoule path
        pathA = os.path.abspath(path).replace('\\', '/')

        # if user want to insert into tex global path, then simple convert
        if abs_path:
            path = pathA

        # but if not, then create relative path from current dir
        else:
            path = os.path.relpath(path, self.setts.path()).replace('\\', '/')

        # print('abs:',pathA,'\nloc:',path, '\nsetts.path:',self.setts.path)
        # TODO: multifile dont work, change concept of inherited texme...

        # if creat
        if grey_scale:
            path = os.path.splitext(pathA)[0] + '_grey' + os.path.splitext(pathA)[1]
            code = 'magick -colorspace gray "{0}" "{1}"'.format(
                pathA, pathA)
            subprocess.run(code)

        if frame:
            frame = 'frame,'
            width_factor *= 0.999
        else:
            frame = ''

        # if-mode block
        # user can input e.g. table and want to treat it as picture
        # then by mode it can be changed
        # fig must be deafult!
        if mode=='fig':

            if float is True:
                code = '\\begin{figure}\n\\centering{'
            elif float is False:
                code = '\\begin{center}\n'
            elif float is 'H':
                code = '\\begin{figure}[H]\n\\centering{'
            elif float is 'anpb':
                code = self.page('anpb-b', inherit=True)
                code += '\\begin{center}\n'
            else:
                verrs.BCDR_pinky_texme_ERROR_General(
                    'e0626', 'Unknow float mode'
                )

            code += '\\catcode`\\#=12\n'

            code += translate( '\\includegraphics[{1}width={2}\\linewidth,height={3}\\textheight,keepaspectratio]{{0}}\n',
                {'{0}': path,
                 '{1}': frame,
                 '{2}': str(width_factor),
                 '{3}': str(height_factor)})

            if caption:
                caption = regme(caption, re_pc)

                if caption2:
                    cap2='['+regme(
                        caption2,re_pc)+']'
                else:
                    cap2 = ''


                code += translate('\\caption{float}{1}{{0}}\n',
                    {
                        '{0}'    : caption,
                        '{1}'    : cap2,
                        '{float}': ('of{figure}' if not float else '')
                    })


                if type(label) is str:
                    code += '\\figlab{{0}}\n'.replace('{0}', label)

                elif label == True:
                    code += '\\figlab{{0}}\n'.replace('{0}', user_path.replace('\\', '').replace('/', ''))

            if float is False:
                code += '\\end{center}'
            elif float is 'anpb':
                code += '}\\end{center}'
                code += self.page('anpb-e', inherit=True)
            else:
                code += '}\\end{figure}'

        elif mode=='lst':
            pass
            #                 if caption:
            #                     caption = RegME(caption, captionX)
            #                     caption = 'caption={%1}'.replace('%1', caption)
            #                     if type(label) is str:
            #                         caption += ',label={%1},'.replace('%1', label)
            #                     elif label == True:
            #                         caption += ',label={%1},'.replace('%1', os.path.basename(path))
            #                 else:
            #                     caption = ''
            #
            #                 ndict = {'%path': path,
            #                          '%frame': frame,
            #                          '%cap': caption}
            #                 code ='''
            # \\begin{minipage}{\\linewidth}\n\\begin{lstlisting}[%capescapeinside=||, frame=none, numbers=none, xleftmargin=0pt,xrightmargin=0pt]
            # |\\includegraphics[%framewidth=\\linewidth]{%path}|
            # \\end{lstlisting}\n\\end{minipage}'''
            #                 code = translate(code, ndict)
            #                 _name1='img-lst'

        elif mode=='tab':
            pass

            if float is True:
                code = '\\begin{table}\n\\centering{'
            elif float is False:
                code = '\\begin{center}\n'
            elif float is 'H':
                code = '\\begin{figure}[H]\n\\centering{'
            elif float is 'anpb':
                code = self.page('anpb-b', inherit=True)
                code += '\\begin{center}\n'
            else:
                verrs.BCDR_pinky_texme_ERROR_General(
                    'e0626', 'Unknow float mode'
                )

            code += '\\catcode`\\#=12\n'

            if caption:
                caption = regme(caption, re_pc)

                if caption2:
                    cap2='['+regme(caption2,re_pc)+']'
                else:
                    cap2 = ''

                code += translate('\\caption{float}{1}{{0}}\n',
                    {
                        '{0}'    : caption,
                        '{1}'    : cap2,
                        '{float}': ('of{table}' if not float else '')
                    })

                if type(label) is str:
                    code += '\\tablab{{0}}\n'.replace('{0}', label)

                elif label == True:
                    code += '\\tablab{{0}}\n'.replace('{0}', user_path.replace('\\', '').replace('/', ''))

            code += translate( '\\includegraphics[{1}width={2}\\linewidth,height={3}\\textheight,keepaspectratio]{{0}}\n',
                {'{0}': path,
                 '{1}': frame,
                 '{2}': str(width_factor),
                 '{3}': str(height_factor)})

            if float is False:
                code += '\\end{center}'
            elif float is 'anpb':
                code += '}\\end{center}'
                code += self.page('anpb-e', inherit=True)
            else:
                code += '}\\end{figure}'

            #                 if float:
            #                     code = '\\begin{table}\n\\centering{'
            #                 else:
            #                     code = '\\begin{table}[H]\n\\centering{'


            #                 if caption:
            #                     caption = RegME(caption, captionX)
            #                     code += '\\caption%2{%1}\n'.replace('%1', caption)
            #                     if caption2:
            #                         code = code.replace('%2', '['+ caption2 +']')
            #                     else:
            #                         code = code.replace('%2', '')
            #                     if type(label) is str:
            #                         code += '\\label{{0}}\n'.replace('{0}', label)
            #                     elif label == True:
            #                         code += '\\label{{0}}\n'.replace('{0}', os.path.basename(path))
            #                 code += '\\includegraphics[%2width=\\linewidth,height=0.90\\textheight,keepaspectratio]{%1}\n}\\end{table}'.replace(
            #                     '%1', path).replace('%2', frame)
            #

        else:
            raise ValueError('unknown mode atribute, allowed are: "fig", "tab", "lst"')


        if 'p' in echo:
            display(Image(
                pathA, width=self.setts.picset(check='display_width')
            ))

        return self.add(
            submodule = 'pic',
            code      = pbeg+code+pend,
            inherit   = inherit,
            echo      = echo,
        )
    p = pic


#$$$ ____________ def math _________________________________________________ #

    def math(self, equation, mode='i', label=None, re_mt=None, re_me=None, re_mo=None, strip=True, active=None, inherit=None, echo=None, pbeg=None, pend=None):
        '''
        Please remember about problem with equation block - there is fault working labels. To fix it use gather instead equation block. \\leavemode should fix it, but it is not tested yet.
        '''

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # if given is list, then return self looped
        if type(equation)==list:
            if type(mode)==list:
                return [self.math(equation=eq, mode=mo, label=label, re_mt=re_mt, re_me=re_me, re_mo=re_mo, strip=strip, active=active, inherit=inherit, echo=echo, pbeg=pbeg, pend=pend) for eq,mo in zip(equation, mode)]
            else:
                return [self.math(equation=eq, mode=mode, label=label, re_mt=re_mt, re_me=re_me, re_mo=re_mo, strip=strip, active=active, inherit=inherit, echo=echo, pbeg=pbeg, pend=pend) for eq in equation]

        # if page is typed
        pbeg = self.page(pbeg, inherit='beg')
        pend = self.page(pend, inherit='end')

        # use global settings
        self.setts.tools.check = True
        echo    = self.setts.echo  ( echo  )
        re_mt = self.setts.re(mt=re_mt, check='mt')
        re_me = self.setts.re(mt=re_me, check='me')
        re_mo = self.setts.re(mt=re_mo, check='mo')
        self.setts.tools.check = False

        if strip: equation = equation.strip()

        if mode in ['t*', 't+', 't']:
            code = regme(equation, re_mt)

            if 'm' in echo:
                display(Markdown(code))

            return self.add(
                submodule = 'm',
                code      = pbeg+code+pend,
                inherit   = inherit,
                echo      = echo,
            )

        equation = regme(equation, re_me)

        if label:
            lab = '\\equlab{' + label + '}'

        else:
            lab = ''


        if mode in ['e+']:
            code = '\\leavevmode\\begin{equation} ' + lab + \
                '\n' + equation + '\n\\end{equation}'

        elif mode in ['e*', 'e']:
            code = '\\begin{equation*} ' + lab + \
                '\n' + equation + '\n\\end{equation*}'

        elif mode in ['i*', 'i']:
            code = '$' + equation + '$'

        elif mode in ['m+']:
            code = '\\begin{multline} ' + lab + \
                '\n' + equation + '\n\\end{multline}'

        elif mode in ['m*', 'm']:
            code = '\\begin{multline*} ' + lab + \
                '\n' + equation + '\n\\end{multline*}'

        elif mode in ['a+']:
            code = '\\begin{align} ' + lab + \
                '\n' + equation + '\n\\end{align}'

        elif mode in ['a*','a']:
            code = '\\begin{align*} ' + lab + \
                '\n' + equation + '\n\\end{align*}'

        elif mode in ['d+']:
            code = '\\begin{dmath} ' + lab + \
                '\n' + equation + '\n\\end{dmath}'

        elif mode in ['g+']:
            code = '\\begin{gather} ' + lab + \
                '\n' + equation + '\n\\end{gather}'

        elif mode in ['g*', 'g']:
            code = '\\begin{gather*} ' + lab + \
                '\n' + equation + '\n\\end{gather*}'

        elif mode in ['ead+']:
            code = '\\begin{equation}\\begin{aligned} ' + lab + \
                '\n' + equation + '\n\\end{aligned}\\end{equation}'

        if 'm' in echo:
            display(Latex(
                '$'+regme(equation, re_mo)+'$'
            ))

        return self.add(
            submodule = 'm',
            code      = pbeg+code+pend,
            inherit   = inherit,
            echo      = echo,
        )
    m = math



#$$$ ____________ def tab __________________________________________________ #

    def tab(self, cols, data, options=r'\textwidth', caption=None, label=None, float=False, header=None, stretchV=1.5, re_tc=None, re_td=None, active=None, inherit=None, echo=None, pbeg=None, pend=None):

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # if page is typed
        pbeg = self.page(pbeg, inherit='beg')
        pend = self.page(pend, inherit='end')

        # use global settings
        self.setts.tools.check = True
        echo  = self.setts.echo  ( echo  )
        re_tc = self.setts.re(tc=re_tc, check='tc')
        re_td = self.setts.re(tc=re_td, check='td')
        float = self.setts.float(tab=float, check='tab')
        self.setts.tools.check = False

        if caption:
            if label:
                label = '\\tablab{'+label+'}'
            else:
                label = ''

            caption = '\\caption{' + \
                regme(caption, re_tc) + '}'+ label +'\\\\'
        else:
            caption = ''

        if header:
            header = '\\hlineb\n' + \
                regme(header, re_td) + \
                '\n\\\\\\hlineb\n\\endhead'
        elif not float:
            header = '\\endhead'
        else:
            header = ''

        tex = ("\\begingroup\n"
            "\\renewcommand*{\\arraystretch}{%StV}\n"
            "\\begin{tabularx}{%Opt}{%Col}\n"
            "%Cap\n"
            "%Hea\n"
            "%Dat\n"
            "\\end{tabularx}\n"
            "\\endgroup")

        ndict = {'%Opt': options,
                 '%Col': cols,
                 '%Cap': caption,
                 '%StV': str(stretchV),
                 '%Lab': label,
                 '%Hea': header,
                 '%Dat': regme(data, re_td)}
        tex = translate(tex, ndict)

        if float == True:
            tex = '\\begin{table}\n' + tex + '\n\\end{table}'
        elif float == False:
            pass
        elif float == 'H':
            tex = '\\begin{table}[H]\n' + tex + '\n\\end{table}'

        return self.add(
            submodule = 't',
            code      = tex,
            inherit   = inherit,
            echo      = echo,
        )
    t = tab


#$$$ ____________ def code _________________________________________________ #

    def code(self, code, caption='', label='', style=None, language=None, re=None, strip=True, mathescape=True, active=None, inherit=None, echo=None, pbeg=None, pend=None):

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # if page is typed
        pbeg = self.page(pbeg, inherit='beg')
        pend = self.page(pend, inherit='end')

        # use global settings
        self.setts.tools.check = True
        echo     = self.setts.echo     ( echo               )
        re       = self.setts.re       ( re                 )
        label    = self.setts.label    ( c=label , check='c')
        style    = self.setts.lststyle(
            style if style!='rst' else 'bcdr_rst_tables')
        self.setts.tools.check = False

        if mathescape:
            var1 = ', mathescape'
        else:
            var1 = ''

        if language:
            var2 = ',language={' + language + '}'
        else:
            var2 = ''

        if style:
            style = ',style={' + style + '}'
        else:
            style = ''

        caption = regme(caption, re['cc'])

        if code == True:
            self._temp = [inspect.currentframe().f_back.f_lineno]

            tex = translate('\\begin{lstlisting}[caption={%1}%2%3%5%4]'
                ,{
                    '%1': caption,
                    '%2': ',label={'+label+'},' if label else '',
                    '%4': var1,
                    '%3': var2,
                    '%5': style,
                })

        elif code == False:
            self._temp.append(
                inspect.currentframe().f_back.f_lineno - 1)

            tex = '%%%-TO-REPLACE-%%%' + str(self._temp)

            self._add('c-replace', tex, inherit)

            tex = '\n\\end{lstlisting}'

        elif type(code) == str:

            tex = translate('\\begin{lstlisting}[caption={%1}%2%3%5%4]'
                ,{
                    '%1': caption,
                    '%2': ',label={'+label+'},' if label else '',
                    '%4': var1,
                    '%3': var2,
                    '%5': style,
                })

            code = regme(code, re['ce'])

            if strip:
                code = code.strip()

            tex += '\n' + code + '\n'
            tex += '\\end{lstlisting}'


        return self.add(
            submodule = 'c',
            code      = tex,
            inherit   = inherit,
            echo      = echo,
        )
    c = code



#$$$ ____________ def file _________________________________________________ #

    def file(self, path, caption=None, label=None, first_line=0, last_line=1e10, absolute_path=False, language='Python', re=None, active=None, inherit=None, echo=None, pbeg=None, pend=None):
        '''
        '''

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # if page is typed
        pbeg = self.page(pbeg, inherit='beg')
        pend = self.page(pend, inherit='end')

        # use global settings
        self.setts.tools.check = True
        echo     = self.setts.echo     ( echo               )
        label    = self.setts.label    ( f=label , check='f')
        re       = self.setts.re       ( re                 )
        self.setts.tools.check = False

        if language:
            var2 = ',language={' + language + '}'
        else:
            var2 = ''

        pathA = os.path.abspath(path).replace('\\', '/')

        if absolute_path:
            path = pathA
        else:
            path = os.path.relpath(path, self.path).replace('\\', '/')

        if label==True:
            label = os.path.basename(path)
        else:
            label = ''

        tex = '\\lstinputlisting[language=%5, firstline=%3, lastline=%4, caption={%1}, label={%2}, inputencoding=utf8, mathescape]{%6}'
        tex = tex.replace('%1', regme(caption, re['fc']))
        tex = tex.replace('%2', label)
        tex = tex.replace('%3', first_line)
        tex = tex.replace('%4', last_line)
        tex = tex.replace('%5', var2)
        tex = tex.replace('%6', path.replace('\\', '/'))

        return self.add(
            submodule = 'f',
            code      = tex,
            inherit   = inherit,
            echo      = echo,
        )
    f = file


#$$$ ____________ def item _________________________________________________ #

    def item(self, text=None, equation=None, mode='i', lmath=None, label=None, width=None, lvl=None, prefix='*', postfix=':', re_mt=None, re_me=None, re_mo=None, re_xt=None, col_l=None, col_r=None, active=None, inherit=None, echo=None, pbeg=None, pend=None):
        '''
        Column type must can defined explicit size in length dimension (like p{50mm} (or q,w,e).
        '''

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # if page is typed
        pbeg = self.page(pbeg, inherit='beg')
        pend = self.page(pend, inherit='end')

        # use global settings
        self.setts.tools.check = True
        width = self.setts.itemset(width=width, check='width')
        lvl = self.setts.itemset(lvl=lvl, check='lvl')
        # re_ht = self.setts.re(re_ht)
        self.setts.tools.check = False

        # simple resolve empty text box
        if text=='': text = '...'

        if type(text)==list:
            tadd = regme(r'\newline' + r' \newline '.join(text[1:]).strip(),  re_xt)
            text = text[0]
        else:
            tadd = ''

        # prefix if-block
        if prefix in ['',' ']:
            ptext = r'{}&'*(lvl-1)
            pcols = r'q{3mm}'*(lvl-1)
            width -= (lvl-1)*5

        elif prefix in ['|']:
            ptext = r''
            pcols = r'@{\hspace{1mm}}|' + r'@{\hspace{3mm}}|'*(lvl-1)
            width -= 2+(lvl-1)*4

        elif prefix in ['-']:
            ptext = r'{}&'*(lvl-1) + r'-- & '
            pcols = r'q{3mm}'*lvl
            width -= (lvl-1)*7

        elif prefix in ['*']:
            ptext = r'{}&'*(lvl-1) + r'\textbullet & '
            pcols = r'q{3mm}'*lvl
            width -= (lvl-1)*7

        else:
            verrs.BCDR_pinky_texme_ERROR_General(
                'e0627', 'Unrecognized prefix element'
            )

        # remove too big space between to texme-items
        if self.ldef['type'] == 'i':
            space_bt = '\\vspace*{-11pt}\n'
        elif self.ldef['type'] == 'h':
            space_bt = '\\vspace*{-5pt}\n'
        else:
            space_bt = ''


        # flush math equation to left, rith or center
        if lmath is True:
            flush_math = '\\mathleft\n'
        else:
            flush_math = ''


        # here, if block 3 options: t&e, t, e
        if text and equation:
            if mode in ['i*', 't*', 'i', 't']:

                if col_l is None: col_l = 'q'
                if col_r is None: col_r = 'L'

                # create column pattern
                columns = translate('{{pcols}{col_l}{{width}}{col_r}}', {
                    '{pcols}'   : pcols,
                    '{col_l}'   : col_l,
                    '{col_r}'   : col_r,
                    '{width}'   : str(width)+'mm',
                })

                tex = (
                    r"{space_bt}"
                    r"\begin{tabularx}{\textwidth}{columns}""\n"
                    r"{ptext}{text}{postfix}{tadd}&%""\n"
                    r"{flush_math}"
                    r"{equation}""\n"
                    r"\end{tabularx}"
                    )

                glue = '\n' + r'\newline' + '\n\n'

            else:

                if col_l is None: col_l = 'L'

                # create column pattern
                columns = translate('{{pcols}{col_l}}',{
                    '{pcols}'   : pcols,
                    '{col_l}'   : col_l,
                })


                if not prefix in ['|']:
                    tex = (
                        r"{space_bt}"
                        r"\begin{tabularx}{\textwidth}{columns}""\n"
                        r"{ptext}{text}{postfix}{tadd}%""\n"
                        r"{flush_math}"
                        r"\end{tabularx}""\n"
                        r"\vspace*{-7mm}""\n"
                        r"{equation}"
                        )
                else:
                    tex = (
                        r"{space_bt}"
                        r"\begin{tabularx}{\textwidth}{columns}""\n"
                        r"{ptext}{text}{postfix}{tadd}%""\n"
                        r"{flush_math}"
                        r"{equation}"
                        r"\vspace*{-3mm}""\n"
                        r"\end{tabularx}""\n"
                        )

                glue = '\n'


        elif text:

            if col_l is None: col_l = 'L'

            # create column pattern
            columns = translate('{{pcols}{col_l}}',{
                '{pcols}'   : pcols,
                '{col_l}'   : col_l,
            })

            tex = (
                r"{space_bt}"
                r"\begin{tabularx}{\textwidth}{columns}""\n"
                r"{ptext}{text}{postfix}{tadd}%""\n"
                r"\end{tabularx}"
                )

            glue = ''

        if equation:
            equation = self.math(
                mode        = mode,
                equation    = equation,
                label       = label,
                re_mt       = re_mt,
                re_me       = re_me,
                re_mo       = re_mo,
                inherit     = True,
            )

            if type(equation)==list:
                equation = glue.join(equation)


        tex = translate(tex, {
            '{space_bt}'  : space_bt,
            '{columns}'   : columns,
            '{ptext}'     : ptext,
            '{text}'      : regme(text.strip(), re_xt),
            '{postfix}'   : postfix,
            '{tadd}'      : tadd,
            '{flush_math}': flush_math,
            '{equation}'  : equation,
        })



        return self.add(
            submodule = 'i',
            code      = tex,
            inherit   = inherit,
            echo      = echo,
        )
    i = item









#$ ____ class slave ________________________________________________________ #

class slave:


    def __init__(self, othe, core=None):
        self.othe = othe
        self.core = core
        self.data = {}


    def new(self, id, **kwargs):
        self.data[id] = texme(core=self.core)
        self.data[id].setts.tools.master = self.othe.setts.tools
        for key,val in kwargs.items():
            getattr(self.data[id].setts, key)(val)



    def add(self, code):
        for tex in self.data.values():
            if tex.setts.active()==True:
                tex.buffer += [code]
            # tex.add(code, inherit, submodule, echo, presymbol, postsymbol)


    def push(self, active=None):
        for tex in self.data.values():
            tex.push(active)


    def active(self, mode, id=None):
        if id==None: id=list(self.data.keys())
        if type(id)==list:
            for id1 in id:
                self.data[id1].setts.active(mode)
        else:
            self.data[id].setts.active(mode)


    def __call__(self, id):
        return self.data[id]






        # if path==None and name==None and check!=True:
        #
        #     if mode=='pn':
        #
        #         return os.path.join(
        #             self.tools.get('source_path'),
        #             self.tools.get('source_name'),
        #         )
        #
        #     elif mode=='p':
        #
        #         return self.tools.get('source_path')
        #
        #     elif mode=='n':
        #
        #         return self.tools.get('source_name')
        #
        # elif check!=True:
        #
        #     if path!=None: self.tools.set('source_path', path)
        #
        #     if name!=None: self.tools.set('source_name', name)
        #
        #
        # elif check==True:
        #
        #     path = self.tools.chk('source_path', path)
        #
        #     name = self.tools.chk('source_name', name)
        #
        #     if mode=='pn':
        #
        #         return os.path.join(path, name)
        #
        #     elif mode=='p':
        #
        #         return path
        #
        #     elif mode=='n':
        #
        #         return name






        # if path!=None: self.tools.set('source_path', path)
        #
        # if name!=None: self.tools.set('source_name', name)
        #
        # if path!=None or name!=None: return
        #
        # path = self.tools.get('source_path')
        #
        # name = self.tools.get('source_name')
        #
        # if mode=='pn':
        #
        #     return os.path.join(
        #         self.tools.get('source_path'),
        #         self.tools.get('source_name'),
        #     )
        #
        #
        # elif mode=='p': return self.tools.get('source_path')
        #
        # elif mode=='n': return self.tools.get('source_name')


#$ ######################################################################### #
