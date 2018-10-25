import os
import subprocess
import glob


class simpl:
    sofi_e18 = r'c:\Program Files\SOFiSTiK\2018\SOFiSTiK 2018'
    sofi_e16 = r'c:\Program Files\SOFiSTiK\2016\ANALYSIS_33_X64'
    sofi_env = None
    sofi_wps = r'wps.exe'
    sofi_sps = r'sps.exe'
    sofi_urs = r'ursula.exe'
    magi_707 = r'c:\Program Files\ImageMagick-7.0.7-Q16'
    magi_env = magi_707
    magi_mck = r'magick.exe'
    size     = {'h':'2023x1296+289+289',
                'v':'2023x2668+289+289',
                's':'2139x1266+229+242'}

    @classmethod
    def jpg_watermark(self, name, copy=False):
        '''
        Convert graphic file, trim and delete watermark symbol.
        '''

        # loop over files adequete to file pattern
        for file in glob.glob(name):

            if copy:
                splitted = os.path.basename(file).split('.')
                name_out = splitted[0] + '_out.' + splitted[1]
            else:
                name_out = os.path.basename(file)

            # create cmd statment
            code = 'cmd /c pushd "{p0}" & "{p1}" "{p2}" -fuzz 25% -fill white -opaque "RGB(190,190,190)" "{p3}"'.format(**{
                # output path
                'p0': os.path.dirname(name),
                # create ImageMagick execute file path
                'p1': os.path.join(self.magi_env, self.magi_mck),
                # create base file
                'p2': os.path.basename(file),
                # output name
                'p3': name_out})

            # run command!
            subprocess.run(code)