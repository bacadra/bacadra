from . import dxcad


#$ class index
class index:
    #$$ __init__
    def __init__(self, core):
        self.dxcad = dxcad.dxcad(core=core)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass