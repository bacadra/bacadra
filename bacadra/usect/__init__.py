#$ class index
class index:
    #$$ --init--
    def __init__(self, core):
        from . import usec1
        from . import usec2
        from . import usec3

        self.usec1 = usec1.index(core=core)
        self.usec2 = usec2.index(core=core)
        self.usec3 = usec3.index(core=core)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass