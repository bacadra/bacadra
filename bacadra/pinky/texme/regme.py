'''
------------------------------------------------------------------------------
BCDR += ***** create (reg)ular expressions (m)assive (e)nvelope *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

import re
import regex
import numpy as np
from ... import tools
from ...cunit.units import cunit

#$ ____ class RegME ________________________________________________________ #


regme_bslash = re.compile(r'( |^|\n|~|\+|\-|\%|\@|=|\*|\(|\)|\{|\}|\$|\:)(begin|end|cfrac|frac|vec|ref|eqref|equref|figref|tabref|hedref|lstref|figlab|tablab|lstlab|equlab|hedlab|cite|vspace|makecell|sqrt|b|i|u|t|bu|ub|iu|ui|ib|bi|ibu|iub|biu|bui|uib|ubi|mn|mt|mi|mb|mm|tm|trm)(\{|\[)')

regme_recomp1 = re.compile(r'(\{?[a-zA-Z0-9α-ωΑ-Ω]\}?\_)([a-zA-Z0-9α-ωΑ-Ω\_,]+)')

regme_recomp2 = re.compile(r'(\_\{[a-zA-Z0-9α-ωΑ-Ω,]+)\_(?!\{)')

# usuwanie gwiazdki przez jednostkami
str_begin = r'(\*|\\cdot|~)[ ]*'
str_unit  = r'(m|kN|s|C|N|MN|mm|cm|km|Pa|kPa|MPa|GPa|kNm|Nm|MNm|kg|Hz|kHz|rad|mrad|deg|minu|hr|day|yr)'
str_end   = r'( |\n|~|\+|\-|\%|\@|=|\*|\(|\)|{|}|\$|\:|$|\^|\\)'
regme_unit1 = re.compile(str_begin + str_unit + str_end)


# prostowanie jednostek
str_begin = r'( |[0-9]|\n|~|\+|\-|\%|\@|=|\*|\(|\)|{|}|\$|\:)[ ]*'
regme_unit2 = re.compile(str_begin + str_unit + str_end)

str_begin = r'( |[0-9]|\n|~|\+|\-|\%|\@|=|\*|\(|\)|}|\$|\:)[ ]*'
str_function = r'(arccos|arcsin|arctan|arg|cos|cosh|cot|coth|csc|deg|det|dim|exp|inf|lim|log|max|ln|min|sin|sinh|sup|tan|tanh|if|abs)'
str_end = r'(~*)([a-zA-Z0-9α-ωΑ-Ω\~\(\\\)]*)'
regme_function1 = re.compile(str_begin + str_function + str_end)

regme_mfrac = regex.compile(r'\(([^\(\)]*+(?:\((?1)\)[^\(\)]*)*+)\)\/\(([^\(\)]*+(?:\((?1)\)[^\(\)]*)*+)\)')

regme_mfrac2 = regex.compile(r'([a-zA-Z0-9\\α-ωΑ-Ω\_\,]+)\/([a-zA-Z0-9\\α-ωΑ-Ω\_\,]+)')

regme_sbrac1 = re.compile(r'\(')
regme_sbrac2 = re.compile(r':\\left\(')
regme_sbrac3 = re.compile(r'\)')
regme_sbrac4 = re.compile(r':\\right\)')


bm = r'\{([^\{\}]*+(?:\{(?1)\}[^\{\}]*)*+)\}'
regme_textstyle1 = regex.compile(r'\\(?:mn)'+bm)
regme_textstyle2 = regex.compile(r'\\(?:mt|trm)'+bm)
regme_textstyle3 = regex.compile(r'\\(?:mi|i)'+bm)
regme_textstyle4 = regex.compile(r'\\(?:mb|b)'+bm)
regme_textstyle5 = regex.compile(r'\\(?:mm|tm)'+bm)





class regme:
    #$$ def __init__
    def __init__(self, text='', dict={}):
        self.text = text
        self.math_mode = False
        self.dict = dict


    #$$ def math_inline
    def math_inline(self, RegMEFunctions):
        '''Detect math in string.'''
        a = [self.text.find('$')]
        i = 0
        while a[i] != -1:
            a.append(self.text.find('$', a[i] + 1))
            i += 1
        a.insert(0, -1)
        a.insert(len(a) - 1, len(self.text))
        if len(a) > 3:
            new = ''
            for i in range(len(a) - 2):
                if i % 2 == 0:
                    new += self.text[a[i] + 1:a[i + 1]]
                if i % 2 == 1:
                    new += '$' + \
                        RegMEFunctions(self.text[a[i] + 1:a[i + 1]]) + '$'
            self.text = new
        else:
            self.text = self.text
        return self.text


    #$$ def eval
    def eval(self):
        '''Detect math in string.'''
        def root(text):
            old = cunit.style
            cunit.style = 'latex'
            try:
                a = [text.find('@')]
                i = 0
                while True:
                    if a[i] == -1:
                        break
                    a.append(text.find('@', a[i] + 1))
                    i += 1
                a.insert(0, -1)
                a.insert(len(a) - 1, len(text))
                if len(a) > 3:
                    new = ''
                    for i in range(len(a) - 2):
                        if i % 2 == 0:
                            new += text[a[i] + 1:a[i + 1]]
                        if i % 2 == 1:
                            new1 = eval(self.text[a[i] + 1:a[i + 1]], self.dict)

                            # if type is list form like list or ndarray
                            if type(new1) in [list, np.ndarray]:

                                dim = 1
                                for row in new1:
                                    if type(row) in [list, np.ndarray]:
                                        dim = 2
                                        for row1 in row:
                                            if type(row1) in [list, np.ndarray]:
                                                dim = 3
                                                break

                                if dim==1:
                                    code = r'\begin{bmatrix}'"\n"
                                    code += '&'.join(str(val) for val in new1)
                                    code += "\n"r'\end{bmatrix}'

                                elif dim==2:
                                    code = r'\begin{bmatrix}'"\n"
                                    for row in new1:
                                        if type(row) in [list, np.ndarray]:
                                            code += '&'.join(str(val) for val in row)
                                        else:
                                            code += str(row)
                                        code += r'\\'
                                    code = code[:-2]+ "\n"r'\end{bmatrix}'

                                else:
                                    code = str(new1)

                                new += code

                            else:
                                new += str(new1)
                    text = new
            finally:
                cunit.style = old
            return text


        if self.math_mode:
            self.text = self.math_inline(root)
        else:
            self.text = root(self.text)

    #$$ def wb
    def wb(self):
        '''
        Wdowy i bekarty
        '''
        def root(text):
            match = re.compile(r'( \w| \w\w|~\w|~\w\w|Rys\.|Fig\.|Tab\.) ')
            for i in range(2):
                text = match.sub(r'\1~', text)
            return text

        if self.math_mode:  self.text = self.math_inline(root)
        else:               self.text = root(self.text)

    ##$ def greek
    def greek(self):
        '''
        Translate original greek to latex greek.
        '''
        def root(text):
            ndict = { 'ς': '{\\zeta}', # V
                      'ε': '{\\varepsilon}', # e
                      'ϕ': '{\\varphi}', # j
                      'ϵ': '{\\epsilon}', # ϵ
                      'ρ': '{\\rho}', # r
                      'τ': '{\\tau}', # t
                      'υ': '{\\upsilon}', # u
                      'θ': '{\\theta}', # q
                      'ι': '{\\iota}', # i
                      'ο': '{\\o}', # o
                      'π': '{\\pi}', # p
                      'α': '{\\alpha}', # a
                      'σ': '{\\sigma}', # s
                      'δ': '{\\delta}', # d
                      'φ': '{\\phi}', # f
                      'γ': '{\\gamma}', # g
                      'η': '{\\eta}', # h
                      'ξ': '{\\xi}', # x
                      'κ': '{\\kappa}', # k
                      'λ': '{\\lambda}', # l
                      'ζ': '{\\zeta}', # z
                      'χ': '{\\chi}', # c
                      'ψ': '{\\psi}', # y
                      'ω': '{\\omega}', # w
                      'β': '{\\beta}', # b
                      'ν': '{\\nu}', # n
                      'μ': '{\\mu}', # m
                      'Τ': '{\\T}', # T
                      'Θ': '{\\Theta}', # Q
                      'Π': '{\\Pi}', # P
                      'Σ': '{\\sum}', # S
                      'Δ': '{\\Delta}', # D
                      'Φ': '{\\Phi}', # F
                      'Γ': '{\\Gamma}', # G
                      'Ξ': '{\\Xi}', # X
                      'Λ': '{\\Lambda}', # L
                      'Ψ': '{\\Psi}', # Y
                      'Ω': '{\\Omega}'} # W
            text = tools.translate(text, ndict)
            return text

        if self.math_mode:  self.text = self.math_inline(root)
        else:               self.text = root(self.text)

    #$$ def bslash
    # TODO: problem with statment like frac{mt{ib{....
    def bslash(self):
        def root(text):
            for i in range(3):
                text = regme_bslash.sub(r'\1\\\2\3', text)
            return text

        if self.math_mode:  self.text = self.math_inline(root)
        else:               self.text = root(self.text)

    #$$ def subscript
    def subscript(self):
        def root(text):
            text = regme_recomp1.sub(r'\1{\2}', text)
            for i in range(4):
                text = regme_recomp2.sub(r'\1,', text)
            return text

        if self.math_mode:  self.text = self.math_inline(root)
        else:               self.text = root(self.text)

    #$$ def unit
    def unit(self):
        def root(text):
            text = regme_unit1.sub(r' \2 \3', text)
            # text = regme_unit2.sub(r'\1~\\textrm{\2}\3',text)
            # text = text.replace('{~', '{')
            return text

        if self.math_mode:  self.text = self.math_inline(root)
        else:               self.text = root(self.text)

    #$$ def rmfunction
    def rmfunction(self):
        def root(text):
            text_old = text
            while True:
                text = regme_function1.sub(r'\1\\textrm{\2}\3\4',text_old)
                if text_old==text:
                    break
                else:
                    text_old = text
            return text

        if self.math_mode:  self.text = self.math_inline(root)
        else:               self.text = root(self.text)

    #$$ def math-fraction
    def math_fraction(self):
        def root(text):
            while True:
                text_old = text
                text = regme_mfrac.sub(r'\\cfrac{\1}{\2}', text)
                if text_old==text:
                    break
            text = regme_mfrac2.sub(r'\\cfrac{\1}{\2}', text)
            return text

        if self.math_mode:  self.text = self.math_inline(root)
        else:               self.text = root(self.text)

    #$$ def symbols
    def symbols(self):
        def root(text):
            ndict = {
                '**': '^',
                 '*': ' \\cdot ',
                 '⋅': ' \\cdot ',
                 '<=': ' \\leqslant ',
                 '>=': ' \\geqslant ',
                 '==': ' \\equiv ',
                 '=~=': ' \\approx ',
                 '!=': ' \\neq ',
                 '≠': ' \\neq ',
                 #'/':  ' \\div ',
                 '||': ' \\parallel',
                 '_|_': ' \perp',

                 '<->': ' \\Leftrightarrow ',
                 '->': ' \\Rightarrow ',
                 '<-': ' \\Leftarrow ',

                 '∫[':  '\\int\\limits_[',
                 '∫{':  '\\int\\limits_{',
                 '∫':   '\\int\\limits ',
                 '∬[':  '\\iint\\limits_[',
                 '∬{':  '\\iint\\limits_{',
                 '∬':  '\\iint\\limits ',
                 '∭[':  '\\iiint\\limits_[',
                 '∭{':  '\\iiint\\limits_{',
                 '∭':  '\\iiint\\limits ',
                 '∑[':  '\\sum\\limits_[',
                 '∑{':  '\\sum\\limits_{',
                 '∑':  '\\sum\\limits ',
                 '√':  '\\sqrt',
                 '∂':  '\\partial ',
                 '∞':  '\\infty ',
            }
            text = tools.translate(text, ndict)

            # reverse badly convert
            ndict = {
                 '{^}': '**',
                 '{ \\cdot }': '*',
            }
            text = tools.translate(text, ndict)

            return text

        if self.math_mode:  self.text = self.math_inline(root)
        else:               self.text = root(self.text)

    #$$ def symbols-bracket
    def symbols_bracket(self):
        def root(text):
            text = regme_sbrac1.sub(r'\\left(', text)
            text = regme_sbrac2.sub(r'(', text)
            text = regme_sbrac3.sub(r'\\right)', text)
            text = regme_sbrac4.sub(r')', text)
            return text

        if self.math_mode:  self.text = self.math_inline(root)
        else:               self.text = root(self.text)


    #$$ def mcadenv
    def mcadenv(self): # only to display math in hydrogen latex python
        pass
        # self.text = re.sub('\\begin\{mcad\}', r'\\begin{array}{|l}', self.text)
        # self.text = re.sub('\\\\begin\{mcin\}\{(.+)\}\{(.+)\}', r'\1 \; \2 \\\\[5pt]'+'\n\\\\begin{array}{|l}', self.text)
        # self.text = re.sub(r'\\end{mcad}', r'\\end{array}', self.text)
        # self.text = re.sub(r'\\end{mcin}', r'\\end{array}', self.text)

    #$$ def textstyle
    def textstyle(self): # only to display math in hydrogen latex python
        def root(text):
            text = regme_textstyle1.sub(r'\\mathnormal{\1}', text)
            text = regme_textstyle2.sub(r'\\mathrm{\1}'    , text)
            text = regme_textstyle3.sub(r'\\mathit{\1}'    , text)
            text = regme_textstyle4.sub(r'\\mathbf{\1}'    , text)
            text = regme_textstyle5.sub(r'\\mathtt{\1}'    , text)
            return text
        if self.math_mode:  self.text = self.math_inline(root)
        else:               self.text = root(self.text)

    #$$ def package
    def package(self, mode=1):
        if mode==0:
            pass

        elif mode==1:
            self.math_mode = False
            self.eval()
            self.math_mode = True
            self.math_fraction()
            self.symbols_bracket()
            self.unit()
            self.subscript()
            self.symbols()
            self.math_mode = False
            self.bslash()
            self.rmfunction()
            self.greek()
            self.wb()


        elif mode==11:
            self.math_mode = False
            self.eval()
            self.math_fraction()
            self.symbols_bracket()
            self.unit()
            self.subscript()
            self.symbols()
            self.bslash()
            self.rmfunction()
            self.greek()
            self.wb()

        elif mode==99:
            self.mcadenv()
            self.textstyle()
        return self.text
