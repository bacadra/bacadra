import numpy as np

np.set_printoptions(suppress=True)

#$ ____ class statx ________________________________________________________ #

class statx:
    #$$ def --init--
    def __init__(self, core):
        self.core = core

        self._ndof     = None # dof of single node
        self._ndof_sum = None # summary dof in system
        self._ldof     = []   # list of single node dof True/False
        self._cdof     = []   # list of constraint dof -> supports

        self._K_stif   = None # stiffness matrix
        self._F_load   = None # load vector
        self._Q_disp   = None # displacement vector
        self._R_reac   = None # reaction vector


    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass


#$$ ________ static analysis _______________________________________________ #

#$$$ ____________ def build ________________________________________________ #

    def build(self, grp=None):
        '''
        Build system to static analysis. The dof system depending on system type are activated, global numeration of nodes establishing and stiffness matrix of system builded. Boundary conditions are apply to K matrix.
        '''

        # active dof to actual system
        self._dof_active()

        # create glboal numbering of nodes
        self._create_noG()

        # first we need to estimate dof count
        self._estimate_ndof()

        # set the complete stiffnes matrix
        self._K_summary()

        # set boundary condition
        self._bc_K()


#$$$ ____________ def solve ________________________________________________ #

    def solve(self, lcase):
        '''
        Solve system depending on load cases. lcase can be input as id (int, str) or list or range. In second and third case the loop over cases have place.

        Load vector is builded, then boundary condition to load vector applied, next step is solve the static system K*q=F, next one reactions R=K_f*q-F_f wher K_f and F_f are system without boundary condition. Postevaluate of force and some other paramaters done too.
        '''

        # check if system is crated
        if self._K_stif is None:
            raise ValueError('At first build the system with method obj.build()')

        # check type of lcase argument
        type_lcase = type(lcase)

        # if lcase is input as single lc
        if type_lcase in [int, str]:
            # set the complete vector
            self._F_sumary(lcase=lcase)

            # boundary condition on load vector
            self._bc_F()

            # calc displacement vector
            self._displacement()

            # calc reactions
            self._reactions()

            # store results
            # self._store_RQ(lcase=lcase)

            # post evaluating
            # TODO: postevaluate should better work after static, then can download full table of results and work, hmm
            # self._posts(lcase=lcase)

        # if lcase is input as list
        elif type_lcase == list:
            # then loop over arguments
            for lcase_unpack in lcase:
                self.solve(lcase_unpack)

        # if lcase is input as range
        elif type_lcase == range:
            # then return self as list, so in result loop over arguments
            self.solve(list(lcase))


#$$ ________ optimize ______________________________________________________ #

#$$$ ____________ def -dof-active __________________________________________ #

    def _dof_active(self):
        '''
        Set the correct list of dof and calculate count of dof in system.
        '''

        # dof list pattern:
        # [DX, DY, DZ, RX, RY, RZ, RW]

        # get the settings about dof system
        system_dof = self.core.mdata.setts.get('system_dof')

        if type(system_dof) is list:
            self._ldof = system_dof

        elif system_dof == '2t':
            # planar truss
            self._ldof = ['dx','dz']

        elif system_dof == '3t':
            # space truss
            self._ldof = ['dx','dy','dz']

        elif system_dof == '2d':
            # planar beams
            self._ldof = ['dx','dz','ry']

        elif system_dof == '3d':
            # space beams
            self._ldof = ['dx','dy','dz','rx','ry','rz']

        elif system_dof == '3d7':
            # space beams with warping dof
            self._ldof = ['dx','dy','dz','rx','ry','rz','rw']

        elif system_dof == 'ss':
            # plain stress
            self._ldof = ['dx','dz','rz']

        elif system_dof == 'sn':
            # plain strain
            self._ldof = ['dx','dz','rz']

        elif system_dof == 'as':
            # axial symetry
            self._ldof = ['dx','dz','rz']

        else:
            raise ValueError('The unknown dof system')

        self._ndof = len(self._ldof)




#$$$ ____________ def -create-noG___________________________________________ #

    def _create_noG(self):
        '''
        Optimize nodes numbering. Create noG rows in topoz table.
        '''

        nodes = self.core.dbase.get('SELECT [id] FROM [111:nodes:topos]')

        # TODO: optimize numbering
        # now the optimize is in sort order number ...

        noG = 0
        for node in nodes:
            self.core.dbase.add(
                table = '[111:nodes:optim]',
                cols  = '[id],[noG]',
                data  = (node[0], noG)
            )
            noG += 1

#$$$ ____________ def -estimate-ndof _______________________________________ #

    def _estimate_ndof(self):
        '''
        Estimate count of nodal degree of freedom of our structure. Get the max node number in actual building.
        '''

        self.max_node_noG = self.core.dbase.get('''
        SELECT max([noG]) FROM [111:nodes:optim]
        ''')[0][0]

        # TODO: variable size of cell or autodefine dof size
        # +1 because matrix start from 0
        self._ndof_sum = self._ndof * (self.max_node_noG+1)

#$$ ________ stiffness matrix ______________________________________________ #

#$$$ ____________ def -K-summary ___________________________________________ #

    def _K_summary(self):
        '''
        Create stiffeness matrix. A method call to other methods to build subsquently stiffnes.
        '''

        # TODO: create solver for sparse matrix

        # init stiffness matrix
        self._K_stif = np.zeros((self._ndof_sum, self._ndof_sum))

        # call method to different type of elements
        self._K_truss() # +truss
        self._K_beams() # +beams

        # create copy of K matrix, because in next step we need to calculate reactions ...
        self._K_free = self._K_stif.copy()


#$$$ ____________ def -K-assembly __________________________________________ #

    def _K_assembly(self, n1, n2, kg11, kg12, kg22):

        # assembly local matrix to global stif matrix
        # upper left
        self._K_stif[
            n1*self._ndof:n1*self._ndof+self._ndof,
            n1*self._ndof:n1*self._ndof+self._ndof] += kg11

        # upper right
        self._K_stif[
            n1*self._ndof:n1*self._ndof+self._ndof,
            n2*self._ndof:n2*self._ndof+self._ndof] += kg12

        # bottom left as transposed upper right
        self._K_stif[
            n2*self._ndof:n2*self._ndof+self._ndof,
            n1*self._ndof:n1*self._ndof+self._ndof] += kg12.T

        # bottom right
        self._K_stif[
            n2*self._ndof:n2*self._ndof+self._ndof,
            n2*self._ndof:n2*self._ndof+self._ndof] += kg22

        # print(kg11,kg12,kg12.T,kg22)


    def _kg_assembly(self, size, kg11, kg12, kg22):
        kg_stif = np.zeros((size,size))
        siz2 = int(size/2)
        kg_stif[0:siz2, 0:siz2]       += kg11
        kg_stif[siz2:size, 0:siz2]    += kg12
        kg_stif[0:siz2, siz2:size]    += kg12.T
        kg_stif[siz2:size, siz2:size] += kg22

        # def check_symmetric(a, tol=1e-8):
        #     return np.allclose(a, a.T, atol=tol)

        # print(check_symmetric(kg_stif))
        print(kg_stif)
        return kg_stif




#$$$ ____________ def -K-truss _____________________________________________ #

    def _K_truss(self):
        '''
        Create stiffnes matrix of truss elements.
        '''

        # get elements from database
        trusses = self.core.dbase.get('''
        SELECT
            [TS].[id],
            [TS].[L],
            [TS].[ΔX],
            [TS].[ΔY],
            [TS].[ΔZ],
            [N1].[noG],
            [N2].[noG],
            [CS].[A],
            [MT].[E_1]
        FROM [121:truss:topos]      AS [TS]
        LEFT JOIN [111:nodes:optim] AS [N1] ON [TS].[n1]   = [N1].[id]
        LEFT JOIN [111:nodes:optim] AS [N2] ON [TS].[n2]   = [N2].[id]
        LEFT JOIN [021:usec1:value] AS [CS] ON [TS].[sect] = [CS].[id]
        LEFT JOIN [011:mates:umate] AS [MT] ON [CS].[mate] = [MT].[id]
        ''')

        for truss in trusses:
            # unpack db data
            id,L,Δx,Δy,Δz,n1,n2,A,E_1 = truss

            # create local eye of matrix
            kg11 = self._kg_truss(E_1, A, L, Δx, Δy, Δz)

            # assembly local matrix to global stif matrix
            self._K_assembly(n1,n2,kg11,-kg11,kg11)



    def _kg_truss(self, E_1, A, L, Δx, Δy, Δz):

        # check system
        system = self.core.mdata.setts.get('system_dof')

        # calculate sin,cos itd
        Cx, Cy, Cz = Δx/L, Δy/L, Δz/L

        if system == '2t':
            kg11 = E_1 * A / L * np.array(
                [[+Cx*Cx, +Cx*Cz],
                 [+Cx*Cz, +Cz*Cz]])

        elif system == '3t':
            kg11 = E_1 * A / L * np.array(
                [[+Cx*Cx, +Cx*Cy, +Cx*Cz],
                 [+Cx*Cy, +Cy*Cy, +Cy*Cz],
                 [+Cx*Cz, +Cy*Cz, +Cz*Cz]])

        elif system == '2d':
            kg11 = E_1 * A / L * np.array(
                [[+Cx*Cx, +Cx*Cz, 0],
                 [+Cx*Cz, +Cz*Cz, 0],
                 [0,           0, 0]])

        elif system == '3d':
            kg11 = E_1 * A / L * np.array(
                [[+Cx*Cx, +Cx*Cy, +Cx*Cz, 0, 0, 0],
                 [+Cx*Cy, +Cy*Cy, +Cy*Cz, 0, 0, 0],
                 [+Cx*Cz, +Cy*Cz, +Cz*Cz, 0, 0, 0],
                 [     0,      0,      0, 0, 0, 0],
                 [     0,      0,      0, 0, 0, 0],
                 [     0,      0,      0, 0, 0, 0]])

        return kg11

#$$$ ____________ def -K-beams _____________________________________________ #

    def _K_beams(self):
        '''
        Create stiffness matrix of beams elements.
        '''

        # get elements from database
        beams = self.core.dbase.get('''
        SELECT
            [BM].[id],
            [BM].[L],
            [BM].[ΔX],
            [BM].[ΔY],
            [BM].[ΔZ],
            [N1].[noG],
            [N2].[noG],
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

        for beam in beams:
            # unpack db data
            id,L,Δx,Δy,Δz,n1,n2,A,I_t,I_y,I_z,E_1,G_1 = beam

            # create local eye of matrix
            kg11,kg12,kg22 = self._kg_beams(
                Δx, Δy, Δz, L, E_1, A, I_y, I_z, I_t, G_1)

            # assembly local matrix to global stif matrix
            self._K_assembly(n1,n2,kg11,kg12,kg22)


    def _kg_beams(self, Δx, Δy, Δz, L, E_1, A, I_y, I_z, I_t, G_1):

        # check system
        system = self.core.mdata.setts.get('system_dof')

        if system == '2t':
            raise ValueError('Element type error. The actual system does not provide rotational dof')

        elif system == '3t':
            raise ValueError('Element type error. The actual system does not provide rotational dof')

        elif system == '2d':
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
             [-Cz*EIL2, Cx*EIL2, EIL1]
            ])

            # create right upper
            kg12 = np.array([
             [-Cx2*EAL - Cz2*EIL3, -Cxz*EAL + Cxz*EIL3, -Cz*EIL2],
             [-Cxz*EAL + Cxz*EIL3, -Cz2*EAL - Cx2*EIL3, Cx*EIL2],
             [Cz*EIL2, -Cx*EIL2, EIL0]
            ])

            # create right down part
            kg22 = np.array([
             [Cx2*EAL + Cz2*EIL3, Cxz*EAL - Cxz*EIL3, Cz*EIL2],
             [Cxz*EAL - Cxz*EIL3, Cz2*EAL + Cx2*EIL3, -Cx*EIL2],
             [Cz*EIL2, -Cx*EIL2, EIL1]
            ])

        elif system == '3d':
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

        return kg11,kg12,kg22



#$$ ________ load vector ___________________________________________________ #

#$$$ ____________ def -F-summary ___________________________________________ #

    def _F_sumary(self, lcase):
        '''
        Create the load vector. Building of load vector is depened on load case loading. The boundary condition are also apply on load vector.
        '''

        # init 1d vector for loads
        # 1d vector is not horizontal and not vertical, just 1d
        # we can multiply array * 1d vector and we get 1d vector (only if cols count of matrix and element count in vector is the same)
        self._F_load = np.zeros(self._ndof_sum)

        # add loads from nodes and elemenets
        self._F_nodes(lcase)

        # create copy of F vector, because in next step we need to calculate reactions ...
        self._F_free = self._F_load.copy()



#$$$ ____________ def -F-nodes _____________________________________________ #

    def _F_nodes(self, lcase):
        '''
        Get nodal loads.
        '''

        # TODO: kinematic loads is inactive
        # get elements from database
        loads = self.core.dbase.get(f'''
        SELECT
            [NZ].[noG],
            [NZ].[id],
            [px],
            [py],
            [pz]
            [mz]
        FROM [112:nodes:loads]      as [NL]
        LEFT JOIN [111:nodes:optim] as [NZ] ON [NL].[node] = [NZ].[id]
        WHERE [lcase] = "{lcase}"
        ''')

        def prwarn(dof, node_id):
            # print warning
            print(f'warning bc-dof-102:\nThe loads at node {node_id} is noneffective, because global {dof} dof is inactive')

        for load in loads:
            # unpack row from db
            noG,node_id,px,py,pz = load
            # base dof number
            adof = noG * self._ndof

            # load pattern
            # here must be if (no elif) because user can add load in few directions in one statment

            if px:
                if 'dx' in self._ldof:
                    self._F_load[adof + self._ldof.index('dx')] += px
                else:
                    prwarn('dx',node_id)

            if py:
                if 'dy' in self._ldof:
                    self._F_load[adof + self._ldof.index('dy')] += py
                else:
                    prwarn('dy',node_id)

            if pz:
                if 'dz' in self._ldof:
                    self._F_load[adof + self._ldof.index('dz')] += pz
                else:
                    prwarn('dz',node_id)

            # if mx:
            #     if 'rx' in self._ldof:
            #         self._F_load[adof + self._ldof.index('rx')] += mx
            #     else:
            #         prwarn('rx',node_id)
            #
            # if my:
            #     if 'ry' in self._ldof:
            #         self._F_load[adof + self._ldof.index('ry')] += my
            #     else:
            #         prwarn('ry',node_id)
            #
            # if mz:
            #     if 'rz' in self._ldof:
            #         self._F_load[adof + self._ldof.index('rz')] += mz
            #     else:
            #         prwarn('rz',node_id)




#$$ ________ boundary condition ____________________________________________ #

#$$$ ____________ def -bc-K ________________________________________________ #

    def _bc_K(self):
        '''
        Set boundary condition on the K matrix.
        '''

        nodes = self.core.dbase.get('''
        SELECT
            [NZ].[noG],
            [NS].[fix],
            [NZ].[id]
        FROM [111:nodes:topos]      as [NS]
        LEFT JOIN [111:nodes:optim] as [NZ] ON [NS].[id] = [NZ].[id]
        WHERE [fix] NOT NULL
        ''')

        # loop over nodes with defined fix
        for node in nodes:
            # unpack row from db
            noG,fix,node_id = node

            # base dof number
            adof = noG * self._ndof

            # divide string
            fix = [fix[i:i+2] for i in range(0, len(fix), 2)]

            # loop over divided string
            for fix1 in fix:

                # parse divided string to adds, return list with additional dof number
                fix_adds = self._bc_pattern(fix1, node_id)
                if fix_adds is None:
                    continue

                for adds in fix_adds:
                    # dof number to block it
                    add1 = adof+adds

                    # add blocked dof to list, it will be used to bc_F and more
                    self._cdof.append(add1)

        self._K11 = np.delete(np.delete(self._K_stif, self._cdof, axis=0),
            self._cdof, axis=1)

        self._K22 = self._K_stif[np.ix_(self._cdof,self._cdof)]

        self._K21 = np.delete(self._K_stif[np.ix_(self._cdof)],
            self._cdof, axis=1)

        self._K12 = self._K21.T



#$$$ ____________ def -bc-F ________________________________________________ #

    def _bc_F(self):
        '''
        Set boundary condition on the F vector.
        '''

        self._F1 = np.delete(self._F_load, self._cdof)
        self._F2 = self._F_load[np.ix_(self._cdof)]

        self._Q2 = np.zeros(len(self._cdof))


#$$$ ____________ def -bc-pattern __________________________________________ #

    def _bc_pattern(self, name, node_id):
        '''
        Additional dof number depend on force load type.
        '''

        def prwarn(name,dof):
            # print warning
            print(f'warning bc-dof-101:\nThe support at node {node_id} is noneffective, because global {dof} dof is inactive')

        # get the settings about dof system
        system_dof = self.core.mdata.setts.get('system_dof')

        # if-block depend on static load type

        if   name == 'F0':
            return []

        elif name == 'PX':
            return [self._ldof.index('dx')]

        elif name == 'PY':
            return [self._ldof.index('dy')]

        elif name == 'PZ':
            return [self._ldof.index('dz')]


        elif name == 'XP':
            return [self._ldof.index('dy'),
                    self._ldof.index('dz')]

        elif name == 'YP':
            return [self._ldof.index('dx'),
                    self._ldof.index('dz')]

        elif name == 'ZP':
            return [self._ldof.index('dx'),
                    self._ldof.index('dy')]

        elif name == 'PP':
            return [self._ldof.index('dx'),
                    self._ldof.index('dy'),
                    self._ldof.index('dz')]


        elif name == 'MX':
            return [self._ldof.index('rx')]

        elif name == 'MY':
            return [self._ldof.index('ry')]

        elif name == 'MZ':
            return [self._ldof.index('rz')]


        elif name == 'XM':
            return [self._ldof.index('ry'),
                    self._ldof.index('rz')]

        elif name == 'YM':
            return [self._ldof.index('rx'),
                    self._ldof.index('dz')]

        elif name == 'ZM':
            return [self._ldof.index('rx'),
                    self._ldof.index('ry')]

        elif name == 'MM':
            return [self._ldof.index('rx'),
                    self._ldof.index('ry'),
                    self._ldof.index('rz')]

        elif name == 'FF':
            return [self._ldof.index('dx'),
                    self._ldof.index('dy'),
                    self._ldof.index('dz'),
                    self._ldof.index('rx'),
                    self._ldof.index('ry'),
                    self._ldof.index('rz')]

        else:
            raise ValueError('Unknow boundary condition name')







#$$ ________ post-evaluate _________________________________________________ #

#$$$ ____________ def -displacement ________________________________________ #

    def _displacement(self):
        '''
        Calculate node displacement as result of system solve.
        '''
        # set displacement vector
        self._Q1 = np.linalg.solve(self._K11, self._F1 - self._K12.dot(self._Q2))


#$$$ ____________ def -reactions ____________________________________________ #

    def _reactions(self):
        '''
        Calculate reaction in supports.
        '''

        # calculate reaction depend on unconstrained K and F data
        self._F2 = self._K21.dot(self._Q1) + self._K22.dot(self._Q2)


#$$$ ____________ def -store-db ____________________________________________ #

    def _store_RQ(self, lcase):
        '''
        Store calculated data in db.
        '''

        cols,ndata=self._store_check()

        for noG in range(self.max_node_noG+1):

            adof = noG*self._ndof
            # TODO: get all elements at one kwerend, then get from matrix
            # find id of node
            id = self.core.dbase.get(f'''
                SELECT [id] FROM [111:nodes:optim] WHERE [noG] = {noG}
            ''')[0][0]

            cols,data = self._storeloc(
                cols  = cols,
                ndata = ndata,
                lcase = lcase,
                id    = id,
                adof  = adof)

            self.core.dbase.add(
                table = '[113:nodes:sresu]',
                cols  = cols,
                data  = data,
            )

    def _store_check(self):
        '''
        Check dof of system and return cols
        '''

        cols = '[lcase],[node],'
        for disp in self._ldof:
            if   disp == 'dx': cols += '[px],[dx],'
            elif disp == 'dy': cols += '[py],[dy],'
            elif disp == 'dz': cols += '[pz],[dz],'
            elif disp == 'rx': cols += '[mx],[rx],'
            elif disp == 'ry': cols += '[my],[ry],'
            elif disp == 'rz': cols += '[mz],[rz],'
        ndata = int(cols.count(',')/2)-1
        cols  = cols[:-1]
        return cols, ndata


    def _storeloc(self, cols,ndata,lcase,id,adof):
        '''
        Generate input data
        '''

        data = tuple([lcase,id] + [x for i in range(ndata) for x in (self._R_reac[adof+i],self._Q_disp[adof+i])])

        # data  = tuple(x for i in range(ndata) for x in (self._R_reac[adof+i],self._Q_disp[adof+i]))

        return cols,data






#$$ ________ post analysis _________________________________________________ #

#$$$ ____________ def -posts _______________________________________________ #

    def _posts(self, lcase):
        self._p_truss(lcase=lcase)
        self._p_beams(lcase=lcase)


#$$$ ____________ def -s-truss _____________________________________________ #

    def _p_truss(self, lcase):
        trusses = self.core.dbase.get('''
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


        for truss in trusses:

            id, L, Δx, Δy, Δz, n1, n1id, n2, n2id, A, E_1 = truss

            # first node, must return only one node
            # TODO: validate return of 1 node
            q1 = self.core.dbase.get(f'''
            SELECT
                [dx],
                [dy],
                [dz]
            FROM [113:nodes:sresu] WHERE [lcase]="{lcase}" AND [node]="{n1id}"
            ''')[0]

            # second node, look upper comment
            q2 = self.core.dbase.get(f'''
            SELECT
                [dx],
                [dy],
                [dz]
            FROM [113:nodes:sresu] WHERE [lcase]="{lcase}" AND [node]="{n2id}"
            ''')[0]

            # calculate sin,cos itd
            Cx, Cy, Cz = Δx/L, Δy/L, Δz/L

            # change of length
            if self.core.mdata.setts.get('system_dof') in ['2t','2d']:
                # vector of local displacement sorted like dofs
                q_loc = np.array([q1[0], q1[2], q2[0], q2[2]])
                print(q_loc)

                # change of length
                ΔL = np.array([-Cx, -Cz, Cx, Cz]).dot(q_loc)


            elif self.core.mdata.setts.get('system_dof') in ['3t','3d','3d7']:
                # vector of local displacement sorted like dofs
                q_loc = np.array([q1[0], q1[1], q1[2], q2[0], q2[1], q2[2]])

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
                data  = (id, lcase, N_x, ΔL, ε_x),
            )

            # send to design results
            self.core.dbase.add(
                table = '[124:truss:desig]',
                cols  = '[id],[lcase],[σ_x]',
                data  = (id, lcase, σ_x),
            )


#$$$ ____________ def -s-beams _____________________________________________ #

    def _p_beams(self, lcase):
        beams = self.core.dbase.get('''
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


        for beam in beams:
            # unpack db data
            id,L,Δx,Δy,Δz,n1,n1id,n2,n2id,A,I_t,I_y,I_z,E_1,G_1 = beam

            # first node, must return only one node
            # TODO: validate return of 1 node
            q1 = self.core.dbase.get(f'''
            SELECT
                [dx],
                [dy],
                [dz],
                [rx],
                [ry],
                [rz]
            FROM [113:nodes:sresu] WHERE [lcase]="{lcase}" AND [node]="{n1id}"
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
            FROM [113:nodes:sresu] WHERE [lcase]="{lcase}" AND [node]="{n2id}"
            ''')[0]


            # vector of local displacement sorted like dofs
            q_loc = np.append(q1,q2)

            kg11,kg12,kg22 = self._kg_beams(Δx, Δy, Δz,
                L, E_1, A, I_y, I_z, I_t, G_1)

            kg = self._kg_assembly(len(q_loc), kg11, kg12, kg22)



            # print(q_loc)
            forces = kg.dot(q_loc)

            data = tuple(np.append(np.array([id,lcase]), forces))

            # send to static results
            self.core.dbase.add(
                table = '[133:beams:sresu]',
                cols  = '[id],[lcase],[N_1],[V_y_1],[V_z_1],[M_x_1],[M_y_1],[M_z_1],[N_2],[V_y_2],[V_z_2],[M_x_2],[M_y_2],[M_z_2]',
                data  = data
            )





            # change of length
            if self.core.mdata.setts.get('system_dof') in ['2d']:
                pass
                # # vector of local displacement sorted like dofs
                # q_loc = np.array([q1[0],q1[2],q1[4],q2[0],q2[2],q2[4]])
                #
                # # create local eye of matrix
                # kg11,kg12,kg22 = self._kg_beams(
                #     Δx, Δy, Δz, L, E_1, A, I_y, I_z, I_t, G_1)
                #
                # kg = self._kg_assembly(len(q_loc), kg11, kg12, kg22)
                #
                # # calculate sin,cos itd
                # Cx,  Cz       = Δx/L   , Δz/L
                # Cx2, Cz2, Cxz = Cx**2  , Cz**2 , Cx*Cz
                #
                # C = np.array([[Cx, Cz, 0, 0, 0, 0],
                #               [-Cz, Cx, 0, 0, 0, 0],
                #               [0, 0, 1, 0, 0, 0],
                #               [0, 0, 0, Cx, Cz,  0]
                #               [0, 0, 0, -Cz, Cx,  0],
                #               [0, 0, 0, Cx, Cz,  0]]
                #               )
                #
                #
                # forces = kg.dot(q_loc)
                #
                # data = tuple(np.append(np.array([id,lcase]), forces))
                #
                # # send to static results
                # self.core.dbase.add(
                #     table = '[133:beams:sresu]',
                #     cols  = '[id],[lcase],[N_1],[V_z_1],[M_y_1],[N_2],[V_z_2],[M_y_2]',
                #     data  = data,
                # )



            elif self.core.mdata.setts.get('system_dof') in ['3d','3d7']:

                # vector of local displacement sorted like dofs
                q_loc = np.append(q1,q2)

                kg11,kg12,kg22 = self._kg_beams(Δx, Δy, Δz, L, E_1, A, I_y, I_z, I_t, G_1)

                kg = self._kg_assembly(len(q_loc), kg11, kg12, kg22)

                # additional length of projected y-versor
                # Lxy = (Δx**2+Δy**2)**0.5
                #
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
                #
                # C = np.array([
                #     [cxx, cyx, czx, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                #     [cxy, cyy, czy, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                #     [cxz, cyz, czz, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                #     [0, 0, 0, cxx, cyx, czx, 0, 0, 0, 0, 0, 0],
                #     [0, 0, 0, cxy, cyy, czy, 0, 0, 0, 0, 0, 0],
                #     [0, 0, 0, cxz, cyz, czz, 0, 0, 0, 0, 0, 0],
                #     [0, 0, 0, 0, 0, 0, cxx, cyx, czx, 0, 0, 0],
                #     [0, 0, 0, 0, 0, 0, cxy, cyy, czy, 0, 0, 0],
                #     [0, 0, 0, 0, 0, 0, cxz, cyz, czz, 0, 0, 0],
                #     [0, 0, 0, 0, 0, 0, 0, 0, 0, cxx, cyx, czx],
                #     [0, 0, 0, 0, 0, 0, 0, 0, 0, cxy, cyy, czy],
                #     [0, 0, 0, 0, 0, 0, 0, 0, 0, cxz, cyz, czz]
                #     ])

                # # print(q_loc)
                # forces = kg.dot(q_loc)
                #
                # data = tuple(np.append(np.array([id,lcase]), forces))
                #
                # # send to static results
                # self.core.dbase.add(
                #     table = '[133:beams:sresu]',
                #     cols  = '[id],[lcase],[N_1],[V_y_1],[V_z_1],[M_x_1],[M_y_1],[M_z_1],[N_2],[V_y_2],[V_z_2],[M_x_2],[M_y_2],[M_z_2]',
                #     data  = data
                # )

                # bending moment
                # M_y_1 = E_1 * I_y / L * (4*q1[4]+2*q2[4]-6*(q2[2]-q1[2])/L)
                # M_y_2 = E_1 * I_y / L * (4*q2[4]+2*q1[4]-6*(q2[2]-q1[2])/L)

            # elif self.core.mdata.setts.get('system_dof') in ['3d','3d7']:
            #     # vector of local displacement sorted like dofs
            #     q_loc = np.array([q1[0], q1[1], q1[2], q2[0], q2[1], q2[2]])
            #
            #     # change of length
            #     ΔL = np.array([-Cx, -Cy, -Cz, Cx, Cy, Cz]).dot(q_loc)



            #
            # # axial strain of element
            # ε_x_N = ΔL/L
            #
            # # axial stress in element
            # σ_x_N = E_1 * ε_x_N
            #
            # # axial force
            # N_x = σ_x_N * A


            # # send to static results
            # self.core.dbase.add(
            #     table = '[133:beams:sresu]',
            #     cols  = '[id],[lcase],[N_1],[ΔL],[ε_x_N]',
            #     data  = (id, lcase, N_x, ΔL, ε_x_N),
            # )
            #
            # # send to design results
            # self.core.dbase.add(
            #     table = '[134:beams:desig]',
            #     cols  = '[id],[lcase],[σ_x_N]',
            #     data  = (id, lcase, σ_x_N),
            # )






