


#$ ____ class nodes ________________________________________________________ #

class nodes:
    #$$ def --init--
    def __init__(self, dbase, pinky, pvars):
        self.dbase = dbase
        self.pinky = pinky
        self.pvars = pvars

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    def add(self, lcase=None, node=None, px=None, py=None, pz=None, mx=None, my=None, mz=None, dx=None, dy=None, dz=None, rx=None, ry=None, rz=None, ttl=None):

        # if lcase is not defined then use lcase last one defined
        if lcase is None:
            lcase = self.pvars.get('_lcase_ldef')

        # parse data
        cols,data = self.dbase.parse(
            lcase = lcase,
            node  = node,
            px    = px,
            py    = py,
            pz    = pz,
            mx    = mx,
            my    = my,
            mz    = mz,
            dx    = dx,
            dy    = dy,
            dz    = dz,
            rx    = rx,
            ry    = ry,
            rz    = rz,
            ttl   = ttl,
        )

        # add data
        self.dbase.add(
            table = '[112:nodes:loads]',
            cols  = cols,
            data  = data,
        )