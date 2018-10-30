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
            [TS].[id],
            [N1].[noG],
            [N2].[noG],
            [TS].[L],
            [TS].[ΔX],
            [TS].[ΔY],
            [TS].[ΔZ],
            [CS].[A],
            [MT].[E_1]
        FROM [121:truss:topos]      AS [TS]
        LEFT JOIN [111:nodes:optim] AS [N1] ON [TS].[n1]   = [N1].[id]
        LEFT JOIN [111:nodes:optim] AS [N2] ON [TS].[n2]   = [N2].[id]
        LEFT JOIN [021:usec1:value] AS [CS] ON [TS].[sect] = [CS].[id]
        LEFT JOIN [011:mates:umate] AS [MT] ON [CS].[mate] = [MT].[id]
        ''')

        # loop over elements
        for element in elements:
            # create local eye of matrix
            kg11 = self._k_loc_g(element)

            # unpack db data
            id,n1,n2 = element[:3]

            # assembly local matrix to global stif matrix
            self.prog._K_assembly(n1, n1,  kg11)
            self.prog._K_assembly(n1, n2, -kg11)
            self.prog._K_assembly(n2, n1, -kg11)
            self.prog._K_assembly(n2, n2,  kg11)



    #$$$ deg -k-loc-g
    def _k_loc_g(self, element):
        '''
        The method can build stifness in global coors or call to _k_loc and matrix dot cosinus matrix.
        '''
        # check system
        system_space = self.core.mdata.setts.get('system_space')

        # unpack element
        id,n1,n2,L,Δx,Δy,Δz,A,E_1 = element

        # calculate sin,cos itd
        Cx, Cy, Cz = Δx/L, Δy/L, Δz/L

        # block dof in extended system
        k0 = 10**-10 # TODO: what number?

        # if-block as system_space
        # plain truss
        if system_space == '2t':
            kg11 = E_1 * A / L * np.array(
                [[+Cx*Cx, +Cx*Cz],
                 [+Cx*Cz, +Cz*Cz]])

        # space truss
        elif system_space == '3t':
            kg11 = E_1 * A / L * np.array(
                [[+Cx*Cx, +Cx*Cy, +Cx*Cz],
                 [+Cx*Cy, +Cy*Cy, +Cy*Cz],
                 [+Cx*Cz, +Cy*Cz, +Cz*Cz]])

        # plain truss
        elif system_space == '2d':
            kg11 = E_1 * A / L * np.array(
                [[+Cx*Cx, +Cx*Cz, 0],
                 [+Cx*Cz, +Cz*Cz, 0],
                 [0,           0, k0]])

        # spaece truss
        elif system_space == '3d':
            kg11 = E_1 * A / L * np.array(
                [[+Cx*Cx, +Cx*Cy, +Cx*Cz,  0,  0,  0],
                 [+Cx*Cy, +Cy*Cy, +Cy*Cz,  0,  0,  0],
                 [+Cx*Cz, +Cy*Cz, +Cz*Cz,  0,  0,  0],
                 [     0,      0,      0, k0,  0,  0],
                 [     0,      0,      0,  0, k0,  0],
                 [     0,      0,      0,  0,  0, k0]])

        # return local stiffness in global coors
        return kg11


class postr:
    '''
    Post results
    '''

    def __init__(self, core, prog, lcase):
        self.core = core
        self.prog = prog
        self.lcase = lcase

        self._forces()


    def _forces(self):

        # get elements from database
        elements = self.core.dbase.get('''
        SELECT
            [TS].[id],
            [TS].[L],
            [TS].[ΔX],
            [TS].[ΔY],
            [TS].[ΔZ],
            [N1].[noG],
            [N1].[id],
            [N2].[noG],
            [N2].[id],
            [CS].[A],
            [MT].[E_1]
        FROM [121:truss:topos]      AS [TS]
        LEFT JOIN [111:nodes:optim] AS [N1] ON [TS].[n1]   = [N1].[id]
        LEFT JOIN [111:nodes:optim] AS [N2] ON [TS].[n2]   = [N2].[id]
        LEFT JOIN [021:usec1:value] AS [CS] ON [TS].[sect] = [CS].[id]
        LEFT JOIN [011:mates:umate] AS [MT] ON [CS].[mate] = [MT].[id]
        ''')

        # loop over elements
        for element in elements:

            id, L, Δx, Δy, Δz, n1, n1id, n2, n2id, A, E_1 = element

            q1 = self.core.dbase.get(f'''
            SELECT
                [dx],
                [dy],
                [dz]
            FROM [113:nodes:sresu] WHERE [lcase]="{self.lcase}" AND [node]="{n1id}"
            ''')[0]

            # second node, look upper comment
            q2 = self.core.dbase.get(f'''
            SELECT
                [dx],
                [dy],
                [dz]
            FROM [113:nodes:sresu] WHERE [lcase]="{self.lcase}" AND [node]="{n2id}"
            ''')[0]

            # calculate sin,cos itd
            Cx, Cy, Cz = Δx/L, Δy/L, Δz/L

            # vector of local displacement sorted like dofs
            q_loc  = [val if val is not None else 0 for val in q1]
            q_loc += [val if val is not None else 0 for val in q2]

            # change of length
            ΔL = np.array([-Cx, -Cy, -Cz, Cx, Cy, Cz]).dot(q_loc)

            # strain of element
            ε_x = ΔL/L

            # stress in element
            σ_x = E_1 * ε_x

            # axial force
            N_x = σ_x * A

            # send to static results
            self.core.dbase.add(
                table = '[123:truss:sresu]',
                cols  = '[id],[lcase],[N],[ΔL],[ε_x]',
                data  = (id, self.lcase, N_x, ΔL, ε_x),
            )

            # send to design results
            self.core.dbase.add(
                table = '[124:truss:desig]',
                cols  = '[id],[lcase],[σ_x]',
                data  = (id, self.lcase, σ_x),
            )




