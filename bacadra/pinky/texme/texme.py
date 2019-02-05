'''
------------------------------------------------------------------------------
***** create La(TeX) (m)assive (e)nvelope *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ____ import _____________________________________________________________ #

import os
import inspect
import shutil
import subprocess
import importlib.util

from IPython.display import Image, Latex, HTML, Markdown,display

from ...tools.fpack import translate
from ...tools.setts import settsmeta

from . import verrs
from .regme import regme

#$ ____ class setts ________________________________________________________ #

class setts(settsmeta):

    _self = None # here will be placed self instance


#$$ ________ def force_copy ________________________________________________ #


    __force_copy = False

    @property
    def force_copy(self):
        return self.__force_copy

    @force_copy.setter
    def force_copy(self, value):
        '''
        Force update of template, if true new files will be copy indepened of existsing .tex.bak file.
        '''

        if type(value) is not bool:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'bool')

        if self.__save__: self.__force_copy = value
        else:             self.__temp__ = value


#$$ ________ def path ______________________________________________________ #

    __path = r'.\tex'

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        '''
        Output path related to actual state of kernel. In mostly case it refer to input file. The existing of folder will be checked during template coping.
        '''

        if type(value) is not str:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'str')

        if self.__save__: self.__path   = value
        else:             self.__temp__ = value


#$$ ________ def inpath ____________________________________________________ #

    __inpath = None

    @property
    def inpath(self):
            return self.__inpath

    @inpath.setter
    def inpath(self, value):
        '''
        Input path of tex base folder with init .tex.bak document. Path should be set to basename of this file!

        Value can be str value (=simply inpath set) or tuple2 (=inpath, inname)
        '''

        # TODO: inpath is not checked if tuple inserted, rewrite it later

        if not type(value) in [str, tuple]:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'str,tuple')

        if self.__save__:
            if type(value) == str:
                self.__inpath = value

            elif type(value) == tuple:
                self.__inpath = value[0]
                self.inname = value[1]


#$$ ________ def inname ____________________________________________________ #

    __inname = 'main.tex'

    @property
    def inname(self):
            return self.__inname

    @inname.setter
    def inname(self, value):
        '''
        File of main tex document in inpath folder.
        '''

        if type(value) is not str:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'str')

        if self.__save__: self.__inname = value
        else:             self.__temp__ = value


#$$ ________ def cave ______________________________________________________ #

    __cave = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'templates')

    @property
    def cave(self):
            return self.__cave

    @cave.setter
    def cave(self, value):
        '''
        Atribute provide path to folder with templates. As defualt it refere to folder inside pinky.texme module call "templates".
        '''

        if type(value) is not str:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'bool')

        if self.__save__: self.__cave   = value
        else:             self.__temp__ = value



#$$ ________ def template __________________________________________________ #

    __template = None # name of template
    ext = None # here will be placed external module

    @property
    def template(self):
            return self.__template

    @template.setter
    def template(self, value):
        '''
        '''

        if type(value) is not str:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'str')

        path = os.path.join(self.cave, value)

        # if template does not exists, then return error
        if not os.path.exists(path) or not os.path.isdir(path):
            verrs.pathTemplateError(path, self.cave)


        if self.__save__:

            self.__template = value

            self.inpath = path, 'main.tex'

            # load external methods depend on template

            path = os.path.join(path,'main.py')

            spec = importlib.util.spec_from_file_location("external", path)

            external = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(external)

            self.ext = external.ext(self._self)

        else:
            self.__temp__ = value


#$$ ________ def echo ______________________________________________________ #

    __echo = 'hmptc'

    @property
    def echo(self):
        return self.__echo

    @echo.setter
    def echo(self, value):
        '''
        Atribute <echo> set the output of base methods in texme class. It provide letters interface "hmpt" which can turn on/off

        > "h" -- colorful html header,
        > "m" -- rendered latex math equation,
        > "p" -- rendered picture with constant width,
        > "t" -- rendered tables (don't work yet),
        > "c" -- code cell (don't work yet),
        > "+" -- plain tex code which will be included into tex document.

        User can type value as True then will be set "hmptc" configuration or False then no output will be produced.
        '''

        if value == True:
            value = 'hmptc'

        elif value == False:
            value = ''

        else:

            for letter in value:
                if not letter in ['h','m','p','t','c','+']:
                    verrs.BCDR_pinky_texme_ERROR_String_Selector(
                    letter, 'hmptc+,True,False'
                    )

        if self.__save__: self.__echo   = value
        else:             self.__temp__ = value




#$$ ________ def ssel ______________________________________________________ #

    __ssel  = 0   # select scope bank

    # @property
    # def ssel(self):
    #     return self.__ssel
    #
    # @ssel.scope
    # def ssel(self, id):
    #     '''
    #     Selector of scope variable. 0-9.
    #     '''
    #
    #     if type(id) not in [int,bool]:
    #         verrs.BCDR_pinky_texme_ERROR_Type_Check(type(id), 'int,bool')
    #
    #     if id==True:
    #         id = 0
    #
    #     if self.__save__: self.__ssel = id
    #     else:             self.__temp__ = id


#$$ ________ def scope _____________________________________________________ #

    _scope = [{}]*10 # turn off it to printng, to long...
    __ssel  = None # select scope bank

    @property
    def scope(self):
        if self.__ssel==None and self._self and self._self.core:
            return self._self.core.setts.scope
        elif self.__ssel==None:
            return self._scope[0]
        else:
            return self._scope[self.__ssel]

    @scope.setter
    def scope(self, value):
        '''
        There is 11 slots for scope dictonary.

        None -- load external scope from project class, but only if it exists
                if it is imposible to get external git, then return dict 0
        0    -- base dictonary, can be selected by value=True
        1..9 -- other scopes

        to change dictonary <var> = n, {..}; where n is dictonary name
        if {..} is empty, then dict will be only changed, but not replace
        if {..} is not empty, then slot will be replaced with new one dict
        '''

        # simple given dict
        if type(value)==dict:

            id = self.__ssel

            # if scope is external, then save under slot 0, but print warn
            if id==None:
                verrs.BCDR_pinky_texme_WARN_Scope_External()
                id = 0

            if self.__save__: self._scope[id] = value
            else:             self.__temp__ = value

        # if given as number,dict
        elif type(value)==tuple:
            id,value = value

            if self.__save__:
                self.__ssel = id
                verrs.BCDR_pinky_texme_INFO_Scope(id)
                if value:
                    self._scope[id] = value
            else:
                if value:
                    self.__temp__ = value
                else:
                    self.__temp__ = self._scope[id]

        elif value==True:
            self.__ssel = None
            verrs.BCDR_pinky_texme_INFO_Scope('None')




#$$ ________ def inherit ___________________________________________________ #

    __inherit = False

    @property
    def inherit(self):
        return self.__inherit

    @inherit.setter
    def inherit(self, value):
        '''
        If true then code is returned, if false code is added to buffer.
        '''

        if type(value) is not bool:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'bool')

        if self.__save__: self.__inherit = value
        else:             self.__temp__ = value



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


#$$ ________ def label _____________________________________________________ #

    __label = {'h':False, 'p':True, 'f':False, 'c':False}

    @property
    def label(self):
            return self.__label

    @label.setter
    def label(self, value):
        '''
        label is dict with dew substitute labels types.
        h -- header
        p -- picture
        f -- file
        c -- code
        '''

        if value == True:
            ndict = {'h':True, 'p':True, 'f':True}
        elif value == False:
            ndict = {'h':False, 'p':False, 'f':True}
        elif type(value) is dict:
            ndict = self.__label.copy()
            for key,val in value.items():
                if key in self.__label:
                    ndict.update({key:val})
                else:
                    verrs.BCDR_pinky_texme_ERROR_Invalid_Key(
                    key, self.__rx
                    )
        else:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'bool,dict')

        if self.__save__: self.__label  = ndict
        else:             self.__temp__ = ndict



#$$ ________ def rx ________________________________________________________ #

    __rx = {'xt':1, 'ht':1, 'pc':1, 'me':11, 'mt':1, 'td':1, 'tc':1, 'ce':0, 'cc':1, 'fe':0, 'ie':11, 'it':1}

    @property
    def rx(self):
        return self.__rx

    @rx.setter
    def rx(self, value):
        '''
        "ce" -- code-code
        "cc" -- code-caption
        '''

        ndict = self.__rx.copy()

        if type(value) is dict:
            for key,val in value.items():

                if type(val) is not int:
                    verrs.BCDR_pinky_texme_ERROR_Type_Check(type(val), 'int')

                elif key in self.__rx:
                    ndict.update({key:val})

                else:
                    verrs.BCDR_pinky_texme_ERROR_Invalid_Key(
                        key, self.__rx
                    )

        else:
            if type(value) is not int:
                verrs.BCDR_pinky_texme_ERROR_Type_Check(type(val), 'int')

            for key in ndict.keys():
                ndict[key] = value

        if self.__save__: self.__rx     = ndict
        else:             self.__temp__ = ndict


#$$ ________ def float _____________________________________________________ #

    __float = {'p':False, 't':False}

    @property
    def float(self):
            return self.__float

    @float.setter
    def float(self, value):
        '''
        '''

        ndict = self.__float.copy()

        if type(value) is dict:
            for key,val in value.items():

                if key in self.__float:
                    ndict.update({key:val})

                else:
                    verrs.BCDR_pinky_texme_ERROR_Invalid_Key(
                        key, self.__float
                    )
        else:
            for key in ndict.keys():
                ndict[key] = value

        if self.__save__: self.__float  = ndict
        else:             self.__temp__ = ndict


#$$ ________ def minitoc ___________________________________________________ #

    __minitoc = False

    @property
    def minitoc(self):
            return self.__minitoc

    @minitoc.setter
    def minitoc(self, value):
        '''
        '''

        if type(value) is not bool:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'bool')

        if self.__save__: self.__minitoc = value
        else:             self.__temp__ = value

#$$ ________ def pic_root __________________________________________________ #

    __pic_root = r'.'

    @property
    def pic_root(self):
            return self.__pic_root

    @pic_root.setter
    def pic_root(self, value):
        '''
        '''

        if type(value) is not str:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'str')

        if self.__save__: self.__pic_root = value
        else:             self.__temp__ = value


# #$$ ________ def pic_errror ________________________________________________ #
#
#     __pic_error = r'.'
#
#     @property
#     def pic_error(self):
#             return self._pic_error
#
#     @pic_error.setter
#     def pic_error(self, value):
#         '''
#         '''
#
#         if type(value) is not bool:
#             verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'bool')
#
#
#         if self.__save__: self.__pic_error = value
#         else:             self.__temp__ = value


#$$ ________ def pic_diswidth ______________________________________________ #

    __pic_diswidth = 600

    @property
    def pic_diswidth(self):
            return self.__pic_diswidth

    @pic_diswidth.setter
    def pic_diswidth(self, value):
        '''
        '''

        if type(value) is not int:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'int')

        if self.__save__: self.__pic_diswidth = value
        else:             self.__temp__ = value


#$$ ________ def head_lvl_inc ______________________________________________ #

    __head_lvl_inc = 0

    @property
    def head_lvl_inc(self):
            return self.__head_lvl_inc

    @head_lvl_inc.setter
    def head_lvl_inc(self, value):
        '''
        '''

        if type(value) is not int:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'int')

        if self.__save__: self.__head_lvl_inc = value
        else:             self.__temp__ = value



#$$ ________ def item_1c_width _____________________________________________ #

    __item_1c_width = 70

    @property
    def item_1c_width(self):
            return self.__item_1c_width

    @item_1c_width.setter
    def item_1c_width(self, value):
        '''
        '''

        if value==True:
            return 70
        elif type(value) in [int]:
            return value
        else:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'int,True')

        if self.__save__: self.__item_1c_width = value
        else:             self.__temp__ = value


#$$ ________ def keys __________________________________________________ #

    __keys = {}

    @property
    def keys(self):
            return self.__keys

    @keys.setter
    def keys(self, value):
        '''
        '''

        if type(value) is not dict:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'dict')

        if self.__save__: self.__keys   = value
        else:             self.__temp__ = value



#$$ ________ def lststyle ________________________________________________ #

    __lststyle = 'bcdr1'

    @property
    def lststyle(self):
            return self.__lststyle

    @lststyle.setter
    def lststyle(self, value):
        '''
        '''

        if type(value) is not str:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'str')

        if self.__save__: self.__lststyle = value
        else:             self.__temp__ = value



#$$ ________ def mbuff _____________________________________________________ #

    __mbuff = None

    @property
    def mbuff(self):
        return self.__mbuff

    @mbuff.setter
    def mbuff(self, value):
        '''
        '''

        kwargs={}
        if type(value)==tuple:
            value,kwargs=value

        if type(value)!=str:
            value=None


        if self.__save__:

            if type(value)==str:
                if type(self._self.buffer)!=dict:
                    self._self.buffer = {}

                if value not in self._self.buffer:
                    self._self.buffer.update(
                        {value:texme(core=self._self,**kwargs)})
                    # print('new submodule',value)

            else:
                if type(self._self.buffer)!=list:
                    self._self.buffer=[]
                else:
                    pass

            self.__mbuff = value

        else:
            self.__temp__ = value


#$ ____ class texme ________________________________________________________ #

class texme:

    # class setts
    setts = setts('setts', (setts,), {})


#$$ ________ def __init __ _________________________________________________ #

    def __init__(self, core=None, **kwargs):

        self.core = core

        # object setts
        self.setts = self.setts('setts',(),{'_self':self})

        # list with generated and ready-to-insert code
        self.buffer = []

        # hidden atribute with last used generate method
        self.__last_type = None

        for key,val in kwargs.items():
            setattr(self.setts, key, val)


#$$ ________ process methods _______________________________________________ #

#$$$ ____________ def add __________________________________________________ #

    def add(self, code, inherit=None, submodule=None, echo=None, presymbol='', postsymbol='\n%'):
        '''
        Append code to buffer. Method offer adding symbol at the end of statment, inherit base if-block and print block. It is add clear code into buffer (with additional pre- and post- symbol, but only if inherit is False, more, never in echo).
        '''

        # get default parametrs by test if None
        # do not test it in every generate method!!!
        inherit = self.setts.check_loc('inherit', inherit)

        # base on iherit methods then return or add code
        if inherit is True:
            return code

        elif inherit is False:
            self.__last_type = submodule
            if self.setts.mbuff:
                self.buffer[self.setts.mbuff].buffer += [presymbol + code + postsymbol]
            else:
                self.buffer += [presymbol + code + postsymbol]

        # depend on setting echo in "t" print code or not
        # do not test it in every generate method!!!
        if '+' in self.setts.check_loc('echo', echo):
            print(f'[pinky.texme.{submodule}]\n{code}')


#$$$ ____________ def join _________________________________________________ #

    def join(self, data, mbuff=None):
        if self.setts.mbuff:
            if mbuff==None: mbuff=self.setts.mbuff

            if type(data)==list:
                self.buffer[mbuff].buffer += data
            elif type(data)==texme:
                self.buffer[mbuff].buffer += data.buffer
            else:
                raise ValueError

        else:
            if type(data)==list:
                self.buffer += data
            elif type(data)==texme:
                self.buffer += data.buffer
            else:
                raise ValueError()


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

        if self.setts.inpath is None:
            verrs.BCDR_pinky_texme_ERROR_General(
                'e0624', 'Atribute "inpath" do not set!\n'
                'Tip: type .setts.inpath = ...'
            )

        # if force copy is True or folder does not exists
        if self.setts.force_copy or not os.path.exists(self.setts.path):

            # first, if output dir exists, then delete is
            if os.path.isdir(self.setts.path):

                # by full tree
                shutil.rmtree(self.setts.path)

            # then update bibliography by central data
            self.bib_update()

            # at least copy dir from input to output
            shutil.copytree(self.setts.inpath, self.setts.path)


        # if force mode is deactive
        else:
            # exists of path is alredy done
            # save base path
            path = os.path.join(self.setts.path, self.setts.inname)

            # if output folder exists, then check if bak folder exists
            if os.path.exists(path):
                os.remove(path)

            if not os.path.exists(path + '.bak'):
                pathT = os.path.join(self.setts.inpath, self.setts.inname + '.bak')
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


        path = os.path.abspath(os.path.join(self.setts.path,
        os.path.splitext(self.setts.inname)[0]+'.py'))

        spec = importlib.util.spec_from_file_location("template", path)
        template = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(template)
        ndict = template.template().run(self.setts.keys)
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
        path1 = os.path.join(self.setts.path, self.setts.inname)

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
        if not self.setts.check_loc('active', active):
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

    def page(self, mode, val1=None, inherit=None, echo=None):
        '''
        Check reference:

        https://tex.stackexchange.com/questions/45609/is-it-wrong-to-use-clearpage-instead-of-newpage

        https://tex.stackexchange.com/questions/9852/what-is-the-difference-between-page-break-and-new-page

        '''

        # if user want to overwrite global active atribute
        if not self.setts.check_loc('active'): return

        if mode in ['cpage', 'cp', 'clearpage']:
            '''
            Clearpage statment break page and block range for float items.
            '''
            code = r'\clearpage'

        elif mode in ['cdpage', 'cdp', 'cleardoublepage']:
            '''
            Clearpage statment break page and block range for float items.
            '''
            code = r'\cleardoublepage'

        elif mode in ['npage','np','newpage']:
            '''
            Clearpage statment break page and don't block range for float items.
            '''
            code = r'\newpage'

        elif mode in ['bpage', 'bp', 'breakpage', 'pagebreak']:
            code = r'\pagebreak'

        elif mode in ['gpage', 'gp', 'goodbreak']:
            code = r'\goodbreak'

        elif mode in ['anpb-b', 'absolutelynopagebreak-b']:
            code = r'\begin{absolutelynopagebreak}'

        elif mode in ['anpb-e', 'absolutelynopagebreak-e']:
            code = r'\end{absolutelynopagebreak}'

        elif mode in ['vs', 'vspace']:
            code = r'\vspace*{'+val1+'}'

        elif mode in ['newline', 'nl']:
            code = r'\newline'

        elif mode in [None]:
            return

        else:
            verrs.BCDR_pinky_texme_ERROR_General(
                'e0625', 'Unknow mode of page method!\n'
                'Tip: look into manual...'
            )

        return self.add(
            submodule = 'page',
            code      = code,
            inherit   = inherit,
            echo      = echo,
        )


#$$$ ____________ def text _________________________________________________ #

    def text(self, text, rx=None, strip=True, inherit=None, echo=None, page=None, scope=None):
        '''
        Add formated text to tex document. Text can be striped and filter regme changed.
        '''

        # if user want to overwrite global active atribute
        if not self.setts.check_loc('active'): return

        # use global settings
        scope = self.setts.check_loc('scope', scope)
        rx = self.setts.check_loc('rx', rx, 'xt')

        # if page is typed
        if type(page) in [str]:
            self.page(page)
        elif type(page) in [tuple]:
            self.page(page[0])

        # use filter regme
        code = regme(text, scope, rx)

        # strip begind and end of text
        if strip:
            code = code.strip()

        return self.add(
            submodule = 'x',
            code      = code,
            inherit   = inherit,
            echo      = echo,
        )
    x = text


#$$$ ____________ def head _________________________________________________ #

    def head(self, lvl, text, label=None, text2=None, rx=None, without_number=False, minitoc=None, inherit=None, echo=None, page=None, scope=None):
        '''
        '''

        # if user want to overwrite global active atribute
        if not self.setts.check_loc('active'): return

        # use global settings
        scope = self.setts.check_loc('scope', scope)
        echo    = self.setts.check_loc('echo'   , echo)
        label   = self.setts.check_loc('label'  , label, 'h')
        rx      = self.setts.check_loc('rx'     , rx,    'ht')
        minitoc = self.setts.check_loc('minitoc', minitoc)

        # if page is typed
        if type(page) in [str]:
            self.page(page)
        elif type(page) in [tuple]:
            self.page(page[0])

        # use filter regme
        text = regme(text, scope, rx)

        if label is True:
            firstletters = ''.join([i[0].lower() for i in text.split()])
            lab = '\\hedlab{h'+str(lvl)+':' + firstletters + '}'

        elif label:
            lab = '\\hedlab{' + label + '}'

        else:
            lab = ''

        if without_number:
            without_number = '*'
        else:
            without_number = ''


        nlvl = lvl+self.setts.head_lvl_inc

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
                nlvl,self.setts.head_lvl_inc)

        if text2:
            text2 = '[' + regme(text2, scope, rx) + ']'
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

        if type(page) in [tuple]:
            self.page(page[1])

        return self.add(
            submodule = 'h' + str(lvl),
            code      = code,
            inherit   = inherit,
            echo      = echo,
        )

    h = head


#$$$ ____________ def pic __________________________________________________ #

    def pic(self, path, caption=False, label=None, float=None, abs_path=False, frame=True, grey_scale=False, caption2=False, rxc=None, width_factor=1, height_factor=0.9, mode='fig', pic_root=None, pic_error=True, inherit=None, echo=None, page=None, scope=None):
        '''
        '''

        # if user want to overwrite global active atribute
        if not self.setts.check_loc('active'): return

        # use global settings
        scope = self.setts.check_loc('scope', scope)
        echo      = self.setts.check_loc('echo', echo)
        label     = self.setts.check_loc('label', label,'p')
        rx        = self.setts.check_loc('rx', rxc, 'pc')
        float     = self.setts.check_loc('float', float,'p')
        pic_root  = self.setts.check_loc('pic_root',pic_root)

        # if page is typed
        if type(page) in [str]:
            self.page(page)
        elif type(page) in [tuple]:
            self.page(page[0])

        # path = path.replace('/','\\')

        # save inputed path
        user_path = path

        # user can define prepath for picture
        path = os.path.join(pic_root, path)

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
            path = os.path.relpath(path, self.setts.path).replace('\\', '/')

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
                caption = regme(caption, scope, rx)

                if caption2:
                    cap2='['+regme(
                        caption2,scope, rx)+']'
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



            _name1='pic-fig'

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
                caption = regme(caption, scope, rx)

                if caption2:
                    cap2='['+regme(
                        caption2,scope, rx)+']'
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

            _name1='img-tab'



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
            pass
            # raise ValueError('unknown mode atribute, allowed are: "fig", "tab", "lst"')


        if 'p' in echo:
            display(Image(
                pathA, width=self.setts.pic_diswidth
            ))

        if type(page) in [tuple]:
            self.page(page[1])

        return self.add(
            submodule = _name1,
            code      = code,
            inherit   = inherit,
            echo      = echo,
        )
    p = pic


#$$$ ____________ def math _________________________________________________ #

    def math(self, equation, mode='i', label=None, rxe=None, rxt=None, exe=False, strip=True, inherit=None, echo=None, page=None, scope=None):
        '''
        Please remember about problem with equation block - there is fault working labels. To fix it use gather instead equation block. \\leavemode should fix it, but it is not tested yet.
        '''

        # if user want to overwrite global active atribute
        if not self.setts.check_loc('active'): return

        # if page is typed
        if type(page) in [str]:
            self.page(page)
        elif type(page) in [tuple]:
            self.page(page[0])

        # use global settings
        scope = self.setts.check_loc('scope', scope)
        echo      = self.setts.check_loc('echo'   , echo)
        rxe       = self.setts.check_loc('rx'     , rxe, 'me')
        rxt       = self.setts.check_loc('rx'     , rxt, 'mt')

        # if given is list, then return self looped
        if type(equation)==list:
            if type(mode)==list:
                return [self.math(eq1, m1, label, rxe, rxt, exe, inherit, echo) for eq1,m1 in zip(equation, mode)]
            else:
                return [self.math(eq1, mode, label, rxe, rxt, exe, inherit, echo) for eq1 in equation]

        if strip:
            equation = equation.strip()


        if mode in ['t*', 't+', 't']:
            code = regme(equation, scope, rxt)

            if 'm' in echo:
                display(Markdown(code))

            return self.add(
                submodule = 'm',
                code      = code,
                inherit   = inherit,
                echo      = echo,
            )

        equation = regme(equation, scope, rxe)

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
                '$'+regme(equation, scope, 99)+'$'
            ))

        if type(page) in [tuple]:
            self.page(page[1])

        return self.add(
            submodule = 'm',
            code      = code,
            inherit   = inherit,
            echo      = echo,
        )
    m = math



#$$$ ____________ def tab __________________________________________________ #

    def tab(self, cols, data, options='\\textwidth', caption=None, label=None, float=False, header=None, stretchV=1.5, rxc=None, rxd=None, inherit=None, echo=None, page=None, scope=None):
        '''
        '''

        # if user want to overwrite global active atribute
        if not self.setts.check_loc('active'): return

        # use global settings
        scope = self.setts.check_loc('scope', scope)
        echo      = self.setts.check_loc('echo'   , echo)
        float     = self.setts.check_loc('float'  , float)['t']
        rxd       = self.setts.check_loc('rx'     , rxc, 'tc')
        rxd       = self.setts.check_loc('rx'     , rxd, 'td')

        # if page is typed
        if type(page) in [str]:
            self.page(page)
        elif type(page) in [tuple]:
            self.page(page[0])

        if caption:
            if label:
                label = '\\tablab{'+label+'}'
            else:
                label = ''
            caption = '\\caption{' + \
                regme(caption, scope, rxc) + '}'+ label +'\\\\'
        else:
            caption = ''


        if header:
            header = '\\hline\n' + \
                regme(header, scope, rxd) + \
                '\n\\\\\\hline\\hline\\hline\\hline\n\\endhead'
        elif not float:
            header = '\\endhead'
        else:
            header = ''

        tex = ("\\begingroup"
            "\\renewcommand*{\\arraystretch}{%StV}"
            "\\begin{tabularx}{%Opt}{%Col}"
            "%Cap"
            "%Hea"
            "%Dat"
            "\\end{tabularx}"
            "\\endgroup")

        ndict = {'%Opt': options,
                 '%Col': cols,
                 '%Cap': caption,
                 '%StV': str(stretchV),
                 '%Lab': label,
                 '%Hea': header,
                 '%Dat': regme(data, scope, rxd)}
        tex = translate(tex, ndict)

        if float == True:
            tex = '\\begin{table}\n' + tex + '\n\\end{table}'
        elif float == False:
            pass
        elif float == 'H':
            tex = '\\begin{table}[H]\n' + tex + '\n\\end{table}'

        if type(page) in [tuple]:
            self.page(page[1])

        return self.add(
            submodule = 't',
            code      = tex,
            inherit   = inherit,
            echo      = echo,
        )
    t = tab


#$$$ ____________ def code _________________________________________________ #

    def code(self, code, caption='', label='', style=None, language=None, rxe=None, rxc=None, strip=True, mathescape=True, inherit=None, echo=None, page=None, scope=None, rst=False):
        '''
        '''

        # if user want to overwrite global active atribute
        if not self.setts.check_loc('active'): return

        # use global settings
        scope = self.setts.check_loc('scope', scope)
        echo = self.setts.check_loc('echo',echo)
        label = self.setts.check_loc('label',label,'c')
        rxe = self.setts.check_loc('rx', rxe,'ce')
        rxc = self.setts.check_loc('rx', rxc,'cc')
        style = self.setts.check_loc(
            'lststyle', style if rst==False else 'bcdr_rst_tables')

        # if page is typed
        if type(page) in [str]:
            self.page(page)
        elif type(page) in [tuple]:
            self.page(page[0])

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

        caption = regme(caption, scope, rxc)



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

            _name1='c-open'

        elif code == False:
            self._temp.append(
                inspect.currentframe().f_back.f_lineno - 1)

            tex = '%%%-TO-REPLACE-%%%' + str(self._temp)

            self._add('c-replace', tex, inherit)

            tex = '\n\\end{lstlisting}'

            _name1='c-close'

        elif type(code) == str:

            tex = translate('\\begin{lstlisting}[caption={%1}%2%3%5%4]'
                ,{
                    '%1': caption,
                    '%2': ',label={'+label+'},' if label else '',
                    '%4': var1,
                    '%3': var2,
                    '%5': style,
                })

            code = regme(code, scope, rxe)

            if strip:
                code = code.strip()

            tex += '\n' + code + '\n'
            tex += '\\end{lstlisting}'

            _name1='c-text'

        if type(page) in [tuple]:
            self.page(page[1])

        return self.add(
            submodule = _name1,
            code      = tex,
            inherit   = inherit,
            echo      = echo,
        )
    c = code



    def file(self, path, caption=None, label=None, first_line=0, last_line=1e10, absolute_path=False, language='Python', rxe=0, inherit=None, echo=None, page=None, scope=None):
        '''
        '''

        # if user want to overwrite global active atribute
        if not self.setts.check_loc('active'): return

        # use global settings
        scope = self.setts.check_loc('scope', scope)
        label     = self.setts.check_loc('label'  , label, 'f')
        rxe       = self.setts.check_loc('rx'     , rxe, 'fe')

        # if page is typed
        if type(page) in [str]:
            self.page(page)
        elif type(page) in [tuple]:
            self.page(page[0])

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
        tex = tex.replace('%1', regme(caption, scope, rxe))
        tex = tex.replace('%2', label)
        tex = tex.replace('%3', first_line)
        tex = tex.replace('%4', last_line)
        tex = tex.replace('%5', var2)
        tex = tex.replace('%6', path.replace('\\', '/'))

        if type(page) in [tuple]:
            self.page(page[1])

        return self.add(
            submodule = 'f',
            code      = tex,
            inherit   = inherit,
            echo      = echo,
        )
    f = file


#$$$ ____________ def item _________________________________________________ #

    def item(self, text=None, equation=None, mode='i', lmath=None, label=None, width=None, level=1, prefix='*', postfix=':', rxt=None, rxe=None, exe=False, col_l=None, col_r=None, inherit=None, echo=None, page=None, scope=None):
        '''
        Column type must can defined explicit size in length dimension (like p{50mm} (or q,w,e).
        '''

        # if user want to overwrite global active atribute
        if not self.setts.check_loc('active'): return

        # use global settings
        scope = self.setts.check_loc('scope', scope)
        width = self.setts.check_loc('item_1c_width' , width)
        rxe   = self.setts.check_loc('rx', rxe, 'ie')
        rxt   = self.setts.check_loc('rx', rxt, 'it')

        # if page is typed
        if type(page) in [str]:
            self.page(page)
        elif type(page) in [tuple]:
            self.page(page[0])

        # prefix if-block
        if prefix in ['',' ']:
            ptext = r'{}&'*(level-1)
            pcols = r'q{3mm}'*(level-1)
            width -= (level-1)*5

        elif prefix in ['|']:
            ptext = r''
            pcols = r'@{\hspace{1mm}}|' + r'@{\hspace{3mm}}|'*(level-1)
            width -= 2+(level-1)*4

        elif prefix in ['-']:
            ptext = r'{}&'*(level-1) + r'-- & '
            pcols = r'q{3mm}'*level
            width -= (level-1)*7

        elif prefix in ['*']:
            ptext = r'{}&'*(level-1) + r'\textbullet & '
            pcols = r'q{3mm}'*level
            width -= (level-1)*7

        else:
            verrs.BCDR_pinky_texme_ERROR_General(
                'e0627', 'Unrecognized prefix element'
            )

        # remove too big space between to texme-items
        if self.__last_type == 'i':
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
                rxe         = rxe,
                rxt         = rxt,
                inherit     = True,
                exe         = exe)

            if type(equation)==list:
                equation = glue.join(equation)


        tex = translate(tex, {
            '{space_bt}'  : space_bt,
            '{columns}'   : columns,
            '{ptext}'     : ptext,
            '{text}'      : regme(text.strip(), scope, rxt),
            '{postfix}'   : postfix,
            '{flush_math}': flush_math,
            '{equation}'  : equation,
        })

        if type(page) in [tuple]:
            self.page(page[1])

        self.__last_type = 'i'

        return self.add(
            submodule = 'i',
            code      = tex,
            inherit   = inherit,
            echo      = echo,
        )
    i = item

















