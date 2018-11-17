'''
------------------------------------------------------------------------------
BCDR += ***** SOFiSTiK (tools) *****
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

class tools:
    sbase = sbase()

    def watermark(self, name, output='pic-fix', copy=False, echo=True):
        '''
        Convert graphic file, trim and delete watermark symbol.
        '''

        # if output folder does not exists, then create it
        if not os.path.isdir(os.path.abspath(output)):
            os.makedirs(output)

        i = 0
        # loop over files adequete to file pattern
        for file in glob.glob(name):
            i+=1
            if copy:
                splitted = os.path.basename(file).split('.')
                name_out = splitted[0] + '_out.' + splitted[1]
            else:
                name_out = os.path.basename(file)

            name_out = os.path.abspath(os.path.join(output, name_out))

            # create cmd statment
            code = 'cmd /c pushd "{p0}" & "{p1}" "{p2}" -fuzz 25% -fill white -opaque "RGB(190,190,190)" "{p3}"'.format(**{
                # output path
                'p0': os.path.dirname(name),
                # create ImageMagick execute file path
                'p1': os.path.join(self.sbase._magi_env, self.sbase._magi_mck),
                # create base file
                'p2': os.path.basename(file),
                # output name
                'p3': name_out})

            # run command!
            subprocess.run(code)

            if echo:
                print(f'in [{i}]:',os.path.abspath(file))
                print(f'out[{i}]:',name_out)


    def pdf2jpg(self, pdf_path, jpg_output='pdf2jpg', format_name='{name}-%03d.jpg', delete_pdf=False, echo=True, delete_old_jpg=True):
        '''
        Explode multipage pdf to single page graphics .jpg.
        '''

        # if output folder does not exists, then create it
        if not os.path.isdir(os.path.abspath(jpg_output)):
            os.makedirs(jpg_output)
        elif delete_old_jpg:
            # create filename pattern
            filepattern = os.path.join(jpg_output, os.path.splitext(pdf_path)[0])+"-*.jpg"

            # loop over files adequete to filepattern
            for file in glob.glob(filepattern):

                # remove file
                os.remove(file)

        i = 0
        for pdf in glob.glob(pdf_path):
            i += 1
            # create cmd statment
            code = 'cmd /c pushd "{p0}" & "{p1}" -density 300 "{p2}" -quality 100 -scene 1 "{pattern}"'.replace(
                '{pattern}', format_name,
                ).format(**{
                # change current dir to project folder
                'p0': os.path.abspath(os.path.dirname(pdf)),
                # create path to ImageMagick execute file
                'p1': os.path.join(self.sbase._magi_env, self.sbase._magi_mck),
                # crete name of pdf file
                'p2': os.path.basename(pdf),
                # create output base path
                'name': os.path.join(os.path.abspath(jpg_output), os.path.splitext(os.path.basename(pdf))[0])})

            # run code in cmd!
            subprocess.run(code)

            if echo:
                print(f'in [{i}]:',os.path.abspath(pdf))
                print(f'out[{i}]:',os.path.join(os.path.abspath(jpg_output), os.path.splitext(os.path.basename(pdf))[0])+format_name.replace('{name}',''))

            if delete_pdf:
                os.remove(pdf)

