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

from IPython.display import Image, Latex, HTML, Markdown,display

from ...tools.fpack import translate
from ...tools.setts import setts_init

from . import verrs
from .regme import regme

#$ ____ class setts ________________________________________________________ #

class setts(setts_init):

    _last_head = {} # {lvl: {'text':}}
    _last_type = None

#$$ ________ def force_copy ________________________________________________ #

    def force_copy(self, value=None, check=None, reset=None):
        '''
        Force update of template, if true new files will be copy indepened of existsing .tex.bak file.
        '''

        if value!=None and type(value) is not bool:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'bool')
        return self.tools.gst('force_copy', value, check, reset)

#$$ ________ def path ______________________________________________________ #

    def path(self, value=None, check=None, reset=None):
        '''
        Output path related to actual state of kernel. In mostly case it refer to input file. The existing of folder will be checked during template coping.
        '''

        if value!=None and type(value) is not str:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'str')
        return self.tools.gst('path', value, check, reset)

#$$ ________ def inpath ____________________________________________________ #

    def inpath(self, value=None, check=None, reset=None):
        '''
        Input path of tex base folder with init .tex.bak document. Path should be set to basename of this file!
        '''

        if value!=None and not type(value)==str:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'str')
        return self.tools.gst('inpath', value, check, reset)

#$$ ________ def inname ____________________________________________________ #

    def inname(self, value=None, check=None, reset=None):
        '''
        File of main tex document in inpath folder.
        '''

        if value!=None and not type(value)==str:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'str')
        return self.tools.gst('inname', value, check, reset)


#$$ ________ def cave ______________________________________________________ #

    def cave(self, value=None, check=None, reset=None):
        '''
        Atribute provide path to folder with templates. As defualt it refere to folder inside pinky.texme module call "templates".
        '''

        if value!=None and not type(value)==str:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'str')
        return self.tools.gst('cave', value, check, reset)




#$$ ________ def template __________________________________________________ #

    def template(self, value=None, check=None, reset=None):
        '''
        File of main tex document in inpath folder.
        '''
        if check==None: check=self.tools.check


        if value==None:
            self.tools.get('template', reset)

        elif value==False:
            self.tools.data['template'] = False

        else:
            if type(value)!=str:
                verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'str')

            path = os.path.join(self.cave(), value)

            # if template does not exists, then return error
            if not os.path.exists(path) or not os.path.isdir(path):
                verrs.pathTemplateError(path, self.cave())

            if check==False:

                self.tools.gst('template', value, check)

                self.tools.gst('inpath', path, check)

                self.tools.gst('inname', 'main.tex', check)

                # load external methods depend on template

                path = os.path.join(path,'main.py')

                spec = importlib.util.spec_from_file_location("external", path)

                external = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(external)

                if self.tools.other==None: obj = texme
                else: obj = self.tools.other

                obj.ext = external.ext(self.tools.other)

            else:
                return value


#$$ ________ def echo ______________________________________________________ #

    def echo(self, value=None, h=None, m=None, p=None, t=None, c=None, x=None, check=None, reset=None):
        '''
        Atribute <echo> set the output of base methods in texme class. It provide letters interface "hmpt" which can turn on/off

        > "h" -- colorful html header,
        > "m" -- rendered latex math equation,
        > "p" -- rendered picture with constant width,
        > "t" -- rendered tables (don't work yet),
        > "c" -- code cell (don't work yet),
        > "x" -- plain tex code which will be included into tex document.

        User can type value as True then will be set "hmptc" configuration or False then no output will be produced.
        '''

        return self.tools.let('echo', value, check, reset,
            h=h, m=m, p=p, t=t, c=c, x=x,
            full={'True':'hmptc', 'False':''}
        )



#$$ ________ def scope _____________________________________________________ #

    def scope(self, id=None, value=None, check=None, reset=None):
        if id!=None:
            if check==True:
                id = self.tools.set('scope', id, check)
            else:
                self.tools.set('scope', id, check)
        else:
            id = self.tools.get('scope')

        if value==None:
            if self.tools.exists('_scope_'+str(id)):
                return self.tools.get('_scope_'+str(id), reset)
            elif self.tools.other.core.setts.tools.exists('_scope_'+str(id)):
                return self.tools.other.core.setts.tools.get('_scope_'+str(id), reset)
            else:
                return
        else:
            return self.tools.set('_scope_'+str(id), value, check)



#$$ ________ def inherit ___________________________________________________ #

    def inherit(self, value=None, check=None, reset=None):
        '''
        If true then code is returned, if false code is added to buffer.
        '''

        if value!=None and not type(value)==bool:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'bool')
        return self.tools.gst('inherit', value, check, reset)



#$$ ________ def active ____________________________________________________ #

    def active(self, value=None, check=None, reset=None):
        '''
        Atribute provide path to folder with templates. As defualt it refere to folder inside pinky.texme module call "templates".
        '''

        if value!=None and type(value)!=bool:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'bool')
        return self.tools.gst('active', value, check, reset)



#$$ ________ def label _____________________________________________________ #


    def label(self, value=None, h=None, p=None, f=None, c=None, check=None, reset=None):
        '''
        label is dict with dew substitute labels types.
        h -- header
        p -- picture
        f -- file
        c -- code
        '''

        return self.tools.dct('label', value, check, reset,
            h=h, p=p, f=f, c=c
        )



#$$ ________ def re ________________________________________________________ #

    def re(self, value=None, xt=None, ht=None, ht2=None, pc=None, pc2=None, mt=None, me=None, mo=None, tc=None, td=None, ce=None, cc=None, fc=None, check=None, reset=None):
        '''
        xt  - text    + text             | item + text
        ht  - head    + text
        ht2 - head    + text2
        pc  - picture + caption
        pc2 - picture + caption2
        mt  - math    + text             | item + math
        me  - math    + equation         | item + math
        mo  - math    + echo             | item + math
        tc  - table   + caption
        td  - table   + data & header
        ce  - code    + code
        cc  - code    + caption
        fc  - file    + caption
        '''

        return self.tools.dct('re', value, check, reset,
            xt=xt, ht=ht, ht2=ht2, pc=pc, pc2=pc2, mt=mt, me=me, mo=mo, tc=tc, td=td, ce=ce, cc=cc, fc=fc,
        )


#$$ ________ def float _____________________________________________________ #

    def float(self, value=None, p=None, t=None, check=None, reset=None):
        '''
        label is dict with dew substitute labels types.
        h -- header
        p -- picture
        f -- file
        c -- code
        '''

        return self.tools.dct('float', value, check, reset,
            p=p, t=t
        )



#$$ ________ def pic_root __________________________________________________ #

    def pic_root(self, value=None, check=None, reset=None):
        '''
        File of main tex document in inpath folder.
        '''

        if value!=None and not type(value)==str:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'str')
        return self.tools.gst('pic_root', value, check, reset)




#$$ ________ def pic_diswidth ______________________________________________ #

    def pic_diswidth(self, value=None, check=None, reset=None):
        '''
        File of main tex document in inpath folder.
        '''

        if value!=None and not type(value)==int:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'int')
        return self.tools.gst('pic_diswidth', value, check, reset)




#$$ ________ def hlvl_inc __________________________________________________ #

    def hlvl_inc(self, value=None, check=None, reset=None):
        '''
        File of main tex document in inpath folder.
        '''

        if value!=None and not type(value)==int:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'int')
        return self.tools.gst('hlvl_inc', value, check, reset)


#$$ ________ def iwidth ____________________________________________________ #

    def iwidth(self, value=None, check=None, reset=None):
        '''
        File of main tex document in inpath folder.
        '''

        if value!=None and not type(value)==int:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'int')
        return self.tools.gst('iwidth', value, check, reset)



#$$ ________ def ilvl ______________________________________________________ #

    def ilvl(self, value=None, check=None, reset=None):
        if value!=None and not type(value)==int:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'int')
        return self.tools.gst('ilvl', value, check, reset)


#$$ ________ def keys __________________________________________________ #

    def keys(self, value=None, check=None, reset=None):
        '''
        Atribute provide path to folder with templates. As defualt it refere to folder inside pinky.texme module call "templates".
        '''

        if value!=None and not type(value)==dict:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'dict')
        return self.tools.gst('keys', value, check, reset)


#$$ ________ def lststyle ________________________________________________ #

    def lststyle(self, value=None, check=None, reset=None):
        if value!=None and not type(value)==str:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'str')
        return self.tools.gst('lststyle', value, check, reset)

    __lststyle = 'bcdr1'



#$ ____ class texme ________________________________________________________ #

class texme:

    setts = setts()
    setts.force_copy(False)
    setts.path(r'.\tex')
    setts.inpath(r'.\template')
    setts.inname(r'main.tex')
    setts.cave(os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'templates'))
    setts.template(False)
    setts.echo('hmptc')
    setts.tools.data['scope'] = True
    setts.inherit(False)
    setts.active(True)
    setts.label({'h':False, 'p':True, 'f':False, 'c':False})
    setts.re({
        'xt' :'e$fbusy$hrgo',
        'ht' :'e$fbusy$hrgo',
        'ht2':'e$fbusy$hrgo',
        'pc' :'e$fbusy$hrgo',
        'pc2':'e$fbusy$hrgo',
        'mt' :'e$fbusy$hrgo',
        'me' :'efbusyhrgo',
        'mo' :'mt',
        'tc' :'e$fbusy$hrgo',
        'td' :'e$fbusy$hrgo',
        'ce' :'',
        'cc' :'e$fbusy$hrgo',
    })
    setts.float({'p':False, 't':False})
    setts.pic_root(r'.')
    setts.pic_diswidth(600)
    setts.hlvl_inc(0)
    setts.iwidth(70)
    setts.ilvl(1)
    setts.keys({})
    setts.lststyle('bcdr1')



#$$ ________ def __init __ _________________________________________________ #

    def __init__(self, core=None, **kwargs):

        self.core = core

        self.setts = setts(self.setts, self)

        # list with generated and ready-to-insert code
        self.buffer = []

        for key,val in kwargs.items():
            getattr(self.setts, key)(val)


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
        if inherit is True:
            return code

        elif inherit is False:
            self.setts._last_type = submodule

            # if self.setts.mbuff():
            #     self.buffer[self.setts.mbuff].buffer += [presymbol + code + postsymbol]

            # else:
            self.buffer += [presymbol + code + postsymbol]

            self.slave._add(presymbol + code + postsymbol)

        # depend on setting echo in "t" print code or not
        # do not test it in every generate method!!!
        if self.setts.echo(echo, check='x'):
            print(f'[pinky.texme.{submodule}]\n{code}')


#$$$ ____________ class slave ______________________________________________ #

    class slave:
        def __init__(self, core=None):
            self.core = core
            self.data = {}

        def add(self, id, **kwargs):
            self.data[id] = texme(core=self.core, **kwargs)

        def _add(self, code):
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

    slave = slave()


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
        os.system(os.path.join(basepath, r'templates\bibme.bat'))


#$$$ ____________ def _copy_template ______________________________________ #

    def _copy_template(self):
        '''
        Copy template tree from input to output dir. It working in two mode: force and inteligent (.force_copy is cotroler).
        '''

        # todo if exists
        if self.setts.inpath() is None:
            verrs.BCDR_pinky_texme_ERROR_General(
                'e0624', 'Atribute "inpath" do not set!\n'
                'Tip: type .setts.inpath = ...'
            )

        # if force copy is True or folder does not exists
        if self.setts.force_copy() or not os.path.exists(self.setts.path()):

            # first, if output dir exists, then delete is
            if os.path.isdir(self.setts.path()):

                # by full tree
                shutil.rmtree(self.setts.path())

            # then update bibliography by central data
            self.bib_update()

            # at least copy dir from input to output
            shutil.copytree(self.setts.inpath(), self.setts.path())


        # if force mode is deactive
        else:
            # exists of path is alredy done
            # save base path
            path = os.path.join(self.setts.path(), self.setts.inname())

            # if output folder exists, then check if bak folder exists
            if os.path.exists(path):
                os.remove(path)

            if not os.path.exists(path + '.bak'):
                pathT = os.path.join(self.setts.inpath(), self.setts.inname() + '.bak')
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


        path = os.path.abspath(os.path.join(self.setts.path(),
        os.path.splitext(self.setts.inname())[0]+'.py'))

        spec = importlib.util.spec_from_file_location("template", path)
        template = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(template)
        ndict = template.template().run(self.setts.keys())
        sdict.update({'%<'+k+'>%': v for k, v in ndict.items()})

        # print(sdict)

        del spec,template,ndict

        # more - add user dictonary do full bank
        # sdict.update({'%<'+k+'>%': v for k, v in self.setts.keys.items()})

        return sdict


#$$$ ____________ def _substitution_via ______________________________________ #

    def _substitution_via(self, ndict, mode):
        '''
        Copy .tex.bak file to .tex with substitution variables.
        '''

        # output main tex file path
        path1 = os.path.join(self.setts.path(), self.setts.inname())

        # output main tex file path bak file
        path2 = path1 + '.bak'

        # copy and substituion
        with open(path2, encoding='utf-8') as infile, open(path1, mode, encoding='utf-8') as outfile:
            # copy line by line
            for line in infile:
                outfile.write(translate(line, ndict))

    # TODO: latex run methods should be rewrite, bib dont work corretly etc

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
        if not self.setts.active(active, check=True):
            return

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


#$$$ ____________ def make _________________________________________________ #

    # TODO: process methods like run latex are incoplate

    # #$$$ def make
    # def make(self, active=None, fclear=None, times=None, force_mode=True, shell_escape=False, synctex=True):
    #
    #     # if user want to overwrite global active atribute
    #     if active is None: active = self._active
    #
    #     # if user want to overwrite global times atribute
    #     if times  is None: times  = self._times
    #
    #     # if user want to overwrite global fclear atribute
    #     if fclear is None: fclear = self._fclear
    #
    #     if active:
    #
    #         # if times is more than zero, then start loop making pdf
    #         for i in range(times):
    #             self._pdf_maker(force_mode, shell_escape, synctex)
    #             if i == 2:
    #                 self._bib_loader()
    #
    #         # after all you can clean output dir
    #         if fclear:
    #             self._tex_clear()


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

    def text(self, text, re=None, strip=True, active=None, inherit=None, echo=None, pbeg=None, pend=None, scope=None):
        '''
        Add formated text to tex document. Text can be striped and filter regme changed.
        '''

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # if page is typed
        pbeg = self.page(pbeg, inherit='beg')
        pend = self.page(pend, inherit='end')

        # use global settings
        scope = self.setts.check('scope', scope)
        re    = self.setts.check('re'   ,
            {'xt':re} if type(re)==str else re)

        # use filter regme
        code = regme(text, scope, re['xt'])

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

    def head(self, lvl, text, label=None, text2=None, re=None, without_number=False, minitoc=None, active=None, inherit=None, echo=None, pbeg=None, pend=None, scope=None):
        '''
        '''

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # if page is typed
        pbeg = self.page(pbeg, inherit='beg')
        pend = self.page(pend, inherit='end')

        # use global settings
        self.setts.tools.check = True
        scope   = self.setts.scope ( scope )
        echo    = self.setts.echo  ( echo  )
        re      = self.setts.re    ( re    )
        label   = self.setts.label ( h=label , check='h'   )
        minitoc = False
        self.setts.tools.check = False

        # use filter regme
        texo = text
        text = regme(text, scope, re['ht'])

        if label is True:
            firstletters = ''.join([i[0].lower() for i in texo.split()])
            lab = '\\hedlab{h'+str(lvl)+':' + firstletters + '}'

        elif label:
            lab = '\\hedlab{' + label + '}'

        else:
            lab = ''

        if without_number:
            without_number = '*'
        else:
            without_number = ''

        nlvl = lvl+self.setts.hlvl_inc()

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
                nlvl,self.setts.hlvl_inc)

        if text2:
            text2 = '[' + regme(text2, scope, re['ht2']) + ']'
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

            display(HTML(source.strip()))

        self.setts._last_head.update(
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

    def pic(self, path, caption=False, label=None, float=None, abs_path=False, frame=True, grey_scale=False, caption2=False, re=None, width_factor=1, height_factor=0.95, mode='fig', pic_root=None, pic_error=True, active=None, inherit=None, echo=None, pbeg=None, pend=None, scope=None):
        '''
        '''

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # if page is typed
        pbeg = self.page(pbeg, inherit='beg')
        pend = self.page(pend, inherit='end')

        # use global settings
        self.setts.tools.check = True
        scope    = self.setts.scope    ( scope              )
        echo     = self.setts.echo     ( echo               )
        re       = self.setts.re       ( re                 )
        pic_root = self.setts.pic_root ( pic_root           )
        label    = self.setts.label    ( p=label , check='p')
        float    = self.setts.float    ( p=float , check='p')
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

            code += translate( '\\includegraphics[{1}width={2}\\linewidth,height={3}\\textheight,keepaspectratio]{{0}}\n',
                {'{0}': path,
                 '{1}': frame,
                 '{2}': str(width_factor),
                 '{3}': str(height_factor)})

            if caption:
                caption = regme(caption, scope, re['pc'])

                if caption2:
                    cap2='['+regme(
                        caption2,scope, re['pc2'])+']'
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

            if caption:
                caption = regme(caption, scope, re['pc'])

                if caption2:
                    cap2='['+regme(caption2,scope, re['pc2'])+']'
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
                pathA, width=self.setts.pic_diswidth()
            ))

        return self.add(
            submodule = 'pic',
            code      = pbeg+code+pend,
            inherit   = inherit,
            echo      = echo,
        )
    p = pic


#$$$ ____________ def math _________________________________________________ #

    def math(self, equation, mode='i', label=None, re=None, exe=False, strip=True, active=None, inherit=None, echo=None, pbeg=None, pend=None, scope=None):
        '''
        Please remember about problem with equation block - there is fault working labels. To fix it use gather instead equation block. \\leavemode should fix it, but it is not tested yet.
        '''

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # if given is list, then return self looped
        if type(equation)==list:
            if type(mode)==list:
                return [self.math(equation=eq, mode=mo, label=label, re=re, exe=exe, strip=strip, active=active, inherit=inherit, echo=echo, pbeg=pbeg, pend=pend, scope=scope) for eq,mo in zip(equation, mode)]
            else:
                return [self.math(equation=eq, mode=mode, label=label, re=re, exe=exe, strip=strip, active=active, inherit=inherit, echo=echo, pbeg=pbeg, pend=pend, scope=scope) for eq in equation]

        # if page is typed
        pbeg = self.page(pbeg, inherit='beg')
        pend = self.page(pend, inherit='end')

        # use global settings
        self.setts.tools.check = True
        scope   = self.setts.scope ( scope )
        echo    = self.setts.echo  ( echo  )
        re      = self.setts.re    ( re    )
        self.setts.tools.check = False

        if strip:
            equation = equation.strip()

        if mode in ['t*', 't+', 't']:
            code = regme(equation, scope, re['mt'])

            if 'm' in echo:
                display(Markdown(code))

            return self.add(
                submodule = 'm',
                code      = pbeg+code+pend,
                inherit   = inherit,
                echo      = echo,
            )

        equation = regme(equation, scope, re['me'])

        if exe:
            exec(equation, scope)

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

        if 'm' in echo:
            display(Latex(
                '$'+regme(equation, scope, re['mo'])+'$'
            ))

        return self.add(
            submodule = 'm',
            code      = pbeg+code+pend,
            inherit   = inherit,
            echo      = echo,
        )
    m = math



#$$$ ____________ def tab __________________________________________________ #

    def tab(self, cols, data, options=r'\textwidth', caption=None, label=None, float=False, header=None, stretchV=1.5, re=None, active=None, inherit=None, echo=None, pbeg=None, pend=None, scope=None):

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # if page is typed
        pbeg = self.page(pbeg, inherit='beg')
        pend = self.page(pend, inherit='end')

        # use global settings
        self.setts.tools.check = True
        scope   = self.setts.scope ( scope )
        echo    = self.setts.echo  ( echo  )
        re      = self.setts.re    ( re    )
        float    = self.setts.float( t=float , check='t')
        self.setts.tools.check = False

        if caption:
            if label:
                label = '\\tablab{'+label+'}'
            else:
                label = ''

            caption = '\\caption{' + \
                regme(caption, scope, re['tc']) + '}'+ label +'\\\\'
        else:
            caption = ''

        if header:
            header = '\\hlineb\n' + \
                regme(header, scope, re['td']) + \
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
                 '%Dat': regme(data, scope, re['td'])}
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

    def code(self, code, caption='', label='', style=None, language=None, re=None, strip=True, mathescape=True, active=None, inherit=None, echo=None, pbeg=None, pend=None, scope=None):

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # if page is typed
        pbeg = self.page(pbeg, inherit='beg')
        pend = self.page(pend, inherit='end')

        # use global settings
        self.setts.tools.check = True
        scope    = self.setts.scope    ( scope              )
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

        caption = regme(caption, scope, re['cc'])

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

            code = regme(code, scope, re['ce'])

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



    def file(self, path, caption=None, label=None, first_line=0, last_line=1e10, absolute_path=False, language='Python', re=None, active=None, inherit=None, echo=None, pbeg=None, pend=None, scope=None):
        '''
        '''

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # if page is typed
        pbeg = self.page(pbeg, inherit='beg')
        pend = self.page(pend, inherit='end')

        # use global settings
        self.setts.tools.check = True
        scope    = self.setts.scope    ( scope              )
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
        tex = tex.replace('%1', regme(caption, scope, re['fc']))
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

    def item(self, text=None, equation=None, mode='i', lmath=None, label=None, width=None, ilvl=None, prefix='*', postfix=':', re=None, exe=False, col_l=None, col_r=None, active=None, inherit=None, echo=None, pbeg=None, pend=None, scope=None):
        '''
        Column type must can defined explicit size in length dimension (like p{50mm} (or q,w,e).
        '''

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # use global settings
        self.setts.tools.check = True
        scope    = self.setts.scope    ( scope              )
        width    = self.setts.iwidth   ( width              )
        re       = self.setts.re       ( re                 )
        ilvl     = self.setts.ilvl     (ilvl                )
        self.setts.tools.check = False

        # if page is typed
        pbeg = self.page(pbeg, inherit='beg')
        pend = self.page(pend, inherit='end')

        # prefix if-block
        if prefix in ['',' ']:
            ptext = r'{}&'*(ilvl-1)
            pcols = r'q{3mm}'*(ilvl-1)
            width -= (ilvl-1)*5

        elif prefix in ['|']:
            ptext = r''
            pcols = r'@{\hspace{1mm}}|' + r'@{\hspace{3mm}}|'*(ilvl-1)
            width -= 2+(ilvl-1)*4

        elif prefix in ['-']:
            ptext = r'{}&'*(ilvl-1) + r'-- & '
            pcols = r'q{3mm}'*ilvl
            width -= (ilvl-1)*7

        elif prefix in ['*']:
            ptext = r'{}&'*(ilvl-1) + r'\textbullet & '
            pcols = r'q{3mm}'*ilvl
            width -= (ilvl-1)*7

        else:
            verrs.BCDR_pinky_texme_ERROR_General(
                'e0627', 'Unrecognized prefix element'
            )

        # remove too big space between to texme-items
        if self.setts._last_type == 'i':
            space_bt = '\\vspace*{-11pt}\n'
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
                    r"{ptext}{text}{postfix}&%""\n"
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
                        r"{ptext}{text}{postfix}%""\n"
                        r"{flush_math}"
                        r"\end{tabularx}""\n"
                        r"\vspace*{-7mm}""\n"
                        r"{equation}"
                        )
                else:
                    tex = (
                        r"{space_bt}"
                        r"\begin{tabularx}{\textwidth}{columns}""\n"
                        r"{ptext}{text}{postfix}%""\n"
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
                r"{ptext}{text}{postfix}%""\n"
                r"\end{tabularx}"
                )

            glue = ''

        if equation:
            equation = self.math(
                mode        = mode,
                equation    = equation,
                label       = label,
                re          = re,
                inherit     = True,
                exe         = exe,
                scope       = scope,
            )

            if type(equation)==list:
                equation = glue.join(equation)


        tex = translate(tex, {
            '{space_bt}'  : space_bt,
            '{columns}'   : columns,
            '{ptext}'     : ptext,
            '{text}'      : regme(text.strip(), scope, re['xt']),
            '{postfix}'   : postfix,
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

#$ ######################################################################### #
