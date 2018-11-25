'''
------------------------------------------------------------------------------
BCDR += ***** (S)OFiSTiK data(base) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

# import os
# import ctypes
# from ctypes import c_int
#
# from . import rdbse

import os
import platform
import ctypes
import copy

from ctypes import c_int

from . import rdbse
from . import verrs


class sbase:

    def __init__(self):
        pass

    def path(self):
        self.sofi_env()
        self.sofi_run()
        self.sofi_urs()
        self.magi_env()
        self.magi_mck()

    @classmethod
    def sofi_env(self, path='v2018', inherit=False):
        '''
        Create self._sofi_env atribute.
        '''

        if path=='v2018':
            _sofi_env = r'c:\Program Files\SOFiSTiK\2018\SOFiSTiK 2018'
        elif path=='v2016':
            _sofi_env = r'c:\Program Files\SOFiSTiK\2016\ANALYSIS_33_X64'
        elif path:
            _sofi_env = path

        if not os.path.exists(_sofi_env):
            verrs.envcheckBCDRsofixError(_sofi_env)

        if inherit:
            return _sofi_env
        else:
            self._sofi_env = _sofi_env


    @classmethod
    def sofi_run(self, path='sps'):
        '''
        Create self._sofi_run atribute.
        '''

        if path=='wps':
            self._sofi_run = r'wps.exe'
        elif path=='sps':
            self._sofi_run = r'sps.exe'
        else:
            self._sofi_run = path
        os.path.exists(os.path.join(self._sofi_env, self._sofi_run))
        return self._sofi_run

    @classmethod
    def sofi_urs(self, path=None):
        '''
        Create self._sofi_urs atribute.
        '''

        if path is None:
            self._sofi_urs  = r'ursula.exe'
        else:
            self._sofi_urs  = path
        os.path.exists(os.path.join(self._sofi_env, self._sofi_urs))
        return self._sofi_urs

    @classmethod
    def sofi_dll(self, ver_edu=True):
        '''
        Create self._sofi_dll atribute and self.sof_cdb_get(..) & self.sof_cdb_kenq(..) functions.
        '''

        sofPlatform = str(platform.architecture())

        if sofPlatform.find('32Bit') < 0:

            dllPath = os.path.join(self._sofi_env, r'interfaces\64bit') + ';' + self._sofi_env

            if ver_edu:
                dll_fn = 'cdb_w_edu50_x64.dll'
            else:
                dll_fn = 'cdb_w50_x64.dll'

        else:

            dllPath = os.path.join(self._sofi_env, r'interfaces\32bit')

            if ver_edu:
                dll_fn = 'cdb_w31_edu.dll'
            else:
                dll_fn = 'cdb_w31.dll'

        # extend system variables
        os.environ['Path'] = dllPath + ';' + os.environ["Path"]

        # Get the dll functions
        self._sofi_dll = ctypes.cdll.LoadLibrary(dll_fn)

        # self.sof_cdb_get = self._sofi_dll.sof_cdb_get
        # self.sof_cdb_get.restype = c_int

        # self.sof_cdb_kenq = self._sofi_dll.sof_cdb_kenq_ex


    @classmethod
    def magi_env(self, path='v7.0.7-Q16'):
        '''
        Create self._magi_env atribute.
        '''

        if path=='v7.0.7-Q16':
            self._magi_env = r'c:\Program Files\ImageMagick-7.0.7-Q16'
        else:
            self._magi_env = path
        os.path.exists(self._magi_env)

    @classmethod
    def magi_mck(self, path=None):
        '''
        Create self._magi_mck atribute.
        '''

        if path is None:
            self._magi_mck = r'magick.exe'
        else:
            self._magi_mck = path
        os.path.exists(os.path.join(self._magi_env, self._magi_mck))

    def connect(self, path, ver_edu=True, cdbIndex=99):
        '''
        The database FileName will be opened and accessible via Index. It becomes the active database. This function has to be called before any other activity is allowed. It will create a scratch database during the first call.

        FileName      is the complete filename including extension
                      conforming to the rules of the hosting
                      operating system.

        Index = 0     initialise CDBASE and open scratch data base only
        Index > 0     open an existing data base with exactly tis index
                      (STATUS=UNKNOWN) = somehow obsolete call, use 99!
        Index = 99    test if NAME is a valid database and open the base
                      if possible. Return with the assigned index.
                      If the file does not exist, it will be created.
        Index = 97    open the database via pvm
                      Return with the assigned index.
        Index = 96    open a scratch database, filename is the path to
                      use or NULL.
        Index = 95    open in read-only mode
        Index = 94    create a new data base (STATUS=NEW)

        Returnvalue:  Index for further access
                     (<0 if error, see clib1.h for meaning of error codes)
                     ( 0 if not a database when called with Index = 99)
        '''
        self.sofi_dll(ver_edu=ver_edu)

        self._sofi_icdb = self._sofi_dll.sof_cdb_init(path.encode('ascii'), cdbIndex)


    def close(self):
        '''
        The database is physicaly closed. (Index = 0 for all files)
        '''

        self._sofi_dll.sof_cdb_close(0)
        self._sofi_icdb = None

    def status(self):
        '''
        The current status of the file with Index is returned.

        Index       Index of DB
        Returnvalue Stat Bitpattern
            CD_STAT_AKTIV   (1) CDBase is active
            CD_STAT_OPEN    (2) Index is connected to file
            CD_STAT_SWAP    (4) File has ByteSwap
            CD_STAT_READ    (8) File has been read
            CD_STAT_WRITE  (16) File has been written
            CD_STAT_LOCK   (32) File has active locks
            CD_STAT_PVM    (64) File is opened via pvm server

        If called with ( index = -1 ), than the Returnvalue will be the
        index of the active database. If the system is not yet opened, a
        value of -1 is returned.
        '''

        status = self._sofi_dll.sof_cdb_status(self._sofi_icdb)

        if status <= 0:
            print('Database is closed, status:',status)
        else:
            print('System is opened, status:',status)


    def get(self, kwh=None, kwl=None, data=None, preset=None, pos=1, convert=True):
        '''
        A record is read from the active database or the read pointer is set to a specific position (seek). Only keys with their directory in memory will be found. To get access to the actual complete set of keys call sof_cdb_flush before.

        With the first reading a lock will be set to this key which is released after reaching the end of the key.

          icdb            index of database
          kwh / kwl       key ( 0/0 is not allowed )
          Data            Starting address of the data
          RecLen          max. length for Data in Bytes
                          will be overwritten with the actual Length of the
                          item (may be shorter or longer)
                          = 0 setting only the pointer for the next read
          Pos             Position indicator
                          < 0 Position Pos Positions before current read
                              pointer ( -1 = the last record again).
                              if Reclen>0 the read pointer will be
                              restored to the current position
                          = 0 Position to first Item (REWIND)
                          > 0 Read next item from current read pointer
                              read pointer will advance by one item.
          Returnvalue     Errorcondition
                            CD_ERR_NONE       (0) no error
                            CD_ERR_TOOLONG    (1) Item is longer than Data
                            CD_ERR_DATAEND    (2) End of file reached
                            CD_ERR_NOTFOUND   (3) key does not exist
        '''

        if preset:
            if preset == 'nodes':
                if not kwh : kwh  = 20
                if not kwl : kwl  = 0
                if not data: data = rdbse.cnode
            elif preset == 'sect':
                if not kwh : kwh  = 9
                if not kwl : kwl  = 0
                if not data: data = rdbse.csect
            elif preset == 'beams':
                if not kwh : kwh  = 100
                if not kwl : kwl  = 0
                if not data: data = rdbse.cbeam
            elif preset == 'nodes_results':
                if not kwh : kwh  = 24
                # kwl: here kwl mind loadcase number, so user must input it
                if not data: data = rdbse.cn_dispc
            elif preset == 'beam_forces':
                if not kwh : kwh  = 102
                if not data: data = rdbse.cbeam_foc
            elif preset == 'sto':
                if not kwh : kwh  = 0
                if not kwl : kwl  = 100
                if not data: data = rdbse.cctrl_var

            elif type(data) == str:
                exec(f'data = rdbse.{data}')
            else:
                raise ValueError('Unknow preset settings')

        output = []

        ie = 0
        RecLen = c_int(ctypes.sizeof(data))
        if self._sofi_dll.sof_cdb_kexist(kwh, kwl) == 2: # the key exists and contains data
            while ie < 2:
                ie = self._sofi_dll.sof_cdb_get(self._sofi_icdb, kwh, kwl, ctypes.byref(data), ctypes.byref(RecLen), pos)
                if convert:
                    data_out = copy.deepcopy(data).convert()
                else:
                    data_out = copy.deepcopy(data)
                output += [data_out]
                RecLen = c_int(ctypes.sizeof(data))
        else:
            output = None

        return output

    #
    # size      = {'h':'2023x1296+289+289',
    #             'v':'2023x2668+289+289',
    #             's':'2139x1266+229+242'}