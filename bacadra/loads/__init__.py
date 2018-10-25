from . import cates
from . import lcase
from . import nodes
from . import handy

#$ class navix
class navix:
    #$$ --init--
    def __init__(self, dbase, pinky, pvars):
        self.cates = cates.cates(dbase, pinky, pvars)
        self.lcase = lcase.lcase(dbase, pinky, pvars)
        self.nodes = nodes.nodes(dbase, pinky, pvars)
        self.handy = handy.handy(dbase, pinky, pvars)

    #$$ --enter--
    def __enter__(self):
        return self

    #$$ --exit--
    def __exit__(self, type, value, traceback):
        pass