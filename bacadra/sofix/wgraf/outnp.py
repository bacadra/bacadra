import os

from . import out1p

class outnp:
    def __init__(self, output, cdb, wdata, delete=True, active=True):
        self.active = active
        self.output = output
        self.cdb = cdb
        self.wdata = wdata
        self.delete = delete

        self._start_system()

    def _start_system(self):
        if self.active:
            for cdb in self.cdb:

                output_path = os.path.join(self.output, os.path.basename(cdb[1]))

                out1p(cdb=cdb[1], wdata=self.wdata, delete=self.delete, output=output_path, active=cdb[0])
