'''
------------------------------------------------------------------------------
***** word (doc)ument generator *****
==============================================================================

Problems:

- relly slowly math adding! this way there is no sesnse to build-up more advance module :/

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''
#$ ######################################################################### #

import os

import win32com.client as win32

from ...tools.setts import sinit


#$ ____ class setts ________________________________________________________ #

class setts(sinit):

#$$ ________ def cave ______________________________________________________ #

    def cave(self, value=None):
        '''
        Atribute provide path to folder with templates. As defualt it refere to folder inside pinky.docme module call "templates".
        '''

        if value==None: return self.tools.get('cave')

        self.tools.set('cave', value)

#$$ ________ def template __________________________________________________ #

    def template(self, value=None):
        '''
        File of main doc document in inpath folder.
        '''

        if value==None: return self.tools.get('template')

        self.tools.set('template', value)






#$ ____ class docme ________________________________________________________ #

class docme:

    setts = setts()

    setts.cave(os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'templates'))

    setts.template(False)


    def __init__(self, core=None):

        self.core = core

        self.setts = setts(master=self.setts.tools, root=self)


    def open(self):

        # self.wordApp = win32.gencache.EnsureDispatch('Word.Application')

        self.wordApp = win32.Dispatch('Word.Application')

        self.wordApp.Visible = False

        self.wordApp.Application.OMathAutoCorrect.UseOutsideOMath = True


        if self.setts.template():

            path = os.path.abspath(os.path.join(
                self.setts.cave(),
                self.setts.template(),
                'main.docx',
            ))

            self.doc = self.wordApp.Application.Documents.Open(path)

        else:

            self.doc = self.wordApp.Documents.Add()

    def close(self, path):

        self.wordApp.ActiveDocument.SaveAs(FileName=os.path.abspath(path))

        self.doc.Close()

        self.wordApp.Quit()

    def x(self, text):
        rng       = self.doc.Paragraphs.Last.Range
        rng.Style = 'Normal'
        rng.Text  = text
        rng.InsertParagraphAfter()

    def h(self, lvl, text):
        rng       = self.doc.Paragraphs.Last.Range
        rng.Style = "Heading " + str(lvl)
        rng.Text  = text
        rng.InsertParagraphAfter()

    def p(self, path):
        rng       = self.doc.Paragraphs.Last.Range
        rng.InlineShapes.AddPicture(os.path.abspath(path))
        rng.InsertParagraphAfter()

    def m(self, eq):
        rng       = self.doc.Paragraphs.Last.Range
        rng.Text = eq

        for AC in self.wordApp.Application.OMathAutoCorrect.Entries:
            if rng.Text.find(AC.Name) >= 0:
                rng.Text = rng.Text.replace(AC.Name, AC.Value)

        rng = rng.OMaths.Add(rng)
        rng.OMaths(1).BuildUp()
        rng.InsertParagraphAfter()



#$ ######################################################################### #
