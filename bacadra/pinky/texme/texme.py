'''
------------------------------------------------------------------------------
BCDR += ***** create La(TeX) (m)assive (e)nvelope *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''


#$ ____ import _____________________________________________________________ #

import os
import inspect
import shutil
import subprocess
import importlib.util

from IPython.display import Image, Latex, HTML, Markdown
from IPython.display import display as ipdisplay

from ... import tools
from ...tools import setts

from . import verrs
from .regme import regme


#$ ____ class texme ________________________________________________________ #

class texme:

#$$ ________ magic methods _________________________________________________ #

#$$$ ____________ def __init__ _____________________________________________ #

    def __init__(self, core=None, **kwargs):
        self.core = core

        # other argument will be send to setts class
        # if kwarg do not exists in setts, then setts raise error
        self.setts = self.setts('setts',(),{})
        self.setts.othe = self
        self.setts.__run_init__(**kwargs)

        # list with generated and ready-to-insert code
        self.buffer = []

        # hidden atribute with last used generate method
        self.__last_type = None

#$$$ ____________ def __setattr__ __________________________________________ #

    def __setattr__(self, name, value):
        '''
        Method do not allow create new variable in class. It is provide more control over user correctly or spell-checker.
        '''

        if not hasattr(self, name) and inspect.stack()[1][3] != '__init__':
            raise AttributeError(f"Creating new attributes <{name}> is not allowed!")
        super(texme, self).__setattr__(name, value)


#$$ ________ class setts ___________________________________________________ #

    class setts(setts.settsmeta):
        '''
        class provide set of atributes which working as settings. additionaly provide testing and printing methods.
        '''

        othe = None

        def __run_init__(self, **kwargs):
            # loop over items send from texme class
            for key,val in kwargs.items():
                exec(f'self.{key}={val}')



#$$$ ____________ atribute force-copy ______________________________________ #

        _force_copy = False

        @property
        def force_copy(self):
                return self._force_copy

        @force_copy.setter
        def force_copy(self, value):
            '''
            Force update of template, if true new files will be copy indepened of existsing .tex.bak file.
            '''

            if type(value) is not bool:
                raise ValueError('Type of "value" must be bool!')

            self._force_copy = value




#$$$ ____________ atribute path ____________________________________________ #

        _path = r'.\tex'

        @property
        def path(self):
                return self._path

        @path.setter
        def path(self, value):
            '''
            Output path related to actual state of kernel. In mostly case it refer to input file. The existing of folder will be checked during template coping.
            '''

            if type(value) is not str:
                raise ValueError('Type of "value" must be str!')

            self._path = value



#$$$ ____________ atribute inpath __________________________________________ #

        _inpath = None

        @property
        def inpath(self):
                return self._inpath

        @inpath.setter
        def inpath(self, value):
            '''
            Input path of tex base folder with init .tex.bak document. Path should be set to basename of this file!

            Value can be str value (=simply inpath set) or tuple2 (=inpath, inname)
            '''

            # TODO: inpath is not checked if tuple inserted, rewrite it later

            if not type(value) in [str, tuple]:
                raise ValueError('Type of "value" must be str or tuple2!')

            if type(value) == str:
                self._inpath = value

            elif type(value) == tuple:
                self._inpath = value[0]
                self.inname = value[1]



#$$$ ____________ atribute inname __________________________________________ #

        _inname = 'main.tex'

        @property
        def inname(self):
                return self._inname

        @inname.setter
        def inname(self, value):
            '''
            File of main tex document in inpath folder.
            '''

            if type(value) is not str:
                raise ValueError('Type of "value" must be str!')

                self._inname = value




#$$$ ____________ atribute cave ____________________________________________ #

        _cave = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), 'templates')

        @property
        def cave(self):
                return self._cave

        @cave.setter
        def cave(self, value):
            '''
            Atribute provide path to folder with templates. As defualt it refere to folder inside pinky.texme module call "templates".
            '''

            if type(value) is not str:
                raise ValueError('Type of "value" must be str!')

            self._cave = value



#$$$ ____________ atribute template ________________________________________ #

        _template = None

        @property
        def template(self):
                return self._template

        @template.setter
        def template(self, value):
            '''
            '''

            if type(value) is not str:
                raise ValueError('Type of "value" must be str!')

            path = os.path.join(self.cave, value)

            # if template does not exists, then return error
            if not os.path.exists(path) or not os.path.isdir(path):
                verrs.pathTemplateError(path, self.cave)

            self._template = value

            self.inpath = path, 'main.tex'


            # load external methods depend on template

            path = os.path.join(path,'main.py')

            spec = importlib.util.spec_from_file_location("external", path)

            external = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(external)

            # self.othe.ext = external.ext(self.othe)





#$$$ ____________ atribute echo ____________________________________________ #

        _echo = 'hmp'

        @property
        def echo(self):
            return self._echo

        @staticmethod
        def _echo_(value):
            if value == True:
                return 'hmp'

            elif value == False:
                return ''

            else:

                for letter in value:
                    if not letter in ['h','m','p','t']:
                        raise ValueError('Undefined driver, you can use only mix of "hmpt" letters or True/False.')

                return value

        @echo.setter
        def echo(self, value):
            '''
            Atribute <echo> set the output of base methods in texme class. It provide letters interface "hmpt" which can turn on/off

            > "h" -- colorful html header,
            > "m" -- rendered latex math equation,
            > "p" -- rendered picture with constant width,
            > "t" -- plain tex code which will be included into tex document.

            User can type value as True then will be set "hmp" configuration or False then no output will be produced.
            '''

            self._echo = self._echo_(value)


#$$$ ____________ atribute scope ___________________________________________ #

        # TODO: turn off it to printng, to long...

        _scope = {}
        scopb = {}

        @property
        def scope(self):
            if self._scope == {} and self.othe.core:
                # if user use texme as part of bacadra project and do not set texme.setts.scope then use project.mdata.setts
                if not self.scopb:
                    return self.othe.core.mdata.setts.get('scope')
                else:
                    return {**self.othe.core.mdata.setts.get('scope'), **self.scopb}
            else:
                if not self.scopb:
                    return self._scope
                else:
                    return {**self._scope, **self.scopb}

        @staticmethod
        def _scope_(value):
            if type(value) is not dict:
                raise ValueError('Type of "value" must be dictonary!')
            return value

        @scope.setter
        def scope(self, value):
            self._scope = self._scope_(value)


#$$$ ____________ atribute inherit _________________________________________ #

        _inherit = False

        @property
        def inherit(self):
                return self._inherit

        def _inherit_(self, value):
            if type(value) is not bool:
                raise ValueError('Type of "value" must be bool!')

            return value

        @inherit.setter
        def inherit(self, value):
            '''
            If true then code is returned, if false code is added to buffer.
            '''

            self._inherit = self._inherit_(value)



#$$$ ____________ atribute active __________________________________________ #

        _active = True

        @property
        def active(self):
                return self._active

        def _active_(self, value):
            if type(value) is not bool:
                raise ValueError('Type of "value" must be bool!')

            return value

        @active.setter
        def active(self, value):
            '''
            User can deactive all methods, then methods will exit at the begging.
            '''

            self._active = self._active_(value)





#$$$ ____________ atribute label ___________________________________________ #

        _label = {'h':False, 'p':True, 'f':False}

        @property
        def label(self):
                return self._label

        def _label_(self, value):
            if value == True:
                return {'h':True, 'p':True}
            elif value == False:
                return {'h':False, 'p':False}
            elif type(value) is dict:
                ndict = self._label.copy()
                for key,val in value.items():
                    if key in self._label:
                        ndict.update({key:val})
                return ndict
            else:
                raise ValueError('Type of "value" must be bool or dict!')


        @label.setter
        def label(self, value):
            '''
            label is dict with dew substitute labels types.
            '''

            self._label = self._label_(value)





#$$$ ____________ atribute rx ______________________________________________ #

        _rx = {'xt':1, 'ht':1, 'pc':1, 'me':11, 'mt':1, 'td':1, 'tc':1, 'ce':0, 'cc':1, 'fe':0, 'ie':11, 'it':1}

        @property
        def rx(self):
                return self._rx

        def _rx_(self, value):

            ndict = self._rx.copy()

            if type(value) is dict:
                for key,val in value.items():

                    if type(val) is not int:
                        raise ValueError('Type of "value" must be int!')

                    elif key in self._rx:
                        ndict.update({key:val})

                    else:
                        raise ValueError(f'Invalid key! \nTip: {self._rx}')

            else:
                if type(value) is not int:
                    raise ValueError('Type of "value" must be int!')

                for key in ndict.keys():
                    ndict[key] = value

            return ndict


        @rx.setter
        def rx(self, value):
            '''
            '''

            self._rx = self._rx_(value)




#$$$ ____________ atribute float ___________________________________________ #

        _float = {'p':False, 't':False}

        @property
        def float(self):
                return self._float

        def _float_(self, value):

            ndict = self._float.copy()

            if type(value) is dict:
                for key,val in value.items():

                    if key in self._float:
                        ndict.update({key:val})

                    else:
                        raise ValueError(f'Invalid key! \nTip: {self._float}')

            else:
                for key in ndict.keys():
                    ndict[key] = value

            return ndict


        @float.setter
        def float(self, value):
            '''
            '''

            self._float = self._float_(value)



#$$$ ____________ atribute minitoc __________________________________________ #

        _minitoc = False

        @property
        def minitoc(self):
                return self._minitoc

        def _minitoc_(self, value):
            if type(value) is not bool:
                raise ValueError('Type of "value" must be bool!')

            return value

        @minitoc.setter
        def minitoc(self, value):
            '''
            '''

            self._minitoc = self._minitoc_(value)



#$$$ ____________ atribute pic-root ________________________________________ #

        _pic_root = r'.'

        @property
        def pic_root(self):
                return self._pic_root

        @staticmethod
        def _pic_root_(value):
            '''
            '''

            if type(value) is not str:
                raise ValueError('Type of "value" must be str!')

            return value


        @pic_root.setter
        def pic_root(self, value):
            '''
            '''

            self._pic_root = self._pic_root_(value)


#$$$ ____________ atribute pic-error _______________________________________ #

        _pic_error = r'.'

        @property
        def pic_error(self):
                return self._pic_error

        @staticmethod
        def _pic_error_(value):
            '''
            '''

            if type(value) is not bool:
                raise ValueError('Type of "value" must be bool!')

            return value


        @pic_error.setter
        def pic_error(self, value):
            '''
            '''

            self._pic_error = self._pic_error_(value)



#$$$ ____________ atribute pic_diswidth ___________________________________ #

        _pic_diswidth = 600

        @property
        def pic_diswidth(self):
                return self._pic_diswidth

        def _pic_diswidth_(self, value):
            '''
            '''

            if type(value) is not int:
                raise ValueError('Type of "value" must be int!')

            return value


        @pic_diswidth.setter
        def pic_diswidth(self, value):
            '''
            '''

            self._pic_diswidth = self._pic_diswidth_(value)


#$$$ ____________ atribute head_lvl_inc ____________________________________ #

        _head_lvl_inc = 0

        @property
        def head_lvl_inc(self):
                return self._head_lvl_inc

        @staticmethod
        def _head_lvl_inc_(value):
            '''
            '''

            if type(value) is not int:
                raise ValueError('Type of "value" must be int!')

            return value


        @head_lvl_inc.setter
        def head_lvl_inc(self, value):
            '''
            '''

            self._head_lvl_inc = self._head_lvl_inc_(value)



#$$$ ____________ atribute item_1c_width _______________________________ #

        _item_1c_width = 70

        @property
        def item_1c_width(self):
                return self._item_1c_width

        def _item_1c_width_(self, value):
            '''
            '''

            if value==True:
                return 70
            elif type(value) in [int]:
                return value
            else:
                raise ValueError('Type of "value" must be int or True!')


        @item_1c_width.setter
        def item_1c_width(self, value):
            '''
            '''

            self._item_1c_width = self._item_1c_width_(value)



#$$$ ____________ atribute keys ________________________________________ #

        _keys = {}

        @property
        def keys(self):
                return self._keys

        @keys.setter
        def keys(self, value):
            '''
            '''

            if type(value) is not dict:
                raise ValueError('Type of "value" must be dict!')

            self._keys =  value



#$$ ________ class setts ___________________________________________________ #

    class setts(setts, metaclass=setts):
        pass


#$$ ________ process methods _______________________________________________ #

#$$$ ____________ def __call__ _____________________________________________ #

    # TODO: im not sure is it needed in new style, should be checked in future

    # def __call__(self, **kwargs):
    #     '''
    #     Explicit init function. It is needed, when texme is called trough project class.
    #     '''
    #
    #     for key,val in kwargs.items():
    #         if key in texme.__dict__:
    #             setattr(self, key, val)
    #         else:
    #             raise ValueError(f'Undefined parameter <{key}>.')
    #     return self


#$$$ ____________ def add __________________________________________________ #

    def add(self, code, inherit=None, submodule=None, echo='', presymbol='', postsymbol='\n%'):
        '''
        Append code to buffer. Method offer adding symbol at the end of statment, inherit base if-block and print block. It is add clear code into buffer (with additional pre- and post- symbol, but only if inherit is False, more, never in echo).
        '''

        # get default parametrs by test if None
        # do not test it in every generate method!!!
        inherit = self.setts.test('inherit', inherit)

        # base on iherit methods then return or add code
        if inherit is True:
            return code
        elif inherit is False:
            self.__last_type = submodule
            self.buffer += [presymbol + code + postsymbol]

        # depend on setting echo in "t" print code or not
        # do not test it in every generate method!!!
        self.msg(submodule=submodule, code=code, echo=echo)


#$$$ ____________ def msg __________________________________________________ #

    def msg(self, submodule, code, echo):
        '''
        Print generated code in prefered style, like text, markdown or tex.
        '''

        if 't' in echo:
            print(f'[pinky.texme.{submodule}]\n{code}')


#$$$ ____________ def clear-buffer _________________________________________ #

    def clear_buffer(self):
        '''
        Clear buffer.
        '''

        self.buffer = []


#$$$ ____________ def _bibliography_update ________________________________ #

    def _bibliography_update(self):
        '''
        Update biblography files in depend templates. It run bat script which provide copy methods.
        It should be run only before template copy, if user return calculation on already copied - then no updating prefered.
        '''

        basepath = os.path.dirname(os.path.realpath(__file__))
        os.system(os.path.join(basepath, r'templates\bibme.bat'))



#$$$ ____________ def _copy-template ______________________________________ #

    def _copy_template(self):
        '''
        Copy template tree from input to output dir. It working in two mode: force and inteligent (.force_copy is cotroler).
        '''

        if self.setts.inpath is None:
            raise ValueError('Please input inpath project')

        # if force copy is True or folder does not exists
        if self.setts.force_copy or not os.path.exists(self.setts.path):

            # first, if output dir exists, then delete is
            if os.path.isdir(self.setts.path):

                # by full tree
                shutil.rmtree(self.setts.path)

            # then update bibliography by central data
            self._bibliography_update()

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
                outfile.write(tools.translate(line, ndict))


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
        if not self.setts.test('active', active):
            return

        # prepare template to replace blocks
        self._copy_template()

        # replace in file
        self._substitution_via(self._dictonary(), mode)


#$$$ ____________ def push _________________________________________________ #

    def push(self):
        '''
        Push method is connection of save and clear_buffer methods.
        '''

        self.save()
        self.clear_buffer()


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
        if not self.setts.test('active'):
            return

        # use global settings
        inherit = self.setts.test('inherit', inherit)
        echo    = self.setts.test('echo'   , echo)

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
            raise ValueError('Unknow mode')

        return self.add(
            submodule = 'page',
            code      = code,
            inherit   = inherit,
            echo      = echo,
        )

#$$$ ____________ def ext __________________________________________________ #

    ext = None

#$$$ ____________ def text _________________________________________________ #

    def text(self, text, rx=None, strip=True, inherit=None, echo=None, page=None, scope=None):
        '''
        Add formated text to tex document. Text can be striped and filter regme changed.
        '''

        # if user want to overwrite global active atribute
        if not self.setts.test('active'):
            return

        # use global settings
        inherit = self.setts.test('inherit', inherit)
        echo    = self.setts.test('echo'   , echo)
        rx      = self.setts.test('rx'     , rx, 'xt')

        # if page is typed
        if type(page) in [str]:
            self.page(page)
        elif type(page) in [tuple]:
            self.page(page[0])

        # if scope is extended, becarfull, it overwrite
        if scope:
            self.setts._scope.update(scope)

        # use filter regme
        code = regme(text, self.setts.scope).package(rx)

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
        if not self.setts.test('active'):
            return

        # use global settings
        inherit = self.setts.test('inherit', inherit)
        echo    = self.setts.test('echo'   , echo)
        label   = self.setts.test('label'  , label, 'h')
        rx      = self.setts.test('rx'     , rx,    'ht')
        minitoc = self.setts.test('minitoc', minitoc)

        # if page is typed
        if type(page) in [str]:
            self.page(page)
        elif type(page) in [tuple]:
            self.page(page[0])

        # if scope is extended, becarfull, it overwrite
        if scope:
            self.setts._scope.update(scope)

        # use filter regme
        text = regme(text, self.setts.scope).package(rx)

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


        if lvl+self.setts.head_lvl_inc == -1:
            tex = '\\part' + without_number + '%2{%1} ' + lab
            if minitoc:
                tex += '\n\\minitoc'

        elif lvl+self.setts.head_lvl_inc == 0:
            tex = '\\chapter' + without_number + '%2{%1} ' + lab
            if minitoc:
                tex += '\n\\minitoc'

        elif lvl+self.setts.head_lvl_inc == 1:
            tex = '\\section' + without_number + '%2{%1} ' + lab

        elif lvl+self.setts.head_lvl_inc == 2:
            tex = '\\subsection' + without_number + '%2{%1} ' + lab

        elif lvl+self.setts.head_lvl_inc == 3:
            tex = '\\subsubsection' + without_number + '%2{%1} ' + lab

        elif lvl+self.setts.head_lvl_inc == 4:
            tex = '\\paragraph' + without_number + '%2{%1} ' + lab

        elif lvl+self.setts.head_lvl_inc == 5:
            tex = '\\subparagraph' + without_number + '%2{%1} ' + lab

        else:
            raise ValueError('The header level must be between <-1,5>, now lvl += alvle = '+str(lvl+self.alvl))


        if text2:
            text2 = '[' + regme(text2, self.setts.scope).package(rx) + ']'
        else:
            text2 = ''

        code = tex.replace('%1', text.strip())
        code = code.replace('%2', text2)

        if 'h' in echo:
            lvlnow = lvl+self.setts.head_lvl_inc+1

            if   lvlnow==1: color = "255,127,80"
            elif lvlnow==2: color = "165,127,80"
            elif lvlnow==3: color = "125,127,80"
            elif lvlnow==4: color = "125,177,80"
            else          : color = "255,255,255"

            source = "<h{2} style='color: rgb({0})'>{1}</h1>".format(
                color,
                text,
                lvlnow,
            )

            ipdisplay(HTML(source.strip()))

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

    def pic(self, path, caption=False, label=None, float=False, abs_path=False, frame=True, grey_scale=False, caption2=False, rxc=None, width_factor=1, height_factor=0.9, mode='fig', pic_root=None, pic_error=None, inherit=None, echo=None, page=None, scope=None):
        '''
        '''

        # if user want to overwrite global active atribute
        if not self.setts.test('active'):
            return

        # use global settings
        inherit   = self.setts.test('inherit', inherit)
        echo      = self.setts.test('echo'   , echo)
        label     = self.setts.test('label'  , label, 'p')
        rx        = self.setts.test('rx'     , rxc, 'pc')
        float     = self.setts.test('float'  , float, 'p')
        pic_root  = self.setts.test('pic_root', pic_root)
        pic_error = self.setts.test('pic_error', pic_error)

        # if page is typed
        if type(page) in [str]:
            self.page(page)
        elif type(page) in [tuple]:
            self.page(page[0])

        # if scope is extended, becarfull, it overwrite
        if scope:
            self.setts._scope.update(scope)

        # path = path.replace('/','\\')

        # save inputed path
        user_path = path

        # user can define prepath for picture
        path = os.path.join(pic_root, path)

        # first check if file is exists
        if not os.path.exists(path):
            if pic_error:
                verrs.pathError(path)
            else:
                print('Path does not exists. Picture error flag is False.\n<'+path+'>')
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
                raise ValueError('Unknow float mode')

            code += tools.translate( '\\includegraphics[{1}width={2}\\linewidth,height={3}\\textheight,keepaspectratio]{{0}}\n',
                {'{0}': path,
                 '{1}': frame,
                 '{2}': str(width_factor),
                 '{3}': str(height_factor)})

            if caption:
                caption = regme(caption, self.setts.scope).package(rx)

                if caption2:
                    cap2='['+regme(
                        caption2,self.setts.scope).package(rx)+']'
                else:
                    cap2 = ''


                code += tools.translate('\\caption{float}{1}{{0}}\n',
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
#                     caption = RegME(caption).package(captionX)
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
#                 code = tools.translate(code, ndict)
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
                raise ValueError('Unknow float mode')

            if caption:
                caption = regme(caption, self.setts.scope).package(rx)

                if caption2:
                    cap2='['+regme(
                        caption2,self.setts.scope).package(rx)+']'
                else:
                    cap2 = ''

                code += tools.translate('\\caption{float}{1}{{0}}\n',
                    {
                        '{0}'    : caption,
                        '{1}'    : cap2,
                        '{float}': ('of{table}' if not float else '')
                    })

                if type(label) is str:
                    code += '\\tablab{{0}}\n'.replace('{0}', label)

                elif label == True:
                    code += '\\tablab{{0}}\n'.replace('{0}', user_path.replace('\\', '').replace('/', ''))

            code += tools.translate( '\\includegraphics[{1}width={2}\\linewidth,height={3}\\textheight,keepaspectratio]{{0}}\n',
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
#                     caption = RegME(caption).package(captionX)
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
            ipdisplay(Image(
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

    def math(self, equation, mode='i', label=None, rxe=None, rxt=None, exe=False, inherit=None, strip=True, echo=None, page=None, scope=None):
        '''
        Please remember about problem with equation block - there is fault working labels. To fix it use gather instead equation block. \\leavemode should fix it, but it is not tested yet.
        '''

        # if user want to overwrite global active atribute
        if not self.setts.test('active'):
            return

        # if page is typed
        if type(page) in [str]:
            self.page(page)
        elif type(page) in [tuple]:
            self.page(page[0])

        # if scope is extended, becarfull, it overwrite
        if scope:
            self.setts._scope.update(scope)

        # if given is list, then return self looped
        if type(equation)==list:
            if type(mode)==list:
                return [self.math(eq1, m1, label, rxe, rxt, exe, inherit, echo) for eq1,m1 in zip(equation, mode)]
            else:
                return [self.math(eq1, mode, label, rxe, rxt, exe, inherit, echo) for eq1 in equation]

        if strip:
            equation = equation.strip()


        # use global settings
        inherit   = self.setts.test('inherit', inherit)
        echo      = self.setts.test('echo'   , echo)
        rxe       = self.setts.test('rx'     , rxe, 'me')
        rxt       = self.setts.test('rx'     , rxt, 'mt')

        if mode in ['t*', 't+', 't']:
            code = regme(equation, self.setts.scope).package(rxt)

            if 'm' in echo:
                ipdisplay(Markdown(code))

            return self.add(
                submodule = 'm',
                code      = code,
                inherit   = inherit,
                echo      = echo,
            )

        equation = regme(equation, self.setts.scope).package(rxe)

        if exe:
            exec(equation, self.setts.scope)

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
            ipdisplay(Latex(
                '$'+regme(equation, self.setts.scope).package(99)+'$'
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

    #$$$ def tab
    def tab(self, cols, data, options='\\textwidth', caption=None, label=None, float=False, header=None, stretchV=1.5, rxc=None, rxd=None, inherit=None, echo=None, page=None, scope=None):
        '''
        '''

        # if user want to overwrite global active atribute
        if not self.setts.test('active'):
            return

        # use global settings
        inherit   = self.setts.test('inherit', inherit)
        echo      = self.setts.test('echo'   , echo)
        float     = self.setts.test('float'  , float)['t']
        rxd       = self.setts.test('rx'     , rxc, 'tc')
        rxd       = self.setts.test('rx'     , rxd, 'td')

        # if page is typed
        if type(page) in [str]:
            self.page(page)
        elif type(page) in [tuple]:
            self.page(page[0])

        # if scope is extended, becarfull, it overwrite
        if scope:
            self.setts._scope.update(scope)

        if caption:
            if label:
                label = '\\tablab{'+label+'}'
            else:
                label = ''
            caption = '\\caption{' + \
                regme(caption, self.setts.scope).package(rxc) + '}'+ label +'\\\\'
        else:
            caption = ''


        if header:
            header = '\\hline\n' + \
                regme(header, self.setts.scope).package(rxd) + \
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
                 '%Dat': regme(data, self.setts.scope).package(rxd)}
        tex = tools.translate(tex, ndict)

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

    def code(self, code, caption='', label='', language='python', rxe=None, rxc=None, mathescape=True, inherit=None, echo=None, page=None, scope=None):
        '''
        '''

        # if user want to overwrite global active atribute
        if not self.setts.test('active'):
            return

        # use global settings
        inherit   = self.setts.test('inherit', inherit)
        echo      = self.setts.test('echo'   , echo)
        rxe       = self.setts.test('rx'     , rxe, 'ce')
        rxc       = self.setts.test('rx'     , rxc, 'cc')

        # if page is typed
        if type(page) in [str]:
            self.page(page)
        elif type(page) in [tuple]:
            self.page(page[0])

        # if scope is extended, becarfull, it overwrite
        if scope:
            self.setts._scope.update(scope)


        if mathescape:
            var1 = ', mathescape'
        else:
            var1 = ''

        if language:
            var2 = ',language={' + language + '}'
        else:
            var2 = ''

        if code == True:
            self._temp = [inspect.currentframe().f_back.f_lineno]

            tex = '\\begin{lstlisting}[caption={%1},label={%2}%3%4]'
            tex = tex.replace('%1', caption)
            tex = tex.replace('%2', label)
            tex = tex.replace('%4', var1)
            tex = tex.replace('%3', var2)

            _name1='c-open'

        elif code == False:
            self._temp.append(
                inspect.currentframe().f_back.f_lineno - 1)

            tex = '%%%-TO-REPLACE-%%%' + str(self._temp)

            self._add('c-replace', tex, inherit)

            tex = '\n\\end{lstlisting}'

            _name1='c-close'

        elif type(code) == str:

            tex = '\\begin{lstlisting}[caption={%1},label={%2}%3%4]'
            caption = regme(caption, self.setts.scope).package(rxc)
            tex = tex.replace('%1', caption)
            tex = tex.replace('%2', label)
            tex = tex.replace('%4', var1)
            tex = tex.replace('%3', var2)

            code = regme(code, self.setts.scope).package(rxe)
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
        if not self.setts.test('active'):
            return

        # use global settings
        inherit   = self.setts.test('inherit', inherit)
        echo      = self.setts.test('echo'   , echo)
        label     = self.setts.test('label'  , label, 'f')
        rxe       = self.setts.test('rx'     , rxe, 'fe')

        # if page is typed
        if type(page) in [str]:
            self.page(page)
        elif type(page) in [tuple]:
            self.page(page[0])

        # if scope is extended, becarfull, it overwrite
        if scope:
            self.setts._scope.update(scope)

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
        tex = tex.replace('%1', regme(caption, self.setts.scope).package(rxe))
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
        if not self.setts.test('active'):
            return

        # use global settings
        inherit   = self.setts.test('inherit', inherit)
        echo      = self.setts.test('echo'   , echo)
        width     = self.setts.test('item_1c_width' , width)
        rxe       = self.setts.test('rx'     , rxe, 'ie')
        rxt       = self.setts.test('rx'     , rxt, 'it')

        # if page is typed
        if type(page) in [str]:
            self.page(page)
        elif type(page) in [tuple]:
            self.page(page[0])

        # if scope is extended, becarfull, it overwrite
        if scope:
            self.setts._scope.update(scope)


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
            raise ValueError('Unrecognized prefix element')


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
                columns = tools.translate('{{pcols}{col_l}{{width}}{col_r}}', {
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
                columns = tools.translate('{{pcols}{col_l}}',{
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
            columns = tools.translate('{{pcols}{col_l}}',{
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


        tex = tools.translate(tex, {
            '{space_bt}'  : space_bt,
            '{columns}'   : columns,
            '{ptext}'     : ptext,
            '{text}'      : regme(text.strip(), self.setts.scope).package(rxt),
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
