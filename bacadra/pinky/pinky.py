#!/usr/bin/python
#-*-coding: UTF-8-*-
#$ ____ import _____________________________________________________________ #

import os
import sys
import subprocess
import shutil
import inspect

import numpy as np

from IPython.display import Image, Latex, Markdown
from IPython.display import display as ipdisplay

from .. import tools
from ..cunit.units import cunit
from .regme import RegME

import importlib.util


#$ ____ class TeXM__________________________________________________________ #

class TeXM:
    #$$ def page-break
    def page_break(self,
            mode,
            inherit = None,
        ):
        '''Prevent page break between mode=true nad mode=false.'''
        if self.active:
            if inherit     is None: inherit     = self.inherit

            if mode:
                tex = '\\begin{absolutelynopage_break}\n'
            else:
                tex = '\n\\end{absolutelynopage_break}'
            return self._add('pbreak', tex, inherit)

    #$$ def tex
    def tex(self,
            text,
            textX      = None,
            strip      = False,
            inherit    = None,
            page_break = None,
            scope      = None,
        ):

        '''
        *** pinky ***: Insert LaTeX code into tex report.

        :text: text which be added to latex document
            >{str}<

        :textX: a package of RegME which is used to convert {*}RX variable by regular expression filters
            >{int}<

        :inherit: type of result
            >False< result is added to dbase project
            >True<  result is returned by code

        "page_break
        '''
        if self.active:
            if inherit     is None: inherit     = self.inherit
            if textX is None: textX = self.textXx

            text = RegME(text, self.scope).package(textX)

            if strip:
                text = text.strip()

            if page_break==True:
                text = self.page_break(True, inherit=True) + text
            elif page_break==False:
                text = text + self.page_break(False, inherit=True)

            self._last_TeXM = 'x'
            return self._add('tex', text, inherit)
    x = tex


    #$$ def head
    def head(self,
            lvl,
            text,
            label       = None,
            text2       = None,
            textX       = None,
            text2X      = None,
            minitxt     = False,
            minitoc     = None,
            minilof     = None,
            minilot     = None,
            mininewpage = False,
            nonumber    = False,
            double_page = None,
            inherit     = None,
            page_break  = None,
            newpageb    = False,
            newpagea    = False,
            scope       = None,
        ):

        '''
        *** pinky ***: add header to the project

        :lvl:
            >{int}<

        :text:
            >{str}<

        :label:
            >{str}<
            >True<

        :text2:
            >{str}<

        :minitxt:
            >True<
            >False<

        :minitoc:
            >True<
            >False<

        :minilof:
            >True<
            >False<

        :minilot:
            >True<
            >False<

        :mininewpage:
            >True<
            >False<

        :nonumber:
            >True<
            >False<

        :double_page:
            >True< create double page around chapter header
            >False< don't create blank space around chapter header

        :textX: a package of RegME which is used to convert {*}RX variable by regular expression filters
            >{int}<

        :text2XX: a package of RegME which is used to convert {*}RX variable by regular expression filters
            >{int}<

        :inherit: type of result
            >False< result is added to dbase project
            >True<  result is returned by code

        :page_break:

        '''

        if self.active:
            if inherit     is None: inherit     = self.inherit
            if minitoc     is None: minitoc     = self.minitoc
            if minilof     is None: minilof     = self.minilof
            if minilot     is None: minilot     = self.minilot
            if double_page is None: double_page = self.double_page
            if label       is None: label       = self.autolabelh
            if textX       is None: textX       = self.textXh
            if text2X      is None: text2X      = self.text2Xh

            text = RegME(text, self.scope).package(textX)

            if label is True:
                firstletters = ''.join([i[0].lower() for i in text.split()])
                lab = '\\label{h'+str(lvl)+':' + firstletters + '}'
            elif label:
                lab = '\\label{' + label + '}'
            else:
                lab = ''

            if nonumber or nonumber==2:
                ast = '*'
            else:
                ast = ''

            if lvl+self.alvl == -1:
                tex = '\\part' + ast + '%2{%1} ' + lab
                if nonumber == 2:
                    tex += '\n\\addcontentsline{toc}{part}{%1}'

            elif lvl+self.alvl == 0:
                tex = '\\chapter' + ast + '%2{%1} ' + lab
                if minitxt:
                    tex += '\n' + minitxt + '\\par\n\\bigskip\n'
                if (minitoc or minilof or minilot) and mininewpage:
                    tex += '\\newpage\n'
                if minitoc:
                    tex += '\n\\minitoc\n\\bigskip'
                if minilof:
                    tex += '\n\\minilof\n\\bigskip'
                if minilot:
                    tex += '\n\\minilot\n\\bigskip'
                if nonumber==2:
                    tex += '\n\\mtcaddchapter[%1]'
                if double_page:
                    tex = '\\cleardoublepage\n' + tex

            elif lvl+self.alvl == 1:
                tex = '\\section' + ast + '%2{%1} ' + lab
                if nonumber == 2:
                    tex += '\n\\addcontentsline{toc}{section}{%1}'

            elif lvl+self.alvl == 2:
                tex = '\\subsection' + ast + '%2{%1} ' + lab
                if nonumber == 2:
                    tex += '\n\\addcontentsline{toc}{subsection}{%1}'

            elif lvl+self.alvl == 3:
                tex = '\\subsubsection' + ast + '%2{%1} ' + lab
                if nonumber == 2:
                    tex += '\n\\addcontentsline{toc}{chapter}{%1}'

            elif lvl+self.alvl == 4:
                tex = '\\paragraph' + ast + '%2{%1} ' + lab
                if nonumber == 2:
                    tex += '\n\\addcontentsline{toc}{paragraph}{%1}'

            elif lvl+self.alvl == 5:
                tex = '\\subparagraph' + ast + '%2{%1} ' + lab
                if nonumber == 2:
                    tex += '\n\\addcontentsline{toc}{subparagraph}{%1}'

            else:
                raise ValueError('The header level must be between <-1,5>, now lvl += alvle = '+str(lvl+self.alvl))

            if newpageb:
                tex = '\\newpage\n' + tex
            if newpagea:
                tex += '\n\\newpage'

            tex = tex.replace('%1', text.strip())

            if text2:
                text2 = RegME(text2, self.scope).package(text2X)
                tex = tex.replace('%2', '[' + text2 + ']')
            else:
                tex = tex.replace('%2', '')

            if page_break==True:
                tex = self.page_break(True, inherit=True) + tex
            elif page_break==False:
                tex = tex + self.page_break(False, inherit=True)

            if self.displayh:
                ipdisplay(Markdown('#'*(max(1,lvl)) + ' ' + text.strip()))

            self._last_TeXM = 'h'
            return self._add('h' + str(lvl), tex, inherit)
    h = head

    #$$ def img
    def img(self,
            path,
            caption       = False,
            label         = None,
            float         = None,
            absolute_path = False,
            frame         = True,
            grey_scale    = None,
            caption2      = False,
            captionX      = None,
            caption2X     = None,
            display       = None,
            page_break    = None,
            inherit       = None,
            width_factor  = 1.0,
            height_factor = 0.9,
            display_width = None,
            mode          = 'fig',
            add_space     = False,
            scope         = None
        ):

        if self.active:
            if display_width  is None: display_width = self.display_width
            if inherit        is None: inherit       = self.inherit
            if float          is None: floati     = self.floati
            if grey_scale     is None: grey_scale    = self.grey_scale
            if display        is None: display       = self.displayp
            if label          is None: label         = self.autolabelp
            if captionX       is None: captionX      = self.captionXp
            if caption2X      is None: caption2X     = self.caption2Xp

            user_path = path

            path = os.path.join(self.rootp, path)

            pathA = os.path.abspath(path).replace('\\', '/')

            if absolute_path:
                path = pathA
            else:
                path = os.path.relpath(path, self.path).replace('\\', '/')

            if grey_scale:
                path_old = pathA
                path = os.path.splitext(path_old)[0] + '_grey' + os.path.splitext(path_old)[1]
                code = 'magick -colorspace gray "{0}" "{1}"'.format(
                    path_old, path)
                subprocess.run(code)

            if frame:
                frame = 'frame,'
                width_factor *= 0.999
            else:
                frame = ''

            if mode=='fig':
                if float:
                    tex = '\\begin{figure}\n\\centering{'
                else:
                    tex = '\\begin{figure}[H]\n\\centering{'
                tex += tools.translate( '\\includegraphics[{1}width={2}\\linewidth,height={3}\\textheight,keepaspectratio]{{0}}\n',
                    {'{0}': path,
                     '{1}': frame,
                     '{2}': str(width_factor),
                     '{3}': str(height_factor)})

                if caption:
                    caption = RegME(caption, self.scope).package(captionX)
                    if caption2:
                        caption2 = RegME(caption2, self.scope).package(caption2X)
                        cap2 = '[' + caption2 + ']'
                    else:
                        cap2 = ''
                    tex += tools.translate('\\caption{1}{{0}}\n',
                        {'{0}': caption, '{1}':cap2})
                    if type(label) is str:
                        tex += '\\label{{0}}\n'.replace('{0}', label)
                    elif label == True:
                        auto_name = user_path.replace('\\', '').replace('/', '')
                        # os.path.basename(path)
                        tex += '\\label{{0}}\n'.replace('{0}', 'fig:'+auto_name)
                tex += '}\\end{figure}'

                _name1='img-fig'

            elif mode=='lst':
                if caption:
                    caption = RegME(caption).package(captionX)
                    caption = 'caption={%1}'.replace('%1', caption)
                    if type(label) is str:
                        caption += ',label={%1},'.replace('%1', label)
                    elif label == True:
                        caption += ',label={%1},'.replace('%1', os.path.basename(path))
                else:
                    caption = ''

                ndict = {'%path': path,
                         '%frame': frame,
                         '%cap': caption}
                tex ='''
\\begin{minipage}{\\linewidth}\n\\begin{lstlisting}[%capescapeinside=||, frame=none, numbers=none, xleftmargin=0pt,xrightmargin=0pt]
|\\includegraphics[%framewidth=\\linewidth]{%path}|
\\end{lstlisting}\n\\end{minipage}'''
                tex = tools.translate(tex, ndict)
                _name1='img-lst'

            elif mode=='tab':
                if float:
                    tex = '\\begin{table}\n\\centering{'
                else:
                    tex = '\\begin{table}[H]\n\\centering{'
                if caption:
                    caption = RegME(caption).package(captionX)
                    tex += '\\caption%2{%1}\n'.replace('%1', caption)
                    if caption2:
                        tex = tex.replace('%2', '['+ caption2 +']')
                    else:
                        tex = tex.replace('%2', '')
                    if type(label) is str:
                        tex += '\\label{{0}}\n'.replace('{0}', label)
                    elif label == True:
                        tex += '\\label{{0}}\n'.replace('{0}', os.path.basename(path))
                tex += '\\includegraphics[%2width=\\linewidth,height=0.90\\textheight,keepaspectratio]{%1}\n}\\end{table}'.replace(
                    '%1', path).replace('%2', frame)

                _name1='img-tab'

            else:
                raise ValueError('unknown mode atribute, allowed are: "fig", "tab", "lst"')

            if page_break==True:
                tex = self.page_break(True, inherit=True) + tex
            elif page_break==False:
                tex = tex + self.page_break(False, inherit=True)

            if (display is None or True) and (self.display or display):
                ipdisplay(Image(pathA, width=display_width))

            if add_space:
                tex = '\n\n'+tex+'\n\n'

            self._last_TeXM = 'p'
            return self._add(_name1, tex, inherit)
    p = img

    #$$ def math
    def math(self,
            equation   = '',
            mode       = 'e*',
            label      = None,
            equationX  = None,
            add_space  = False,
            page_break = None,
            inherit    = None,
            display    = None,
            exe        = False,
            scope      = None
        ):

        if self.active:
            if inherit    is None: inherit   = self.inherit
            if mode       is None: mode      = self.math_mode
            if equationX  is None: equationX = self.equationXm
            if display    is None: display   = self.displaym


            if mode not in ['t*', 't+']:
                equation = RegME(equation, self.scope).package(equationX)

            if exe:
                exec(equation,self.scope)

            if label:
                lab = '\\label{' + label + '}'
            else:
                lab = ''

            if mode == 'e+':
                tex = '\\begin{equation} ' + lab + \
                    '\n' + equation + '\n\\end{equation}'

            elif mode == 'e*':
                tex = '\\begin{equation*} ' + lab + \
                    '\n' + equation + '\n\\end{equation*}'

            elif mode == 'i*':
                tex = '$' + equation + '$'

            elif mode == 'm+':
                tex = '\\begin{multline} ' + lab + \
                    '\n' + equation + '\n\\end{multline}'

            elif mode == 'm*':
                tex = '\\begin{multline*} ' + lab + \
                    '\n' + equation + '\n\\end{multline*}'

            elif mode == 'a+':
                tex = '\\begin{align} ' + lab + \
                    '\n' + equation + '\n\\end{align}'

            elif mode == 'a*':
                tex = '\\begin{align*} ' + lab + \
                    '\n' + equation + '\n\\end{align*}'

            elif mode == 'd+':
                tex = '\\begin{dmath} ' + lab + \
                    '\n' + equation + '\n\\end{dmath}'

            elif mode == 'g+':
                tex = '\\begin{gather} ' + lab + \
                    '\n' + equation + '\n\\end{gather}'

            elif mode == 'g*':
                tex = '\\begin{gather*} ' + lab + \
                    '\n' + equation + '\n\\end{gather*}'

            elif mode == 't*' or mode == 't+':
                tex = equation

            if add_space:
                tex = '\n' + tex + '\n'

            if (display) and (mode not in ['t*', 't+']):
                ipdisplay(Latex('$'+RegME(equation).package(99)+'$'))

            if page_break==True:
                tex = self.page_break(True, inherit=True) + tex
            elif page_break==False:
                tex = tex + self.page_break(False, inherit=True)

            self._last_TeXM = 'm'
            return self._add('eq', tex, inherit)
    m = math


    #$$ def tab
    def tab(self,
            cols       = '',
            data       = '',
            options    = '\\textwidth',
            caption    = None,
            label      = None,
            float      = False,
            header     = None,
            headerX    = None,
            stretchV   = 1.5,
            captionX   = 1,
            dataX      = 1,
            page_break = None,
            newlinemod = False,
            inherit    = None,
            scope      = None,
        ):

        if self.active:
            if inherit   is None: inherit  = self.inherit
            if float     is None: float    = self.floatt
            if headerX   is None: headerX  = self.equationXt
            if captionX  is None: caption  = self.captionXt
            if dataX     is None: dataX    = self.dataXt

            if caption:
                if label:
                    label = '\\label{'+label+'}'
                else:
                    label = ''
                caption = '\\caption{' + \
                    RegME(caption).package(captionX) + '}'+ label +'\\\\'
            else:
                caption = ''

            if newlinemod==True:
                data = data.replace('\n', '\n\\\\\n')
            elif newlinemod==2:
                data = data[1:-1].replace('\n', '\n\\\\\n')

            if header:
                header = '\\hline\n' + \
                    RegME(header).package(headerX) + \
                    '\n\\\\\\hline\\hline\\hline\\hline\n\\endhead'
            elif not float:
                header = '\\endhead'
            else:
                header = ''

            tex = ('''\\begingroup
\\def\\arraystretch{%StV}
\\begin{tabularx}{%Opt}{%Col}
%Cap
%Hea
%Dat
\\end{tabularx}
\\endgroup''')

            ndict = {'%Opt': options,
                     '%Col': cols,
                     '%Cap': caption,
                     '%StV': str(stretchV),
                     '%Lab': label,
                     '%Hea': header,
                     '%Dat': RegME(data).package(dataX)}
            tex = tools.translate(tex, ndict)

            if float == True:
                tex = '\\begin{table}\n' + tex + '\n\\end{table}'
            elif float == False:
                tex = '\\begin{table}[H]\n' + tex + '\n\\end{table}'

            if page_break==True:
                tex = self.page_break(True, inherit=True) + tex
            elif page_break==False:
                tex = tex + self.page_break(False, inherit=True)

            self._last_TeXM = 't'
            return self._add('tab', tex, inherit)
    t = tab

    #$$ def code
    def code(self,
            code,
            caption        = '',
            label          = '',
            language       = None,
            codeX          = 0,
            captionX       = 1,
            prevent_divide = True,
            page_break     = '',
            mathescape     = True,
            inherit        = None,
            scope          = None
        ):
        '''LaTeX: Insert into document an part of code. Code block is open for mode=True, which Caption and Label must be defined with start command. mode=False is close the region. To correctly recognized the part of code, the file must be saved and calcuted in completly.'''

        if self.active:
            if inherit is None: inherit = self.inherit
            if codeX is None: codeX = self.codeXc
            if captionX is None: captionX = self.captionXc


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

                if prevent_divide:
                    tex = '\\begin{absolutelynopage_break}\n' + tex

                _name1='c-open'

            elif code == False:
                self._temp.append(
                    inspect.currentframe().f_back.f_lineno - 1)
                tex = '%%%-TO-REPLACE-%%%' + str(self._temp)

                self._add('c-replace', tex, inherit)

                tex = '\n\\end{lstlisting}'

                if prevent_divide:
                    tex += '\\end{absolutelynopage_break}'

                _name1='c-close'

            elif type(code) == str:
                tex = '\\begin{lstlisting}[caption={%1},label={%2}%3%4]'
                caption = RegME(caption).package(captionX)
                tex = tex.replace('%1', caption)
                tex = tex.replace('%2', label)
                tex = tex.replace('%4', var1)
                tex = tex.replace('%3', var2)

                code = RegME(code).package(codeX)
                tex += '\n' + code + '\n'
                tex += '\\end{lstlisting}'

                if prevent_divide:
                    tex = '\\begin{absolutelynopage_break}\n' + tex
                    tex += '\n\\end{absolutelynopage_break}'

                _name1='c-text'

            if page_break==True:
                tex = self.page_break(True, inherit=True) + tex
            elif page_break==False:
                tex = tex + self.page_break(False, inherit=True)

            self._last_TeXM = 'c'
            return self._add(_name1, tex, inherit)
    c = code

    def file(self,
            path,
            caption       = None,
            label         = None,
            first_line    = 0,
            last_line     = 1e10,
            absolute_path = False,
            language      = None,
            page_break    = None,
            inherit       = None,
            captionX      = 1,
            scope         = None
        ):

        if self.active:
            if inherit  is None : inherit  = self.inherit
            if label    is None : label    = self.label
            if captionX is None : captionX = self.captionXf

            if language:
                var2 = ',language={' + language + '}'
            else:
                var2 = ''

            pathA = os.path.abspath(path).replace('\\', '/')
            if absolute_path:
                path = pathA
            else:
                path = os.path.relpath(path, self.path).replace('\\', '/')

            if type(label) is str:
                pass
            if label == True:
                label =os.path.basename(path)
            else:
                label = ''

            tex = '\\lstinputlisting[language=%5, firstline=%3, lastline=%4, caption={%1}, label={%2}, inputencoding=utf8, mathescape]{%6}'
            tex = tex.replace('%1', RegME(caption).package(captionX))
            tex = tex.replace('%2', label)
            tex = tex.replace('%3', first_line)
            tex = tex.replace('%4', last_line)
            tex = tex.replace('%5', var2)
            tex = tex.replace('%6', path.replace('\\', '/'))

            if page_break==True:
                tex = self.page_break(True, inherit=True) + tex
            elif page_break==False:
                tex = tex + self.page_break(False, inherit=True)

            self._last_TeXM = 'f'
            return self._add('file', tex, inherit)
    f = file


    #$$ def item
    def item(self,
            text       = None,
            equation   = None,
            mode       = 'i*',
            mline      = False,
            lalign     = None,
            label      = None,
            width      = None,
            lvl        = 1,
            postfix    = None,
            aligment   = None,
            textX      = None,
            equationX  = None,
            vspace1    = '-9.5mm',
            vspace2    = '-8mm',
            add_space  = False,
            page_break = '',
            inherit    = None,
            exe        = False,
            scope      = None,

            e          = None, # shortcut for equation
            x          = None, # shortcut for text
            m          = None, # shortcut for mode
            smallersp  = True,
        ):

        '''
        [pinky.item]

        :text:
        '''

        if self.active:
            if inherit   is None: inherit   = self.inherit
            if width     is None: width     = self.widthi
            if postfix   is None: postfix   = self.postfixi
            if textX     is None: textX     = self.textXi
            if equationX is None: equationX = self.equationXi

            if e: equation = e
            if x: text = x
            if m: mode = m

            lvl = '|'*lvl

            if scope:
                self.scope.update(scope)

            if self._last_TeXM == 'i' and smallersp:
                tex = '\\vspace*{-10pt}\n'
            else:
                tex = ''

            if text and equation and mode in ['i*', 't*', 't+', False] and not mline:
                if aligment: pass
                else:
                    aligment = lvl+'q{{width}mm} L'
                tex += (
                    "\\begin{tabularx}{\\textwidth}{{aligment}}\n"
                    "{text}&%\n"
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
                    "{text}%\n"
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
                    "{text}&%\n"
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
                    "{text}%"
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


            if equation and mode:
                equation = self.math(
                    mode      = mode,
                    equation  = equation,
                    label     = label,
                    equationX = equationX,
                    add_space = add_space,
                    inherit   = True,
                    exe       = exe)
            elif mode is False:
                equation = RegME(equation).package(textX)



            ndict = {
                '{text}': (RegME(text).package(textX) + postfix if text is not None else ''),
                '{equation}': equation,
                '{aligment}': aligment.replace('{width}',str(width)),
                '{vspace1}': vspace1,
                '{vspace2}': vspace2,
                '{lalign}': ('\\mathleft\n' if lalign else ''),
            }

            tex = tools.translate(tex, ndict)

            if page_break==True:
                tex = self.page_break(True, inherit=True) + tex
            elif page_break==False:
                tex = tex + self.page_break(False, inherit=True)


            self._last_TeXM = 'i'
            return self._add('item', tex, inherit)
    i = item




#$ ____ metaclass cunitmeta ________________________________________________ #

class pinkymeta(type):
    #$$ multiset
    #$$$ @prop:sett root
    @property
    def root(self):
        return os.path.join(self._root_path, self._root_name)

    @root.setter
    def root(self, path):
        # path to the root file, pre @ look in rootdir
        if path[0] == '@':
            path = path[1:]
            self._root_path = os.path.join(self.rootdir, path)
            self._root_name = 'main.tex'

        else:
            self._root_path = os.path.dirname(path)
            self._root_name = os.path.basename(path)

    #$$$ @prop:sett display
    @property
    def display(self):
        return [self.displayh, self.displaym, self.displayp]

    @display.setter
    def display(self, value):
        self.displayh = value
        self.displaym = value
        self.displayp  = value

    #$$$ @prop:sett minilist
    @property
    def minilist(self):
        return [self.minitoc, self.minilof, self.minilot]

    @minilist.setter
    def minilist(self, value):
        self.minitoc = value
        self.minilof = value
        self.minilot = value


    #$$$ @prop:sett autolabel
    @property
    def autolabel(self):
        return [self.autolabelh, self.autolabelp, self.autolabelf]

    @autolabel.setter
    def autolabel(self, value):
        self.autolabelh = value
        self.autolabelp = value
        self.autolabelf = value

    #$$$ @prop:sett float
    @property
    def float(self):
        return [self.floati, self.floatt]

    @float.setter
    def float(self, value):
        self.floati   = value
        self.floatt = value

    #$$$ @prop:sett textX
    @property
    def textX(self):
        return [self.textXx, self.textXh, self.text2Xh, self.textXi]

    @textX.setter
    def textX(self, value):
        self.textXx = value
        self.textXh = value
        self.text2Xh = value
        self.textXi = value

    #$$$ @prop:sett captionX
    @property
    def captionX(self):
        return [self.captionXp, self.caption2Xp, self.captionXt, self.captionXc, self.captionXf]

    @captionX.setter
    def captionX(self, value):
        self.captionXp  = value
        self.caption2Xp = value
        self.captionXt  = value
        self.captionXc = value
        self.captionXf = value

    #$$$ @prop:sett equationX
    @property
    def equationX(self):
        return [self.equationXm, self.equationXi]

    @equationX.setter
    def equationX(self, value):
        self.equationXm = value
        self.equationXi = value

    #$$$ @prop:sett headeX
    @property
    def headerX(self):
        return [self.equationXt]

    @headerX.setter
    def headerX(self, value):
        self.equationXt  = value

    #$$$ @prop:sett dataX
    @property
    def dataX(self):
        return [self.dataXt]

    @dataX.setter
    def dataX(self, value):
        self.dataXt  = value

    #$$$ @prop:sett codeX
    @property
    def codeX(self):
        return [self.codeXc]

    @codeX.setter
    def codeX(self, value):
        self.codeXc  = value


#$ ____ class pinky_________________________________________________________ #

class pinky(TeXM, object, metaclass=pinkymeta):
    #$$ class atributes
    active         = True
        # process method and printing
    makeQ          = True
        # q print pdf or not
    echo           = False
        # display all
    displayh       = True
        # display head toogle
    displaym       = True
        # display math toogle
    displayp       = True
        # display img  toogle
    scope          = {}
        # local dict of main file
    keys           = {}
        # additional keys to template
    keys2          = {}
        # -----
    calcN          = 2
        # how many times make tex doc
    fclear         = False
        # clear path folder after make
    forcecopy      = False
        # force update tex template
    path           = './tex'
        # path to destination folder
    sname          = 'pinky.py'
        # name of source file
    rootdir        = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'template')
        # path to folder of templates
    inherit        = False
         # insert code into db (False) or return tex code (true)
    alvl           = 0
        # additional
    minitoc        = False
        # insert minitor after chapters
    minilof        = False
        # insert minilofts after chapters
    minilot        = False
        # insert minilots after chapters
    double_page    = False
        # double page mode
    display_width  = 600
        # width of rendered pictures in atom ide by ipython.display
    autolabelh     = False
        # automatic label of headers, by level and acronim
    autolabelp     = True
        # automatic labeled images by name of file with img precessor
    autolabelf     = True
        # automatic labeled files by name of files
    floati         = False
        # floated images
    floatt         = False
        # floated tables
    rootp          = '.'
        # root folder of the images, as a shortcut
    grey_scale     = False
        # convert pictures to grey-scale
    math_type      = 'e*'
        # defualt type of mathematic equations
    widthi         = 70
        # width of text column in item
    postfixi       = ':'
        # postifx of tex in items
    textXx         = 1

    textXh         = 1

    text2Xh        = 1

    textXi         = 1

    captionXp      = 1

    caption2Xp     = 1

    captionXt      = 1

    captionXc      = 1

    captionXf      = 1

    equationXm      = 11

    equationXi     = 11

    equationXt     = 1

    dataXt         = 1

    codeXc         = 0


    _root_path     = os.path.join(rootdir, 'c')

    _root_name     = 'main.tex'

    data           = np.array([], dtype=str)

    _store         = {}

    _last_TeXM     = ''


    #$$ --init--
    def __init__(self, root=None, dbase=None, mdata=None, **kwargs):
        for key, val in kwargs.items():
            self.__dict__[key] = val
        if root is not None:
            self.root = root

    #$$ multiset
    #$$$ @prop:sett root
    @property
    def root(self):
        return os.path.join(self._root_path, self._root_name)

    @root.setter
    def root(self, path):
        # path to the root file, pre @ look in rootdir
        if path[0] == '@':
            path = path[1:]
            self._root_path = os.path.join(self.rootdir, path)
            self._root_name = 'main.tex'

        else:
            self._root_path = os.path.dirname(path)
            self._root_name = os.path.basename(path)

    #$$$ @prop:sett display
    @property
    def display(self):
        return [self.displayh, self.displaym, self.displayp]

    @display.setter
    def display(self, value):
        self.displayh = value
        self.displaym = value
        self.displayp  = value

    #$$$ @prop:sett minilist
    @property
    def minilist(self):
        return [self.minitoc, self.minilof, self.minilot]

    @minilist.setter
    def minilist(self, value):
        self.minitoc = value
        self.minilof = value
        self.minilot = value


    #$$$ @prop:sett textX
    @property
    def textX(self):
        return [self.textXx, self.textXh, self.text2Xh, self.textXi]

    @textX.setter
    def textX(self, value):
        self.textXx = value
        self.textXh = value
        self.text2Xh = value
        self.textXi = value

    #$$$ @prop:sett captionX
    @property
    def captionX(self):
        return [self.captionXp, self.caption2Xp, self.captionXt, self.captionXc, self.captionXf]

    @captionX.setter
    def captionX(self, value):
        self.captionXp  = value
        self.caption2Xp = value
        self.captionXt  = value
        self.captionXc = value
        self.captionXf = value

    #$$$ @prop:sett equationX
    @property
    def equationX(self):
        return [self.equationXm, self.equationXi]

    @equationX.setter
    def equationX(self, value):
        self.equationXm  = value
        self.equationXi = value

    #$$$ @prop:sett headeX
    @property
    def headerX(self):
        return [self.equationXt]

    @headerX.setter
    def headerX(self, value):
        self.equationXt  = value

    #$$$ @prop:sett dataX
    @property
    def dataX(self):
        return [self.dataXt]

    @dataX.setter
    def dataX(self, value):
        self.dataXt  = value

    #$$$ @prop:sett codeX
    @property
    def codeX(self):
        return [self.codeXc]

    @codeX.setter
    def codeX(self, value):
        self.codeXc  = value

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    #$$ magic behaviour
    #$$$ def --iadd--
    def __iadd__(self, othe):
        if type(othe) == pinky:
            self.data = np.append(self.data, othe.data)
        return self

    #$$ def append
    def append(self, othe):
        return self.__iadd__(othe)

    #$$ def -add
    def _add(self, name, tex, inherit=False):
        if inherit is True:
            return tex
        elif type(inherit)==str:
            self.store(inherit, tex)
        elif inherit is False:
            self.data = np.append(self.data, tex + '\n%')
            if self.echo:
                print('[pinky.' + name + ']\n' + tex)


    def _bib_update(self):
        basepath = os.path.dirname(os.path.realpath(__file__))
        os.system(os.path.join(basepath, r'template\bibme.bat'))

    #$$ def -copy-temp
    def _copy_temp(self):
        if self.forcecopy:
            if os.path.is_dir(self.path):
                shutil.rmtree(self.path)
            self._bib_update()
            shutil.copytree(self._root_path, self.path)
        else:
            if os.path.isdir(self.path):
                path = os.path.join(self.path, self._root_name)
                if os.path.exists(path):
                    os.remove(path)
                if os.path.exists(path + '.bak'):
                    os.rename(path + '.bak', path)
                else:
                    pathT = os.path.join(self._root_path, self._root_name)
                    shutil.copyfile(pathT, path)
            else:
                self._bib_update()
                shutil.copytree(self._root_path, self.path)



    #$$ def -sdict
    def _sdict(self):
        if type(self.data) is np.ndarray:
            _sdict = {'%<0001>%': '\n'.join(map(str, self.data))}
        elif type(self.data) is dict:
            _sdict = {}
            for key, val in self.data.items():
                _sdict.update({'%<'+key+'>%': '\n'.join(map(str, val.data))})

        _sdict.update({'%<'+k+'>%': v for k, v in self.keys.items()})
        _sdict.update({'%<'+k+'>%': v for k, v in self.keys2.items()})

        try:
        #  try import data from project default
            name = os.path.splitext(self._root_name)[0] + '.py'
            path = os.path.abspath(os.path.join(self.path, name))
            spec   = importlib.util.spec_from_file_location("module.name", path)
            script = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(script)
            for key,val in script.__keys__.items():
                if '%<'+key+'>%' not in _sdict:
                    _sdict['%<'+key+'>%'] = val
            script.__script__(_sdict)
            del script
        except:
            pass

        return _sdict

    #$$ def -rep-in-file
    def _rep_in_file(self, Dict):
        path1 = os.path.join(self.path, self._root_name)
        path2 = path1 + '.bak'

        os.rename(path1, path2)

        with open(path2, encoding='utf-8') as infile, open(path1, 'w', encoding='utf-8') as outfile:
            for line in infile:
                outfile.write(tools.translate(line, Dict))

    #$$ def -pdf-maker
    def _pdf_maker(self, force_mode=True, shell_escape=False, synctex=True):
        '''Start TeX compilating. There is needed pdflatex software. The sheel-escepe and forcecopy can be activated.'''
        sett = ''
        if synctex:      sett += ' -synctex=1'
        if force_mode:   sett += ' -interaction=nonstopmode -file-line-error'
        if shell_escape: sett += '--shell-escape'
        code = 'cd "{0}" & pdflatex {1} "{2}"'.format(
            self.path, sett, self._root_name)
        subprocess.run(code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    #$$ def -bib-loader
    def _bib_loader(self):
        '''Start BiB compilating. There are needed bibtex software. BiB root must have the extension .bib.'''
        name_noext = os.path.basename(os.path.splitext(self._root_name)[0])
        # code = 'cd "{0}" & bibtex "{1}"'.format(
        #     self.path, name_noext + '.aux')
        code = 'cd "{0}" & biber "{1}"'.format(
            self.path, name_noext + '.bcf')
        # code = 'cd "{0}" & bibtex8 "{1}"'.format(
        #     self.path, name_noext + '.bcf')
        subprocess.run(code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    #$$ def -tex-cleaner
    def _tex_cleaner(self):
        '''fclear folder after TeX compiling. There are lots file deleted, so please use it carefully.'''
        ext_list = ['.aux', '.lof', '.lot', '.toc',
                    '.bbl', '.blg', '.lol', '.maf', '.mtc', '.out']

        for i in range(30):
            ext_list.append('.mlf' + str(i))
            ext_list.append('.mlt' + str(i))
            ext_list.append('.mtc' + str(i))

        name_noext = os.path.basename(os.path.splitext(self._root_name)[0])

        for ext in ext_list:
            if os.path.exists(os.path.join(self.path, name_noext) + ext):
                os.remove(os.path.join(self.path, name_noext) + ext)

    #$$ def -post-code
    def _post_code(self):
        '''Postprocessing of code blocks. They must be evaluated in two step.'''
        if self.sname:
            i = 0
            path = self.sname
            f = open(path, encoding='utf-8')
            rootfile = f.readlines()
            f.close()
            for cell in self.data:
                if cell[:18] == '%%%-TO-REPLACE-%%%':
                    val = ''.join(eval('rootfile' + cell[18:].replace(',', ':')))
                    self.data[i] = RegME(val).package(0)
                i += 1

    #$$ def make
    def make(self, calcN=None, fclear=None, force_mode=False, shell_escape=False, synctex=True, active=None):
        if active is None:
            active = self.active
        if active and self.makeQ:
            self._copy_temp()
            # self._post_code()
            self._rep_in_file(self._sdict())
            if calcN==None: calcN=self.calcN
            for i in range(calcN):
                self._pdf_maker(force_mode, shell_escape, synctex)
                if i == 2:
                    self._bib_loader()
            if fclear==None: fclear=self.fclear
            if fclear:
                self._tex_cleaner()

    #$$ def store
    def store(self, name, tex=None):
        self._store[name] = tex

    #$$ def get
    def get(self, mode='r', name=None, textX=0):
        if mode=='r':
            return self._store[name]
        elif mode=='x':
            self.tex(text=self._store[name], textX=textX)
