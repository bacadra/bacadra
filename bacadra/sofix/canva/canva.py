import os
import platform
import string
import ctypes
from ctypes import c_int

from . import sofistik_daten

class canva:

    def __establish_data(self, educational):
        # Check the python platform (32bit or 64bit)
        sofPlatform = str(platform.architecture())

        # get path from system variables
        path = os.environ['Path']

        # Get the dlls (32bit or 64bit dll)
        if sofPlatform.find('32Bit') < 0:

            # folder path of dll files
            dllPath1 = 'C:\\Program Files\\SOFiSTiK\\2018\\SOFiSTiK 2018\\interfaces\\64bit'

            if educational:
                self.dll_filename = 'cdb_w_edu50_x64'
            else:
                self.dll_filename = 'cdb_w50_x64.dll'

        else:
            # folder path of dll files
            dllPath1 = 'C:\\Program Files\\SOFiSTiK\\2018\\SOFiSTiK 2018\\interfaces\\32bit'

            if educational:
                self.dll_filename = 'cdb_w31_edu.dll'
            else:
                self.dll_filename = 'cdb_w31.dll'

        # other necessary dlls
        dllPath2 = 'C:\\Program Files\\SOFiSTiK\\2018\\SOFiSTiK 2018'

        # extend system variables
        os.environ['Path'] = dllPath1 + ';' + dllPath2 + ';' + path

        # Get the dll functions
        self.myDLL = ctypes.cdll.LoadLibrary(self.dll_filename)


    def py_sof_cdb_get(self):
        py_sof_cdb_get = ctypes.cdll.LoadLibrary(self.dll_filename).sof_cdb_get
        py_sof_cdb_get.restype = c_int
        return py_sof_cdb_get


    def py_sof_cdb_kenq(self):
        py_sof_cdb_kenq = ctypes.cdll.LoadLibrary(self.dll_filename).sof_cdb_kenq_ex
        return py_sof_cdb_kenq


    def connect(self, path, educational=True):
        self.__establish_data(educational)

        # Connect to CDB
        Index = c_int()

        cdbIndex = 99

        # important: Unicode call!
        Index.value = self.myDLL.sof_cdb_init(path.encode('ascii'), cdbIndex)

        # get the CDB status
        cdbStat = c_int()

        cdbStat.value = self.myDLL.sof_cdb_status(Index.value)

        # Print the Status of the CDB
        print ('CDB Status:', cdbStat.value)


    def close(self):

        Index = c_int()

        # get the CDB status
        cdbStat = c_int()

        cdbStat.value = self.myDLL.sof_cdb_status(Index.value)

        # Close the CDB, 0 - will close all the files
        self.myDLL.sof_cdb_close(0)

        # Print again the status of the CDB, if status = 0 -> CDB Closed successfully
        cdbStat.value = self.myDLL.sof_cdb_status(Index.value)

        if cdbStat.value == 0:
            print ('CDB closed successfully, status = 0')




    def read_nodes(self):
        pos = c_int(0)
        datalen = c_int(0)

        a = c_int()
        ie = c_int(0)
        datalen.value = sizeof(CNODE)
        RecLen = c_int(sizeof(cnode))