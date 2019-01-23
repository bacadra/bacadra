'''
------------------------------------------------------------------------------
BCDR += ***** ArcerolMittal_V2018_1 (catalog) *****
==============================================================================
http://sections.arcelormittal.com/products-services/products-ranges.html

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

import os
import openpyxl
import subprocess

rootdir = os.path.dirname(os.path.realpath(__file__))

class catalog:
    #$$ def __init__
    def __init__(self, core, value):
        self.core = core
        self._value = value
        self.catalog = 'ArcelorMittal_V2018-1.xlsx'


    def add(self, id=None, mate=None, family=None, name=None, ttl=None):

        family = family.lower()
        name   = name.lower()

        if family == 'beams':
            self._beams(name=name, id=id, mate=mate, ttl=ttl)

        elif family == 'angles':
            self._angles(name=name, id=id, mate=mate, ttl=ttl)

        elif family == 'channels':
            self._channels(name=name, id=id, mate=mate, ttl=ttl)


    def open(self):
        subprocess.Popen(
            ['cmd', '/C', 'start',
            os.path.join(rootdir, self.catalog)]
        )


    def _search(self, name, sheet):
        # create abs path to base file
        path = os.path.join(rootdir, self.catalog)

        # open workbook
        # read_only flags allow to open relly big files
        # with constant memeory consuption
        excl_workbook = openpyxl.load_workbook(path, read_only=True)

        # open needed sheet
        excl_beams = excl_workbook[sheet]

        # loop over sheet and search for looked name
        export = None
        for row in excl_beams.rows:
            # if name is searched
            if row[1].value == name.upper():
                # then return full name, list compre to unpack value
                return [cell.value for cell in row]

        if export is None:
            raise ValueError('Section name is not finded')


    def _beams(self, name, id, mate, ttl):
        # call to search method
        data = self._search(name, 'Beams')

        # parse universal units section 1d data
        self._value.add(
            id     = id,
            mate   = mate,
            A      = data[10]*1e-6,
            A_z    = data[22]*1e-6,
            I_t    = data[28]*1e-12,
            I_ω    = data[29]*1e-15,
            I_y    = data[18]*1e-12,
            I_z    = data[23]*1e-12,
            I_ξ    = data[18]*1e-12,
            I_η    = data[23]*1e-12,
            u      = data[16],
            ttl    = (data[1] if ttl is None else ttl),
            _subcl = 'sprof',
        )


    def _angles(self, name, id, mate, ttl):
        # call to search method
        data = self._search(name, 'Angles')

        # parse universal units section 1d data
        self._value.add(
            id     = id,
            mate   = mate,
            A      = data[10]*1e-6,
            A_z    = data[23]*1e-6,
            I_y    = data[17]*1e-12,
            I_z    = data[17]*1e-12,
            I_ξ    = data[20]*1e-12,
            I_η    = data[22]*1e-12,
            u      = data[15],
            ttl    = (data[1] if ttl is None else ttl),
            _subcl = 'sprof',
        )


    def _channels(self, name, id, mate, ttl):
        # call to search method
        data = self._search(name, 'Channels')

        # parse universal units section 1d data
        self._value.add(
            id     = id,
            mate   = mate,
            A      = data[11]*1e-6,
            I_t    = data[29]*1e-12,
            I_ω    = data[29]*1e-18,
            I_y    = data[19]*1e-12,
            I_z    = data[24]*1e-12,
            I_ξ    = data[19]*1e-12,
            I_η    = data[24]*1e-12,
            u      = data[17],
            ttl    = (data[1] if ttl is None else ttl),
            _subcl = 'sprof',
        )