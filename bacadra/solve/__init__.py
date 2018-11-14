from ..tools.rootx import rootx

#$ class index
class index(rootx):
    #$$ --init--
    def __init__(self, core):
        from . import genea
        self.genea = genea.genea(core=core)