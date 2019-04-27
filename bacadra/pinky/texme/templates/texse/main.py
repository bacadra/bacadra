class tmp:

    def __init__(self, texme):

        self.texme = texme

        self.texme.setts.keys(
            author      = '',
            date        = '',
            date_inc    = '',
            head_line_0 = '%',
            head_line_1 = '%',
            head_line_2 = '%',
            logo_path   = '%',
            bib_path    = r'main.bib',
            title_page  = '',
            tocdepth    = 2,
        )


        self.language('pl')


        # # TODO: test it again please
        # if hasattr(self.texme, 'core'):
        #     lang = self.texme.core.tools.clang.setts.output()
        # else:
        #     from bacadra.tools.clang import clang
        #     lang = clang.setts.output()
        #
        # if lang in ['en', 'pl']:
        #     self.language(lang)
        #
        # else:
        #     raise ValueError('Unsupported language')



    def language(self, language):
        if language=='pl':
            self.texme.setts.keys(lang1='polish')
            self.texme.setts.keys(lang2='Rys.')
            self.texme.setts.keys(lang3='Tab.')
            self.texme.setts.keys(lang4='Kod ')
            self.texme.setts.keys(lang5='% ')
            self.texme.setts.keys(lang6='Strona ')

        elif language=='en':
            self.texme.setts.keys(lang1='english')
            self.texme.setts.keys(lang2='Fig.')
            self.texme.setts.keys(lang2='Tab.')
            self.texme.setts.keys(lang4='Code ')
            self.texme.setts.keys(lang5='')
            self.texme.setts.keys(lang6='Page ')


    def author(self, name):
        self.texme.setts.keys(author=name)

    def date(self, day=None, month=None, year=None):
        day   = r'\day='  +str(day  ) if type(day)==int   else ''
        month = r'\month='+str(month) if type(month)==int else ''
        year  = r'\year=' +str(year ) if type(year)==int  else ''
        self.texme.setts.keys(date='\n'.join((day, month, year)))

    def date_inc(self, day=None, month=None, year=None):
        day   = r'\advance\day by '  +str(day  ) if type(day)==int   else ''
        month = r'\advance\month by '+str(month) if type(month)==int else ''
        year  = r'\advance\year by ' +str(year ) if type(year)==int  else ''
        self.texme.setts.keys(date_inc='\n'.join((day, month, year)))

    def folio(self, h0=None, h1=None, fl=None):
        if h0==True:
            self.texme.setts.keys(head_line_0= '\\normalsize{\\contour{black}{\\textsc{OBLICZENIA STATYCZNO-WYTRZYMAŁOŚCIOWE}}}')
        elif type(h0)==str:
            self.texme.setts.keys(head_line_0= '\\normalsize{\\contour{black}{\\textsc{'+h0+'}}}')

        if type(h1)==str:
            self.texme.setts.keys(head_line_1=r'\footnotesize ' + h1)

        if fl == True:
            self.texme.setts.keys(foot_line_left=r'\fancyfoot[L]{\footnotesize \small{\contour{black}{\textsc{PBW INŻYNIERIA}}} \\ ul. Sokolnicza 5/72-75 \\ 53-676 Wrocław}')
        elif type(fl) == str:
            self.texme.setts.keys(foot_line_left=r'\fancyfoot[L]{\footnotesize \small{\contour{black}{'+fl+'}')

    def tocdepth(self, lvl):
        r'''
        \chapter is level 0
        \section is level 1
        \subsection is level 2
        \subsubsection is level 3
        \paragraph is level 4
        \subparagraph is level 5
        '''
        self.texme.setts.keys(tocdepth=lvl)


    def tpage(self, cat, id):

            if cat == 'railb':

                subtitle = r'Obiekt mostowy przeznaczony dla ruchu kolejowego \\ {' + id + '}'

                self.folio(
                    h0=True,
                    h1=r'Obiekt mostowy przeznaczony dla ruchu kolejowego \\ \scriptsize {' + id + '}')

            elif cat == 'roadb':

                subtitle = r'Obiekt mostowy przeznaczony dla ruchu drogowego \\ {' + id + '}'

                self.folio(
                    h0=True,
                    h1=r'Obiekt mostowy przeznaczony dla ruchu drogowego \\ \scriptsize {' + id + '}')

            elif cat == 'footb':

                subtitle = r'Obiekt mostowy przeznaczony dla ruchu pieszego \\ \textbf{' + id + '}'

                self.folio(
                    h0=True,
                    h1=r'Obiekt mostowy przeznaczony dla ruchu pieszego \\ \scriptsize {' + id + '}'
                )


            else:
                raise ValueError('Undefined type')


            out =  r'''
                \title{

                \Huge \textbf{\uppercase{ZAŁĄCZNIK}} \\ [5.0cm]
        		{\rule{\linewidth}{0.5mm}}           \\ [0.5cm]

        		\Large \textbf{\uppercase{%
                OBLICZENIA \\ STATYCZNO-WYTRZYMAŁOŚCIOWE
                }}

        		{\rule{\linewidth}{0.5mm}}           \\ [0.5cm]

        		'''+subtitle+r'''

        		{\rule{\linewidth}{0.5mm}}           \\ [0.5cm]

        		%\normalsize \today \\ [0.5cm]
        		\normalsize {\MONTH~\YEAR~r.} \\ [0.5cm]

                {\rule{\linewidth}{0.5mm}}           \\ [0.5cm]

                }
                \date{}
                \author{}
                \maketitle\thispagestyle{empty}
                \newpage
            '''

            self.texme.setts.keys(title_page=out)

