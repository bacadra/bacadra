from .linex import linex

#$ class index
class index:
    #$$ --init--
    def __init__(self, core):
        self.linex  = linex.linex(core=core)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass