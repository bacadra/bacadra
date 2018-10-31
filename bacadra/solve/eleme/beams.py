import numpy as np


class stiff:
    def __init__(self, core, prog):
        self.core = core
        self.prog = prog

        # run build
        self._build_K()


    #$$$ def -build-K
    def _build_K(self):
        '''
        Create stiffnes matrix of all truss elements.
        '''

        # get elements from database
        elements = self.core.dbase.get('''
        SELECT
            [BM].[id],
            [N1].[noG],
            [N2].[noG],
            [BM].[L],
            [BM].[ΔX],
            [BM].[ΔY],
            [BM].[ΔZ],
            [CS].[A],
            [CS].[I_t],
            [CS].[I_y],
            [CS].[I_z],
            [MT].[E_1],
            [MT].[G_1]
        FROM [131:beams:topos]      AS [BM]
        LEFT JOIN [111:nodes:optim] AS [N1] ON [BM].[n1]   = [N1].[id]
        LEFT JOIN [111:nodes:optim] AS [N2] ON [BM].[n2]   = [N2].[id]
        LEFT JOIN [021:usec1:value] AS [CS] ON [BM].[sect] = [CS].[id]
        LEFT JOIN [011:mates:umate] AS [MT] ON [CS].[mate] = [MT].[id]
        ''')

        # loop over elements
        for element in elements:
            # create local eye of matrix
            kg11,kg12,kg21,kg22 = self._k_loc_g(element)

            # unpack db data
            id,n1,n2 = element[:3]

            # assembly local matrix to global stif matrix
            self.prog._K_assembly(n1, n1,  kg11)
            self.prog._K_assembly(n1, n2,  kg12)
            self.prog._K_assembly(n2, n1,  kg21)
            self.prog._K_assembly(n2, n2,  kg22)


    #$$$ deg -k-loc-g
    def _k_loc_g(self, element):
        '''
        The method can build stifness in global coors or call to _k_loc and matrix dot cosinus matrix.
        '''
        # check system
        system_space = self.core.mdata.setts.get('system_space')

        # unpack element
        id,n1,n2,L,Δx,Δy,Δz,A,I_t,I_y,I_z,E_1,G_1 = element

        # if-block as system_space
        if system_space == '2t':
            raise ValueError('Element type error. The actual system does not provide rotational dof')

        elif system_space == '3t':
            raise ValueError('Element type error. The actual system does not provide rotational dof')

        elif system_space == '2d':
            # calculate sin,cos itd
            Cx,  Cz       = Δx/L   , Δz/L
            Cx2, Cz2, Cxz = Cx**2  , Cz**2 , Cx*Cz

            # calculate paramaeters for kg_local
            EAL  = (      E_1 * A   / L   )
            EIL3 = (12  * E_1 * I_y / L**3)
            EIL2 = (6   * E_1 * I_y / L**2)
            EIL1 = (4   * E_1 * I_y / L   )
            EIL0 = (2   * E_1 * I_y / L   )

            # create left upper part
            kg11 = np.array([
             [Cx2*EAL + Cz2*EIL3, Cxz*EAL - Cxz*EIL3, -Cz*EIL2],
             [Cxz*EAL - Cxz*EIL3, Cz2*EAL + Cx2*EIL3, Cx*EIL2],
             [-Cz*EIL2          , Cx*EIL2           , EIL1]
            ])

            # create right upper
            kg12 = np.array([
             [-Cx2*EAL - Cz2*EIL3, -Cxz*EAL + Cxz*EIL3, -Cz*EIL2],
             [-Cxz*EAL + Cxz*EIL3, -Cz2*EAL - Cx2*EIL3, Cx*EIL2],
             [Cz*EIL2            , -Cx*EIL2           , EIL0]
            ])

            kg21 = kg12.T

            # create right down part
            kg22 = np.array([
             [Cx2*EAL + Cz2*EIL3, Cxz*EAL - Cxz*EIL3, Cz*EIL2],
             [Cxz*EAL - Cxz*EIL3, Cz2*EAL + Cx2*EIL3, -Cx*EIL2],
             [Cz*EIL2           , -Cx*EIL2          , EIL1]
            ])



        # 3d-space
        elif system_space == '3d':
            # additional length of projected y-versor
            Lxy = (Δx**2+Δy**2)**0.5

            # calculate cos matrix, principles about local axis:
            # - local x axis is defined by start and end points.
            # - local z axis is downward, like grity
            # - local y axis is always horizontal, but the direction is vector
            #   product of x and z axis
            cxx = Δx/L
            cyx = Δy/L
            czx = Δz/L
            cxy = -Δy/Lxy
            cyy = Δx/Lxy
            czy = 0
            cxz = -Δx*Δz/(L*Lxy)
            cyz = -Δy*Δz/(L*Lxy)
            czz = (Δx**2)/(L*Lxy) + (Δy**2)/(L*Lxy)

            # calculate paramaeters for kg_local
            EAL  = ( E_1 * A   / L   )
            GKL  = ( G_1 * I_t / L   )

            EIY0 = ( 2* E_1 * I_y / L   )
            EIY1 = ( 4* E_1 * I_y / L   )
            EIY2 = ( 6* E_1 * I_y / L**2)
            EIY3 = (12* E_1 * I_y / L**3)

            EIZ0 = ( 2* E_1 * I_z / L   )
            EIZ1 = ( 4* E_1 * I_z / L   )
            EIZ2 = ( 6* E_1 * I_z / L**2)
            EIZ3 = (12* E_1 * I_z / L**3)

            def List(*vals):
                return [val for val in vals]

            # create left upper part
            kg11 = np.array(List(List(cxx**2*EAL + cxz**2*EIY3 +
              cxy**2*EIZ3,
             cxx*cyx*EAL + cxz*cyz*EIY3 +
              cxy*cyy*EIZ3,
             cxx*czx*EAL + cxz*czz*EIY3 +
              cxy*czy*EIZ3,
             cxy*cxz*EIY2 + cxy*cxz*EIZ2,
             cxz*cyy*EIY2 + cxy*cyz*EIZ2,
             cxz*czy*EIY2 + cxy*czz*EIZ2),
            List(cxx*cyx*EAL + cxz*cyz*EIY3 +
              cxy*cyy*EIZ3,
             cyx**2*EAL + cyz**2*EIY3 + cyy**2*EIZ3,
             cyx*czx*EAL + cyz*czz*EIY3 +
              cyy*czy*EIZ3,
             cxy*cyz*EIY2 + cxz*cyy*EIZ2,
             cyy*cyz*EIY2 + cyy*cyz*EIZ2,
             cyz*czy*EIY2 + cyy*czz*EIZ2),
            List(cxx*czx*EAL + cxz*czz*EIY3 +
              cxy*czy*EIZ3,
             cyx*czx*EAL + cyz*czz*EIY3 +
              cyy*czy*EIZ3,
             czx**2*EAL + czz**2*EIY3 + czy**2*EIZ3,
             cxy*czz*EIY2 + cxz*czy*EIZ2,
             cyy*czz*EIY2 + cyz*czy*EIZ2,
             czy*czz*EIY2 + czy*czz*EIZ2),
            List(cxy*cxz*EIY2 + cxy*cxz*EIZ2,
             cxy*cyz*EIY2 + cxz*cyy*EIZ2,
             cxy*czz*EIY2 + cxz*czy*EIZ2,
             cxy**2*EIY1 + cxz**2*EIZ1 + cxx**2*GKL,
             cxy*cyy*EIY1 + cxz*cyz*EIZ1 +
              cxx*cyx*GKL,
             cxy*czy*EIY1 + cxz*czz*EIZ1 +
              cxx*czx*GKL),
            List(cxz*cyy*EIY2 + cxy*cyz*EIZ2,
             cyy*cyz*EIY2 + cyy*cyz*EIZ2,
             cyy*czz*EIY2 + cyz*czy*EIZ2,
             cxy*cyy*EIY1 + cxz*cyz*EIZ1 +
              cxx*cyx*GKL,
             cyy**2*EIY1 + cyz**2*EIZ1 + cyx**2*GKL,
             cyy*czy*EIY1 + cyz*czz*EIZ1 +
              cyx*czx*GKL),
            List(cxz*czy*EIY2 + cxy*czz*EIZ2,
             cyz*czy*EIY2 + cyy*czz*EIZ2,
             czy*czz*EIY2 + czy*czz*EIZ2,
             cxy*czy*EIY1 + cxz*czz*EIZ1 +
              cxx*czx*GKL,
             cyy*czy*EIY1 + cyz*czz*EIZ1 +
              cyx*czx*GKL,
             czy**2*EIY1 + czz**2*EIZ1 + czx**2*GKL)))

            # create right upper
            kg12 = np.array(List(List(-(cxx**2*EAL) - cxz**2*EIY3 -
              cxy**2*EIZ3,
             -(cxx*cyx*EAL) - cxz*cyz*EIY3 -
              cxy*cyy*EIZ3,
             -(cxx*czx*EAL) - cxz*czz*EIY3 -
              cxy*czy*EIZ3,
             cxy*cxz*EIY2 + cxy*cxz*EIZ2,
             cxz*cyy*EIY2 + cxy*cyz*EIZ2,
             cxz*czy*EIY2 + cxy*czz*EIZ2),
            List(-(cxx*cyx*EAL) - cxz*cyz*EIY3 -
              cxy*cyy*EIZ3,
             -(cyx**2*EAL) - cyz**2*EIY3 -
              cyy**2*EIZ3,
             -(cyx*czx*EAL) - cyz*czz*EIY3 -
              cyy*czy*EIZ3,
             cxy*cyz*EIY2 + cxz*cyy*EIZ2,
             cyy*cyz*EIY2 + cyy*cyz*EIZ2,
             cyz*czy*EIY2 + cyy*czz*EIZ2),
            List(-(cxx*czx*EAL) - cxz*czz*EIY3 -
              cxy*czy*EIZ3,
             -(cyx*czx*EAL) - cyz*czz*EIY3 -
              cyy*czy*EIZ3,
             -(czx**2*EAL) - czz**2*EIY3 -
              czy**2*EIZ3,cxy*czz*EIY2 + cxz*czy*EIZ2,
             cyy*czz*EIY2 + cyz*czy*EIZ2,
             czy*czz*EIY2 + czy*czz*EIZ2),
            List(-(cxy*cxz*EIY2) - cxy*cxz*EIZ2,
             -(cxy*cyz*EIY2) - cxz*cyy*EIZ2,
             -(cxy*czz*EIY2) - cxz*czy*EIZ2,
             cxy**2*EIY0 + cxz**2*EIZ0 - cxx**2*GKL,
             cxy*cyy*EIY0 + cxz*cyz*EIZ0 -
              cxx*cyx*GKL,
             cxy*czy*EIY0 + cxz*czz*EIZ0 -
              cxx*czx*GKL),
            List(-(cxz*cyy*EIY2) - cxy*cyz*EIZ2,
             -(cyy*cyz*EIY2) - cyy*cyz*EIZ2,
             -(cyy*czz*EIY2) - cyz*czy*EIZ2,
             cxy*cyy*EIY0 + cxz*cyz*EIZ0 -
              cxx*cyx*GKL,
             cyy**2*EIY0 + cyz**2*EIZ0 - cyx**2*GKL,
             cyy*czy*EIY0 + cyz*czz*EIZ0 -
              cyx*czx*GKL),
            List(-(cxz*czy*EIY2) - cxy*czz*EIZ2,
             -(cyz*czy*EIY2) - cyy*czz*EIZ2,
             -(czy*czz*EIY2) - czy*czz*EIZ2,
             cxy*czy*EIY0 + cxz*czz*EIZ0 -
              cxx*czx*GKL,
             cyy*czy*EIY0 + cyz*czz*EIZ0 -
              cyx*czx*GKL,
             czy**2*EIY0 + czz**2*EIZ0 - czx**2*GKL)))

            # create right down part
            kg22 = np.array(List(List(cxx**2*EAL + cxz**2*EIY3 +
              cxy**2*EIZ3,
             cxx*cyx*EAL + cxz*cyz*EIY3 +
              cxy*cyy*EIZ3,
             cxx*czx*EAL + cxz*czz*EIY3 +
              cxy*czy*EIZ3,
             -(cxy*cxz*EIY2) - cxy*cxz*EIZ2,
             -(cxz*cyy*EIY2) - cxy*cyz*EIZ2,
             -(cxz*czy*EIY2) - cxy*czz*EIZ2),
            List(cxx*cyx*EAL + cxz*cyz*EIY3 +
              cxy*cyy*EIZ3,
             cyx**2*EAL + cyz**2*EIY3 + cyy**2*EIZ3,
             cyx*czx*EAL + cyz*czz*EIY3 +
              cyy*czy*EIZ3,
             -(cxy*cyz*EIY2) - cxz*cyy*EIZ2,
             -(cyy*cyz*EIY2) - cyy*cyz*EIZ2,
             -(cyz*czy*EIY2) - cyy*czz*EIZ2),
            List(cxx*czx*EAL + cxz*czz*EIY3 +
              cxy*czy*EIZ3,
             cyx*czx*EAL + cyz*czz*EIY3 +
              cyy*czy*EIZ3,
             czx**2*EAL + czz**2*EIY3 + czy**2*EIZ3,
             -(cxy*czz*EIY2) - cxz*czy*EIZ2,
             -(cyy*czz*EIY2) - cyz*czy*EIZ2,
             -(czy*czz*EIY2) - czy*czz*EIZ2),
            List(-(cxy*cxz*EIY2) - cxy*cxz*EIZ2,
             -(cxy*cyz*EIY2) - cxz*cyy*EIZ2,
             -(cxy*czz*EIY2) - cxz*czy*EIZ2,
             cxy**2*EIY1 + cxz**2*EIZ1 + cxx**2*GKL,
             cxy*cyy*EIY1 + cxz*cyz*EIZ1 +
              cxx*cyx*GKL,
             cxy*czy*EIY1 + cxz*czz*EIZ1 +
              cxx*czx*GKL),
            List(-(cxz*cyy*EIY2) - cxy*cyz*EIZ2,
             -(cyy*cyz*EIY2) - cyy*cyz*EIZ2,
             -(cyy*czz*EIY2) - cyz*czy*EIZ2,
             cxy*cyy*EIY1 + cxz*cyz*EIZ1 +
              cxx*cyx*GKL,
             cyy**2*EIY1 + cyz**2*EIZ1 + cyx**2*GKL,
             cyy*czy*EIY1 + cyz*czz*EIZ1 +
              cyx*czx*GKL),
            List(-(cxz*czy*EIY2) - cxy*czz*EIZ2,
             -(cyz*czy*EIY2) - cyy*czz*EIZ2,
             -(czy*czz*EIY2) - czy*czz*EIZ2,
             cxy*czy*EIY1 + cxz*czz*EIZ1 +
              cxx*czx*GKL,
             cyy*czy*EIY1 + cyz*czz*EIZ1 +
              cyx*czx*GKL,
             czy**2*EIY1 + czz**2*EIZ1 + czx**2*GKL)))

            kg21 = kg12.T

        return kg11,kg12,kg21,kg22



