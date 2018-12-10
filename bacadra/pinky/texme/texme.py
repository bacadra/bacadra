'''
------------------------------------------------------------------------------
BCDR += ***** create La(TeX) (m)assive (e)nvelope *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ____ import _____________________________________________________________ #

import os
import inspect
import shutil
import json
import subprocess

from IPython.display import Image, Latex, HTML
from IPython.display import display as ipdisplay

from . import verrs
from .regme import regme
from ... import tools



#$ ____ metaclass texmeta __________________________________________________ #

class texmemeta(type):
    #$$ class atributes

    propme = []

    #$$$ def *prop&sett scope
    propme += ['''
        @property
        def scope(self):
            if self.core:
                return self.core.mdata.setts.get('scope')
            else:
                return self._scope
        @scope.setter
        def scope(self, value):
            self._scope = value
    ''']


    #$$$ def *prop&sett tvar
    propme += ['''
        @property
        def tvar(self):
            return self._tvar
        @tvar.setter
        def tvar(self, value):
            self._tvar = value
    ''']


    #$$$ def *prop&sett times
    propme += ['''
        @property
        def times(self):
            return self._times
        @times.setter
        def times(self, value):
            self._times = value
    ''']


    #$$$ def *prop&sett fclear
    propme += ['''
        @property
        def fclear(self):
            return self._fclear
        @fclear.setter
        def fclear(self, value):
            self._fclear = value
    ''']


    #$$$ def *prop&sett keys
    propme += ['''
        @property
        def keys(self):
            return self._keys
        @keys.setter
        def keys(self, value):
            self._keys = value
    ''']


    #$$$ def *prop&sett fcopy
    propme += ['''
        @property
        def fcopy(self):
            return self._fcopy
        @fcopy.setter
        def fcopy(self, value):
            self._fcopy = value
    ''']


    #$$$ def *prop&sett template-dir
    propme += ['''
        @property
        def template_dir(self):
            return self._template_dir
        @template_dir.setter
        def template_dir(self, value):
            self._template_dir = value
    ''']


    #$$$ def *prop&sett template
    propme += ['''
        @property
        def template(self):
            return self._template
        @template.setter
        def template(self, value):
            path = os.path.join(self._template_dir, value)
            if not os.path.exists(path):
                verrs.pathError(path)

            self._template  = value
            self._input_dir  = path
            self._input_name = 'main.tex'
    ''']


    #$$$ def *prop&sett input-dir
    propme += ['''
        @property
        def input_dir(self):
            return self._input_dir
        @input_dir.setter
        def input_dir(self, value):
            self._input_dir = value
    ''']


    #$$$ def *prop&sett input_name
    propme += ['''
        @property
        def input_name(self):
            return self._input_name
        @input_name.setter
        def input_name(self, value):
            self._input_name = value
    ''']


    #$$$ def *prop&sett output-dir
    propme += ['''
        @property
        def out_path(self):
            return self._out_path
        @out_path.setter
        def out_path(self, value):
            self._out_path = value
    ''']


    #$$$ def *prop&sett active
    propme += ['''
        @property
        def active(self):
            return self._active
        @active.setter
        def active(self, value):
            self._active = value
    ''']


    #$$$ def *prop&sett echo
    propme += ['''
        @property
        def echo(self):
            return self._echo
        @echo.setter
        def echo(self, value):
            if value == True:
                self._echo = 'thmp'
            elif value == False:
                self._echo = ''
            else:
                self._echo = value
    ''']


    #$$$ def *prop&sett inherit
    propme += ['''
        @property
        def inherit(self):
            return self._inherit
        @inherit.setter
        def inherit(self, value):
            self._inherit = value
    ''']

    #$$$ def *prop&sett display-width
    propme += ['''
        @property
        def display_width(self):
            return self._display_width
        @display_width.setter
        def display_width(self, value):
            self._display_width = value
    ''']

    #$$$ def *prop&sett picture-root
    propme += ['''
        @property
        def pic_root(self):
            return self._pic_root
        @pic_root.setter
        def pic_root(self, value):
            self._pic_root = value
    ''']

    #$$$ def *prop&sett pic-error
    propme += ['''
        @property
        def pic_error(self):
            return self._pic_error
        @pic_error.setter
        def pic_error(self, value):
            self._pic_error = value
    ''']

    #$$$ def *prop&sett lvl-add
    propme += ['''
        @property
        def lvl_add(self):
            return self._lvl_add
        @lvl_add.setter
        def lvl_add(self, value):
            self._lvl_add = value
    ''']

    #$$$ def *prop&sett rm_text
    propme += ['''
        @property
        def rm_text(self):
            return {'._x_rm_text':self._x_rm_text, '._h_rm_text':self._h_rm_text, '._i_rm_text':self._i_rm_text}
        @rm_text.setter
        def rm_text(self, value):
            self._x_rm_text = value
            self._h_rm_text = value
            self._i_rm_text = value
    ''']

    #$$$ def *prop&sett picture-root
    propme += ['''
        @property
        def pic_root(self):
            return self._pic_root
        @pic_root.setter
        def pic_root(self, value):
            self._pic_root = value
    ''']

    #$$$ def *prop&sett minitoc
    propme += ['''
        @property
        def minitoc(self):
            return self._minitoc
        @minitoc.setter
        def minitoc(self, value):
            self._minitoc  = value
    ''']

    propme = inspect.cleandoc('\n'.join(propme))
    exec(propme)



#$ ____ class texme ________________________________________________________ #

class texme(metaclass=texmemeta):
    #$$ class atributes
    exec(texmemeta.propme)

    # locals of current notebook. If none, it will be try to get from self.core.dbase
    _scope = {}

    # variable to fill template settings
    _tvar = {}

    # how many times the tex will be compile
    _times = 4

    # the latex temp files will be deleted
    _fclear = False

    # force update of template, if true new files will be copy indepened of bak
    _fcopy = False

    # keys as additional replace pattern
    _keys = {}

    # path to dir, where template projects are located
    # as default it is set to pinky/texme/template folder
    _template_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'template')

    # template sett full path
    _template = 'pbw1'

    # path to root folder
    _input_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'template', 'pbw1')

    # name of main tex file in root folder
    _input_name = 'main.tex'

    # output folder
    _out_path = r'.\tex'

    # last code generation
    __last_type = ''



    # active or inactive methods to generate data
    _active = True

    # global settings change of echo settings
    # h - markdown headings
    # m - latex math
    # p - picture
    # t - plain text
    _echo = 'hmp'

    # global settings of inherit in insert method's
    _inherit = False

    # width of render images in ipython
    _display_width = 600

    # prepath of image path
    _pic_root = '.'

    # additional header level
    _lvl_add = 0

    _minitoc = True

    _pic_error = True

    # x: global
    _x_rm_text = 1

    # h: global
    _h_label = False
    _h_rm_text = 1

    # p: global
    _p_float = False
    _p_grey_scale = False
    _p_label = True
    _p_rm_caption = 1

    # m: global
    _m_mode = 'e*'
    _m_rm_equation = 11
    _m_rm_text     = 1

    # t: global
    _t_rm_float = False
    _t_rm_data = 1
    _t_rm_caption = 1

    # c: global
    _c_label = False
    _c_rm_code = 0
    _c_rm_caption = 1

    # f: global
    _f_label = False
    _f_rm_caption = 1

    # i: global
    _i_width = 70
    _i_prefix  = '*'
    _i_postfix = ':'
    _i_mode    = 'i*'
    _i_rm_text = 1
    _i_rm_equation = 11




    #$$ magic methods

    #$$$ def --init--
    def __init__(self, core=None, **kwargs):
        self.core = core

        for key,val in kwargs.items():
            if key in texme.__dict__:
                setattr(self, key, val)
            else:
                raise ValueError(f'Undefined parameter <{key}>.')


        # list with generated and ready-to-insert code
        self.buffer = []

    #$$$ def --enter--
    def __enter__(self):
        return self

    #$$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    #$$$ def --iadd--
    def __iadd__(self, othe):
        if type(othe) == texme:
            self.buffer += othe.buffer
        return self



    #$$ working methods

    #$$$ def set
    def __call__(self, **kwargs):
        '''
        Explicit init function. It is needed, when texme is called trough project class.
        '''

        for key,val in kwargs.items():
            if key in texme.__dict__:
                setattr(self, key, val)
            else:
                raise ValueError(f'Undefined parameter <{key}>.')
        return self

    #$$$ def add
    def add(self, code, inherit=False, submodule=None, echo='', presymbol='', postsymbol='\n%'):
        '''
        Append code to buffer. Method offer adding symbol at the end of statment, inherit base if-block and print block. It is add clear code into buffer (with additional pre- and post- symbol, but only if inherit is False, more, never in echo).
        '''

        if inherit is True:
            return code
        elif inherit is False:
            self.__last_type = submodule
            self.buffer += [presymbol + code + postsymbol]

        self.msg(submodule, code, echo=echo)


    #$$$ def msg
    def msg(self, submodule, code, echo):
        '''
        Print generated code in prefered style, like text, markdown or tex.
        '''

        if 't' in echo:
            print(f'[pinky.texme.{submodule}]\n{code}')



    #$$$ def clear-buffer
    def clear_buffer(self):
        '''
        Clear buffer.
        '''

        self.buffer = []

    def _bibliography_update(self):
        basepath = os.path.dirname(os.path.realpath(__file__))
        os.system(os.path.join(basepath, r'template\bibme.bat'))
        pass

    #$$$ def -copy-temp
    def _copy_template(self):
        '''
        Copy template tree from input to output dir. It working in two mode: force and inteligent (.fcopy is cotroler).
        '''
        # print(self._out_path)

        # if force copy is True
        if self._fcopy or not os.path.exists(self._out_path):
            # first, if output dir exists, then delete is
            if os.path.isdir(self._out_path):
                # by full tree
                shutil.rmtree(self._out_path)

            # then update bibliography by central data
            self._bibliography_update()

            # at least copy dir from input to output
            shutil.copytree(self._input_dir, self._out_path)

        # if force mode is deactive
        else:
            # exists of path is alredy done
            # save base path
            path = os.path.join(self._out_path, self._input_name)

            # if output folder exists, then check if bak folder exists
            if os.path.exists(path):
                os.remove(path)

            if not os.path.exists(path + '.bak'):
                pathT = os.path.join(self._input_dir, self._input_name + '.bak')
                shutil.copyfile(pathT, path)


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

        # then try to load template defaults
        # try import data from project default
        try:
            name = os.path.splitext(self._input_name)[0] + '.json'
            path = os.path.abspath(os.path.join(self._out_path, name))

            with open(path, encoding='utf8') as f:
                for key,val in json.load(f)['keys'].items():
                    sdict['%<'+key+'>%'] = val
        except:
            pass

        # more - add user dictonary do full bank
        sdict.update({'%<'+k+'>%': v for k, v in self.keys.items()})

        return sdict


    #$$$ def -replace-in-file
    def _replace_in_file(self, Dict, mode):
        path1 = os.path.join(self._out_path, self._input_name)
        path2 = path1 + '.bak'

        with open(path2, encoding='utf-8') as infile, open(path1, mode, encoding='utf-8') as outfile:
            for line in infile:
                outfile.write(tools.translate(line, Dict))

    #$$$ def -pdf-maker
    def _pdf_maker(self, force_mode, shell_escape, synctex):
        '''Start TeX compilating. There is needed pdflatex software. The sheel-escepe and forcecopy can be activated.'''
        sett = ''
        if synctex:      sett += ' -synctex=1'
        if force_mode:   sett += ' -interaction=nonstopmode -file-line-error'
        if shell_escape: sett += '--shell-escape'

        code = 'cd "{0}" & pdflatex {1} "{2}"'.format(
            self._out_path, sett, self._input_name)
        subprocess.run(code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    #$$$ def -bib-loader
    def _bib_loader(self, mode='biber'):
        '''Start BiB compilating. There are needed bibtex software. BiB root must have the extension .bib.'''
        name_noext = os.path.basename(os.path.splitext(self._input_name)[0])

        # if bibtex:
        if mode=='bibtex':
            code = 'cd "{0}" & bibtex "{1}"'.format(
                self._out_path, name_noext + '.aux')
        elif mode=='biber':
            code = 'cd "{0}" & biber "{1}"'.format(
            self._out_path, name_noext + '.bcf')
        elif mode=='bibtex8':
            code = 'cd "{0}" & bibtex8 "{1}"'.format(
            self._out_path, name_noext + '.bcf')

        subprocess.run(code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


    #$$$ def -tex-clear
    def _tex_clear(self):
        '''fclear folder after TeX compiling. There are lots file deleted, so please use it carefully.'''

        ext_list = ['.aux', '.bcf', '.fdb_latexmk', '.fls', '.run.xml', '.lof', '.lot', '.toc',
                    '.bbl', '.blg', '.lol', '.maf', '.mtc', '.out']

        for i in range(30):
            ext_list.append('.mlf' + str(i))
            ext_list.append('.mlt' + str(i))
            ext_list.append('.mtc' + str(i))

        name_noext = os.path.basename(os.path.splitext(self._input_name)[0])

        for ext in ext_list:
            if os.path.exists(os.path.join(self._out_path, name_noext) + ext):
                os.remove(os.path.join(self._out_path, name_noext) + ext)

    #$$$ def save
    def save(self, mode='w', active=None):
        # if user want to overwrite global active atribute
        if active is None: active = self._active

        if active:
            # prepare template to replace blocks
            self._copy_template()

            # replace in file
            self._replace_in_file(self._dictonary(), mode)


    #$$$ def push
    def push(self):
        # TODO: now push and save is the same
        self.save()
        self.clear_buffer()

    #$$$ def make
    def make(self, active=None, fclear=None, times=None, force_mode=True, shell_escape=False, synctex=True):

        # if user want to overwrite global active atribute
        if active is None: active = self._active

        # if user want to overwrite global times atribute
        if times  is None: times  = self._times

        # if user want to overwrite global fclear atribute
        if fclear is None: fclear = self._fclear

        if active:

            # if times is more than zero, then start loop making pdf
            for i in range(times):
                self._pdf_maker(force_mode, shell_escape, synctex)
                if i == 2:
                    self._bib_loader()

            # after all you can clean output dir
            if fclear:
                self._tex_clear()


    #$$ generate methods

    #$$$ def page
    def page(self, mode, val1=None, inherit=None, echo=None):
        '''
        Check reference:

        https://tex.stackexchange.com/questions/45609/is-it-wrong-to-use-clearpage-instead-of-newpage

        https://tex.stackexchange.com/questions/9852/what-is-the-difference-between-page-break-and-new-page

        '''

        if not self._active:
            return

        if inherit        is None: inherit       = self._inherit
        if echo           is None: echo          = self._echo

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

        else:
            raise ValueError('Unknow mode')

        return self.add(
            submodule = 'page',
            code      = code,
            inherit   = inherit,
            echo      = echo,
        )

    #$$$ def text
    def text(self, text, rm_text=None, strip=True, inherit=None, echo=None, page=None, scope=None):
        '''
        '''

        if not self._active:
            return

        if page:
            self.page(page)

        if scope:
            self.scope.update(scope)

        # use global settings
        if inherit        is None: inherit       = self._inherit
        if echo           is None: echo          = self._echo
        if rm_text        is None: rm_text       = self._x_rm_text

        code = regme(text, self.scope).package(rm_text)

        if strip:
            code = code.strip()

        return self.add(
            submodule = 'x',
            code      = code,
            inherit   = inherit,
            echo      = echo,
        )
    x = text


    #$$$ def head
    def head(self, lvl, text, label=None, text2=None, rm_text=None, without_number=False, minitoc=None, inherit=None, echo=None, page=None, scope=None):
        '''
        '''

        if not self.active:
            return

        if page:
            self.page(page)

        if scope:
            self.scope.update(scope)

        # use global settings
        if inherit        is None: inherit       = self._inherit
        if echo           is None: echo          = self._echo
        if label          is None: label         = self._h_label
        if rm_text        is None: rm_text       = self._h_rm_text
        if minitoc        is None: minitoc       = self._minitoc

        text = regme(text, self.scope).package(rm_text)

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


        if lvl+self._lvl_add == -1:
            tex = '\\part' + without_number + '%2{%1} ' + lab
            if minitoc:
                tex += '\n\\minitoc'

        elif lvl+self._lvl_add == 0:
            tex = '\\chapter' + without_number + '%2{%1} ' + lab
            if minitoc:
                tex += '\n\\minitoc'

        elif lvl+self._lvl_add == 1:
            tex = '\\section' + without_number + '%2{%1} ' + lab

        elif lvl+self._lvl_add == 2:
            tex = '\\subsection' + without_number + '%2{%1} ' + lab

        elif lvl+self._lvl_add == 3:
            tex = '\\subsubsection' + without_number + '%2{%1} ' + lab

        elif lvl+self._lvl_add == 4:
            tex = '\\paragraph' + without_number + '%2{%1} ' + lab

        elif lvl+self._lvl_add == 5:
            tex = '\\subparagraph' + without_number + '%2{%1} ' + lab

        else:
            raise ValueError('The header level must be between <-1,5>, now lvl += alvle = '+str(lvl+self.alvl))


        if text2:
            text2 = '[' + regme(text2, self.scope).package(rm_text) + ']'
        else:
            text2 = ''

        code = tex.replace('%1', text.strip())
        code = code.replace('%2', text2)

        if 'h' in echo:
            lvlnow = lvl+self._lvl_add+1

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


        return self.add(
            submodule = 'h' + str(lvl),
            code      = code,
            inherit   = inherit,
            echo      = echo,
        )

    h = head



    #$$$ def pic
    def pic(self, path, caption=False, label=None, float=False, abs_path=False, frame=True, grey_scale=None, caption2=False, rm_caption=None, width_factor=1, height_factor=0.9, mode='fig', inherit=None, echo=None, page=None, scope=None):
        '''
        '''

        if not self.active:
            return

        if page:
            self.page(page)

        if scope:
            self.scope.update(scope)

        # use global settings
        if inherit        is None: inherit       = self._inherit
        if echo           is None: echo          = self._echo
        if float          is None: float         = self._p_float
        if grey_scale     is None: grey_scale    = self._p_grey_scale
        if label          is None: label         = self._p_label
        if rm_caption     is None: rm_caption    = self._p_rm_caption

        # save inputed path
        user_path = path

        # user can define prepath for picture
        path = os.path.join(self._pic_root, path)

        # first check if file is exists
        if not os.path.exists(path):
            if self.pic_error:
                verrs.pathError(path)
            else:
                print('Path does not exists. Picture error flag is False.')
                return

        # create absoule path
        pathA = os.path.abspath(path).replace('\\', '/')

        # if user want to insert into tex global path, then simple convert
        if abs_path:
            path = pathA

        # but if not, then create relative path from current dir
        else:
            path = os.path.relpath(path, self._out_path).replace('\\', '/')

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

            code += tools.translate( '\\includegraphics[{1}width={2}\\linewidth,height={3}\\textheight,keepaspectratio]{{0}}\n',
                {'{0}': path,
                 '{1}': frame,
                 '{2}': str(width_factor),
                 '{3}': str(height_factor)})

            if caption:
                caption = regme(caption, self.scope).package(rm_caption)

                if caption2:
                    cap2='['+regme(
                        caption2,self.scope).package(rm_caption)+']'
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
                    code += '\\figlab{{0}}\n'.replace('{0}', 'fig:'+user_path.replace('\\', '').replace('/', ''))

            if float is False:
                code += '\\end{center}'
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
#                 _name1='img-tab'

        else:
            pass
            # raise ValueError('unknown mode atribute, allowed are: "fig", "tab", "lst"')


        if 'p' in echo:
            ipdisplay(Image(
                pathA, width=self._display_width
            ))

        return self.add(
            submodule = _name1,
            code      = code,
            inherit   = inherit,
            echo      = echo,
        )
    p = pic


    #$$$ def math
    def math(self, equation, mode=None, label=None, rm_equation=None, rm_text=None, exe=False, inherit=None, echo=None, strip=True, page=None, scope=None):
        '''
        Please remember about problem with equation block - there is fault working labels. To fix it use gather instead equation block. \\leavemode should fix it, but it is not tested yet.
        '''

        if not self.active or equation is None:
            return

        if page:
            self.page(page)

        if scope:
            self.scope.update(scope)

        # if given is list, then return self looped
        if type(equation)==list:
            if type(mode)==list:
                return [self.math(eq1, m1, label, rm_equation, rm_text, exe, inherit, echo) for eq1,m1 in zip(equation, mode)]
            else:
                return [self.math(eq1, mode, label, rm_equation, rm_text, exe, inherit, echo) for eq1 in equation]

        if strip:
            equation = equation.strip()

        # use global settings
        if inherit        is None: inherit       = self._inherit
        if echo           is None: echo          = self._echo
        if mode           is None: mode          = self._m_mode
        if rm_equation    is None: rm_equation   = self._m_rm_equation
        if rm_text        is None: rm_text       = self._m_rm_text


        if mode in ['t*', 't+', 't']:
            if 'm' in echo:
                ipdisplay(HTML(equation))

            return self.add(
                submodule = 'm',
                code      = regme(equation, self.scope).package(rm_text),
                inherit   = inherit,
                echo      = echo,
            )

        equation = regme(equation, self.scope).package(rm_equation)

        if exe:
            exec(equation, self.scope)

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
                '$'+regme(equation, self.scope).package(99)+'$'
            ))

        return self.add(
            submodule = 'm',
            code      = code,
            inherit   = inherit,
            echo      = echo,
        )
    m = math





    #$$$ def tab
    def tab(self, cols, data, options='\\textwidth', caption=None, label=None, float=False, header=None, stretchV=1.5, rm_caption=None, rm_data=None, inherit=None, echo=None, page=None, scope=None):
        '''
        '''

        if not self.active:
            return

        if page:
            self.page(page)

        if scope:
            self.scope.update(scope)

        # use global settings
        if inherit        is None: inherit       = self._inherit
        if echo           is None: echo          = self._echo
        if float          is None: float         = self._t_rm_float
        if rm_data        is None: rm_data       = self._t_rm_data
        if rm_caption     is None: rm_caption    = self._t_rm_caption

        if caption:
            if label:
                label = '\\tablab{'+label+'}'
            else:
                label = ''
            caption = '\\caption{' + \
                regme(caption, self.scope).package(rm_caption) + '}'+ label +'\\\\'
        else:
            caption = ''


        if header:
            header = '\\hline\n' + \
                regme(header, self.scope).package(rm_data) + \
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
                 '%Dat': regme(data, self.scope).package(rm_data)}
        tex = tools.translate(tex, ndict)

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


    #$$$ def code
    def code(self, code, caption='', label='', language='python', rm_code=None, rm_caption=None, mathescape=True, inherit=None, echo=None, page=None, scope=None):
        '''
        '''

        if not self.active:
            return

        if page:
            self.page(page)

        if scope:
            self.scope.update(scope)

        # use global settings
        if inherit        is None: inherit       = self._inherit
        if echo           is None: echo          = self._echo
        if rm_code        is None: rm_code       = self._c_rm_code
        if label          is None: label         = self._c_label
        if rm_caption     is None: rm_caption    = self._c_rm_caption

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
            caption = regme(caption, self.scope).package(rm_caption)
            tex = tex.replace('%1', caption)
            tex = tex.replace('%2', label)
            tex = tex.replace('%4', var1)
            tex = tex.replace('%3', var2)

            code = regme(code, self.scope).package(rm_code)
            tex += '\n' + code + '\n'
            tex += '\\end{lstlisting}'

            _name1='c-text'


        return self.add(
            submodule = _name1,
            code      = tex,
            inherit   = inherit,
            echo      = echo,
        )
    c = code



    def file(self, path, caption=None, label=None, first_line=0, last_line=1e10, absolute_path=False, language='Python', rm_caption=1, inherit=None, echo=None):
        '''
        '''

        if not self.active:
            return

        # use global settings
        if inherit        is None: inherit       = self._inherit
        if echo           is None: echo          = self._echo
        if label          is None: label         = self._f_label
        if rm_caption     is None: rm_caption    = self._f_rm_caption

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
        tex = tex.replace('%1', regme(caption, self.scope).package(rm_caption))
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


    #$$$ def item
    def item(self, text=None, equation=None, mode=None, lmath=None, label=None, width=None, level=1, prefix=None, postfix=None, rm_text=None, rm_equation=None, exe=False, col_type='q', inherit=None, echo=None, page=None, scope=None):
        '''
        Column type must can defined explicit size in length dimension (like p{50mm} (or q,w,e).
        '''

        # if active flag is False then with None return
        if not self.active:
            return

        if page:
            self.page(page)

        if scope:
            self.scope.update(scope)

        # use global settings
        if inherit        is None: inherit       = self._inherit
        if echo           is None: echo          = self._echo
        if width          is None: width         = self._i_width
        if mode           is None: mode          = self._i_mode
        if prefix         is None: prefix        = self._i_prefix
        if postfix        is None: postfix       = self._i_postfix
        if rm_text        is None: rm_text       = self._i_rm_text
        if rm_equation    is None: rm_equation   = self._i_rm_equation


        # prefix if-block
        if prefix in ['',' ']:
            ptext = r'{}&'*(level-1)
            pcols = r'q{3mm}'*(level-1)
            width -= (level-1)*5

        elif prefix in ['|']:
            ptext = r''
            pcols = r'@{\hspace{1mm}}|' + r'@{\hspace{3mm}}|'*(level-1)
            width -= 2+(level-1)*4

            # ptext = r'{}&'*(level-1)
            # pcols = r'@{\hspace{1mm}}|'+r'q{1mm}|'*(level-1)
            # width -= (level-1)*5

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
            if mode in ['i*', 't*', 'g*', 'm*', 'i', 't', 'g', 'm']:

                # create column pattern
                columns = tools.translate('{{pcols}{col_type}{{width}}L}', {
                    '{pcols}'   : pcols,
                    '{col_type}': col_type,
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
                # create column pattern
                columns = '{{pcols}L}'.replace('{pcols}', pcols)

                # tex = self.page('anpb-b', inherit=True)

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

            # create column pattern
            columns = '{{pcols}L}'.replace('{pcols}', pcols)

            tex = (
                r"{space_bt}"
                r"\begin{tabularx}{\textwidth}{columns}""\n"
                r"{ptext}{text}{postfix}%""\n"
                r"\end{tabularx}"
                )

            glue = ''


        equation = self.math(
            mode        = mode,
            equation    = equation,
            label       = label,
            rm_equation = rm_equation,
            rm_text     = rm_text,
            inherit     = True,
            exe         = exe)

        if type(equation)==list:
            equation = glue.join(equation)


        tex = tools.translate(tex, {
            '{space_bt}'  : space_bt,
            '{columns}'   : columns,
            '{ptext}'     : ptext,
            '{text}'      : regme(text.strip(), self.scope).package(rm_text),
            '{postfix}'   : postfix,
            '{flush_math}': flush_math,
            '{equation}'  : equation,
        })

        self.__last_type = 'i'

        return self.add(
            submodule = 'i',
            code      = tex,
            inherit   = inherit,
            echo      = echo,
        )
    i = item



    #$$$ def item2
    def item2(self, text=None, equation=None, mode='i*', mline=False, lalign=None, label=None, width=None, lvl=1, postfix=None, aligment=None, rm_text=None, rm_equation=None, vspace1='-9.5mm', vspace2='-8mm', prefix='*', add_space=False, exe=False, inherit=None, echo=None,
    e=None, # shortcut for equation
    x=None, # shortcut for text
    m=None, # shortcut for mode
    ):
        '''
        '''

        if not self.active:
            return

        # use global settings
        if inherit        is None: inherit       = self._inherit
        if echo           is None: echo          = self._echo
        if width          is None: width         = self._i_width
        if postfix        is None: postfix       = self._i_postfix
        if rm_text        is None: rm_text       = self._i_rm_text
        if rm_equation    is None: rm_equation   = self._i_rm_equation

        if e: equation = e
        if x: text = x
        if m: mode = m


        if prefix in ['|','']:
            lvl = prefix*lvl
            pre = ''

        elif prefix in ['-']:
            lvl = 'q{3mm}'
            pre = '$-$&'

        elif prefix in ['*']:
            lvl = 'q{3mm}'
            pre = r'\textbullet &'

        if self.__last_type == 'i':
            tex = '\\vspace*{-10pt}\n'
        else:
            tex = ''

        if text and equation and mode in ['i*', 't*', 't+', False, 't'] and not mline:
            if aligment: pass
            else:
                aligment = lvl+'q{{width}mm} L'
            tex += (
                "\\begin{tabularx}{\\textwidth}{{aligment}}\n"
                f"{pre}""{text}&%\n"
                "{equation}\n"
                "\\end{tabularx}"
                )

        elif text and equation and mline:
            if aligment is not None: pass
            else:
                aligment = lvl+'L'

            if lalign is not None: pass
            else: lalign = False

            tex += (
                "\\begin{tabularx}{\\textwidth}{{aligment}}\n"
                f"{pre}""{text}%\n"
                "{lalign}"
                "{equation}\n"
                "\\vspace*{{vspace2}}\n"
                "\\end{tabularx}"
                )


        elif text and equation:
            if aligment: pass
            else:
                aligment = lvl+'q{{width}mm} L'

            if lalign is not None: pass
            else: lalign = True

            tex += (
                "\\begin{tabularx}{\\textwidth}{{aligment}}\n"
                f"{pre}""{text}&%\n"
                "\\vspace*{{vspace1}}\n"
                "{lalign}"
                "{equation}\n"
                "\\vspace*{{vspace2}}\n"
                "\\end{tabularx}"
                )

        elif text and mline==True:
            if aligment: pass
            else:
                aligment = lvl+'L'

            tex += (
                "\\begin{tabularx}{\\textwidth}{{aligment}}\n"
                f"{pre}""{text}%"
                )

        elif equation and mline==True:
            aligment = ''
            if lalign is not None: pass
            else: lalign = False

            tex += (
                "{lalign}"
                "{equation}\n"
                "\\vspace*{{vspace2}}\n"
                "\\end{tabularx}"
                )


        if equation and mode is not 't':
            equation = self.math(
                mode        = mode,
                equation    = equation,
                label       = label,
                rm_equation = rm_equation,
                inherit     = True,
                exe         = exe)

        elif mode is 't':
            equation = regme(equation, self.scope).package(rm_text)

        ndict = {
            '{text}': (regme(text, self.scope).package(rm_text) + postfix if text is not None else ''),
            '{equation}': equation,
            '{aligment}': aligment.replace('{width}',str(width)),
            '{vspace1}': vspace1,
            '{vspace2}': vspace2,
            '{lalign}': ('\\mathleft\n' if lalign else ''),
        }

        tex = tools.translate(tex, ndict)

        self.__last_type = 'i'

        return self.add(
            submodule = 'i',
            code      = tex,
            inherit   = inherit,
            echo      = echo,
        )
    i2 = item2


