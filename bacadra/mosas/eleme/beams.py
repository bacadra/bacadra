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


            # def sign(value):
            #     if value >= 0:
            #         return 1
            #     else:
            #         return -1
            #
            # cxx = Δx/L
            # cxz = Δz/L
            # czx = -Δz*sign(Δx)/L
            # czz = Δx*sign(Δx)/L
            #
            # # calculate paramaeters for kg_local
            # EAL  = (      E_1 * A   / L   )
            # EIL3 = (12  * E_1 * I_y / L**3)
            # EIL2 = (6   * E_1 * I_y / L**2)
            # EIL1 = (4   * E_1 * I_y / L   )
            # EIL0 = (2   * E_1 * I_y / L   )
            #
            # def List(*vals):
            #     return [val for val in vals]
            #
            # kg11 = np.array(List(
            # List(cxx**2*EAL + cxz**2*EIL3,
            #  cxx*czx*EAL + cxz*czz*EIL3,cxz*EIL2),
            # List(cxx*czx*EAL + cxz*czz*EIL3,
            #  czx**2*EAL + czz**2*EIL3,czz*EIL2),
            # List(cxz*EIL2,czz*EIL2,EIL1)))
            #
            # kg12 = np.array(List(
            # List(-(cxx**2*EAL) - cxz**2*EIL3,
            #  -(cxx*czx*EAL) - cxz*czz*EIL3,cxz*EIL2),
            # List(-(cxx*czx*EAL) - cxz*czz*EIL3,
            #  -(czx**2*EAL) - czz**2*EIL3,czz*EIL2),
            # List(-(cxz*EIL2),-(czz*EIL2),EIL0)))
            #
            # kg21 = kg12.T
            #
            # kg22 = np.array(List(
            # List(cxx**2*EAL + cxz**2*EIL3,
            #  cxx*czx*EAL + cxz*czz*EIL3,-(cxz*EIL2)),
            # List(cxx*czx*EAL + cxz*czz*EIL3,
            #  czx**2*EAL + czz**2*EIL3,-(czz*EIL2)),
            # List(-(cxz*EIL2),-(czz*EIL2),EIL1)))



        # 3d-space
        elif system_space == '3d':
            # additional length of projected y-versor
            # Lxy = (Δx**2+Δy**2)**0.5
            #
            # # calculate cos matrix, principles about local axis:
            # # - local x axis is defined by start and end points.
            # # - local z axis is downward, like grity
            # # - local y axis is always horizontal, but the direction is vector
            # #   product of x and z axis
            # cxx = Δx/L
            # cyx = Δy/L
            # czx = Δz/L
            # cxy = -Δy/Lxy
            # cyy = Δx/Lxy
            # czy = 0
            # cxz = -Δx*Δz/(L*Lxy)
            # cyz = -Δy*Δz/(L*Lxy)
            # czz = (Δx**2)/(L*Lxy) + (Δy**2)/(L*Lxy)
            #
            # # calculate paramaeters for kg_local
            # EAL  = ( E_1 * A   / L   )
            # GKL  = ( G_1 * I_t / L   )
            #
            # EIY0 = ( 2* E_1 * I_y / L   )
            # EIY1 = ( 4* E_1 * I_y / L   )
            # EIY2 = ( 6* E_1 * I_y / L**2)
            # EIY3 = (12* E_1 * I_y / L**3)
            #
            # EIZ0 = ( 2* E_1 * I_z / L   )
            # EIZ1 = ( 4* E_1 * I_z / L   )
            # EIZ2 = ( 6* E_1 * I_z / L**2)
            # EIZ3 = (12* E_1 * I_z / L**3)
            #
            # def List(*vals):
            #     return [val for val in vals]
            #
            # # create left upper part
            # kg11 = np.array(List(
            # List(cxx**2*EAL + cxz**2*EIY3 +  cxy**2*EIZ3, cxx*cyx*EAL + cxz*cyz*EIY3 +  cxy*cyy*EIZ3, cxx*czx*EAL + cxz*czz*EIY3 +  cxy*czy*EIZ3, cxy*cxz*EIY2 + cxy*cxz*EIZ2, cxz*cyy*EIY2 + cxy*cyz*EIZ2, cxz*czy*EIY2 + cxy*czz*EIZ2),
            # List(cxx*cyx*EAL + cxz*cyz*EIY3 +  cxy*cyy*EIZ3, cyx**2*EAL + cyz**2*EIY3 + cyy**2*EIZ3, cyx*czx*EAL + cyz*czz*EIY3 +  cyy*czy*EIZ3, cxy*cyz*EIY2 + cxz*cyy*EIZ2, cyy*cyz*EIY2 + cyy*cyz*EIZ2, cyz*czy*EIY2 + cyy*czz*EIZ2),
            # List(cxx*czx*EAL + cxz*czz*EIY3 + cxy*czy*EIZ3,cyx*czx*EAL + cyz*czz*EIY3 + cyy*czy*EIZ3,czx**2*EAL + czz**2*EIY3 + czy**2*EIZ3,cxy*czz*EIY2 + cxz*czy*EIZ2,cyy*czz*EIY2 + cyz*czy*EIZ2,czy*czz*EIY2 + czy*czz*EIZ2),
            # List(cxy*cxz*EIY2 + cxy*cxz*EIZ2, cxy*cyz*EIY2 + cxz*cyy*EIZ2, cxy*czz*EIY2 + cxz*czy*EIZ2, cxy**2*EIY1 + cxz**2*EIZ1 + cxx**2*GKL, cxy*cyy*EIY1 + cxz*cyz*EIZ1 +  cxx*cyx*GKL, cxy*czy*EIY1 + cxz*czz*EIZ1 +  cxx*czx*GKL),
            # List(cxz*cyy*EIY2 + cxy*cyz*EIZ2, cyy*cyz*EIY2 + cyy*cyz*EIZ2, cyy*czz*EIY2 + cyz*czy*EIZ2, cxy*cyy*EIY1 + cxz*cyz*EIZ1 +  cxx*cyx*GKL, cyy**2*EIY1 + cyz**2*EIZ1 + cyx**2*GKL, cyy*czy*EIY1 + cyz*czz*EIZ1 +  cyx*czx*GKL),
            # List(cxz*czy*EIY2 + cxy*czz*EIZ2, cyz*czy*EIY2 + cyy*czz*EIZ2, czy*czz*EIY2 + czy*czz*EIZ2, cxy*czy*EIY1 + cxz*czz*EIZ1 +  cxx*czx*GKL, cyy*czy*EIY1 + cyz*czz*EIZ1 +  cyx*czx*GKL, czy**2*EIY1 + czz**2*EIZ1 + czx**2*GKL)))
            #
            # # create right upper
            # kg12 = np.array(List(
            # List(-(cxx**2*EAL) - cxz**2*EIY3 - cxy**2*EIZ3,-(cxx*cyx*EAL) - cxz*cyz*EIY3 - cxy*cyy*EIZ3,-(cxx*czx*EAL) - cxz*czz*EIY3 - cxy*czy*EIZ3,cxy*cxz*EIY2 + cxy*cxz*EIZ2,cxz*cyy*EIY2 + cxy*cyz*EIZ2,cxz*czy*EIY2 + cxy*czz*EIZ2),
            # List(-(cxx*cyx*EAL) - cxz*cyz*EIY3 - cxy*cyy*EIZ3,-(cyx**2*EAL) - cyz**2*EIY3 - cyy**2*EIZ3,-(cyx*czx*EAL) - cyz*czz*EIY3 - cyy*czy*EIZ3,cxy*cyz*EIY2 + cxz*cyy*EIZ2,cyy*cyz*EIY2 + cyy*cyz*EIZ2,cyz*czy*EIY2 + cyy*czz*EIZ2),
            # List(-(cxx*czx*EAL) - cxz*czz*EIY3 - cxy*czy*EIZ3,-(cyx*czx*EAL) - cyz*czz*EIY3 - cyy*czy*EIZ3,-(czx**2*EAL) - czz**2*EIY3 - czy**2*EIZ3,cxy*czz*EIY2 + cxz*czy*EIZ2,cyy*czz*EIY2 + cyz*czy*EIZ2,czy*czz*EIY2 + czy*czz*EIZ2),
            # List(-(cxy*cxz*EIY2) - cxy*cxz*EIZ2, -(cxy*cyz*EIY2) - cxz*cyy*EIZ2, -(cxy*czz*EIY2) - cxz*czy*EIZ2, cxy**2*EIY0 + cxz**2*EIZ0 - cxx**2*GKL, cxy*cyy*EIY0 + cxz*cyz*EIZ0 -  cxx*cyx*GKL, cxy*czy*EIY0 + cxz*czz*EIZ0 -  cxx*czx*GKL),
            # List(-(cxz*cyy*EIY2) - cxy*cyz*EIZ2, -(cyy*cyz*EIY2) - cyy*cyz*EIZ2, -(cyy*czz*EIY2) - cyz*czy*EIZ2, cxy*cyy*EIY0 + cxz*cyz*EIZ0 -  cxx*cyx*GKL, cyy**2*EIY0 + cyz**2*EIZ0 - cyx**2*GKL, cyy*czy*EIY0 + cyz*czz*EIZ0 -  cyx*czx*GKL),
            # List(-(cxz*czy*EIY2) - cxy*czz*EIZ2, -(cyz*czy*EIY2) - cyy*czz*EIZ2, -(czy*czz*EIY2) - czy*czz*EIZ2, cxy*czy*EIY0 + cxz*czz*EIZ0 -  cxx*czx*GKL, cyy*czy*EIY0 + cyz*czz*EIZ0 -  cyx*czx*GKL, czy**2*EIY0 + czz**2*EIZ0 - czx**2*GKL)))
            #
            # # create left down part
            # kg21 = kg12.T
            #
            # # create right down part
            # kg22 = np.array(List(
            # List(cxx**2*EAL + cxz**2*EIY3 +  cxy**2*EIZ3, cxx*cyx*EAL + cxz*cyz*EIY3 +  cxy*cyy*EIZ3, cxx*czx*EAL + cxz*czz*EIY3 +  cxy*czy*EIZ3, -(cxy*cxz*EIY2) - cxy*cxz*EIZ2, -(cxz*cyy*EIY2) - cxy*cyz*EIZ2, -(cxz*czy*EIY2) - cxy*czz*EIZ2),
            # List(cxx*cyx*EAL + cxz*cyz*EIY3 + cxy*cyy*EIZ3,cyx**2*EAL + cyz**2*EIY3 + cyy**2*EIZ3,cyx*czx*EAL + cyz*czz*EIY3 + cyy*czy*EIZ3,-(cxy*cyz*EIY2) - cxz*cyy*EIZ2,-(cyy*cyz*EIY2) - cyy*cyz*EIZ2,-(cyz*czy*EIY2) - cyy*czz*EIZ2),
            # List(cxx*czx*EAL + cxz*czz*EIY3 + cxy*czy*EIZ3,cyx*czx*EAL + cyz*czz*EIY3 + cyy*czy*EIZ3,czx**2*EAL + czz**2*EIY3 + czy**2*EIZ3,-(cxy*czz*EIY2) - cxz*czy*EIZ2,-(cyy*czz*EIY2) - cyz*czy*EIZ2,-(czy*czz*EIY2) - czy*czz*EIZ2),
            # List(-(cxy*cxz*EIY2) - cxy*cxz*EIZ2, -(cxy*cyz*EIY2) - cxz*cyy*EIZ2, -(cxy*czz*EIY2) - cxz*czy*EIZ2, cxy**2*EIY1 + cxz**2*EIZ1 + cxx**2*GKL, cxy*cyy*EIY1 + cxz*cyz*EIZ1 +  cxx*cyx*GKL, cxy*czy*EIY1 + cxz*czz*EIZ1 +  cxx*czx*GKL),
            # List(-(cxz*cyy*EIY2) - cxy*cyz*EIZ2, -(cyy*cyz*EIY2) - cyy*cyz*EIZ2, -(cyy*czz*EIY2) - cyz*czy*EIZ2, cxy*cyy*EIY1 + cxz*cyz*EIZ1 +  cxx*cyx*GKL, cyy**2*EIY1 + cyz**2*EIZ1 + cyx**2*GKL, cyy*czy*EIY1 + cyz*czz*EIZ1 +  cyx*czx*GKL),
            # List(-(cxz*czy*EIY2) - cxy*czz*EIZ2, -(cyz*czy*EIY2) - cyy*czz*EIZ2, -(czy*czz*EIY2) - czy*czz*EIZ2, cxy*czy*EIY1 + cxz*czz*EIZ1 +  cxx*czx*GKL, cyy*czy*EIY1 + cyz*czz*EIZ1 +  cyx*czx*GKL, czy**2*EIY1 + czz**2*EIZ1 + czx**2*GKL)))
















            # # additional length of projected y-versor
            # Lxy = (Δx**2+Δy**2)**0.5
            #
            # # calculate cos matrix, principles about local axis:
            # # - local x axis is defined by start and end points.
            # # - local z axis is downward, like grity
            # # - local y axis is always horizontal, but the direction is vector
            # #   product of x and z axis
            # cxx = Δx/L
            # cyx = Δy/L
            # czx = Δz/L
            # cxy = -Δy/Lxy
            # cyy = Δx/Lxy
            # czy = 0
            # cxz = -Δx*Δz/(L*Lxy)
            # cyz = -Δy*Δz/(L*Lxy)
            # czz = (Δx**2)/(L*Lxy) + (Δy**2)/(L*Lxy)













            # X21 = Δx
            # Y21 = Δy
            # Z21 = Δz
            #
            # X31 = 0
            # Y31 = 1
            # Z31 = 0
            #
            # A123 = (
            #     (Y21*Z31 - Y31*Z21)**2 +
            #     (Z21*X31 - Z31*X21)**2 +
            #     (X21*Y31 - X31*Y21)**2
            # )**0.5
            #
            #
            # cxx = X21/L
            # cyx = Y21/L
            # czx = Z21/L
            #
            # cxz = (Y21*Z31 - Y31*Z21)/(2*A123)
            # cyz = (Z21*X31 - Z31*X21)/(2*A123)
            # czz = (X21*Y31 - X31*Y21)/(2*A123)
            #
            # cxy = cyz*czx - czz*cyx
            # cyy = czz*cxx - cxz*czx
            # czy = cxz*cyx - cyz*cxx

            #
            # cxx,cyx,czx,cxy,cyy,czy,cxz,cyz,czz =
            #
            #
            #
            #
            #
            #
            #
            #
            #
            #
            #
            #
            #
            # # calculate paramaeters for kg_local
            # EAL  = ( E_1 * A   / L   )
            # GKL  = ( G_1 * I_t / L   )
            #
            # EIY3 = (12* E_1 * I_y / L**3)
            # EIY2 = ( 6* E_1 * I_y / L**2)
            # EIY1 = ( 4* E_1 * I_y / L   )
            # EIY0 = ( 2* E_1 * I_y / L   )
            #
            # EIZ3 = (12* E_1 * I_z / L**3)
            # EIZ2 = ( 6* E_1 * I_z / L**2)
            # EIZ1 = ( 4* E_1 * I_z / L   )
            # EIZ0 = ( 2* E_1 * I_z / L   )
            #
            # def List(*vals):
            #     return [val for val in vals]
            #
            #
            #
            # # create left upper part
            # kg11 = np.array(List(
            # List(cxx**2*EAL + cxz**2*EIY3 +  cxy**2*EIZ3, cxx*cyx*EAL + cxz*cyz*EIY3 +  cxy*cyy*EIZ3, cxx*czx*EAL + cxz*czz*EIY3 +  cxy*czy*EIZ3, cxy*cxz*EIY2 + cxy*cxz*EIZ2, cxz*cyy*EIY2 + cxy*cyz*EIZ2, cxz*czy*EIY2 + cxy*czz*EIZ2),
            # List(cxx*cyx*EAL + cxz*cyz*EIY3 +  cxy*cyy*EIZ3, cyx**2*EAL + cyz**2*EIY3 + cyy**2*EIZ3, cyx*czx*EAL + cyz*czz*EIY3 +  cyy*czy*EIZ3, cxy*cyz*EIY2 + cxz*cyy*EIZ2, cyy*cyz*EIY2 + cyy*cyz*EIZ2, cyz*czy*EIY2 + cyy*czz*EIZ2),
            # List(cxx*czx*EAL + cxz*czz*EIY3 + cxy*czy*EIZ3,cyx*czx*EAL + cyz*czz*EIY3 + cyy*czy*EIZ3,czx**2*EAL + czz**2*EIY3 + czy**2*EIZ3,cxy*czz*EIY2 + cxz*czy*EIZ2,cyy*czz*EIY2 + cyz*czy*EIZ2,czy*czz*EIY2 + czy*czz*EIZ2),
            # List(cxy*cxz*EIY2 + cxy*cxz*EIZ2, cxy*cyz*EIY2 + cxz*cyy*EIZ2, cxy*czz*EIY2 + cxz*czy*EIZ2, cxy**2*EIY1 + cxz**2*EIZ1 + cxx**2*GKL, cxy*cyy*EIY1 + cxz*cyz*EIZ1 +  cxx*cyx*GKL, cxy*czy*EIY1 + cxz*czz*EIZ1 +  cxx*czx*GKL),
            # List(cxz*cyy*EIY2 + cxy*cyz*EIZ2, cyy*cyz*EIY2 + cyy*cyz*EIZ2, cyy*czz*EIY2 + cyz*czy*EIZ2, cxy*cyy*EIY1 + cxz*cyz*EIZ1 +  cxx*cyx*GKL, cyy**2*EIY1 + cyz**2*EIZ1 + cyx**2*GKL, cyy*czy*EIY1 + cyz*czz*EIZ1 +  cyx*czx*GKL),
            # List(cxz*czy*EIY2 + cxy*czz*EIZ2, cyz*czy*EIY2 + cyy*czz*EIZ2, czy*czz*EIY2 + czy*czz*EIZ2, cxy*czy*EIY1 + cxz*czz*EIZ1 +  cxx*czx*GKL, cyy*czy*EIY1 + cyz*czz*EIZ1 +  cyx*czx*GKL, czy**2*EIY1 + czz**2*EIZ1 + czx**2*GKL)))
            #
            # # create right upper
            # kg12 = np.array(List(
            # List(-(cxx**2*EAL) - cxz**2*EIY3 - cxy**2*EIZ3,-(cxx*cyx*EAL) - cxz*cyz*EIY3 - cxy*cyy*EIZ3,-(cxx*czx*EAL) - cxz*czz*EIY3 - cxy*czy*EIZ3,cxy*cxz*EIY2 + cxy*cxz*EIZ2,cxz*cyy*EIY2 + cxy*cyz*EIZ2,cxz*czy*EIY2 + cxy*czz*EIZ2),
            # List(-(cxx*cyx*EAL) - cxz*cyz*EIY3 - cxy*cyy*EIZ3,-(cyx**2*EAL) - cyz**2*EIY3 - cyy**2*EIZ3,-(cyx*czx*EAL) - cyz*czz*EIY3 - cyy*czy*EIZ3,cxy*cyz*EIY2 + cxz*cyy*EIZ2,cyy*cyz*EIY2 + cyy*cyz*EIZ2,cyz*czy*EIY2 + cyy*czz*EIZ2),
            # List(-(cxx*czx*EAL) - cxz*czz*EIY3 - cxy*czy*EIZ3,-(cyx*czx*EAL) - cyz*czz*EIY3 - cyy*czy*EIZ3,-(czx**2*EAL) - czz**2*EIY3 - czy**2*EIZ3,cxy*czz*EIY2 + cxz*czy*EIZ2,cyy*czz*EIY2 + cyz*czy*EIZ2,czy*czz*EIY2 + czy*czz*EIZ2),
            # List(-(cxy*cxz*EIY2) - cxy*cxz*EIZ2, -(cxy*cyz*EIY2) - cxz*cyy*EIZ2, -(cxy*czz*EIY2) - cxz*czy*EIZ2, cxy**2*EIY0 + cxz**2*EIZ0 - cxx**2*GKL, cxy*cyy*EIY0 + cxz*cyz*EIZ0 -  cxx*cyx*GKL, cxy*czy*EIY0 + cxz*czz*EIZ0 -  cxx*czx*GKL),
            # List(-(cxz*cyy*EIY2) - cxy*cyz*EIZ2, -(cyy*cyz*EIY2) - cyy*cyz*EIZ2, -(cyy*czz*EIY2) - cyz*czy*EIZ2, cxy*cyy*EIY0 + cxz*cyz*EIZ0 -  cxx*cyx*GKL, cyy**2*EIY0 + cyz**2*EIZ0 - cyx**2*GKL, cyy*czy*EIY0 + cyz*czz*EIZ0 -  cyx*czx*GKL),
            # List(-(cxz*czy*EIY2) - cxy*czz*EIZ2, -(cyz*czy*EIY2) - cyy*czz*EIZ2, -(czy*czz*EIY2) - czy*czz*EIZ2, cxy*czy*EIY0 + cxz*czz*EIZ0 -  cxx*czx*GKL, cyy*czy*EIY0 + cyz*czz*EIZ0 -  cyx*czx*GKL, czy**2*EIY0 + czz**2*EIZ0 - czx**2*GKL)))
            #
            # # create left down part
            # kg21 = kg12.T
            #
            # # create right down part
            # kg22 = np.array(List(
            # List(cxx**2*EAL + cxz**2*EIY3 +  cxy**2*EIZ3, cxx*cyx*EAL + cxz*cyz*EIY3 +  cxy*cyy*EIZ3, cxx*czx*EAL + cxz*czz*EIY3 +  cxy*czy*EIZ3, -(cxy*cxz*EIY2) - cxy*cxz*EIZ2, -(cxz*cyy*EIY2) - cxy*cyz*EIZ2, -(cxz*czy*EIY2) - cxy*czz*EIZ2),
            # List(cxx*cyx*EAL + cxz*cyz*EIY3 + cxy*cyy*EIZ3,cyx**2*EAL + cyz**2*EIY3 + cyy**2*EIZ3,cyx*czx*EAL + cyz*czz*EIY3 + cyy*czy*EIZ3,-(cxy*cyz*EIY2) - cxz*cyy*EIZ2,-(cyy*cyz*EIY2) - cyy*cyz*EIZ2,-(cyz*czy*EIY2) - cyy*czz*EIZ2),
            # List(cxx*czx*EAL + cxz*czz*EIY3 + cxy*czy*EIZ3,cyx*czx*EAL + cyz*czz*EIY3 + cyy*czy*EIZ3,czx**2*EAL + czz**2*EIY3 + czy**2*EIZ3,-(cxy*czz*EIY2) - cxz*czy*EIZ2,-(cyy*czz*EIY2) - cyz*czy*EIZ2,-(czy*czz*EIY2) - czy*czz*EIZ2),
            # List(-(cxy*cxz*EIY2) - cxy*cxz*EIZ2, -(cxy*cyz*EIY2) - cxz*cyy*EIZ2, -(cxy*czz*EIY2) - cxz*czy*EIZ2, cxy**2*EIY1 + cxz**2*EIZ1 + cxx**2*GKL, cxy*cyy*EIY1 + cxz*cyz*EIZ1 +  cxx*cyx*GKL, cxy*czy*EIY1 + cxz*czz*EIZ1 +  cxx*czx*GKL),
            # List(-(cxz*cyy*EIY2) - cxy*cyz*EIZ2, -(cyy*cyz*EIY2) - cyy*cyz*EIZ2, -(cyy*czz*EIY2) - cyz*czy*EIZ2, cxy*cyy*EIY1 + cxz*cyz*EIZ1 +  cxx*cyx*GKL, cyy**2*EIY1 + cyz**2*EIZ1 + cyx**2*GKL, cyy*czy*EIY1 + cyz*czz*EIZ1 +  cyx*czx*GKL),
            # List(-(cxz*czy*EIY2) - cxy*czz*EIZ2, -(cyz*czy*EIY2) - cyy*czz*EIZ2, -(czy*czz*EIY2) - czy*czz*EIZ2, cxy*czy*EIY1 + cxz*czz*EIZ1 +  cxx*czx*GKL, cyy*czy*EIY1 + cyz*czz*EIZ1 +  cyx*czx*GKL, czy**2*EIY1 + czz**2*EIZ1 + czx**2*GKL)))
















            # X21 = Δx
            # Y21 = Δy
            # Z21 = Δz
            #
            # X31 = 0
            # Y31 = 1
            # Z31 = 0
            #
            # A123 = (
            #     (Y21*Z31 - Y31*Z21)**2 +
            #     (Z21*X31 - Z31*X21)**2 +
            #     (X21*Y31 - X31*Y21)**2
            # )**0.5
            #
            #
            # cxx = X21/L
            # cxy = Y21/L
            # cxz = Z21/L
            #
            # czx = (Y21*Z31 - Y31*Z21)/(2*A123)
            # czy = (Z21*X31 - Z31*X21)/(2*A123)
            # czz = (X21*Y31 - X31*Y21)/(2*A123)
            #
            # cyx = czy*cxz - czz*cxy
            # cyy = czz*cxx - czx*cxz
            # cyz = czx*cxy - czy*cxx
            #
            #
            # # calculate paramaeters for kg_local
            # EAL  = ( E_1 * A   / L   )
            # GKL  = ( G_1 * I_t / L   )
            #
            # EIY3 = (12* E_1 * I_y / L**3)
            # EIY2 = ( 6* E_1 * I_y / L**2)
            # EIY1 = ( 4* E_1 * I_y / L   )
            # EIY0 = ( 2* E_1 * I_y / L   )
            #
            # EIZ3 = (12* E_1 * I_z / L**3)
            # EIZ2 = ( 6* E_1 * I_z / L**2)
            # EIZ1 = ( 4* E_1 * I_z / L   )
            # EIZ0 = ( 2* E_1 * I_z / L   )
            #
            # def List(*vals):
            #     return [val for val in vals]
            #
            # kg11 = np.array(List(List(cxx**2*EAL + czx**2*EIY3 +   cyx**2*EIZ3, cxx*cxy*EAL + czx*czy*EIY3 +   cyx*cyy*EIZ3, cxx*cxz*EAL + czx*czz*EIY3 +   cyx*cyz*EIZ3, -(cyx*czx*EIY2) + cyx*czx*EIZ2, -(cyy*czx*EIY2) + cyx*czy*EIZ2, -(cyz*czx*EIY2) + cyx*czz*EIZ2),List(cxx*cxy*EAL + czx*czy*EIY3 +   cyx*cyy*EIZ3, cxy**2*EAL + czy**2*EIY3 + cyy**2*EIZ3, cxy*cxz*EAL + czy*czz*EIY3 +   cyy*cyz*EIZ3, -(cyx*czy*EIY2) + cyy*czx*EIZ2, -(cyy*czy*EIY2) + cyy*czy*EIZ2, -(cyz*czy*EIY2) + cyy*czz*EIZ2),List(cxx*cxz*EAL + czx*czz*EIY3 +   cyx*cyz*EIZ3, cxy*cxz*EAL + czy*czz*EIY3 +   cyy*cyz*EIZ3, cxz**2*EAL + czz**2*EIY3 + cyz**2*EIZ3, -(cyx*czz*EIY2) + cyz*czx*EIZ2, -(cyy*czz*EIY2) + cyz*czy*EIZ2, -(cyz*czz*EIY2) + cyz*czz*EIZ2),List(-(cyx*czx*EIY2) + cyx*czx*EIZ2, -(cyx*czy*EIY2) + cyy*czx*EIZ2, -(cyx*czz*EIY2) + cyz*czx*EIZ2, cyx**2*EIY1 + czx**2*EIZ1 + cxx**2*GKL, cyx*cyy*EIY1 + czx*czy*EIZ1 +   cxx*cxy*GKL, cyx*cyz*EIY1 + czx*czz*EIZ1 +   cxx*cxz*GKL),List(-(cyy*czx*EIY2) + cyx*czy*EIZ2, -(cyy*czy*EIY2) + cyy*czy*EIZ2, -(cyy*czz*EIY2) + cyz*czy*EIZ2, cyx*cyy*EIY1 + czx*czy*EIZ1 +   cxx*cxy*GKL, cyy**2*EIY1 + czy**2*EIZ1 + cxy**2*GKL, cyy*cyz*EIY1 + czy*czz*EIZ1 +   cxy*cxz*GKL),List(-(cyz*czx*EIY2) + cyx*czz*EIZ2, -(cyz*czy*EIY2) + cyy*czz*EIZ2, -(cyz*czz*EIY2) + cyz*czz*EIZ2, cyx*cyz*EIY1 + czx*czz*EIZ1 +   cxx*cxz*GKL, cyy*cyz*EIY1 + czy*czz*EIZ1 +   cxy*cxz*GKL, cyz**2*EIY1 + czz**2*EIZ1 + cxz**2*GKL)))
            #
            # kg12 = np.array(List(List(-(cxx**2*EAL) - czx**2*EIY3 -   cyx**2*EIZ3, -(cxx*cxy*EAL) - czx*czy*EIY3 -   cyx*cyy*EIZ3, -(cxx*cxz*EAL) - czx*czz*EIY3 -   cyx*cyz*EIZ3, cyx*czx*EIY2 - cyx*czx*EIZ2, cyy*czx*EIY2 - cyx*czy*EIZ2, cyz*czx*EIY2 - cyx*czz*EIZ2),List(-(cxx*cxy*EAL) - czx*czy*EIY3 -   cyx*cyy*EIZ3, -(cxy**2*EAL) - czy**2*EIY3 -   cyy**2*EIZ3, -(cxy*cxz*EAL) - czy*czz*EIY3 -   cyy*cyz*EIZ3, cyx*czy*EIY2 - cyy*czx*EIZ2, cyy*czy*EIY2 - cyy*czy*EIZ2, cyz*czy*EIY2 - cyy*czz*EIZ2),List(-(cxx*cxz*EAL) - czx*czz*EIY3 -   cyx*cyz*EIZ3, -(cxy*cxz*EAL) - czy*czz*EIY3 -   cyy*cyz*EIZ3, -(cxz**2*EAL) - czz**2*EIY3 -   cyz**2*EIZ3, cyx*czz*EIY2 - cyz*czx*EIZ2, cyy*czz*EIY2 - cyz*czy*EIZ2, cyz*czz*EIY2 - cyz*czz*EIZ2),List(-(cyx*czx*EIY2) + cyx*czx*EIZ2, -(cyx*czy*EIY2) + cyy*czx*EIZ2, -(cyx*czz*EIY2) + cyz*czx*EIZ2, cyx**2*EIY0 + czx**2*EIZ0 - cxx**2*GKL, cyx*cyy*EIY0 + czx*czy*EIZ0 -   cxx*cxy*GKL, cyx*cyz*EIY0 + czx*czz*EIZ0 -   cxx*cxz*GKL),List(-(cyy*czx*EIY2) + cyx*czy*EIZ2, -(cyy*czy*EIY2) + cyy*czy*EIZ2, -(cyy*czz*EIY2) + cyz*czy*EIZ2, cyx*cyy*EIY0 + czx*czy*EIZ0 -   cxx*cxy*GKL, cyy**2*EIY0 + czy**2*EIZ0 - cxy**2*GKL, cyy*cyz*EIY0 + czy*czz*EIZ0 -   cxy*cxz*GKL),List(-(cyz*czx*EIY2) + cyx*czz*EIZ2, -(cyz*czy*EIY2) + cyy*czz*EIZ2, -(cyz*czz*EIY2) + cyz*czz*EIZ2, cyx*cyz*EIY0 + czx*czz*EIZ0 -   cxx*cxz*GKL, cyy*cyz*EIY0 + czy*czz*EIZ0 -   cxy*cxz*GKL, cyz**2*EIY0 + czz**2*EIZ0 - cxz**2*GKL)))
            #
            # kg21 = kg12.T
            #
            # kg22 = np.array(List(List(cxx**2*EAL + czx**2*EIY3 +   cyx**2*EIZ3, cxx*cxy*EAL + czx*czy*EIY3 +   cyx*cyy*EIZ3, cxx*cxz*EAL + czx*czz*EIY3 +   cyx*cyz*EIZ3, cyx*czx*EIY2 - cyx*czx*EIZ2, cyy*czx*EIY2 - cyx*czy*EIZ2, cyz*czx*EIY2 - cyx*czz*EIZ2),List(cxx*cxy*EAL + czx*czy*EIY3 +   cyx*cyy*EIZ3, cxy**2*EAL + czy**2*EIY3 + cyy**2*EIZ3, cxy*cxz*EAL + czy*czz*EIY3 +   cyy*cyz*EIZ3, cyx*czy*EIY2 - cyy*czx*EIZ2, cyy*czy*EIY2 - cyy*czy*EIZ2, cyz*czy*EIY2 - cyy*czz*EIZ2),List(cxx*cxz*EAL + czx*czz*EIY3 +   cyx*cyz*EIZ3, cxy*cxz*EAL + czy*czz*EIY3 +   cyy*cyz*EIZ3, cxz**2*EAL + czz**2*EIY3 + cyz**2*EIZ3, cyx*czz*EIY2 - cyz*czx*EIZ2, cyy*czz*EIY2 - cyz*czy*EIZ2, cyz*czz*EIY2 - cyz*czz*EIZ2),List(cyx*czx*EIY2 - cyx*czx*EIZ2, cyx*czy*EIY2 - cyy*czx*EIZ2, cyx*czz*EIY2 - cyz*czx*EIZ2, cyx**2*EIY1 + czx**2*EIZ1 + cxx**2*GKL, cyx*cyy*EIY1 + czx*czy*EIZ1 +   cxx*cxy*GKL, cyx*cyz*EIY1 + czx*czz*EIZ1 +   cxx*cxz*GKL),List(cyy*czx*EIY2 - cyx*czy*EIZ2, cyy*czy*EIY2 - cyy*czy*EIZ2, cyy*czz*EIY2 - cyz*czy*EIZ2, cyx*cyy*EIY1 + czx*czy*EIZ1 +   cxx*cxy*GKL, cyy**2*EIY1 + czy**2*EIZ1 + cxy**2*GKL, cyy*cyz*EIY1 + czy*czz*EIZ1 +   cxy*cxz*GKL),List(cyz*czx*EIY2 - cyx*czz*EIZ2, cyz*czy*EIY2 - cyy*czz*EIZ2, cyz*czz*EIY2 - cyz*czz*EIZ2, cyx*cyz*EIY1 + czx*czz*EIZ1 +   cxx*cxz*GKL, cyy*cyz*EIY1 + czy*czz*EIZ1 +   cxy*cxz*GKL, cyz**2*EIY1 + czz**2*EIZ1 + cxz**2*GKL)))















            # calculate paramaeters for kg_local
            EAL  = ( E_1 * A   / L   )
            GKL  = ( G_1 * I_t / L   )

            EIY3 = (12* E_1 * I_y / L**3)
            EIY2 = ( 6* E_1 * I_y / L**2)
            EIY1 = ( 4* E_1 * I_y / L   )
            EIY0 = ( 2* E_1 * I_y / L   )

            EIZ3 = (12* E_1 * I_z / L**3)
            EIZ2 = ( 6* E_1 * I_z / L**2)
            EIZ1 = ( 4* E_1 * I_z / L   )
            EIZ0 = ( 2* E_1 * I_z / L   )


            # cosinus matrix
            X21,Y21,Z21 = Δx, Δy, Δz

            X31,Y31,Z31 = 0, 1, 0

            A123 = (
                (Y21*Z31 - Y31*Z21)**2 +
                (Z21*X31 - Z31*X21)**2 +
                (X21*Y31 - X31*Y21)**2
            )**0.5

            lx, mx, nx = X21/L, Y21/L, Z21/L

            lz = (Y21*Z31 - Y31*Z21)/(A123)
            mz = (Z21*X31 - Z31*X21)/(A123)
            nz = (X21*Y31 - X31*Y21)/(A123)

            ly = mz*nx - nz*mx
            my = nz*lx - lz*nx
            ny = lz*mx - mz*lx


            # Lxy = (Δx**2+Δy**2)**0.5
            # lx = Δx/L
            # mx = Δy/L
            # nx = Δz/L
            # ly = -Δy/Lxy
            # my = Δx/Lxy
            # ny = 0
            # lz = -Δx*Δz/(L*Lxy)
            # mz = -Δy*Δz/(L*Lxy)
            # nz = (Δx**2)/(L*Lxy) + (Δy**2)/(L*Lxy)








            def List(*vals):
                return [val for val in vals]

            kg11 = np.array(List(List(EAL*lx**2 + EIZ3*ly**2 + EIY3*lz**2,EAL*lx*mx + EIZ3*ly*my + EIY3*lz*mz,EAL*lx*nx + EIZ3*ly*ny + EIY3*lz*nz, -(EIY2*ly*lz) + EIZ2*ly*lz,-(EIY2*lz*my) + EIZ2*ly*mz,-(EIY2*lz*ny) + EIZ2*ly*nz),List(EAL*lx*mx + EIZ3*ly*my + EIY3*lz*mz,EAL*mx**2 + EIZ3*my**2 + EIY3*mz**2,EAL*mx*nx + EIZ3*my*ny + EIY3*mz*nz, EIZ2*lz*my - EIY2*ly*mz,-(EIY2*my*mz) + EIZ2*my*mz,-(EIY2*mz*ny) + EIZ2*my*nz),List(EAL*lx*nx + EIZ3*ly*ny + EIY3*lz*nz,EAL*mx*nx + EIZ3*my*ny + EIY3*mz*nz,EAL*nx**2 + EIZ3*ny**2 + EIY3*nz**2, EIZ2*lz*ny - EIY2*ly*nz,EIZ2*mz*ny - EIY2*my*nz,-(EIY2*ny*nz) + EIZ2*ny*nz),List(-(EIY2*ly*lz) + EIZ2*ly*lz,EIZ2*lz*my - EIY2*ly*mz,EIZ2*lz*ny - EIY2*ly*nz,GKL*lx**2 + EIY1*ly**2 + EIZ1*lz**2, GKL*lx*mx + EIY1*ly*my + EIZ1*lz*mz,GKL*lx*nx + EIY1*ly*ny + EIZ1*lz*nz),List(-(EIY2*lz*my) + EIZ2*ly*mz,-(EIY2*my*mz) + EIZ2*my*mz,EIZ2*mz*ny - EIY2*my*nz,GKL*lx*mx + EIY1*ly*my + EIZ1*lz*mz, GKL*mx**2 + EIY1*my**2 + EIZ1*mz**2,GKL*mx*nx + EIY1*my*ny + EIZ1*mz*nz),List(-(EIY2*lz*ny) + EIZ2*ly*nz,-(EIY2*mz*ny) + EIZ2*my*nz,-(EIY2*ny*nz) + EIZ2*ny*nz,GKL*lx*nx + EIY1*ly*ny + EIZ1*lz*nz, GKL*mx*nx + EIY1*my*ny + EIZ1*mz*nz,GKL*nx**2 + EIY1*ny**2 + EIZ1*nz**2)))

            kg21 = np.array(List(List(-(EAL*lx**2) - EIZ3*ly**2 - EIY3*lz**2,-(EAL*lx*mx) - EIZ3*ly*my - EIY3*lz*mz,-(EAL*lx*nx) - EIZ3*ly*ny - EIY3*lz*nz, EIY2*ly*lz - EIZ2*ly*lz,EIY2*lz*my - EIZ2*ly*mz,EIY2*lz*ny - EIZ2*ly*nz),List(-(EAL*lx*mx) - EIZ3*ly*my - EIY3*lz*mz,-(EAL*mx**2) - EIZ3*my**2 - EIY3*mz**2,-(EAL*mx*nx) - EIZ3*my*ny - EIY3*mz*nz, -(EIZ2*lz*my) + EIY2*ly*mz,EIY2*my*mz - EIZ2*my*mz,EIY2*mz*ny - EIZ2*my*nz),List(-(EAL*lx*nx) - EIZ3*ly*ny - EIY3*lz*nz,-(EAL*mx*nx) - EIZ3*my*ny - EIY3*mz*nz,-(EAL*nx**2) - EIZ3*ny**2 - EIY3*nz**2, -(EIZ2*lz*ny) + EIY2*ly*nz,-(EIZ2*mz*ny) + EIY2*my*nz,EIY2*ny*nz - EIZ2*ny*nz),List(-(EIY2*ly*lz) + EIZ2*ly*lz,EIZ2*lz*my - EIY2*ly*mz,EIZ2*lz*ny - EIY2*ly*nz,-(GKL*lx**2) + EIY0*ly**2 + EIZ0*lz**2, -(GKL*lx*mx) + EIY0*ly*my + EIZ0*lz*mz,-(GKL*lx*nx) + EIY0*ly*ny + EIZ0*lz*nz),List(-(EIY2*lz*my) + EIZ2*ly*mz,-(EIY2*my*mz) + EIZ2*my*mz,EIZ2*mz*ny - EIY2*my*nz,-(GKL*lx*mx) + EIY0*ly*my + EIZ0*lz*mz, -(GKL*mx**2) + EIY0*my**2 + EIZ0*mz**2,-(GKL*mx*nx) + EIY0*my*ny + EIZ0*mz*nz),List(-(EIY2*lz*ny) + EIZ2*ly*nz,-(EIY2*mz*ny) + EIZ2*my*nz,-(EIY2*ny*nz) + EIZ2*ny*nz,-(GKL*lx*nx) + EIY0*ly*ny + EIZ0*lz*nz, -(GKL*mx*nx) + EIY0*my*ny + EIZ0*mz*nz,-(GKL*nx**2) + EIY0*ny**2 + EIZ0*nz**2)))

            kg12 = kg21.T

            kg22 = np.array(List(List(EAL*lx**2 + EIZ3*ly**2 + EIY3*lz**2,EAL*lx*mx + EIZ3*ly*my + EIY3*lz*mz,EAL*lx*nx + EIZ3*ly*ny + EIY3*lz*nz, EIY2*ly*lz - EIZ2*ly*lz,EIY2*lz*my - EIZ2*ly*mz,EIY2*lz*ny - EIZ2*ly*nz),List(EAL*lx*mx + EIZ3*ly*my + EIY3*lz*mz,EAL*mx**2 + EIZ3*my**2 + EIY3*mz**2,EAL*mx*nx + EIZ3*my*ny + EIY3*mz*nz, -(EIZ2*lz*my) + EIY2*ly*mz,EIY2*my*mz - EIZ2*my*mz,EIY2*mz*ny - EIZ2*my*nz),List(EAL*lx*nx + EIZ3*ly*ny + EIY3*lz*nz,EAL*mx*nx + EIZ3*my*ny + EIY3*mz*nz,EAL*nx**2 + EIZ3*ny**2 + EIY3*nz**2, -(EIZ2*lz*ny) + EIY2*ly*nz,-(EIZ2*mz*ny) + EIY2*my*nz,EIY2*ny*nz - EIZ2*ny*nz),List(EIY2*ly*lz - EIZ2*ly*lz,-(EIZ2*lz*my) + EIY2*ly*mz,-(EIZ2*lz*ny) + EIY2*ly*nz,GKL*lx**2 + EIY1*ly**2 + EIZ1*lz**2, GKL*lx*mx + EIY1*ly*my + EIZ1*lz*mz,GKL*lx*nx + EIY1*ly*ny + EIZ1*lz*nz),List(EIY2*lz*my - EIZ2*ly*mz,EIY2*my*mz - EIZ2*my*mz,-(EIZ2*mz*ny) + EIY2*my*nz,GKL*lx*mx + EIY1*ly*my + EIZ1*lz*mz, GKL*mx**2 + EIY1*my**2 + EIZ1*mz**2,GKL*mx*nx + EIY1*my*ny + EIZ1*mz*nz),List(EIY2*lz*ny - EIZ2*ly*nz,EIY2*mz*ny - EIZ2*my*nz,EIY2*ny*nz - EIZ2*ny*nz,GKL*lx*nx + EIY1*ly*ny + EIZ1*lz*nz, GKL*mx*nx + EIY1*my*ny + EIZ1*mz*nz,GKL*nx**2 + EIY1*ny**2 + EIZ1*nz**2)))

        return kg11,kg12,kg21,kg22




class postr:
    '''
    Post results
    '''

    def __init__(self, core, prog, lcase):
        self.core = core
        self.prog = prog
        self.lcase = lcase

        self._forces()


    def _forces0(self):

        # get elements from database
        elements = self.core.dbase.get('''
        SELECT
            [BM].[id],
            [BM].[L],
            [BM].[ΔX],
            [BM].[ΔY],
            [BM].[ΔZ],
            [N1].[noG],
            [N1].[id],
            [N2].[noG],
            [N2].[id],
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

            id,L,Δx,Δy,Δz,n1,n1id,n2,n2id,A,I_t,I_y,I_z,E_1,G_1 = element

            q1 = self.core.dbase.get(f'''
            SELECT
                [dx],
                [dy],
                [dz],
                [rx],
                [ry],
                [rz]
            FROM [113:nodes:sresu] WHERE [lcase]="{self.lcase}" AND [node]="{n1id}"
            ''')[0]

            # second node, look upper comment
            q2 = self.core.dbase.get(f'''
            SELECT
                [dx],
                [dy],
                [dz],
                [rx],
                [ry],
                [rz]
            FROM [113:nodes:sresu] WHERE [lcase]="{self.lcase}" AND [node]="{n2id}"
            ''')[0]

            # calculate sin,cos itd
            Cx, Cy, Cz = Δx/L, Δy/L, Δz/L

            # vector of local displacement sorted like dofs
            q_loc  = [val if val is not None else 0 for val in q1]
            q_loc += [val if val is not None else 0 for val in q2]

            # change of length
            q_loc  = [q1[0], q1[1], q1[2], q2[0], q2[1], q2[2]]
            q_loc  = [val if val is not None else 0 for val in q_loc]
            ΔL = np.array([-Cx, -Cy, -Cz, Cx, Cy, Cz]).dot(q_loc)

            # strain of element
            ε_x_N = ΔL/L

            # stress in element
            σ_x_N = E_1 * ε_x_N

            # axial force
            N_x = σ_x_N * A

            # send to static results
            self.core.dbase.add(
                table = '[133:beams:sresu]',
                cols  = '[id],[lcase],[N_1],[N_2],[ΔL],[ε_x_N]',
                data  = (id, self.lcase, N_x, N_x, ΔL, ε_x_N),
            )

            # send to design results
            self.core.dbase.add(
                table = '[134:beams:desig]',
                cols  = '[id],[lcase],[σ_x_N]',
                data  = (id, self.lcase, σ_x_N),
            )


    def _forces(self):

        # get elements from database
        elements = self.core.dbase.get('''
        SELECT
            [BM].[id],
            [BM].[L],
            [BM].[ΔX],
            [BM].[ΔY],
            [BM].[ΔZ],
            [N1].[noG],
            [N1].[id],
            [N2].[noG],
            [N2].[id],
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

            id,L,Δx,Δy,Δz,n1,n1id,n2,n2id,A,I_t,I_y,I_z,E_1,G_1 = element

            q1 = self.core.dbase.get(f'''
            SELECT
                [dx],
                [dy],
                [dz],
                [rx],
                [ry],
                [rz]
            FROM [113:nodes:sresu] WHERE [lcase]="{self.lcase}" AND [node]="{n1id}"
            ''')[0]

            # second node, look upper comment
            q2 = self.core.dbase.get(f'''
            SELECT
                [dx],
                [dy],
                [dz],
                [rx],
                [ry],
                [rz]
            FROM [113:nodes:sresu] WHERE [lcase]="{self.lcase}" AND [node]="{n2id}"
            ''')[0]

            # vector of local displacement sorted like dofs
            q_glo  = [val if val is not None else 0 for val in q1]
            q_glo += [val if val is not None else 0 for val in q2]


            # cosinus matrix
            X21,Y21,Z21 = Δx, Δy, Δz

            X31,Y31,Z31 = 0, 1, 0

            A123 = (
                (Y21*Z31 - Y31*Z21)**2 +
                (Z21*X31 - Z31*X21)**2 +
                (X21*Y31 - X31*Y21)**2
            )**0.5

            lx, mx, nx = X21/L, Y21/L, Z21/L

            lz = (Y21*Z31 - Y31*Z21)/(A123)
            mz = (Z21*X31 - Z31*X21)/(A123)
            nz = (X21*Y31 - X31*Y21)/(A123)

            ly = mz*nx - nz*mx
            my = nz*lx - lz*nx
            ny = lz*mx - mz*lx


            def List(*vals):
                return [val for val in vals]

            # q_loc = np.array(List(
            # lx*q_glo[0] + mx*q_glo[1] + nx*q_glo[2],
            # ly*q_glo[0] + my*q_glo[1] + ny*q_glo[2],
            # lz*q_glo[0] + mz*q_glo[1] + nz*q_glo[2],
            # lx*q_glo[3] + mx*q_glo[4] + nx*q_glo[5],
            # ly*q_glo[3] + my*q_glo[4] + ny*q_glo[5],
            # lz*q_glo[3] + mz*q_glo[4] + nz*q_glo[5],
            # lx*q_glo[6] + mx*q_glo[7] + nx*q_glo[8],
            # ly*q_glo[6] + my*q_glo[7] + ny*q_glo[8],
            # lz*q_glo[6] + mz*q_glo[7] + nz*q_glo[8],
            # lx*q_glo[9] + mx*q_glo[10] + nx*q_glo[11],
            # ly*q_glo[9] + my*q_glo[10] + ny*q_glo[11],
            # lz*q_glo[9] + mz*q_glo[10] + nz*q_glo[11],
            # ))

            q0,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11 = q_glo

            q_loc = np.array(List(
                lx*q0 + mx*q1 + nx*q2,
                ly*q0 + my*q1 + ny*q2,
                lz*q0 + mz*q1 + nz*q2,
                lx*q3 + mx*q4 + nx*q5,
                ly*q3 + my*q4 + ny*q5,
                lz*q3 + mz*q4 + nz*q5,
                lx*q6 + mx*q7 + nx*q8,
                ly*q6 + my*q7 + ny*q8,
                lz*q6 + mz*q7 + nz*q8,
                mx*q10 + nx*q11 + lx*q9,
                my*q10 + ny*q11 + ly*q9,
                mz*q10 + nz*q11 + lz*q9,
            ))

            # q_loc = np.array(q_glo)

            # print('q_glo', q_glo)
            # print('q_loc', q_loc)

            # ψ = (q_loc[8] - q_loc[2])/L
            #
            # N_x   = E_1*A*(q_loc[6] - q_loc[0])
            # V_z_1 = E_1*I_y/L**2 * (-6*q_loc[4] - 6*q_loc[10])
            # M_y_1 = E_1*I_y/L * (4*q_loc[4] + 2*q_loc[10] - 6*ψ)
            #
            # V_z_2 = E_1*I_y/L**2 * (-6*q_loc[10] - 6*q_loc[4])
            # M_y_2 = E_1*I_y/L * (4*q_loc[10] + 2*q_loc[4] - 6*ψ)
            #
            # M_y_1_l = E_1*I_y/L * (4*q_loc[4] + 2*q_loc[10] - 6*ψ)
            # M_y_1_g = E_1*I_y/L * (4*q_glo[4] + 2*q_glo[10] - 6*ψ)
            # print('2', q_glo[2], q_loc[2])
            # print('8', q_glo[8], q_loc[8])
            # print(M_y_1_l, M_y_1_g)


            # # # Cx, Cy, Cz = Δx/L, Δy/L, Δz/L
            # #
            # nixx = lambda x,L: np.array([
            #     0,
            #     -(6/L**2) + (12*x)/L**3,
            #     L*(-(4/L**2) + (6*x)/L**3),
            #     0,
            #     6/L**2 - (12*x)/L**3,
            #     L*(-(2/L**2) + (6*x)/L**3)]
            # )
            #
            # nixxx = lambda x,L: np.array([
            #     0,
            #     12/L**3,
            #     6/L**2,
            #     0,
            #     -12/L**3,
            #     6/L**2]
            # )
            #
            # ΔL = 0 #np.array([-Cx, -Cz, 0  , Cx, Cz, 0 ]).dot(q_loc)
            #
            # # strain of element
            # ε_x = ΔL/L
            #
            # # stress in element
            # σ_x = E_1 * ε_x
            #
            # # axial force
            # N_x = σ_x * A
            #
            # q_loc = np.array([
            #     0,
            #     q_loc[2],
            #     q_loc[4],
            #     0,
            #     q_loc[8],
            #     q_loc[10],
            # ])
            #
            # M_y_1 = np.array(nixx(0,L)).dot(q_loc)*(-E_1*I_y)
            # M_y_2 = np.array(nixx(L,L)).dot(q_loc)*(-E_1*I_y)
            #
            # V_z_1 = np.array(nixxx(0,L)).dot(q_loc)*(-E_1*I_y)
            # V_z_2 = np.array(nixxx(L,L)).dot(q_loc)*(-E_1*I_y)
            #
            # # send to static results
            # self.core.dbase.add(
            #     table = '[133:beams:sresu]',
            #     cols  = '[id],[lcase],[N_x_1],[N_x_2],[M_y_1],[M_y_2],[V_z_1],[V_z_2]',
            #     data  = (id, self.lcase, N_x, N_x, M_y_1, M_y_2, V_z_1, V_z_2),
            # )



            # 
            # # calculate paramaeters for kg_local
            # EAL  = ( E_1 * A   / L   )
            # GKL  = ( G_1 * I_t / L   )
            #
            # EIY3 = (12* E_1 * I_y / L**3)
            # EIY2 = ( 6* E_1 * I_y / L**2)
            # EIY1 = ( 4* E_1 * I_y / L   )
            # EIY0 = ( 2* E_1 * I_y / L   )
            #
            # EIZ3 = (12* E_1 * I_z / L**3)
            # EIZ2 = ( 6* E_1 * I_z / L**2)
            # EIZ1 = ( 4* E_1 * I_z / L   )
            # EIZ0 = ( 2* E_1 * I_z / L   )
            #
            #
            # ke = np.array(List(List(EAL,0,0,0,0,0,-EAL,0,0,0,0,0),List(0,EIZ3,0,0,0,EIZ2,0,-EIZ3,0,0,0,EIZ2),List(0,0,EIY3,0,-EIY2,0,0,0,-EIY3,0,-EIY2,0),
            # List(0,0,0,GKL,0,0,0,0,0,-GKL,0,0),List(0,0,-EIY2,0,EIY1,0,0,0,EIY2,0,EIY0,0),List(0,EIZ2,0,0,0,EIZ1,0,-EIZ2,0,0,0,EIZ0),
            # List(-EAL,0,0,0,0,0,EAL,0,0,0,0,0),List(0,-EIZ3,0,0,0,-EIZ2,0,EIZ3,0,0,0,-EIZ2),List(0,0,-EIY3,0,EIY2,0,0,0,EIY3,0,EIY2,0),
            # List(0,0,0,-GKL,0,0,0,0,0,GKL,0,0),List(0,0,-EIY2,0,EIY0,0,0,0,EIY2,0,EIY1,0),List(0,EIZ2,0,0,0,EIZ0,0,-EIZ2,0,0,0,EIZ1)))


            # print( ke.dot(q_loc))