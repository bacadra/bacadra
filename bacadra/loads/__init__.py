from ..tools.rootx import rootx

#$ class index
class index(rootx):
    #$$ --init--
    def __init__(self, core):
        from .ltree import cates
        from .ltree import lcase
        from .assig import nodes
        from .assig import handy

        self.cates = cates.cates(core=core)
        self.lcase = lcase.lcase(core=core)
        self.nodes = nodes.nodes(core=core)
        self.handy = handy.handy(core=core)