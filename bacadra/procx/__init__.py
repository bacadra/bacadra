from . import static

#$ class navix
class navix:
    #$$ --init--
    def __init__(self, dbase, pinky, pvars):
        self.static = static.static(dbase, pinky, pvars)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass