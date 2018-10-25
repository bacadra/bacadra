from . import unics

#$ class navix
class navix:
    #$$ --init--
    def __init__(self, dbase, pinky, pvars):
        self.unics = unics.unics(dbase, pinky, pvars)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass
