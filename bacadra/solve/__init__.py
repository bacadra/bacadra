from .statx import statx

#$ class index
class index:
    #$$ --init--
    def __init__(self, core):
        self.statx  = statx.statx(core=core)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass