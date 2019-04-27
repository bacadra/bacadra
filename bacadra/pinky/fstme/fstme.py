'''
------------------------------------------------------------------------------
***** create r)e(s)ructured (t)ext (m)assive (e)nvelope *****
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

import sympy as sp

from sympy.parsing.sympy_parser import parse_expr

from IPython.display import Image, Latex, HTML, Markdown, display

# from . import verrs

from ...tools import table

from ...tools.setts import sinit

import textwrap


#$ ____ class setts ________________________________________________________ #

class setts(sinit):

#$$ ________ def active ____________________________________________________ #

    def active(self, value=None, check=None):
        '''
        User can deactive all methods, then methods will exit at the begging.
        '''
        return self.tools.sgc('active', value, check)


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


#$$ ________ def path ______________________________________________________ #

    def path(self, folder_path=None, check=None):
        '''
        Output path related to actual state of kernel. In mostly case it refer to input file. The existing of folder will be checked during template coping.
        '''

        path = self.tools.chk('path', folder_path)

        if path==True:

            self.tools.set('path', True)


            if hasattr(self.tools.root, 'core') and hasattr(self.tools.root.core, 'dbase'):

                if self.tools.core.dbase.setts.path()==':memory:':
                    return 'main.bfst'

                else:

                    return os.path.splitext(
                        self.tools.core.dbase.setts.path())[0]+ '.bfst'

            else:
                    return 'main.bfst'

        else:
            return self.tools.sgc('path', folder_path, check)




#$$ ________ def width _____________________________________________________ #

    def width(self, value=None, check=None):
        '''
        Width of the page as monospace symbols count.
        '''
        return self.tools.sgc('width', value, check)


#$$ ________ def inherit ________________________________________________ #

    def inherit(self, value=None, check=None):
        '''
        If true then code is returned, if false code is added to buffer.
        '''

        return self.tools.sgc('inherit', value, check)


#$$ ________ def anum ______________________________________________________ #

    def anum(self, value=None, check=None):
        return self.tools.sgc('anum', value, check)






#$ ____ class fstme ________________________________________________________ #

class fstme:

    setts = setts()

    setts.active(True)

    setts.echo(True)

    setts.path(True)

    setts.width(80)

    setts.inherit(False)

    setts.anum(True)


#$$ ________ def __init __ _________________________________________________ #

    def __init__(self, core=None, **kwargs):

        self.core = core

        self.setts = setts(master=self.setts.tools, root=self)

        # list with generated and ready-to-insert code
        self.buffer = []

        for key,val in kwargs.items():
            getattr(self.setts, key)(val)

        self.ldef = {
            'type':None,
            'head':{-1:0, 0:0, 1:0, 2:0, 3:0, 4:0, 5:0,
                'last_lvl':None},
            'toc': [],
        }

        self.slave = slave(self, core)

        self.lib = {}






#$$ ________ process methods _______________________________________________ #

#$$$ ____________ def add __________________________________________________ #

    def add(self, code, inherit=None, submodule=None, echo=None, presymbol='', postsymbol='\n\n'):
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
            print(f'[pinky.fstme.{submodule}]\n{code}')




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
        if not self.setts.active(active, check=True): return

        with open(self.setts.path(), mode, encoding='utf-8') as f:
            f.writelines(self.buffer)

#$$$ ____________ def push _________________________________________________ #

    def push(self, active=None):
        '''
        Push method is connection of save and clear methods.
        '''

        if len(self.buffer) > 0:
            self.save(active=active)
        self.clear()




#$$ ________ generate methods ______________________________________________ #

#$$$ ____________ def text _________________________________________________ #

    def text(self, text, strip=True, wrap=True, active=None, inherit=None, echo=None):
        '''
        Add formated text to document. Text can be striped and wrapped.
        '''

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # if strip flag
        if strip:
            # then replace text with striped text
            text = text.strip()

        # if wrap flag
        if wrap:

            # divide text by new line symbol
            code = text.split('\n')

            # new three-lvl list comprehension
            code = '\n'.join(['\n'.join(['\n'.join(textwrap.wrap(line, self.setts.width(),
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

    def head(self, lvl, text, add2toc=True, anum=None, active=None, inherit=None, echo=None):
        '''
        #  with overline, for parts
        *  with overline, for chapters
        =, for sections
        -, for subsections
        ^, for subsubsections
        ", for paragraphs
        '''

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # use global settings
        self.setts.tools.check = True
        echo  = self.setts.echo(echo)
        self.setts.tools.check = False

        anum = self.setts.anum(anum, check=True)

        if anum==True:

            self.ldef['head'][lvl]+=1

            for i in range(5-lvl):

                self.ldef['head'][5-i]=0

            number = '.'.join(str(x) for x in
                [self.ldef['head'][i] for i in range(1, lvl+1)]) + '  '

        else:
            number =''

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

        # else:
        #     verrs.BCDR_pinky_fstme_ERROR_Header_Level(lvl)

        code = (

            '\n\n'+(sep_u*self.setts.width() + '\n' if sep_u else '') +

            ('\n' if lvl==0 else '') +

            '#' + '$'*lvl + ' ' + number + text + '\n' +

            ('\n' if lvl==0 else '') +

            (sep_l*self.setts.width() + '\n' if sep_l else '')

        )

        if add2toc: self.ldef['toc'] += [[number,text]]


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
#
#
# #$$$ ____________ def math _________________________________________________ #
#
#     def math(self, equation, mode='p', center=True, inherit=None, echo=None, page=None, scope=None):
#         '''
#         '''
#
#         if mode == 'p': # pretty print
#             equation = sp.pretty(parse_expr(equation, evaluate=False), use_unicode=False)
#
#         elif mode =='i':
#             equation = equation
#
#         if center and mode not in ['i']:
#             code_div = equation.split('\n')
#             max_len = 0
#             for chunk in code_div:
#                 if len(chunk) > max_len:
#                     max_len = len(chunk)
#
#             add_len = int((self.setts.width - max_len)/2)
#             for i in range(len(code_div)):
#                 code_div[i] = add_len*' ' + code_div[i]
#
#             code = '\n'.join(code_div)
#
#         else:
#             code = equation
#
#         return self.add(
#             submodule = 'm',
#             code      = code,
#             inherit   = inherit,
#             echo      = echo,
#         )
#     m = math


#$$$ ____________ def tab __________________________________________________ #

    def tab(self, data, header=None, width=None, halign=None, valign=None, dtype=None, wrap=True, caption=None, precision=None, border=None, active=None, inherit=None, echo=None):
        '''
        '''

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # use global settings
        self.setts.tools.check = True
        echo  = self.setts.echo(echo)
        self.setts.tools.check = False

        tabobj = table.table()
        tabobj.wrap = wrap

        if width     !=None: tabobj.set_cols_width(width)
        if halign    !=None: tabobj.set_cols_align(halign)
        if valign    !=None: tabobj.set_cols_valign(valign)
        if dtype     !=None: tabobj.set_cols_dtype(dtype)
        if precision !=None: tabobj.set_precision(precision)
        if header    !=None: tabobj.header(header)

        if border == False: tabobj.set_deco(0)

        tabobj.add_rows(rows=data, header=False)

        code = tabobj.draw()

        if caption: code = '#t Tab. ' + caption + '\n' + code

        if 't' in echo: print(code)

        return self.add(
            submodule = 't',
            code      = code,
            inherit   = inherit,
            echo      = echo,
        )
    t = tab



# #$$$ ____________ def code _________________________________________________ #
#
#     def code(self, code, language = None, inherit = None):
#         pass
#
#
# #$$$ ____________ def toc __________________________________________________ #
#
#     def toc(self, mode='b'):
#
#         head = self.h(1, 'List of Content', inherit=True, add2toc=False, anum=False)
#
#         data = self.core.pinky.fstme.table(
#             wrap   = [False, True],
#             width  = [10,True],
#             halign = ['r','l'],
#             valign = ['u','u'],
#             dtype  = ['t','t'],
#             data   = self._toc_list,
#             border = False,
#             inherit= True,
#         )
#
#         if not data: return
#
#         # if mode is begging
#         if mode=='b':
#             self.buffer = [head + '\n' + data + '\n\n\n'] + self.buffer
#
#         # if mode is end
#         elif mode=='e':
#             self.buffer += [head + '\n' + data]
#
#         # if mode is True
#         elif mode==True:
#             self.buffer += [head + '\n' + data]




#$ ____ class slave ________________________________________________________ #

class slave:


    def __init__(self, othe, core=None):
        self.othe = othe
        self.core = core
        self.data = {}


    def new(self, id, **kwargs):
        self.data[id] = fstme(core=self.core)
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


#$ ######################################################################### #
