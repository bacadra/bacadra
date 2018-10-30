import numpy as np

from . import space
from . import stiff
from . import bound
from . import lvect
from . import verrs
from . import staqr
from . import postr

np.set_printoptions(suppress=True)

#$ ____ class linex ________________________________________________________ #

class linex:
    #$$ def --init--
    def __init__(self, core):
        self.core = core

        self._ldof = []   # list of named dofs in one node
        self._sdof = None # summary dof in system
        self._cdof = []   # list of constrained dof

        self._K    = None # stiffness matrix full
        self._K11  = None # stiffness matrix part
        self._K12  = None # stiffness matrix part
        self._K21  = None # stiffness matrix part
        self._K22  = None # stiffness matrix part

        self._F    = None # F1 - load vector as force
        self._R    = None # F2 - reaction in support
        self._Q    = None # Q1 - displacement vector
        self._D    = None # Q2 - imposed displamenet


    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass


#$$ ________ interface _____________________________________________________ #

    #$$$ def build
    def build(self, grp=None):
        # create space & system
        space.space(self)

        # build stiffness matrix without bc
        stiff.stiff(self.core, self)

        # apply boundary condition to system
        bound.bound(self.core, self).stiff()

    def solve(self, lcase):
        # check if system is crated
        if self._K is None:
            verrs.f3SolveStatxSystemError()

        # set the complete vector
        lvect.lvect(self.core, self, lcase)

        # boundary condition on load vector
        bound.bound(self.core, self).lvect()

        # solve system
        staqr.staqr(self.core, self, lcase)

        # basis post-process
        postr.postr(self.core, self, lcase)

