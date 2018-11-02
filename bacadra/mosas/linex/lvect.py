import numpy as np

from .. import eleme

class lvect:
    #$$ def --init--
    def __init__(self, core, prog, lcase):
        self.core = core
        self.prog = prog

        # init 1d vector for loads and imposed displacement
        # 1d vector is not horizontal and not vertical, just 1d
        # we can multiply array * 1d vector and we get 1d vector (only if cols count of matrix and element count in vector is the same)
        self.prog._F = np.zeros(self.prog._sdof)
        self.prog._D = np.zeros(self.prog._sdof)

        # call method to different type of elements
        eleme.nodes.lvect(core, self, lcase) # +nodal loads

    #$$$ def -F-assembly
    def _F_assembly(self, n1, index, F):
        '''
        You can apply load or discplacement to dof. All elements of F in one node must be added separatly.
        '''

        ndof = len(self.prog._ldof)
        n1add = self.prog._ldof.index(index)

        # assembly local matrix to global stif matrix
        self.prog._F[n1*ndof+n1add] += F

    #$$$ def -F-assembly
    def _D_assembly(self, n1, index, D):
        '''
        You can apply load or discplacement to dof. All elements of D in one node must be added separatly.
        '''

        ndof = len(self.prog._ldof)
        n1add = self.prog._ldof.index(index)

        # assembly local matrix to global stif matrix
        self.prog._D[n1*ndof+n1add] += D