import numpy as np

from .. import eleme

class stiff:
    #$$ def --init--
    def __init__(self, core, prog):
        self.core = core
        self.prog = prog # needed: _K, K11, K12, K21, K22, _ldof, _sdof

        # init stiffness matrix
        self.prog._K = np.zeros((self.prog._sdof, self.prog._sdof))

        # call method to different type of elements
        eleme.truss.stiff(core, self) # +truss
        eleme.beams.stiff(core, self) # +beams


    #$$$ def -K-assembly
    def _K_assembly(self, n1, n2, kg):
        '''
        You can apply element with n-nodes. All elements must be added one next one.
        '''

        ndof = len(self.prog._ldof)

        # assembly local matrix to global stif matrix
        self.prog._K[
            n1*ndof:n1*ndof+ndof,
            n2*ndof:n2*ndof+ndof,
        ] += kg
