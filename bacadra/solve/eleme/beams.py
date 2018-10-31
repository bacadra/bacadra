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
            kg11 = np.array(List(
            List(cxx**2*EAL + cxz**2*EIY3 +  cxy**2*EIZ3, cxx*cyx*EAL + cxz*cyz*EIY3 +  cxy*cyy*EIZ3, cxx*czx*EAL + cxz*czz*EIY3 +  cxy*czy*EIZ3, cxy*cxz*EIY2 + cxy*cxz*EIZ2, cxz*cyy*EIY2 + cxy*cyz*EIZ2, cxz*czy*EIY2 + cxy*czz*EIZ2),
            List(cxx*cyx*EAL + cxz*cyz*EIY3 +  cxy*cyy*EIZ3, cyx**2*EAL + cyz**2*EIY3 + cyy**2*EIZ3, cyx*czx*EAL + cyz*czz*EIY3 +  cyy*czy*EIZ3, cxy*cyz*EIY2 + cxz*cyy*EIZ2, cyy*cyz*EIY2 + cyy*cyz*EIZ2, cyz*czy*EIY2 + cyy*czz*EIZ2),
            List(cxx*czx*EAL + cxz*czz*EIY3 + cxy*czy*EIZ3,cyx*czx*EAL + cyz*czz*EIY3 + cyy*czy*EIZ3,czx**2*EAL + czz**2*EIY3 + czy**2*EIZ3,cxy*czz*EIY2 + cxz*czy*EIZ2,cyy*czz*EIY2 + cyz*czy*EIZ2,czy*czz*EIY2 + czy*czz*EIZ2),
            List(cxy*cxz*EIY2 + cxy*cxz*EIZ2, cxy*cyz*EIY2 + cxz*cyy*EIZ2, cxy*czz*EIY2 + cxz*czy*EIZ2, cxy**2*EIY1 + cxz**2*EIZ1 + cxx**2*GKL, cxy*cyy*EIY1 + cxz*cyz*EIZ1 +  cxx*cyx*GKL, cxy*czy*EIY1 + cxz*czz*EIZ1 +  cxx*czx*GKL),
            List(cxz*cyy*EIY2 + cxy*cyz*EIZ2, cyy*cyz*EIY2 + cyy*cyz*EIZ2, cyy*czz*EIY2 + cyz*czy*EIZ2, cxy*cyy*EIY1 + cxz*cyz*EIZ1 +  cxx*cyx*GKL, cyy**2*EIY1 + cyz**2*EIZ1 + cyx**2*GKL, cyy*czy*EIY1 + cyz*czz*EIZ1 +  cyx*czx*GKL),
            List(cxz*czy*EIY2 + cxy*czz*EIZ2, cyz*czy*EIY2 + cyy*czz*EIZ2, czy*czz*EIY2 + czy*czz*EIZ2, cxy*czy*EIY1 + cxz*czz*EIZ1 +  cxx*czx*GKL, cyy*czy*EIY1 + cyz*czz*EIZ1 +  cyx*czx*GKL, czy**2*EIY1 + czz**2*EIZ1 + czx**2*GKL)))

            # create right upper
            kg12 = np.array(List(
            List(-(cxx**2*EAL) - cxz**2*EIY3 - cxy**2*EIZ3,-(cxx*cyx*EAL) - cxz*cyz*EIY3 - cxy*cyy*EIZ3,-(cxx*czx*EAL) - cxz*czz*EIY3 - cxy*czy*EIZ3,cxy*cxz*EIY2 + cxy*cxz*EIZ2,cxz*cyy*EIY2 + cxy*cyz*EIZ2,cxz*czy*EIY2 + cxy*czz*EIZ2),
            List(-(cxx*cyx*EAL) - cxz*cyz*EIY3 - cxy*cyy*EIZ3,-(cyx**2*EAL) - cyz**2*EIY3 - cyy**2*EIZ3,-(cyx*czx*EAL) - cyz*czz*EIY3 - cyy*czy*EIZ3,cxy*cyz*EIY2 + cxz*cyy*EIZ2,cyy*cyz*EIY2 + cyy*cyz*EIZ2,cyz*czy*EIY2 + cyy*czz*EIZ2),
            List(-(cxx*czx*EAL) - cxz*czz*EIY3 - cxy*czy*EIZ3,-(cyx*czx*EAL) - cyz*czz*EIY3 - cyy*czy*EIZ3,-(czx**2*EAL) - czz**2*EIY3 - czy**2*EIZ3,cxy*czz*EIY2 + cxz*czy*EIZ2,cyy*czz*EIY2 + cyz*czy*EIZ2,czy*czz*EIY2 + czy*czz*EIZ2),
            List(-(cxy*cxz*EIY2) - cxy*cxz*EIZ2, -(cxy*cyz*EIY2) - cxz*cyy*EIZ2, -(cxy*czz*EIY2) - cxz*czy*EIZ2, cxy**2*EIY0 + cxz**2*EIZ0 - cxx**2*GKL, cxy*cyy*EIY0 + cxz*cyz*EIZ0 -  cxx*cyx*GKL, cxy*czy*EIY0 + cxz*czz*EIZ0 -  cxx*czx*GKL),
            List(-(cxz*cyy*EIY2) - cxy*cyz*EIZ2, -(cyy*cyz*EIY2) - cyy*cyz*EIZ2, -(cyy*czz*EIY2) - cyz*czy*EIZ2, cxy*cyy*EIY0 + cxz*cyz*EIZ0 -  cxx*cyx*GKL, cyy**2*EIY0 + cyz**2*EIZ0 - cyx**2*GKL, cyy*czy*EIY0 + cyz*czz*EIZ0 -  cyx*czx*GKL),
            List(-(cxz*czy*EIY2) - cxy*czz*EIZ2, -(cyz*czy*EIY2) - cyy*czz*EIZ2, -(czy*czz*EIY2) - czy*czz*EIZ2, cxy*czy*EIY0 + cxz*czz*EIZ0 -  cxx*czx*GKL, cyy*czy*EIY0 + cyz*czz*EIZ0 -  cyx*czx*GKL, czy**2*EIY0 + czz**2*EIZ0 - czx**2*GKL)))

            # create left down part
            kg21 = kg12.T

            # create right down part
            kg22 = np.array(List(
            List(cxx**2*EAL + cxz**2*EIY3 +  cxy**2*EIZ3, cxx*cyx*EAL + cxz*cyz*EIY3 +  cxy*cyy*EIZ3, cxx*czx*EAL + cxz*czz*EIY3 +  cxy*czy*EIZ3, -(cxy*cxz*EIY2) - cxy*cxz*EIZ2, -(cxz*cyy*EIY2) - cxy*cyz*EIZ2, -(cxz*czy*EIY2) - cxy*czz*EIZ2),
            List(cxx*cyx*EAL + cxz*cyz*EIY3 + cxy*cyy*EIZ3,cyx**2*EAL + cyz**2*EIY3 + cyy**2*EIZ3,cyx*czx*EAL + cyz*czz*EIY3 + cyy*czy*EIZ3,-(cxy*cyz*EIY2) - cxz*cyy*EIZ2,-(cyy*cyz*EIY2) - cyy*cyz*EIZ2,-(cyz*czy*EIY2) - cyy*czz*EIZ2),
            List(cxx*czx*EAL + cxz*czz*EIY3 + cxy*czy*EIZ3,cyx*czx*EAL + cyz*czz*EIY3 + cyy*czy*EIZ3,czx**2*EAL + czz**2*EIY3 + czy**2*EIZ3,-(cxy*czz*EIY2) - cxz*czy*EIZ2,-(cyy*czz*EIY2) - cyz*czy*EIZ2,-(czy*czz*EIY2) - czy*czz*EIZ2),
            List(-(cxy*cxz*EIY2) - cxy*cxz*EIZ2, -(cxy*cyz*EIY2) - cxz*cyy*EIZ2, -(cxy*czz*EIY2) - cxz*czy*EIZ2, cxy**2*EIY1 + cxz**2*EIZ1 + cxx**2*GKL, cxy*cyy*EIY1 + cxz*cyz*EIZ1 +  cxx*cyx*GKL, cxy*czy*EIY1 + cxz*czz*EIZ1 +  cxx*czx*GKL),
            List(-(cxz*cyy*EIY2) - cxy*cyz*EIZ2, -(cyy*cyz*EIY2) - cyy*cyz*EIZ2, -(cyy*czz*EIY2) - cyz*czy*EIZ2, cxy*cyy*EIY1 + cxz*cyz*EIZ1 +  cxx*cyx*GKL, cyy**2*EIY1 + cyz**2*EIZ1 + cyx**2*GKL, cyy*czy*EIY1 + cyz*czz*EIZ1 +  cyx*czx*GKL),
            List(-(cxz*czy*EIY2) - cxy*czz*EIZ2, -(cyz*czy*EIY2) - cyy*czz*EIZ2, -(czy*czz*EIY2) - czy*czz*EIZ2, cxy*czy*EIY1 + cxz*czz*EIZ1 +  cxx*czx*GKL, cyy*czy*EIY1 + cyz*czz*EIZ1 +  cyx*czx*GKL, czy**2*EIY1 + czz**2*EIZ1 + czx**2*GKL)))


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
                [dz],
                [ry]
            FROM [113:nodes:sresu] WHERE [lcase]="{self.lcase}" AND [node]="{n1id}"
            ''')[0]

            # second node, look upper comment
            q2 = self.core.dbase.get(f'''
            SELECT
                [dx],
                [dz],
                [ry]
            FROM [113:nodes:sresu] WHERE [lcase]="{self.lcase}" AND [node]="{n2id}"
            ''')[0]

            # vector of local displacement sorted like dofs
            q_loc  = [val if val is not None else 0 for val in q1]
            q_loc += [val if val is not None else 0 for val in q2]
            q_loc = np.array(q_loc)
            # print(q_loc)

            # force = np.array(k_g).dot(q_loc)
            # print(force)

            # Sum[qe[[ie, i]]*Nkxx[[i]]*(-EI), {i, 5}];

            Cx, Cy, Cz = Δx/L, Δy/L, Δz/L

            nixx = lambda x,L: np.array([
                0,
                -(6/L**2) + (12*x)/L**3,
                L*(-(4/L**2) + (6*x)/L**3),
                0,
                6/L**2 - (12*x)/L**3,
                L*(-(2/L**2) + (6*x)/L**3)]
            )

            nixxx = lambda x,L: np.array([
                0,
                12/L**3,
                6/L**2,
                0,
                -12/L**3,
                6/L**2]
            )

            ΔL = np.array([-Cx, -Cz, 0  , Cx, Cz, 0 ]).dot(q_loc)

            # strain of element
            ε_x = ΔL/L

            # stress in element
            σ_x = E_1 * ε_x

            # axial force
            N_x = σ_x * A

            q_loc = np.array([
                (Cx*q1[0] + Cz*q1[1])/(Cx**2 + Cz**2),
                (-Cz*q1[0] + Cx*q1[1])/(Cx**2 + Cz**2),
                q1[2],
                (Cx*q2[0] + Cz*q2[1])/(Cx**2 + Cz**2),
                (-Cz*q2[0] + Cx*q2[1])/(Cx**2 + Cz**2),
                q2[2],
            ])



            M_y_1 = np.array(nixx(0,L)).dot(q_loc)*(-E_1*I_y)
            M_y_2 = np.array(nixx(L,L)).dot(q_loc)*(-E_1*I_y)

            V_z_1 = np.array(nixxx(0,L)).dot(q_loc)*(-E_1*I_y)
            V_z_2 = np.array(nixxx(L,L)).dot(q_loc)*(-E_1*I_y)

            # send to static results
            self.core.dbase.add(
                table = '[133:beams:sresu]',
                cols  = '[id],[lcase],[N_x_1],[N_x_2],[M_y_1],[M_y_2],[V_z_1],[V_z_2]',
                data  = (id, self.lcase, N_x, N_x, M_y_1, M_y_2, V_z_1, V_z_2),
            )