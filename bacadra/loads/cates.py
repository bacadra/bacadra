
# import setts

#$ ____ class cates ________________________________________________________ #

class cates:
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

    def add(self, id=None, gamu=None, gamf=None, gama=None, gam1=None, gam2=None, gam3=None, psi0=None, psi1=None,psi1s=None,psi2=None, ttl=None):

        # overwrite last defined category
        self.pvars.set({'_cates_ldef':id})

        # parse data
        cols,data = self.dbase.parse(
            id    = id,
            gamu  = gamu,
            gamf  = gamf,
            gama  = gama,
            gam1  = gam1,
            gam2  = gam2,
            gam3  = gam3,
            psi0  = psi0,
            psi1  = psi1,
            psi1s = psi1s,
            psi2  = psi2,
            ttl   = ttl,
        )

        # add data
        self.dbase.add(
            table = '[051:loads:cates]',
            cols  = cols,
            data  = data,
        )