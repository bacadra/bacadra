class template:
    def __init__(self):

        self.base_keys = {
            'author'         : None,
            'head_line_0'    : None,
            'date_inc'       : None,
            'date'           : None,
            'head_line_1'    : None,
            'foot_line_left' : None,
            'logo_path'      : None,
            'bib_path'       : None,
            'title_page'     : None,
        }

    def run(self, keys):
        self.exte_keys = keys
        for key,val in self.base_keys.items():
            # remember that method should modify base_keys or do somethink
            # return method with the same name and send value
            if key in self.exte_keys:
                val = self.exte_keys[key]
            exec(f'self.{key}({val})')
        return self.base_keys

    def author(self, val):
        if val == None:
            val = ''

        self.base_keys['author'] = val


    def date_inc(self, val):
        if val == None:
            val = ''

        elif type(val) is int:
            val = r'\advance\day by ' + str(val)

        elif type(val) in [list,tuple]:
            val = (r'\advance\day by '   + str(val[0]) + '\n' +
                   r'\advance\month by ' + str(val[1]) + '\n' +
                   r'\advance\year by '  + str(val[2]))


        else:
            raise ValueError('Type of val must be val or None')

        self.base_keys['date_inc'] = val



    def date(self, val):
        if val == None:
            val = ''

        elif type(val) is int:
            val = r'\day=' + str(val)

        elif type(val) in [list,tuple]:
            val = (r'\day='   + str(val[0]) + '\n' +
                   r'\month=' + str(val[1]) + '\n' +
                   r'\year='  + str(val[2]))


        else:
            raise ValueError('Type of val must be val or None')

        self.base_keys['date'] = val




    def head_line_0(self, val):
        if val == None:
            val = '\\normalsize{\\contour{black}{\\textsc{OBLICZENIA STATYCZNO-WYTRZYMAŁOŚCIOWE}}}'

        self.base_keys['head_line_0'] = val


    def head_line_1(self, val):
        if val == None:
            val = r'%'

        elif type(val) == str:
            val = r'\footnotesize ' + val

        self.base_keys['head_line_1'] = val


    def foot_line_left(self, val):
        if val == None:
            val = '%'

        elif val == True:
            val =  r'\fancyfoot[L]{\footnotesize \small{\contour{black}{\textsc{PBW INŻYNIERIA}}} \\ ul. Sokolnicza 5/72-75 \\ 53-676 Wrocław}'

        elif type(val) == str:
            val =  r'\fancyfoot[L]{\footnotesize \small{\contour{black}{'+val+'}'


        self.base_keys['foot_line_left'] = val


    def logo_path(self, val):
        if val == None:
            val = r'%'

        elif val == True:
            val = r'\lhead{\includegraphics[height=1.5cm]{logo-pbw.png}}'

        elif type(val) is str:
            val = r'\lhead{\includegraphics[height=1.5cm]{'+val+'}}'


        self.base_keys['logo_path'] = val


    def bib_path(self, val):
        if val == None:
            val = r'main.bib'

        self.base_keys['bib_path'] = val

    def title_page(self, val):
        if val == None:
            out = ''

        elif type(val) is dict:

            if val['style'] == 'simple':

                if val['type'] == 'train':

                    subtitle = r'Obiekt mostowy przeznaczony dla ruchu kolejowego \\ \textbf{' + val['LK'] + '}'

                    self.head_line_1(r'Obiekt mostowy przeznaczony dla ruchu kolejowego \\ \scriptsize \textbf{' + val['LK'] + '}')

                elif val['type'] == 'road':

                    subtitle = r'Obiekt mostowy przeznaczony dla ruchu drogowego \\ \textbf{' + val['DK'] + '}'

                elif val['type'] == 'foot':

                    subtitle = r'Obiekt mostowy przeznaczony dla ruchu pieszego \\ \textbf{' + val['ID'] + '}'

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

            else:
                out = val

        self.base_keys['title_page'] = out

class ext:
    def __init__(self, othe):
        self.othe = othe

    # only for test purpose
    def item_head(self, tex):
        self.othe.add(tex)


