'''
------------------------------------------------------------------------------
BCDR += ***** (w)in(graf) postexe *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

import os
import subprocess
import glob

from . import sbase
from . import verrs

class wgraf1:
    sbase = sbase()

    size     = {'h':'2023x1296+289+289',
                'v':'2023x2668+289+289',
                's':'2139x1266+229+242'}

    def __init__(self, cdb, wdata, delete=True, output='.', active=False, watermark=True):
        self.active = active
        self.cdb    = cdb
        self.wdata  = wdata
            # wdata[0] active state: True or False
            # wdata[1] paper type, eg. 's'
            # wdata[2] wingraf name
        self.output = output
        self.delete = delete
        self.watermark = watermark

        # start system while class object defined
        self._start_system()


    def _check_gra(self, path):
        path = os.path.join(os.path.dirname(self.cdb), path)
        if not os.path.exists(path):
            raise verrs.gracheckBCDRsofixError(str(os.path.abspath(path)))

    def _gra2plb(self, name):
        '''
        Run parser of wingraf file. The cdb name should be defined. Wingraf file and cdb files must be in same directory! This can be improve in sofistik.def file.
        '''

        # cmd command, first change the actual localisation, we use here pushd instead of cd, because push can change also drive letter. then run sofistik parser eg. sps or wps, send cdb name and name of wingraf
        code = 'cmd /c pushd "{p0}" & "{p1}" -cdb:"{p2}" "{p3}"'.format(**{
            'p0': os.path.abspath(os.path.dirname(self.cdb)),
            'p1': os.path.join(self.sbase.sofi_env(), self.sbase.sofi_run()).replace('/', '\\'),
            'p2': os.path.basename(self.cdb),
            'p3': name})
        subprocess.run(code)


    def _plb2pdf(self, name):
        '''
        Convert sofistik report .plb to portable document format .pdf.
        '''

        # if sofistik 2016 is avaiable then use them, sofi16 has not problem with color print...
        se16 = r'c:\Program Files\SOFiSTiK\2016\ANALYSIS_33_X64'
        if os.path.exists(se16):
            sofi_loc = se16
        else:
            sofi_loc = self.sbase.sofi_env()

        # create cmd command, first change folder to project, then use report browser (ursula) to convert report->pdf
        code = 'cmd /c pushd "{p0}" & "{p1}" "{p2}" -printto:"PDF" -picture:all'.format(**{
            'p0': os.path.abspath(os.path.dirname(self.cdb)),
            'p1': os.path.join(sofi_loc, self.sbase.sofi_urs()).replace('/', '\\'),
            'p2': os.path.splitext(name)[0]+'.plb'})
        subprocess.run(code)


    def _pdf2jpg(self, name):
        '''
        Explode multipage pdf to single page graphics .jpg.
        '''

        # if output folder does not exists, then create it
        if not os.path.isdir(os.path.abspath(self.output)):
            os.makedirs(self.output)

        # create cmd statment
        code = 'cmd /c pushd "{p0}" & "{p1}" -density 300 "{p2}" -quality 100 -scene 1 "{p3}-%03d.jpg"'.format(**{
            # change current dir to project folder
            'p0': os.path.abspath(os.path.dirname(self.cdb)),
            # create path to ImageMagick execute file
            'p1': os.path.join(self.sbase.magi_env(), self.sbase.magi_mck()),
            # crete name of pdf file
            'p2': os.path.splitext(name)[0]+'.pdf',
            # create output base path
            'p3': os.path.join(os.path.abspath(self.output), os.path.splitext(name)[0])})

        # run code in cmd!
        subprocess.run(code)


    def _jpg_convert(self, name, size):
        '''
        Convert graphic file, trim and delete watermark symbol.
        '''

        # convert size symbol lowercase
        size = size.lower()

        # if-case size format already defined then use them, othercase raise error with size dict
        if size in self.size:
            trim_dim = self.size[size]
        else:
            raise ValueError('Undefined graphic size, current size list: '+str(self.size))

        # create jpg list as special symbol pattern
        filepattern = os.path.join(self.output, os.path.splitext(name)[0])+"-*.jpg"

        # loop over files adequete to file pattern
        for file in glob.glob(filepattern):

            if self.watermark is True:
                wmark = '-fuzz 15% -fill white -opaque "RGB(192,192,192)"'
            else:
                wmark = ''

            # create cmd statment
            code = 'cmd /c pushd "{p0}" & "{p1}" "{p2}" -crop {p3} {wmark} "{p2}"'.format(**{
                # output path
                'p0': self.output,
                # create ImageMagick execute file path
                'p1': os.path.join(self.sbase.magi_env(), self.sbase.magi_mck()),
                # create base file
                'p2': os.path.basename(file),
                # insert format file
                'p3': trim_dim,
                'wmark': wmark,
            })

            # run command!
            subprocess.run(code)


    def _del_old_jpg(self, name):
        '''
        Delete old image files of the same basename.
        '''

        # create filename pattern
        filepattern = os.path.join(self.output, os.path.splitext(name)[0])+"-*.jpg"

        # loop over files adequete to filepattern
        for file in glob.glob(filepattern):

            # remove file
            os.remove(file)


    def _start_system(self):
        if self.active:
            # check that cdb exists
            if not os.path.exists(self.cdb):
                raise verrs.BCDRsofixError(str(os.path.abspath(self.cdb)))

            # loop over wdata (active, format, wingraf file name)
            for data in self.wdata:

                # if active is true
                if data[0]:

                    # check that gra exists
                    self._check_gra(data[2])

                    # run sps with wingraf file
                    self._gra2plb(data[2])

                    # convert .plb to .pdf
                    self._plb2pdf(data[2])

                    # delete old images
                    if self.delete:
                        self._del_old_jpg(data[2])

                    # convert .pdf to .jpg
                    self._pdf2jpg(data[2])

                    # convert jpg files
                    self._jpg_convert(data[2], data[1])



class wgraf:
    def __init__(self, output, cdb, wdata, delete=True, active=True, watermark=True):
        self.active = active
        self.output = output
        self.cdb    = cdb
        self.wdata  = wdata
        self.delete = delete
        self.watermark=watermark

        self._start_system()

    def _start_system(self):
        if self.active:
            i=0
            for cdb in self.cdb:
                i+=1
                print(i,'. ',cdb)

                output_path = os.path.join(self.output, os.path.basename(cdb[1]))

                wgraf1(cdb=cdb[1], wdata=self.wdata, delete=self.delete, output=output_path, active=cdb[0], watermark=self.watermark)
