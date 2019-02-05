'''
------------------------------------------------------------------------------
BCDR += ***** create (r)e(s)ructured (t)ext (m)assive (e)nvelope *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
    Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

import os
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

from IPython.display import Image, Latex, HTML, Markdown, display

from . import verrs
from . import texttable
from . import cjkwrap

from ...tools.setts import settsmeta



#$ ____ class setts ________________________________________________________ #

class setts(settsmeta):

    _self = None # here will be placed self instance
    _report_mode = None # support variable

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
            verrs.BCDR_pinky_rstme_ERROR_Type_Check(type(value), 'bool')

        if self.__save__: self.__active = value
        else:             self.__temp__ = value


#$$ ________ def echo ______________________________________________________ #

    __echo = ''

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
        > "t" -- table,
        > "r" -- plain tex code which will be included into tex document.

        User can type value as True then will be set "hmpt" configuration or False then no output will be produced.
        '''

        if value == True:
            value = 'hmpt'

        elif value == False:
            value = ''

        elif type(value)==str:

            for letter in value:
                if not letter in ['h','m','p','t','r']:
                    verrs.BCDR_pinky_rstme_ERROR_String_Selector(letter, 'hmptr')

        else:
            verrs.BCDR_pinky_rstme_ERROR_Type_Check(type(value), 'str|bool')

        if self.__save__: self.__echo   = value
        else:             self.__temp__ = value


        # # automaticly call to msg method after all built method
        # self.display = False


#$$ ________ def path ______________________________________________________ #

    __path = None

    @property
    def path(self):
        if self.__path is None:
            if self._self.core:
                if self._self.core.dbase.setts.path==':memory:':
                    return 'main.brst'
                else:
                    return os.path.splitext(self._self.core.dbase.setts.path)[0] + '.brst'
            else:
                return 'main.brst'
        else:
            return self.__path

    @path.setter
    def path(self, value):
        '''
        Output path related to actual state of kernel. In mostly case it refer to input file. The existing of folder will be checked during template coping.
        '''

        if type(value) is not str:
            verrs.BCDR_pinky_rstme_ERROR_Type_Check(type(value), 'str')

        if self.__save__: self.__path   = value
        else:             self.__temp__ = value


#$$ ________ def width _____________________________________________________ #

    __width = 80

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        '''
        Width of the page as monospace symbols count.
        '''

        if type(value) is not int:
            verrs.BCDR_pinky_rstme_ERROR_Type_Check(type(value), 'int')

        if self.__save__: self.__width  = value
        else:             self.__temp__ = value


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
            verrs.BCDR_pinky_rstme_ERROR_Type_Check(type(value), 'bool')

        if self.__save__: self.__inherit = value
        else:             self.__temp__ = value





#$$ ________ def wrap ______________________________________________________ #

    __wrap = 'xhmt'

    @property
    def wrap(self):
        return self.__wrap

    @wrap.setter
    def wrap(self, value):
        '''
        '''

        if value == True:
            nval = 'xhmt'

        elif value == False:
            nval = ''

        elif type(value)==str:
            for letter in value:
                if not letter in ['x','h','m','t','c']:
                    verrs.BCDR_pinky_rstme_ERROR_String_Selector(letter, 'xhmtc')

        if self.__save__: self.__wrap   = nval
        else:             self.__temp__ = nval


#$$ ________ def hautonum __________________________________________________ #

    __hautonum = True

    @property
    def hautonum(self):
        return self.__hautonum

    @hautonum.setter
    def hautonum(self, value):
        '''
        '''

        if type(value) is not bool:
            verrs.BCDR_pinky_rstme_ERROR_Type_Check(type(value), 'bool')

        if self.__save__: self.__hautonum = value
        else:             self.__temp__ = value



#$ ____ class rstme ________________________________________________________ #

class rstme:

    # class setts
    setts = setts('setts', (setts,), {})


#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, core=None):

        self.core = core

        # object setts
        self.setts = self.setts('setts',(),{'_self':self})

        # buffer list
        self.buffer = []

        # last one used command, its helpful to stylish file
        self.__last_type = None


        self._head_level = [True, 0,0,0,0,0]
        self._toc_list   = []

#$$ ________ process methods _______________________________________________ #

#$$$ ____________ def add __________________________________________________ #

    def add(self, code, inherit=None, submodule=None, echo=None, presymbol='', postsymbol='\n\n'):
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
            self.buffer += [presymbol + code + postsymbol]

        # depend on setting echo in "t" print code or not
        # do not test it in every generate method!!!
        if 'r' in self.setts.check_loc('echo', echo):
            print(f'[pinky.rstme.{submodule}]\n{code}')




#$$$ ____________ def clear _________________________________________ #

    def clear(self):
        '''
        Clear buffer.
        '''

        self.buffer = []

#$$$ ____________ def save _________________________________________________ #

    def save(self, mode='w', active=None):
        '''
        Save buffer to file, copy and substitute into inpath+inname file.
        '''

        # if user want to overwrite global active atribute
        if not self.setts.check_loc('active', active):
            return

        with open(self.setts.path, mode, encoding='utf-8') as f:
            f.writelines(self.buffer)

#$$$ ____________ def push _________________________________________________ #

    def push(self, active=None):
        '''
        Push method is connection of save and clear methods.
        '''

        if len(self.buffer) > 0:
            self.save(active=active)
        self.clear()



#$$$ ____________ def report _______________________________________________ #

    def report(self,
        mode='a+',

        general_information                 = None,
        model_data                          = None,
            materials                       = None,
                tab_mates_umate             = None,
            unit_sections                   = None,
                unit_sections_1d            = None,
                    tab_usecp_value         = None,
                    tab_usecp_point         = None,
                    tab_usecp_tsect         = None,
            nodes                           = None,
                tab_geomf_nodes             = None,
            truss                           = None,
                tab_geomf_truss             = None,
        loads                               = None,
            tab_loads_cates                 = None,
            tab_loads_lcase                 = None,
        combinations                        = None,
        static_analysis                     = None,
        dynamic_analysis                    = None,
        design_analysis                     = None,
        summary                             = None,
        toc                                 = 'b',

        ):

        if mode==False: mode=''
        lvl_list = [mode]*5

        def mloc(lvl, now):
            if now==None:
                lvl_list[lvl] = lvl_list[lvl-1]
                self.setts._report_mode = lvl_list[lvl]
                return self.setts._report_mode
            elif type(now)==str:
                lvl_list[lvl] = now
                self.setts._report_mode = lvl_list[lvl]
                return self.setts._report_mode
            else:
                return ''


        if mloc(1, general_information):

            self.h(1, 'General information')

        if mloc(1, model_data):

            self.h(1, 'Model data')

        if mloc(2, materials):

            self.h(2, 'Materials')

        if mloc(3, tab_mates_umate):

            self.core.mates.umate.echo(mode=self.setts._report_mode)

        if mloc(2, unit_sections):

            self.h(2, 'Unit sections')

        if mloc(3, unit_sections):

            self.h(3, 'Unit sections 1d')

        if mloc(4, tab_usecp_value):

            self.core.usecp.value.echo(mode=self.setts._report_mode)

        if mloc(4, tab_usecp_point):

            self.core.usecp.point.echo(mode=self.setts._report_mode)

        if mloc(4, tab_usecp_tsect):

            self.core.usecp.tsect.echo(mode=self.setts._report_mode)

        if mloc(2, nodes):

            self.h(2, 'Nodes') #$$#

        if mloc(3, tab_geomf_nodes):

            self.core.geomf.nodes.echo(mode=self.setts._report_mode)

        if mloc(2, truss):

            self.h(2, 'Truss elements') #$$#

        if mloc(3, tab_geomf_truss):

            self.core.geomf.truss.echo(mode=self.setts._report_mode)

        if mloc(1, loads):

            self.h(1, 'Loads')

        if mloc(2, tab_loads_cates):

            self.core.loads.cates.echo(mode=self.setts._report_mode)

        if mloc(2, tab_loads_lcase):

            self.core.loads.lcase.echo(mode=self.setts._report_mode)

        if mloc(1, combinations):

            self.h(1, 'Combinations')

        if mloc(1, static_analysis):

            self.h(1, 'Static analysis')

        if mloc(1, dynamic_analysis):

            self.h(1, 'Dynamic analysis')

        if mloc(1, design_analysis):

            self.h(1, 'Design analysis')

        if mloc(1, summary):

            self.h(1, 'Summary')

        if mloc(1, toc):

            self.toc(mode=self.setts._report_mode)


#$$ ________ generate methods ______________________________________________ #

#$$$ ____________ def text _________________________________________________ #

    def text(self, text, strip=True, wrap=None, inherit=None, echo=None, page=None, scope=None):
        '''
        Add formated text to document. Text can be striped and wrapped.
        '''

        # if user want to overwrite global active atribute
        if not self.setts.check_loc('active'): return

        # if strip flag
        if strip:
            # then replace text with striped text
            text = text.strip()

        # use global settings
        wrap = self.setts.check_loc('wrap', wrap)

        # if wrap flag
        if 'x' in wrap:

            # divide text by new line symbol
            code = text.split('\n')

            # new three-lvl list comprehension
            code = '\n'.join(['\n'.join(['\n'.join(cjkwrap.wrap(line, self.setts.width,
                     break_long_words=False, replace_whitespace=False))
                     for line in text.splitlines() if line.strip() != ''])
                     for text in code])

        # if wrap is turned off, then simply code refer to text
        else:
            code = text

        return self.add(
            submodule = 'x',
            code      = code,
            inherit   = inherit,
            echo      = echo,
        )
    x = text


#$$$ ____________ def head _________________________________________________ #

    def head(self, lvl, text, add_to_toc=True, hautonum=None, inherit=None, echo=None, page=None, scope=None):
        '''
        # with overline, for parts
        * with overline, for chapters
        =, for sections
        -, for subsections
        ^, for subsubsections
        ", for paragraphs
        '''

        hautonum = self.setts.check_loc('hautonum', hautonum)

        if hautonum==True:
            self._head_level[lvl]+=1

            for i in range(5-lvl) :
                self._head_level[5-i]=0

            number = '.'.join(str(x) for x in self._head_level[1:lvl+1]) + '  '

        else:
            number =''

        # if user want to overwrite global active atribute
        if not self.setts.check_loc('active'): return

        # use global settings
        echo = self.setts.check_loc('echo', echo)

        if lvl==0:
            sep_u,sep_l = '#','#'
        elif lvl==1:
            sep_u,sep_l = '*','*'
        elif lvl==2:
            sep_u,sep_l = None,'='
        elif lvl==3:
            sep_u,sep_l = None,'-'
        elif lvl==4:
            sep_u,sep_l = None,'^'
        elif lvl==5:
            sep_u,sep_l = None,'"'
        else:
            verrs.BCDR_pinky_rstme_ERROR_Header_Level(lvl)

        code = (
            '\n\n'+(sep_u*self.setts.width + '\n' if sep_u else '') +
            ('\n' if lvl==0 else '') +
            '#' + '$'*lvl + ' ' + number + text + '\n' +
            ('\n' if lvl==0 else '') +
            (sep_l*self.setts.width + '\n' if sep_l else '')
        )

        if add_to_toc:
            self._toc_list += [[number,text]]

        if 'h' in echo:
            if   lvl==1: color = "255,127,80"
            elif lvl==2: color = "165,127,80"
            elif lvl==3: color = "125,127,80"
            elif lvl==4: color = "125,177,80"
            else          : color = "255,255,255"

            source = "<h{2} style='color: rgb({0})'>{1}</h1>".format(
                color,text,lvl)

            display(HTML(source.strip()))

        return self.add(
            submodule = 'h' + str(lvl),
            code      = code,
            inherit   = inherit,
            echo      = echo,
        )
    h = head


#$$$ ____________ def math _________________________________________________ #

    def math(self, equation, mode='p', center=True, inherit=None, echo=None, page=None, scope=None):
        '''
        '''

        if mode == 'p': # pretty print
            equation = sp.pretty(parse_expr(equation, evaluate=False), use_unicode=False)

        elif mode =='i':
            equation = equation

        if center and mode not in ['i']:
            code_div = equation.split('\n')
            max_len = 0
            for chunk in code_div:
                if len(chunk) > max_len:
                    max_len = len(chunk)

            add_len = int((self.setts.width - max_len)/2)
            for i in range(len(code_div)):
                code_div[i] = add_len*' ' + code_div[i]

            code = '\n'.join(code_div)

        else:
            code = equation

        return self.add(
            submodule = 'm',
            code      = code,
            inherit   = inherit,
            echo      = echo,
        )
    m = math


#$$$ ____________ def tab __________________________________________________ #

    def table(self, data, header=None, width=None, halign=None, valign=None, dtype=None, wrap=True, caption=None, precision=None, border=None, inherit=None, echo=None, page=None, scope=None):
        '''
        '''

        # if user want to overwrite global active atribute
        if not self.setts.check_loc('active'): return

        # use global settings
        echo = self.setts.check_loc('echo', echo)

        table = texttable.Texttable()
        table.wrap = wrap

        if width     : table.set_cols_width(width)
        if halign    : table.set_cols_align(halign)
        if valign    : table.set_cols_valign(valign)
        if dtype     : table.set_cols_dtype(dtype)
        if precision : table.set_precision(precision)
        if header    : table.header(header)

        if border == False:
            table.set_deco(0)

        # convert None to empty string, better to plot...
        # DONE: in texttable module
        # data = [[item if item!=None else '.' for item in row] for row in data]

        table.add_rows(rows=data, header=False)

        code = table.draw()

        if caption:
            code = '#t Tab. ' + caption + '\n' + code

        if 't' in echo:
            print(code)

        return self.add(
            submodule = 't',
            code      = code,
            inherit   = inherit,
            echo      = echo,
        )
    t = table



#$$$ ____________ def code _________________________________________________ #

    def code(self, code, language = None, inherit = None):
        pass


#$$$ ____________ def toc __________________________________________________ #

    def toc(self, mode='b'):

        head = self.h(1, 'List of Content', inherit=True, add_to_toc=False, hautonum=False)

        data = self.core.pinky.rstme.table(
            wrap   = [False, True],
            width  = [10,True],
            halign = ['r','l'],
            valign = ['u','u'],
            dtype  = ['t','t'],
            data   = self._toc_list,
            border = False,
            inherit= True,
        )

        if not data: return

        # if mode is begging
        if mode=='b':
            self.buffer = [head + '\n' + data + '\n\n\n'] + self.buffer

        # if mode is end
        elif mode=='e':
            self.buffer += [head + '\n' + data]

        # if mode is True
        elif mode==True:
            self.buffer += [head + '\n' + data]


