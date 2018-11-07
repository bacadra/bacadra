from ..tools.rootx import rootx

#$ class index
class index(rootx):
    def __init__(self, dbase):
        from . import setts
        self.setts = setts.setts(dbase)

        from . import annex
        self.annex = annex.annex(dbase)