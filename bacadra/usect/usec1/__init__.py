from . import value

#$ class index
class index:
    #$$ --init--
    def __init__(self, core):
        self.value = value.value(core=core)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass
