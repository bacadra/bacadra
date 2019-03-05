'''
------------------------------------------------------------------------------
                      ***** (w)in(graf) postexe *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ____ import _____________________________________________________________ #

import os
import subprocess
import glob

from ..tools.setts import setts_init
from . import verrs

#$ ____ class setts ________________________________________________________ #

class setts(setts_init):

#$$ ________ def active ____________________________________________________ #

    def active(self, value=None, check=None, reset=None):
        return self.tools.gst('active', value, check, reset)

#$$ ________ def project ___________________________________________________ #

    def project(self, value=None, check=None, reset=None):
        # if self._self.core and not self.__project:
        #     return self._self.core.sofix.sbase.setts.project
        # else:
        #     return self.__project
        return self.tools.gst('project', value, check, reset)

#$$ ________ def cdb_name __________________________________________________ #

    def cdb_name(self, value=None, check=None, reset=None):
        # if self._self.core and not self.__cdb_name:
        #     return self._self.core.sofix.sbase.setts.cdb_name
        # else:
        #     return self.__cdb_name
        return self.tools.gst('cdb_name', value, check, reset)

#$$ ________ def gra_name __________________________________________________ #

    def gra_name(self, value=None, check=None, reset=None):
        # if self._self.core and not self.__cdb_name:
        #     return self._self.core.sofix.sbase.setts.cdb_name
        # else:
        #     return self.__cdb_name
        return self.tools.gst('gra_name', value, check, reset)

#$$ ________ def output __________________________________________________ #

    def output(self, value=None, check=None, reset=None):
        return self.tools.gst('output', value, check, reset)


#$$ ________ def watermark _________________________________________________ #

    def watermark(self, value=None, check=None, reset=None):
        return self.tools.gst('watermark', value, check, reset)

#$$ ________ def size ______________________________________________________ #

    def size(self, value=None, check=None, reset=None):

        if value in 'hvsa':
            value = {
                'h': [2023,1296,289,289],
                'v': [2033,2668,289,289],
                's': [2139,1266,229,242], # 18.00 x 10.50 [cm]
                'a': [2139,1000,229,242], # 18.00 x  8.50 [cm]
            }[value]

        elif value==None:
            size = self.tools.get('size')[:]
            size[3] += self.addtopline * 49
            value = '{}x{}+{}+{}'.format(size[0],size[1],size[2],size[3])

        return self.tools.gst('size', value, check, reset)

#$$ ________ def addtopline ________________________________________________ #

    def addtopline(self, value=None, check=None, reset=None):
        return self.tools.gst('addtopline', value, check, reset)

#$$ ________ def delete ____________________________________________________ #

    def delete(self, value=None, check=None, reset=None):
        return self.tools.gst('delete', value, check, reset)

#$ ____ class wgraf ________________________________________________________ #

class wgraf:

    setts = setts()
    setts.active(True)
    setts.project(r'.')
    setts.cdb_name('c_main.cdb')
    setts.gra_name('c_main.gra')
    setts.output(r'.')
    setts.watermark(True)
    setts.size('s')
    setts.addtopline(True)
    setts.delete(True)


#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, core=None, **kwargs):

        self.core = core

        self.setts = setts(self.setts, self)

        for key,val in kwargs:
            setattr(self.setts, key, val)


#$$ ________ def _check_cdb ________________________________________________ #

    def _check_cdb(self):
        path = os.path.join(self.setts.project(), self.setts.cdb_name())
        if not os.path.exists(path):
            raise ValueError()

#$$ ________ def _check_gra ________________________________________________ #

    def _check_gra(self):
        path = os.path.join(self.setts.project(), self.setts.gra_name())
        if not os.path.exists(path):
            raise ValueError()



#$$ ________ def _gra2plb __________________________________________________ #

    def _gra2plb(self):
        '''
        Run parser of wingraf file. The cdb name should be defined. Wingraf file and cdb files must be in same directory! This can be improve in sofistik.def file.
        '''

        # cmd command, first change the actual localisation, we use here pushd instead of cd, because push can change also drive letter. then run sofistik parser eg. sps or wps, send cdb name and name of wingraf
        code = 'cmd /c pushd "{p0}" & "{p1}" -cdb:"{p2}" "{p3}"'.format(**{
            'p0': os.path.abspath(self.setts.project()),
            'p1': os.path.join(
                self.core.sbase.setts.sofi_env(),
                self.core.sbase.setts.sofi_run()
                ).replace('/', '\\'),
            'p2': self.setts.cdb_name(),
            'p3': self.setts.gra_name()})
        subprocess.run(code)

#$$ ________ def _plb2pdf __________________________________________________ #

    def _plb2pdf(self):
        '''
        Convert sofistik report .plb to portable document format .pdf.
        '''

        # if sofistik 2016 is avaiable then use them, sofi16 has not problem with color print...

        se16 = self.core.sbase.setts.sofi_env('v2016', check=True)

        if os.path.exists(se16):
            sofi_loc = se16
        else:
            sofi_loc = self.core.sbase.setts.sofi_env()

        # create cmd command, first change folder to project, then use report browser (ursula) to convert report->pdf
        code = 'cmd /c pushd "{p0}" & "{p1}" "{p2}" -printto:"PDF" -picture:all'.format(**{
            'p0': os.path.abspath(self.setts.project()),
            'p1': os.path.join(
                sofi_loc,
                self.core.sbase.setts.sofi_urs()
                ).replace('/', '\\'),
            'p2': os.path.splitext(self.setts.gra_name())[0]+'.plb'})
        subprocess.run(code)


#$$ ________ def _del_old_jpg ______________________________________________ #

    def _del_old_jpg(self):
        '''
        Delete old image files of the same basename.
        '''

        if self.setts.delete():

            # create filename pattern
            filepattern = os.path.join(self.setts.output(), os.path.splitext(self.setts.gra_name())[0])+"-*.jpg"

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
        code = 'cmd /c pushd "{p0}" & "{p1}" -density 300 "{p2}" -quality 100 -scene 1 "{p3}-%03d.jpg"'.format(**{
            # change current dir to project folder
            'p0': os.path.abspath(self.setts.project()),
            # create path to ImageMagick execute file
            'p1': os.path.join(
                self.core.sbase.setts.magi_env(),
                self.core.sbase.setts.magi_mck()),
            # crete name of pdf file
            'p2': os.path.splitext(self.setts.gra_name())[0]+'.pdf',
            # create output base path
            'p3': os.path.join(os.path.abspath(self.setts.output()), os.path.splitext(self.setts.gra_name())[0])})

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
                'p1': os.path.join(
                    self.core.sbase.setts.magi_env(),
                    self.core.sbase.setts.magi_mck()),
                # create base file
                'p2': os.path.basename(file),
                # insert format file
                'p3': self.setts.size(),
                'wmark': wmark,
            })

            # run command!
            subprocess.run(code)





    def _run_one(self, active=None, project=None, cdb_name=None, gra_name=None, output=None, watermark=None, size=None, delete=None):

        othe = wgraf(self.core)

        othe.setts.set(
            active    = active    if active    else self.setts.active    (),
            project   = project   if project   else self.setts.project   (),
            cdb_name  = cdb_name  if cdb_name  else self.setts.cdb_name  (),
            gra_name  = gra_name  if gra_name  else self.setts.gra_name  (),
            output    = output    if output    else self.setts.output    (),
            watermark = watermark if watermark else self.setts.watermark (),
            size      = size      if size      else self.setts.size      (),
            delete    = delete    if delete    else self.setts.delete    (),
        )

        # if user want to overwrite global active atribute
        if not othe.setts.active(active, check=True): return

        # check that cdb exists
        othe._check_cdb()

        # check that gra exists
        othe._check_gra()

        # run sps with wingraf file
        othe._gra2plb()

        # convert .plb to .pdf
        othe._plb2pdf()

        # delete old images
        othe._del_old_jpg()

        # convert .pdf to .jpg
        othe._pdf2jpg()

        # convert jpg files
        othe._jpg_convert()



    def run(self, active=True, project=None, cdb_data=None, gra_data=None, output=None, watermark=None, delete=None):

        if not active: return

        active    = self.setts.check('active'   , active   )
        project   = self.setts.check('project'  , project  )
        output    = self.setts.check('output'   , output   )
        watermark = self.setts.check('watermark', watermark)
        delete    = self.setts.check('delete'   , delete   )


        verrs.BCDR_sofix_INFO_Rum()

        cdb_i = 0
        for cdb_row in cdb_data:
            # (name, active)
            cdb_name, active_1 = cdb_row

            cdb_i+=1; verrs.BCDR_sofix_INFO_General(('i0915', False),
                '{:>2s}'.format(str(cdb_i))+'.    Q:'+
                '{:5s}'.format(str(active_1))+', C: "'+cdb_name+'"')

            if not active_1: continue
            gra_i = 0
            for gra_row in gra_data:
                # (size, wingraf file name, active)
                size, gra_name, active_2 = gra_row

                gra_i+=1; verrs.BCDR_sofix_INFO_General(('i0915', False),
                    '  .{:<2s}'.format(str(gra_i))+'  Q:'+
                    '{:5s}'.format(str(active_2))+', W: "'+gra_name+'"')

                if not active_2: continue

                self._run_one(
                    active    = active_1 and active_2,
                    project   = project,
                    cdb_name  = cdb_name,
                    gra_name  = gra_name,
                    output    = output +'\\'+ cdb_name,
                    watermark = watermark,
                    size      = size,
                    delete    = delete,
                )

        verrs.BCDR_sofix_INFO_General(('i0915', False),'\nOperation <Wingraf-convert-mass> complete!')




        # if active:
        #     i=0
        #     for cdbi in cdb:
        #
        #         if type(cdbi)!=tuple or len(cdbi)!=2:
        #             raise ValueError('Len of cdb line must be equal to 2\nTip: first parameter describe name (or path), second is active bool')
        #
        #         i+=1; print(
        #             '{:<3s}'.format(str(i)+'.')+' Q:',
        #             '{:5s}'.format(str(cdbi[1]))+', "'+cdbi[0]+'"')
        #
        #         if sproj:
        #             path = os.path.join(sproj, cdbi[0])
        #
        #         output_path = os.path.join(output, os.path.basename(cdbi[0]))
        #
        #         wgraf.run(cdb=path, wdata=wdata, delete=delete, output=output_path, active=cdbi[1], watermark=watermark)
        #
        #     print('Operation <Wingraf-convert-mass> complete!')


