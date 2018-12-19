import numpy as np

from .. import eleme

class postr:
    #$$ def __init__
    def __init__(self, core, prog, lcase):
        self.core = core
        self.prog = prog

        # call method to different type of elements
        eleme.truss.postr(core, self, lcase) # +truss post-processing
        eleme.beams.postr(core, self, lcase) # +beams post-processing
