'''
------------------------------------------------------------------------------
BCDR += ***** create (r)e(s)ructured (t)ext (m)assive (e)nvelope *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

import os
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

from . import verrs
from . import texttable
from . import cjkwrap


#$ class rstme
class rstme:
    #$$ def __init__
    def __init__(self, core=None, path=None):
        self.core = core

        # active mode
        self.active = True

        # automaticly call to msg method after all built method
        self.display = False

        # output file path
        self._path = None

        # buffer list
        self.buffer = []

        # width of the page as monospace symbols count
        self.width = 80

        # last one used command, its helpful to stylish file
        self.__last_type = None


    @property
    def path(self):
        if self._path is None and self.core:
            return os.path.splitext(self.core.dbase.path)[0] + '.brst'
        else:
            return self._path

    @path.setter
    def path(self, value):
        self._path = value


    #$$ def -add
    def add(self, code, name=None, inherit=False):
        if self.active:
            if inherit is True:
                return code
            elif inherit is False:
                self.buffer += [code + '\n\n']
            elif inherit == 'print':
                self.msg(name, code)

    #$$ def msg
    def msg(self, module=None, code=None):
        print(f'[pinky.rstme.{module}]\n{code}')

    #$$ def clear-buffer
    def clear_buffer(self):
        self.buffer = []

    #$$ def clear-file
    def clear_file(self, path=None):
        if path is None: path = self.path
        open(path, 'w').close()

    #$$ def save
    def save(self, mode='a', path=None):
        if path is None: path = self.path

        with open(path, mode, encoding='utf-8') as f:
            f.writelines(self.buffer)

    #$$ def push
    def push(self, mode='a', path=None, clear=True):
        if path is None: path = self.path

        if clear:
            self.clear_file(path=path)
        self.save(mode=mode, path=path)

        self.clear_buffer()


    #$$ generate methods

    #$$$ def text
    def text(self, text, strip=True, wrap=True, inherit=False):
        '''
        '''

        # if strip flag
        if strip:
            # then replace text with striped text
            text = text.strip()

        # divide text by new line symbol
        code = text.split('\n')

        # if wrap flag
        if wrap:
            # new three-lvl list comprehension
            code = '\n'.join(['\n'.join(['\n'.join(cjkwrap.wrap(line, self.width,
                     break_long_words=False, replace_whitespace=False))
                     for line in text.splitlines() if line.strip() != ''])
                     for text in code])

        # if wrap is turned off, then simply code refer to text
        else:
            code = text

        self._last_TeXM = 'x'
        return self.add('text', code, inherit)
    x = text


    #$$$ def head
    def head(self, lvl, text, inherit=False):
        '''
        # with overline, for parts
        * with overline, for chapters
        =, for sections
        -, for subsections
        ^, for subsubsections
        ", for paragraphs
        '''

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
            verrs.lvlrstmeError(lvl)

        code = (
            (sep_u*self.width + '\n' if sep_u else '') +
            ('\n' if lvl==0 else '') +
            '#' + '$'*lvl + ' ' + text + '\n' +
            ('\n' if lvl==0 else '') +
            (sep_l*self.width + '\n' if sep_l else '')
        )

        self._last_TeXM = 'h'
        return self.add('head', code, inherit)
    h = head


    #$$$ def math
    def math(self, equation, mode='p', center=False, inherit=False):
        if mode == 'p':
            code = sp.pretty(parse_expr(equation, evaluate=False), use_unicode=False)

        if center:
            code_div = code.split('\n')
            max_len = 0
            for chunk in code_div:
                if len(chunk) > max_len:
                    max_len = len(chunk)

            add_len = int((self.width - max_len)/2)
            for i in range(len(code_div)):
                code_div[i] = add_len*' ' + code_div[i]

            code = '\n'.join(code_div)

        self._last_TeXM = 'm'
        return self.add('math', code, inherit)
    m = math


    #$$$ def add
    def table(self, data, header=None, width=None, halign=None, valign=None, dtype=None, wrap=True, caption=None, precision=None, border=None, inherit=False):
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

        table.add_rows(rows=data, header=False)

        code = table.draw()

        if caption:
            code = '#t Tab. ' + caption + '\n' + code

        self._last_TeXM = 't'

        return self.add(
            name    = 'table',
            code    = code,
            inherit = inherit,
        )
    t = table


    #$$$ def code
    def code(self, code, language = None, inherit = None):
        pass



