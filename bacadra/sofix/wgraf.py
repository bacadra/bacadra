'''
------------------------------------------------------------------------------
***** (w)in(graf) post graphics *****
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

import subprocess

import glob

from ..tools.setts import sinit

from . import verrs


#$ ____ class setts ________________________________________________________ #

class setts(sinit):

#$$ ________ def active ____________________________________________________ #

    def active(self, value=None, check=None):
        return self.tools.sgc('active', value, check)

#$$ ________ def gra_name __________________________________________________ #

    def gra_name(self, value=None, check=None):
        return self.tools.sgc('gra_name', value, check)

#$$ ________ def output __________________________________________________ #

    def output(self, value=None, check=None):
        return self.tools.sgc('output', value, check)

#$$ ________ def watermark _________________________________________________ #

    def watermark(self, value=None, check=None):
        return self.tools.sgc('watermark', value, check)

#$$ ________ def size ______________________________________________________ #

    def size(self, value=None, check=None):

        if value!=None:

            if type(value)==list:
                self.tools.set('size', list)

            else:
                self.tools.set('size', {
                    'h': [2023,1296,289,289],
                    'v': [2033,2668,289,289],
                    's': [2139,1266,229,242], # 18.00 x 10.50 [cm]
                    'a': [2139,1000,229,242], # 18.00 x  8.50 [cm]
                }[value])

        elif value==None:

            # create copy
            size = self.tools.get('size')[:]

            # add topline
            size[3] += self.addtopline() * 49

            value = '{}x{}+{}+{}'.format(size[0],size[1],size[2],size[3])

            return value

#$$ ________ def addtopline ________________________________________________ #

    def addtopline(self, value=None, check=None):
        return self.tools.sgc('addtopline', value, check)

#$$ ________ def delete ____________________________________________________ #

    def delete(self, value=None, check=None):
        return self.tools.sgc('delete', value, check)

#$$ ________ def project ___________________________________________________ #

    def project(self, folder_path=None, cdb_name=None, check=None, mode='p'):

        if type(check)==str:
            return self.tools.sgc(name='sofistik:'+check,
                value=eval(check), check=True)


        folder_path = self.tools.sgc(name='project:folder_path', value=folder_path, check=check)

        if folder_path==True:
             folder_path=self.tools.root.core.sofix.sbase.setts.project(
                mode='p')


        cdb_name = self.tools.sgc(name='project:cdb_name', value=cdb_name, check=check)

        if cdb_name==True:
             cdb_name=self.tools.root.core.sofix.sbase.setts.project(
                mode='c')

        if folder_path and cdb_name:

            if   mode=='pc': return os.path.join(folder_path, cdb_name)

            elif mode=='p' : return folder_path

            elif mode=='c' : return cdb_name







#$ ____ class wgraf ________________________________________________________ #

class wgraf:

    setts = setts()

    setts.active(True)

    setts.gra_name(False)

    setts.output('.')

    setts.watermark(False)

    setts.size('h')

    setts.addtopline(0)

    setts.delete(False)

    setts.project(folder_path=True, cdb_name=True)


#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, core=None):

        self.core = core

        self.setts = setts(master=self.setts.tools, root=self)


#$$ ________ def _gra2plb __________________________________________________ #

    def _gra2plb(self):
        '''
        Run parser of wingraf file. The cdb name should be defined. Wingraf file and cdb files must be in same directory! This can be improve in sofistik.def file.
        '''

        # cmd command, first change the actual localisation, we use here pushd instead of cd, because push can change also drive letter. then run sofistik parser eg. sps or wps, send cdb name and name of wingraf

        code = 'cmd /c pushd "{p0}" & "{p1}" -cdb:"{p2}" "{p3}"'.format(**{

            'p0': os.path.abspath(
                self.setts.project(mode='p')),

            'p1': self.core.sofix.sbase.setts.sofistik(mode='ep').replace(
                '/', '\\'),

            'p2': self.setts.project(mode='c'),

            'p3': self.setts.gra_name(),

        })

        subprocess.run(code)

#$$ ________ def _plb2pdf __________________________________________________ #

    def _plb2pdf(self):
        '''
        Convert sofistik report .plb to portable document format .pdf.
        '''

        # if sofistik 2016 is avaiable then use them, sofi16 has not problem with color print...

        se16 = self.core.sofix.sbase.setts.sofistik(env='v2016', check=True, mode='e')

        if os.path.exists(se16):

            sofi_loc = se16

        else:

            sofi_loc = self.core.sofix.sbase.setts.sofistik(mode='e')

        # create cmd command, first change folder to project, then use report browser (ursula) to convert report->pdf

        code = 'cmd /c pushd "{p0}" & "{p1}" "{p2}" -printto:"PDF" -picture:all'.format(**{

            'p0': os.path.abspath(self.setts.project(mode='p')),

            'p1': os.path.join(
                sofi_loc,
                self.core.sofix.sbase.setts.sofistik(mode='u')
                ).replace('/', '\\'),

            'p2': os.path.splitext(self.setts.gra_name())[0]+'.plb',

            })

        subprocess.run(code)




#$$ ________ def _del_old_jpg ______________________________________________ #

    def _del_old_jpg(self):
        '''
        Delete old image files of the same basename.
        '''

        if self.setts.delete():

            # create filename pattern
            filepattern = os.path.join(self.setts.output(),
                os.path.splitext(self.setts.gra_name())[0])+"-*.jpg"

            # loop over files adequete to filepattern
            for file in glob.glob(filepattern):

                # remove file
                os.remove(file)



#$$ ________ def _pdf2jpg __________________________________________________ #

    def _pdf2jpg(self):
        '''
        Explode multipage pdf to single page graphics .jpg.
        '''

        # if output folder does not exists, then create it
        if not os.path.isdir(os.path.abspath(self.setts.output())):
            os.makedirs(self.setts.output())

        # create cmd statment
        code = 'cmd /c pushd "{p0}" & "{p1}" -density 350 "{p2}" -quality 95 -scene 1 "{p3}-%03d.jpg"'.format(**{

            # change current dir to project folder
            'p0': os.path.abspath(self.setts.project(mode='p')),

            # create path to ImageMagick execute file
            'p1': self.core.sofix.sbase.setts.image_magick(mode='em'),

            # crete name of pdf file
            'p2': os.path.splitext(self.setts.gra_name())[0]+'.pdf',

            # create output base path
            'p3': os.path.join(os.path.abspath(self.setts.output()), os.path.splitext(self.setts.gra_name())[0]),

        })

        # run code in cmd!
        subprocess.run(code)








#$$ ________ def _jpg_convert ______________________________________________ #

    def _jpg_convert(self):
        '''
        Convert graphic file, trim and delete watermark symbol.
        '''

        # create jpg list as special symbol pattern
        filepattern = os.path.join(
            self.setts.output(),
            os.path.splitext(self.setts.gra_name())[0])+"-*.jpg"

        # loop over files adequete to file pattern
        for file in glob.glob(filepattern):

            if self.setts.watermark() is True:
                wmark = '-fuzz 15% -fill white -opaque "RGB(192,192,192)"'

            else:
                wmark = ''

            # create cmd statment
            code = 'cmd /c pushd "{p0}" & "{p1}" "{p2}" -crop {p3} {wmark} "{p2}"'.format(**{

                # output path
                'p0': self.setts.output(),

                # create ImageMagick execute file path
                'p1': self.core.sofix.sbase.setts.image_magick(mode='em'),

                # create base file
                'p2': os.path.basename(file),

                # insert format file
                'p3': self.setts.size(),

                'wmark': wmark,

            })

            # run command!
            subprocess.run(code)


#$$ ________ def run _______________________________________________________ #

    def run(self, active=None):

        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        # run sps with wingraf file
        self._gra2plb()

        # convert .plb to .pdf
        self._plb2pdf()

        # delete old images
        self._del_old_jpg()

        # convert .pdf to .jpg
        self._pdf2jpg()

        # convert jpg files
        self._jpg_convert()




#$$ ________ def mass ______________________________________________________ #

    def mass(self, cdb_data=[], gra_data=[], active=None, subpath=True):
        '''

        cdb_data
            p -> folder_path (changed in wgraf)
            c -> cdb_name (changed in wgraf)
            a -> active (changed in wgraf)
            s -> subpath (True or False)

        gra_data
            w -> gra_name
            o -> output
            m -> watermark
            s -> size
            a -> active
            t -> addtopline
            d -> delete

        '''


        # if user want to overwrite global active atribute
        if not self.setts.active(active, check=True): return

        verrs.BCDR_sofix_INFO_mass_start()

        cdb_i = 0
        for cdb_row in cdb_data:
            cdb_i+=1

            gra_i = 0
            for gra_row in gra_data:
                gra_i+=1

                othe = wgraf(core=self.core)
                othe.setts.tools.master = self.setts.tools

                if 'p' in cdb_row: othe.setts.project(folder_path=cdb_row['p'])
                if 'c' in cdb_row: othe.setts.project(cdb_name=cdb_row['c'])

                if 'w' in gra_row: othe.setts.gra_name(gra_row['w'])
                if 'o' in gra_row: othe.setts.output(gra_row['o'])
                if 'm' in gra_row: othe.setts.watermark(gra_row['m'])
                if 's' in gra_row: othe.setts.size(gra_row['s'])
                if 't' in gra_row: othe.setts.addtopline(gra_row['t'])
                if 'd' in gra_row: othe.setts.delete(gra_row['d'])


                if 's' in cdb_row: subpath = cdb_row['s']

                if subpath==True:
                    output = othe.setts.output()
                    othe.setts.output(output+'\\'+othe.setts.project(mode='c'))

                verrs.BCDR_sofix_INFO_mass_loop([
                    cdb_i, cdb_row, gra_i, gra_row
                    ])

                othe.run()

        verrs.BCDR_sofix_INFO_mass_end()



#$ ######################################################################### #
