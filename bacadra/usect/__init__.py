from . import usec1
from . import usec2
from . import usec3

#$ class index
class index:
    #$$ --init--
    def __init__(self, core):
        self.usec1 = usec1.index(core=core)
        self.usec2 = usec1.index(core=core)
        self.usec3 = usec1.index(core=core)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass