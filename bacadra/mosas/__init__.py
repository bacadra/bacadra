from ..tools.rootx import rootx

#$ class index
class index(rootx):
    #$$ --init--
    def __init__(self, core):
        from .linex import linex

        self.linex  = linex.linex(core=core)