from . import dxfin


#$ class navix
class navix:
    #$$ --init--
    def __init__(self, dbase, pinky, pvars):
        self.dxfin = dxfin.dxfin(dbase, pinky, pvars)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass