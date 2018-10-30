
#$ ____ class handy ________________________________________________________ #

class handy:
    #$$ def --init--
    def __init__(self, core):
        self.core = core

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    def add(self, lcase=None, usect=None, px=None, py=None, pz=None, mx=None, my=None, mz=None, dx=None, dy=None, dz=None, rx=None, ry=None, rz=None):

        A,B,C = self.core.dbase.parse(lcase=lcase, usect=usect, px=px, py=py, pz=pz, mx=mx, my=my, mz=mz, dx=dx, dy=dy, dz=dz, rx=rx, ry=ry, rz=rz)

        self.core.dbase.exe("INSERT INTO [102:loads:handy]" + A + " VALUES" + B ,C)
