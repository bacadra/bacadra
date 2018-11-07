from ...tools.rootx import rootx

#$ class index
class index(rootx):
    #$$ --init--
    def __init__(self, core):
        from . import value
        from . import tsect
        from . import thinw
        from .sprof import sprof

        self.value = value.value(core=core)
        self.tsect = tsect.tsect(core=core)
        self.thinw = thinw.thinw(core=core)
        self.sprof = sprof.sprof(core=core)