import numpy as np

from .. import eleme

class stiff:
    def __init__(self, othe):
        # module must have atributes:
        # _K, K11, K12, K21, K22, _ldof, _sdof
        self._prog = othe

        # init stiffness matrix
        self._prog._K = np.zeros((self._prog._sdof, self._prog._sdof))

        # call method to different type of elements
        eleme.truss.stiff(self) # +truss


    #$$$ def -K-assembly
    def _K_assembly(self, n1, n2, kg):
        '''
        You can apply element with n-nodes.
        '''

        ndof = len(self._prog._ldof)

        # assembly local matrix to global stif matrix
        self._prog._K[
            n1*ndof:n1*ndof+ndof,
            n2*ndof:n2*ndof+ndof
        ] += kg
