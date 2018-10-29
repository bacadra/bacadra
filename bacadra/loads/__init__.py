from . import cates
from . import lcase
from . import nodes
from . import handy

#$ class index
class index:
    #$$ --init--
    def __init__(self, core):
        self.cates = cates.cates(core=core)
        self.lcase = lcase.lcase(core=core)
        self.nodes = nodes.nodes(core=core)
        self.handy = handy.handy(core=core)

    #$$ --enter--
    def __enter__(self):
        return self

    #$$ --exit--
    def __exit__(self, type, value, traceback):
        pass