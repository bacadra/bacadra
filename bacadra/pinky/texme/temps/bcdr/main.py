class template:
    def __init__(self):

        self.base_keys = {
            'author'         : None,
            'head_line_0'    : None,
            'head_line_1'    : None,
            'head_line_2'    : None,
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


    def head_line_0(self, val):
        if val == None:
            val = '\\normalsize{\\contour{black}{\\textsc{SOFTWARE DOCUMENTATION}}}'

        self.base_keys['head_line_0'] = val


    def head_line_1(self, val):
        if val == None:
            val = r'%'

        elif type(val) == str:
            val = r'\footnotesize ' + val

        self.base_keys['head_line_1'] = val

    def head_line_2(self, val):
        if val == None:
            val = r'%'

        elif type(val) == str:
            val = r'\scriptsize ' + val

        self.base_keys['head_line_2'] = val

    def foot_line_left(self, val):
        if val == None:
            val =  r'\fancyfoot[L]{\footnotesize \small{\contour{black}{\textsc{bacadadra team}}} \\ \url{www.github.com/bacadra} \\ \href{mailto:bacadra@gmail.com}{bacadra@gmail.com}}'

        elif type(val) == str:
            val =  r'\fancyfoot[L]{\footnotesize \small{\contour{black}{'+val+'}'


        self.base_keys['foot_line_left'] = val


    def logo_path(self, val):
        if val == None:
            val = r'\lhead{\includegraphics[height=1.5cm]{bacadra_logo.jpg}}'

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


                subtitle = r'module \textbf{' + val['module'] + '}'

                version = val['version']

                out =  r'''
                    \title{

                    \vspace{4.0cm}

           		    {\rule{\linewidth}{0.5mm}}           \\ [1.5cm]

                    \Huge \textbf{\uppercase{BACADRA SOFTWARE}} \\ [1.0cm]

            		{\rule{\linewidth}{0.25mm}}           \\ [0.5cm]

            		\Large \textbf{\uppercase{%
                    Documentation \& user manual
                    }}

            		{\rule{\linewidth}{0.25mm}}           \\ [0.5cm]

            		\large  '''+subtitle+r'''

            		{\rule{\linewidth}{0.25mm}}           \\ [0.5cm]

            		\normalsize version '''+ version +r''' \\ [0.5cm]

                    {\rule{\linewidth}{0.5mm}}           \\ [0.5cm]

                    }
                    \date{}
                    \author{}
                    \maketitle\thispagestyle{empty}
                    \newpage

                    \thispagestyle{empty}
                    \vspace{5.0cm}
                    \begin{center}
                    \includegraphics[frame,width=0.999\linewidth,height=0.9\textheight,keepaspectratio]{../bacadra_logo.jpg}
                    \end{center}
                    \newpage
                '''

            else:
                out = val

        self.base_keys['title_page'] = out

class exe:
    def __init__(self, othe):
        self.othe = othe

    def item_head(self, tex):
        self.othe.add(tex)