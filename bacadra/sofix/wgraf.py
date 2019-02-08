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

from ..tools.setts import settsmeta
from . import verrs

#$ ____ class setts ________________________________________________________ #

class setts(settsmeta):

#$$ ________ def active ____________________________________________________ #

    __active = True

    @property
    def active(self):
            return self.__active

    @active.setter
    def active(self, value):
        '''
        User can deactive all methods, then methods will exit at the begging.
        '''

        if type(value) is not bool:
            verrs.BCDR_pinky_texme_ERROR_Type_Check(type(value), 'bool')

        if self.__save__: self.__active = value
        else:             self.__temp__ = value

#$$ ________ def project ___________________________________________________ #

    __project = None

    @property
    def project(self):
        if self._self.core and not self.__project:
            return self._self.core.sbase.setts.project
        else:
            return self.__project

    @project.setter
    def project(self, value):
        if self.__save__: self.__project = value
        else:             self.__temp__ = value


#$$ ________ def cdb_name __________________________________________________ #

    __cdb_name = None

    @property
    def cdb_name(self):
        if self._self.core and not self.__cdb_name:
            return self._self.core.sbase.setts.cdb_name
        else:
            return self.__cdb_name

    @cdb_name.setter
    def cdb_name(self, value):

        if self.__save__: self.__cdb_name = value
        else:             self.__temp__ = value

#$$ ________ def gra_name __________________________________________________ #

    __gra_name = None

    @property
    def gra_name(self):
        return self.__gra_name

    @gra_name.setter
    def gra_name(self, value):

        if self.__save__: self.__gra_name = value
        else:             self.__temp__ = value


#$$ ________ def output ____________________________________________________ #

    __output = None

    @property
    def output(self):
        return self.__output

    @output.setter
    def output(self, value):

        if self.__save__: self.__output = value
        else:             self.__temp__ = value


#$$ ________ def watermark _________________________________________________ #

    __watermark = True

    @property
    def watermark(self):
        return self.__watermark

    @watermark.setter
    def watermark(self, value):

        if self.__save__: self.__watermark = value
        else:             self.__temp__ = value



#$$ ________ def size ______________________________________________________ #

    __size = None

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):

        if value in 'hvsa':
            value = {
                'h':'2023x1296+289+289',
                'v':'2023x2668+289+289',
                's':'2139x1266+229+242', # 18.00 x 10.50 [cm]
                'a':'2139x1000+229+242', # 18.00 x  8.50 [cm]
            }[value]

        if self.__save__: self.__size = value
        else:             self.__temp__ = value



#$$ ________ def delete ____________________________________________________ #

    __delete = True

    @property
    def delete(self):
        return self.__delete

    @delete.setter
    def delete(self, value):

        if self.__save__: self.__delete = value
        else:             self.__temp__ = value


#$ ____ class wgraf ________________________________________________________ #

class wgraf:

    # class setts
    setts = setts('setts', (setts,), {})

#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, core=None, **kwargs):

        self.core = core

        # object setts
        self.setts = self.setts('setts',(),{'_self':self})

        for key,val in kwargs:
            setattr(self.setts, key, val)


#$$ ________ def _check_cdb ________________________________________________ #

    def _check_cdb(self):
        path = os.path.join(self.setts.project, self.setts.cdb_name)
        if not os.path.exists(path):
            raise ValueError()

#$$ ________ def _check_gra ________________________________________________ #

    def _check_gra(self):
        path = os.path.join(self.setts.project, self.setts.gra_name)
        if not os.path.exists(path):
            raise ValueError()



#$$ ________ def _gra2plb __________________________________________________ #

    def _gra2plb(self):
        '''
        Run parser of wingraf file. The cdb name should be defined. Wingraf file and cdb files must be in same directory! This can be improve in sofistik.def file.
        '''

        # cmd command, first change the actual localisation, we use here pushd instead of cd, because push can change also drive letter. then run sofistik parser eg. sps or wps, send cdb name and name of wingraf
        code = 'cmd /c pushd "{p0}" & "{p1}" -cdb:"{p2}" "{p3}"'.format(**{
            'p0': os.path.abspath(self.setts.project),
            'p1': os.path.join(
                self.core.sbase.setts.sofi_env,
                self.core.sbase.setts.sofi_run
                ).replace('/', '\\'),
            'p2': self.setts.cdb_name,
            'p3': self.setts.gra_name})
        subprocess.run(code)

#$$ ________ def _plb2pdf __________________________________________________ #

    def _plb2pdf(self):
        '''
        Convert sofistik report .plb to portable document format .pdf.
        '''

        # if sofistik 2016 is avaiable then use them, sofi16 has not problem with color print...

        se16 = self.core.sbase.setts.check('sofi_env', 'v2016')

        if os.path.exists(se16):
            sofi_loc = se16
        else:
            sofi_loc = self.core.sbase.setts.sofi_env

        # create cmd command, first change folder to project, then use report browser (ursula) to convert report->pdf
        code = 'cmd /c pushd "{p0}" & "{p1}" "{p2}" -printto:"PDF" -picture:all'.format(**{
            'p0': os.path.abspath(self.setts.project),
            'p1': os.path.join(
                sofi_loc,
                self.core.sbase.setts.sofi_urs
                ).replace('/', '\\'),
            'p2': os.path.splitext(self.setts.gra_name)[0]+'.plb'})
        subprocess.run(code)


#$$ ________ def _del_old_jpg ______________________________________________ #

    def _del_old_jpg(self):
        '''
        Delete old image files of the same basename.
        '''

        if self.setts.delete:

            # create filename pattern
            filepattern = os.path.join(self.setts.output, os.path.splitext(self.setts.gra_name)[0])+"-*.jpg"

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
        if not os.path.isdir(os.path.abspath(self.setts.output)):
            os.makedirs(self.setts.output)

        # create cmd statment
        code = 'cmd /c pushd "{p0}" & "{p1}" -density 300 "{p2}" -quality 100 -scene 1 "{p3}-%03d.jpg"'.format(**{
            # change current dir to project folder
            'p0': os.path.abspath(self.setts.project),
            # create path to ImageMagick execute file
            'p1': os.path.join(
                self.core.sbase.setts.magi_env,
                self.core.sbase.setts.magi_mck),
            # crete name of pdf file
            'p2': os.path.splitext(self.setts.gra_name)[0]+'.pdf',
            # create output base path
            'p3': os.path.join(os.path.abspath(self.setts.output), os.path.splitext(self.setts.gra_name)[0])})

        # run code in cmd!
        subprocess.run(code)


#$$ ________ def _jpg_convert ______________________________________________ #

    def _jpg_convert(self):
        '''
        Convert graphic file, trim and delete watermark symbol.
        '''

        # create jpg list as special symbol pattern
        filepattern = os.path.join(
            self.setts.output,
            os.path.splitext(self.setts.gra_name)[0])+"-*.jpg"

        # loop over files adequete to file pattern
        for file in glob.glob(filepattern):

            if self.setts.watermark is True:
                wmark = '-fuzz 15% -fill white -opaque "RGB(192,192,192)"'
            else:
                wmark = ''

            # create cmd statment
            code = 'cmd /c pushd "{p0}" & "{p1}" "{p2}" -crop {p3} {wmark} "{p2}"'.format(**{
                # output path
                'p0': self.setts.output,
                # create ImageMagick execute file path
                'p1': os.path.join(
                    self.core.sbase.setts.magi_env,
                    self.core.sbase.setts.magi_mck),
                # create base file
                'p2': os.path.basename(file),
                # insert format file
                'p3': self.setts.size,
                'wmark': wmark,
            })

            # run command!
            subprocess.run(code)





    def run(self, active=None, project=None, cdb_name=None, gra_name=None, output=None, watermark=None, size=None, delete=None):

        self.setts.set(
            active    = active,
            project   = project,
            cdb_name  = cdb_name,
            gra_name  = gra_name,
            output    = output,
            watermark = watermark,
            size      = size,
            delete    = delete,
        )

        # if user want to overwrite global active atribute
        if not self.setts.check('active', active): return

        # check that cdb exists
        self._check_cdb()

        # check that gra exists
        self._check_gra()

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



    def rum(self, active=True, project=None, cdb_data=None, gra_data=None, output=None, watermark=None, delete=None):

        if not active: return

        verrs.BCDR_sofix_INFO_Rum()

        cdb_i = 0
        for cdb_row in cdb_data:
            # (name, active)
            cdb_name, active_1 = cdb_row

            cdb_i+=1; verrs.BCDR_sofix_INFO_General(('i0915', False),
                '{:>2s}'.format(str(cdb_i))+'.    Q:'+
                '{:5s}'.format(str(active_1))+', F: "'+cdb_name+'"')

            if not active_1: continue
            gra_i = 0
            for gra_row in gra_data:
                # (size, wingraf file name, active)
                size, gra_name, active_2 = gra_row

                gra_i+=1; verrs.BCDR_sofix_INFO_General(('i0915', False),
                    '  .{:<2s}'.format(str(gra_i))+'  Q:'+
                    '{:5s}'.format(str(active_2))+', F: "'+gra_name+'"')

                if not active_2: continue

                self.run(
                    active    = active_1 and active_2,
                    project   = project,
                    cdb_name  = cdb_name,
                    gra_name  = gra_name,
                    output    = output,
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


