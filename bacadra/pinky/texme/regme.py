'''
------------------------------------------------------------------------------
***** create (reg)ular expressions (m)assive (e)nvelope *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ######################################################################### #

import re
import regex
import numpy as np
from ...tools.fpack import translate
from ...unise.unise import unise
from . import verrs

#$ ____ precopiled regex ___________________________________________________ #

regme_bslash = re.compile(r'( |^|\n|~|\+|\-|\%|\@|=|\*|\(|\)|\{|\}|\$|\:)(begin|end|cfrac|frac|vec|ref|eqref|equref|figref|tabref|hedref|lstref|figlab|tablab|lstlab|equlab|hedlab|cite|vspace|makecell|sqrt|b|i|u|t|bu|ub|iu|ui|ib|bi|ibu|iub|biu|bui|uib|ubi|mn|mt|mi|mb|mm|tm|trm)(\{|\[)')

regme_recomp1 = re.compile(r'(\{?[a-zA-Z0-9α-ωΑ-Ω]\}?\_)([a-zA-Z0-9α-ωΑ-Ω\_,]+)')

regme_recomp2 = re.compile(r'(\_\{[a-zA-Z0-9α-ωΑ-Ω,]+)\_(?!\{)')

# usuwanie gwiazdki przez jednostkami
str_begin = r'(\*|\\cdot|~)[ ]*'
str_unit  = r'(m|kg|s|K|rad|mrad|C|Hz|t|cm|mm|km|dm|N|kN|MN|GN|Pa|kPa|MPa|GPa|yr|day|hr|min)'
str_end   = r'( |\n|~|\+|\-|\%|\@|=|\*|\(|\)|{|}|\$|\:|$|\^|\\|/)'
regme_unit1 = re.compile(str_begin + str_unit + str_end)

# prostowanie jednostek
str_begin = r'( |[0-9]|\n|~|\+|\-|\%|\@|=|\*|\(|\)|\{|}|\$|\:|/|\\)[ ]*'
str_end   = r'( |\n|~|\+|\-|\%|\@|=|\*|\(|\)|{|}|\$|\:|$|\^|\\|/)'
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



#$ ____ class Regme ________________________________________________________ #

class Regme:

#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, text='', dict={}, package=None):
        self.text = text
        self.math_mode = False
        self.dict = dict

        self._math_mode = False # in math region True


#$$ ________ def mmode _____________________________________________________ #

    def mmode(self):
        '''
        Toogle math_mode.
        '''

        if self.math_mode==True:
            self.math_mode = False
        else:
            self.math_mode = True

#$$ ________ def math_inline _______________________________________________ #

    def math_inline(self, RegMEFunctions):
        '''
        Detect math in string.
        '''

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

#$$ ________ def eval ______________________________________________________ #

    def eval(self):
        '''
        Detect string chunks to evaluate in string.
        '''

        def root(text):
            old = unise.setts.style
            unise.setts.style = 'latex'
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
                            new1='None'
                            try:
                                new1 = eval(self.text[a[i] + 1:a[i + 1]], self.dict)
                            except NameError as e:
                                verrs.BCDR_pinky_texme_ERROR_Evaluate(e)

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
                unise.setts.style = old
            return text


        if self.math_mode:
            self.text = self.math_inline(root)
        else:
            self.text = root(self.text)

#$$ ________ def orphan ____________________________________________________ #

    def orphan(self):
        '''
        Convert orphan to ~orphan
        '''

        def root(text):
            match = re.compile(r'( \w| \w\w|~\w|~\w\w|Rys\.|Fig\.|Tab\.) ')
            for i in range(2):
                text = match.sub(r'\1~', text)
            return text

        if self.math_mode:  self.text = self.math_inline(root)
        else:               self.text = root(self.text)


#$$ ________ def greek _____________________________________________________ #

    def greek(self):
        '''
        Translate original greek to latex greek.
        '''

        def root(text):
            return translate(text, {
                # q-Q
                '!θ' : r'{\texttheta}'       ,
                'θ'  : r'{\theta}'           ,
                '!Θ' : r'{\textTheta}'       ,
                'Θ'  : r'{\Theta}'           ,

                # w-W
                '!ω' : r'{\textomega}'       ,
                'ω'  : r'{\omega}'           ,
                '!Ω' : r'{\textOmega}'       ,
                'Ω'  : r'{\Omega}'           ,

                # e-E
                '!ε' : r'{\textepsilon}'     ,
                'ε'  : r'{\varepsilon}'      ,
                '!Ε' : r'{\textEpsilon}'     ,
                'Ε'  : r'{\Epsilon}'         ,
                '!ϵ' : r'{\straightepsilon}' ,
                'ϵ'  : r'{\epsilon}'         ,


                # r-R
                '!ρ' : r'{\textrho}'         ,
                'ρ'  : r'{\rho}'             ,
                '!Ρ' : r'{\textRho}'         ,
                'Ρ'  : r'{\Rho}'             ,

                # t-T
                '!τ' : r'{\texttau}'         ,
                'τ'  : r'{\tau}'             ,
                '!Τ' : r'{\textTau}'         ,
                'Τ'  : r'{\Tau}'             ,

                # y-Y
                '!ψ' : r'{\textpsi}'         ,
                'ψ'  : r'{\psi}'             ,
                '!Ψ' : r'{\textPsi}'         ,
                'Ψ'  : r'{\Psi}'             ,

                # u-U
                '!υ' : r'{\textupsilon}'     ,
                'υ'  : r'{\upsilon}'         ,
                '!Υ' : r'{\textUpsilon}'     ,
                'Υ'  : r'{\Upsilon}'         ,

                # i-I
                '!ι' : r'{\textiota}'        ,
                'ι'  : r'{\iota}'            ,
                '!Ι' : r'{\textIota}'        ,
                'Ι'  : r'{\Iota}'            ,

                # o-O
                '!ο' : r'{\textomikron}'     ,
                'ο'  : r'{\omnikron}'        ,
                '!Ο' : r'{\textOmikron}'     ,
                'Ο'  : r'{\Omikron}'         ,

                # p-P
                '!π' : r'{\textpi}'          ,
                'π'  : r'{\pi}'              ,
                '!Π' : r'{\textPi}'          ,
                'Π'  : r'{\Pi}'              ,

                # a-A
                '!α' : r'{\textalpha}'       ,
                'α'  : r'{\alpha}'           ,
                '!Α' : r'{\textAlpha}'       ,
                'Α'  : r'{\Alpha}'           ,

                # s-S
                '!σ' : r'{\textsigma}'       ,
                'σ'  : r'{\sigma}'           ,
                '!Σ' : r'{\textSigma}'       ,
                'Σ'  : r'{\Sigma}'           ,

                # d-D
                '!δ' : r'{\textdelta}'       ,
                'δ'  : r'{\delta}'           ,
                '!Δ' : r'{\textDelta}'       ,
                'Δ'  : r'{\Delta}'           ,

                # f-F
                '!φ' : r'{\straightphi}'     ,
                'φ'  : r'{\phi}'             ,
                '!Φ' : r'{\textPhi}'         ,
                'Φ'  : r'{\Phi}'             ,

                # g-G
                '!γ' : r'{\textgamma}'       ,
                'γ'  : r'{\gamma}'           ,
                '!Γ' : r'{\textGamma}'       ,
                'Γ'  : r'{\Gamma}'           ,

                # h-H
                '!η' : r'{\texteta}'         ,
                'η'  : r'{\eta}'             ,
                '!Η' : r'{\textEta}'         ,
                'Η'  : r'{\Eta}'             ,

                # j-J
                '!ϕ' : r'{\textphi}'         ,
                'ϕ'  : r'{\varphi}'          ,
                '!ϑ' : r'{\scripttheta}'     ,
                'ϑ'  : r'{\theta}'           ,

                # k-K
                '!κ' : r'{\textkappa}'       ,
                'κ'  : r'{\kappa}'           ,
                '!Κ' : r'{\textKappa}'       ,
                'Κ'  : r'{\Kappa}'           ,

                # l-L
                '!λ' : r'{\textlambda}'      ,
                'λ'  : r'{\lambda}'          ,
                '!Λ' : r'{\textLambda}'      ,
                'Λ'  : r'{\Lambda}'          ,

                # z-Z
                '!ζ' : r'{\textzeta}'        ,
                'ζ'  : r'{\zeta}'            ,
                '!Ζ' : r'{\textZeta}'        ,
                'Ζ'  : r'{\Zeta}'            ,

                # x-X
                '!ξ' : r'{\textxi}'          ,
                'ξ'  : r'{\xi}'              ,
                '!Ξ' : r'{\textXi}'          ,
                'Ξ'  : r'{\Xi}'              ,

                # c-C
                '!χ' : r'{\textchi}'         ,
                'χ'  : r'{\chi}'             ,
                '!Χ' : r'{\textChi}'         ,
                'Χ'  : r'{\Chi}'             ,

                # v-V
                '!ς' : r'{\textvarsigma}'    ,

                # b-B
                '!β' : r'{\textbeta}'        ,
                'β'  : r'{\beta}'            ,
                '!Β' : r'{\textBeta}'        ,
                'Β'  : r'{\Beta}'            ,

                # n-N
                '!ν' : r'{\textnu}'          ,
                'ν'  : r'{\nu}'              ,
                '!Ν' : r'{\textNu}'          ,
                'Ν'  : r'{\Nu}'              ,

                # m-M
                '!μ' : r'{\textmugreek}'     ,
                'μ'  : r'{\mu}'              ,
                '!Μ' : r'{\textMu}'          ,
                'Μ'  : r'{\Mu}'              ,


                # '!θ' : r'{\straighttheta}'   ,
            })

        if self.math_mode:  self.text = self.math_inline(root)
        else:               self.text = root(self.text)

#$$ ________ def bslash ____________________________________________________ #

    # TODO: problem with statment like frac{mt{ib{....
    def bslash(self):
        '''
        '''

        def root(text):
            for i in range(3):
                text = regme_bslash.sub(r'\1\\\2\3', text)
            return text

        if self.math_mode:  self.text = self.math_inline(root)
        else:               self.text = root(self.text)

#$$ ________ def subscript _________________________________________________ #

    def subscript(self):
        '''
        '''

        def root(text):
            text = regme_recomp1.sub(r'\1{\2}', text)
            for i in range(4):
                text = regme_recomp2.sub(r'\1,', text)
            return text

        if self.math_mode:  self.text = self.math_inline(root)
        else:               self.text = root(self.text)

#$$ ________ def unit_point ________________________________________________ #

    def unit_point(self):
        '''
        Usuwanie gwiazdek przed jednostka
        '''

        def root(text):
            return regme_unit1.sub(r'\2\3', text)

        if self.math_mode:  self.text = self.math_inline(root)
        else:               self.text = root(self.text)


#$$ ________ def unit_noitalic _____________________________________________ #

    def unit_noitalic(self):
        '''
        Prostowanie jednostek
        '''

        def root(text):
            for i in range(4):
                text = regme_unit2.sub(r'\1\\mathrm{\,\2}\3', text)
            return text

        if self.math_mode:  self.text = self.math_inline(root)
        else:               self.text = root(self.text)



#$$ ________ def rmfunction ________________________________________________ #

    def rmfunction(self):
        '''
        '''

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

#$$ ________ def math_fraction _____________________________________________ #

    def math_fraction(self):
        '''
        Convert math ()/() to frac{}{} and a/b to frac{a}{b}
        '''

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

#$$ ________ def symbols ___________________________________________________ #

    def symbols(self):
        '''
        Convert most popular symbols
        '''

        def root(text):
            ndict = {
                '**'   : '^',
                 '*'   : ' \\cdot ',
                 '⋅'    : ' \\cdot ',
                 '<='  : ' \\leqslant ',
                 '>='  : ' \\geqslant ',
                 '=='  : ' \\equiv ',
                 '=~=' : ' \\approx ',
                 '!='  : ' \\neq ',
                 '≠'   : ' \\neq ',
                 #'/'  : ' \\div ',
                 '||'  : ' \\parallel',
                 '_|_' : ' \perp',
                 '+='  : '\\mathrel{+}=',
                 '**=' : '\\mathrel{**}=',
                 '-='  : '\\mathrel{-}=',

                 '<->' : ' \\Leftrightarrow ',
                 '->'  : ' \\Rightarrow ',
                 '<-'  : ' \\Leftarrow ',

                 '∫['  : '\\int\\limits_[',
                 '∫{'  : '\\int\\limits_{',
                 '∫'   : '\\int\\limits ',
                 '∬['  : '\\iint\\limits_[',
                 '∬{'  : '\\iint\\limits_{',
                 '∬'   : '\\iint\\limits ',
                 '∭['  : '\\iiint\\limits_[',
                 '∭{'  : '\\iiint\\limits_{',
                 '∭'   : '\\iiint\\limits ',
                 '∑['  : '\\sum\\limits_[',
                 '∑{'  : '\\sum\\limits_{',
                 '∑'   : '\\sum\\limits ',
                 '√'   : '\\sqrt',
                 '∂'   : '\\partial ',
                 '∞'   : '\\infty ',
            }
            text = translate(text, ndict)

            # reverse badly convert
            ndict = {
                 '{^}': '**',
                 '{ \\cdot }': '*',
            }
            text = translate(text, ndict)

            return text

        if self.math_mode:  self.text = self.math_inline(root)
        else:               self.text = root(self.text)

#$$ ________ def bracket ___________________________________________ #

    def bracket(self):
        '''
        convert bracket to left and right
        '''

        def root(text):
            text = regme_sbrac1.sub(r'\\left(', text)
            text = regme_sbrac2.sub(r'(', text)
            text = regme_sbrac3.sub(r'\\right)', text)
            text = regme_sbrac4.sub(r')', text)
            return text

        if self.math_mode:  self.text = self.math_inline(root)
        else:               self.text = root(self.text)

#$$ ________ def mcadenv ___________________________________________________ #

    def mcadenv(self): # only to display math in hydrogen latex python
        '''
        '''

        pass
        # self.text = re.sub('\\begin\{mcad\}', r'\\begin{array}{|l}', self.text)
        # self.text = re.sub('\\\\begin\{mcin\}\{(.+)\}\{(.+)\}', r'\1 \; \2 \\\\[5pt]'+'\n\\\\begin{array}{|l}', self.text)
        # self.text = re.sub(r'\\end{mcad}', r'\\end{array}', self.text)
        # self.text = re.sub(r'\\end{mcin}', r'\\end{array}', self.text)

#$$ ________ def textstyle _________________________________________________ #

    def textstyle(self):
        '''
        Only to display math in hydrogen latex python
        '''

        def root(text):
            text = regme_textstyle1.sub(r'\\mathnormal{\1}', text)
            text = regme_textstyle2.sub(r'\\mathrm{\1}'    , text)
            text = regme_textstyle3.sub(r'\\mathit{\1}'    , text)
            text = regme_textstyle4.sub(r'\\mathbf{\1}'    , text)
            text = regme_textstyle5.sub(r'\\mathtt{\1}'    , text)
            return text
        if self.math_mode:  self.text = self.math_inline(root)
        else:               self.text = root(self.text)

#$ ____ def run ____________________________________________________________ #

    def run(self, code=''):
        '''
        + -- math mode toogle
        e -- eval code in @..@

        old packages:
        0  -> ''
        1  -> 'e+fbusy+hrgo'
        11 -> 'efbusyhrgo'
        99 -> 'mt'
        '''

        # loop over letters in run code
        for letter in code:

            # special char, toogle math_mode, default is False
            if   letter=='$': self.mmode()
            elif letter=='e': self.eval()
            elif letter=='o': self.orphan()
            elif letter=='g': self.greek()
            elif letter=='h': self.bslash()
            elif letter=='s': self.subscript()
            elif letter=='u': self.unit_point()
            elif letter=='i': self.unit_noitalic()
            elif letter=='r': self.rmfunction()
            elif letter=='f': self.math_fraction()
            elif letter=='y': self.symbols()
            elif letter=='b': self.bracket()
            elif letter=='m': self.mcadenv()
            elif letter=='t': self.textstyle()

        return self.text

def regme(text, dict, code):
    # create Regme instance
    self = Regme(text, dict, code)

    if code!=None:
        return self.run(code)
    else:
        return self.text

#$ ######################################################################### #
