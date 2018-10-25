import numpy as np
np.set_printoptions(suppress=True, precision=5)

#$ ____ class static _______________________________________________________ #

class static:
    #$$ def --init--
    def __init__(self, dbase, pinky, pvars):
        self.dbase = dbase
        self.pinky = pinky
        self.pvars = pvars

        self._ndof     = None # dof of single node
        self._ldof     = []   # list of single node dof True/False
        self._ndof_sum = None # summary dof in system
        self._cdof     = [] # list of constraint dof -> supports

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

    def build(self):
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
            self._store_RQ(lcase=lcase)

            # post evaluating
            # TODO: postevaluate should better work after static, then can download full table of results and work, hmm
            self._posts(lcase=lcase)

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

#$$$ ____________ def dof-active ___________________________________________ #

    def _dof_active(self):
        '''
        Set the correct list of dof and calculate count of dof in system.
        '''

        # dof list pattern:
        # [DX, DY, DZ, RX, RY, RZ, RW]

        # get the settings about dof system
        system_dof = self.pvars.get('system_dof')

        if type(system_dof) is list:
            self._ldof = system_dof

        elif system_dof == '2t':
            # planar truss
            self._ldof = [True,  True,  False, False, False, False, False]

        elif system_dof == '3t':
            # space truss
            self._ldof = [True,  True,  True,  False, False, False, False]

        elif system_dof == '2d':
            # planar beams
            self._ldof = [True,  True,  False, False, False, False, True ]

        elif system_dof == '3d':
            # space beams
            self._ldof = [True,  True,  True,  True,  True,  True,  False]

        elif system_dof == '3d7':
            # space beams with warping dof
            self._ldof = [True,  True,  True,  True,  True,  True,  True ]

        else:
            raise ValueError('The unknown dof system')

        self._ndof = self._ldof.count(True)




#$$$ ____________ def -create-noG___________________________________________ #

    def _create_noG(self):
        '''
        Optimize nodes numbering. Create noG rows in topoz table.
        '''

        nodes = self.dbase.get('SELECT [id] FROM [111:nodes:topos]')

        # TODO: optimize numbering
        # now the optimize is in sort order number ...

        noG = 0
        for node in nodes:
            self.dbase.add(
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

        self.max_node_noG = self.dbase.get('''
        SELECT max([noG]) FROM [111:nodes:optim]
        ''')[0][0]

        # TODO: variable size of cell or autodefine dof size
        self._ndof_sum = self._ndof * (self.max_node_noG+1)

#$$ ________ stiffness matrix ______________________________________________ #

#$$$ ____________ def -K-summary ___________________________________________ #

    def _K_summary(self):
        '''
        Create stiffeness matrix. A method call to other methods to build subsquently stiffnes.
        '''

        # TODO: create solver for sparse matrix
        # TODO: create method to assembly global matrix

        # init stiffness matrix
        self._K_stif = np.zeros((self._ndof_sum, self._ndof_sum))

        # call method to different type of elements
        self._K_truss() # +truss
        self._K_beams() # +beams

        # create copy of K matrix, because in next step we need to calculate reactions ...
        self._K_free = self._K_stif.copy()

#$$$ ____________ def -K-truss _____________________________________________ #

    def _K_truss(self):
        '''
        Create stiffnes matrix of truss elements.
        '''

        trusses = self.dbase.get('''
        SELECT
            [TS].[id],
            [TS].[L],
            [TS].[delta_X],
            [TS].[delta_Y],
            [TS].[delta_Z],
            [N1].[noG],
            [N2].[noG],
            [CS].[A],
            [CS].[m_g],
            [MT].[E_1],
            [MT].[texp]
        FROM [121:truss:topos]      AS [TS]
        LEFT JOIN [111:nodes:optim] AS [N1] ON [TS].[n1]   = [N1].[id]
        LEFT JOIN [111:nodes:optim] AS [N2] ON [TS].[n2]   = [N2].[id]
        LEFT JOIN [021:usec1:unics] AS [CS] ON [TS].[sect] = [CS].[id]
        LEFT JOIN [011:mates:umate] AS [MT] ON [CS].[mate] = [MT].[id]
        ''')

        def k_local(E_1, A, L, Cx, Cy, Cz):
            if self.pvars.get('system_dof') == '2t':
                # if system is planar truss 2t

                kloc = E_1 * A / L * np.array(
                    [[+Cx*Cx, +Cx*Cy],
                     [+Cx*Cy, +Cy*Cy]])

            elif self.pvars.get('system_dof') == '3t':
                kloc = E_1 * A / L * np.array(
                    [[+Cx*Cx, +Cx*Cy, +Cx*Cz],
                     [+Cx*Cy, +Cy*Cy, +Cy*Cz],
                     [+Cx*Cz, +Cy*Cz, +Cz*Cz]])

            return kloc



        for truss in trusses:
            # unpack db data
            id,L,Δx,Δy,Δz,n1,n2,A,m_g,E_1,texp = truss

            # calculate sin,cos itd
            Cx, Cy, Cz = Δx/L, Δy/L, Δz/L

            # create local eye of matrix
            kg11 = k_local(E_1, A, L, Cx, Cy, Cz)

            # assembly local matrix to global stif matrix
            self._K_stif[
                n1*self._ndof:n1*self._ndof+self._ndof,
                n1*self._ndof:n1*self._ndof+self._ndof] += +kg11

            self._K_stif[
                n1*self._ndof:n1*self._ndof+self._ndof,
                n2*self._ndof:n2*self._ndof+self._ndof] += -kg11

            self._K_stif[
                n2*self._ndof:n2*self._ndof+self._ndof,
                n1*self._ndof:n1*self._ndof+self._ndof] += -kg11

            self._K_stif[
                n2*self._ndof:n2*self._ndof+self._ndof,
                n2*self._ndof:n2*self._ndof+self._ndof] += +kg11



#$$$ ____________ def -K-beams _____________________________________________ #

    def _K_beams6(self):
        beams = self.dbase.get('''
        SELECT
            [BM].[id],
            [BM].[L],
            [BM].[delta_X],
            [BM].[delta_Y],
            [N1].[noG],
            [N2].[noG],
            [CS].[A],
            [CS].[I_y],
            [MT].[E_1]
        FROM [131:beams:topos]      AS [BM]
        LEFT JOIN [111:nodes:optim] AS [N1] ON [BM].[n1]   = [N1].[id]
        LEFT JOIN [111:nodes:optim] AS [N2] ON [BM].[n2]   = [N2].[id]
        LEFT JOIN [021:usec1:unics] AS [CS] ON [BM].[sect] = [CS].[id]
        LEFT JOIN [011:mates:umate] AS [MT] ON [CS].[mate] = [MT].[id]
        ''')

        for beam in beams:
            # unpack db data
            id,L,Δx,Δy,n1,n2,A,I_y,E_1 = beam

            # calculate sin,cos itd
            Cx,  Cy       = Δx/L   , Δy/L
            Cx2, Cy2, Cxy = Cx**2  , Cy**2 , Cx*Cy

            # calculate paramaeters for kg_local
            EAL  = (      E_1 * A   / L   )
            EIL3 = (12  * E_1 * I_y / L**3)
            EIL2 = (6   * E_1 * I_y / L**2)
            EIL1 = (4   * E_1 * I_y / L   )
            EIL0 = (2   * E_1 * I_y / L   )


            # create left upper part
            kg11 = np.array([
             [Cx2*EAL + Cy2*EIL3, Cxy*EAL - Cxy*EIL3, -Cy*EIL2],
             [Cxy*EAL - Cxy*EIL3, Cy2*EAL + Cx2*EIL3, Cx*EIL2],
             [-Cy*EIL2, Cx*EIL2, EIL1]
            ])

            # create right upper
            kg12 = np.array([
             [-Cx2*EAL - Cy2*EIL3, -Cxy*EAL + Cxy*EIL3, -Cy*EIL2],
             [-Cxy*EAL + Cxy*EIL3, -Cy2*EAL - Cx2*EIL3, Cx*EIL2],
             [Cy*EIL2, -Cx*EIL2, EIL0]
            ])

            # create right upper
            kg21 = np.array([
             [-Cx2*EAL - Cy2*EIL3, -Cxy*EAL + Cxy*EIL3, Cy*EIL2],
             [-Cxy*EAL + Cxy*EIL3, -Cy2*EAL - Cx2*EIL3, -Cx*EIL2],
             [-Cy*EIL2, Cx*EIL2, EIL0]
            ])

            # create right down part
            kg22 = np.array([
             [Cx2*EAL + Cy2*EIL3, Cxy*EAL - Cxy*EIL3, Cy*EIL2],
             [Cxy*EAL - Cxy*EIL3, Cy2*EAL + Cx2*EIL3, -Cx*EIL2],
             [Cy*EIL2, -Cx*EIL2, EIL1]
            ])

            # assembly local matrix to global stif matrix
            self._K_stif[
                n1*self._ndof:n1*self._ndof+self._ndof,
                n1*self._ndof:n1*self._ndof+self._ndof] += +kg11

            self._K_stif[
                n1*self._ndof:n1*self._ndof+self._ndof,
                n2*self._ndof:n2*self._ndof+self._ndof] += kg12

            self._K_stif[
                n2*self._ndof:n2*self._ndof+self._ndof,
                n1*self._ndof:n1*self._ndof+self._ndof] += kg21

            self._K_stif[
                n2*self._ndof:n2*self._ndof+self._ndof,
                n2*self._ndof:n2*self._ndof+self._ndof] += kg22


            # # calculate paramaeters for kg_local
            # EAL  = (      E_1 * A   / L   )
            # EIL3 = (12  * E_1 * I_y / L**3)
            # EIL2 = (6   * E_1 * I_y / L**2)
            # EIL1 = (4   * E_1 * I_y / L   )
            # EIL0 = (2   * E_1 * I_y / L   )
            #
            #
            # # create left upper part
            # kg11 = np.array([
            #  [EAL, 0, 0],
            #  [0, EIL3, EIL2],
            #  [0, EIL2, EIL1]
            # ])
            #
            # # create right upper and left down parts
            # kg12 = np.array([
            #  [-EAL, 0, 0],
            #  [0, -EIL3, EIL2],
            #  [0, -EIL2, EIL0]
            # ])
            #
            # # create right upper and left down parts
            # kg21 = np.array([
            #  [-EAL, 0, 0],
            #  [0, -EIL3, -EIL2],
            #  [0, EIL2, EIL0]
            # ])
            #
            # # create right down part
            # kg22 = np.array([
            #  [EAL, 0, 0],
            #  [0, EIL3, -EIL2],
            #  [0, -EIL2, EIL1]
            # ])
            #
            # # assembly local matrix to global stif matrix
            # self._K_stif[
            #     n1*self._ndof:n1*self._ndof+self._ndof,
            #     n1*self._ndof:n1*self._ndof+self._ndof] += +kg11
            #
            # self._K_stif[
            #     n2*self._ndof:n2*self._ndof+self._ndof,
            #     n1*self._ndof:n1*self._ndof+self._ndof] += kg21
            #
            # self._K_stif[
            #     n1*self._ndof:n1*self._ndof+self._ndof,
            #     n2*self._ndof:n2*self._ndof+self._ndof] += kg12
            #
            # self._K_stif[
            #     n2*self._ndof:n2*self._ndof+self._ndof,
            #     n2*self._ndof:n2*self._ndof+self._ndof] += kg22


#$$$ ____________ def -K-beams _____________________________________________ #

    def _K_beams2(self):
        beams = self.dbase.get('''
        SELECT
            [BM].[id],
            [BM].[L],
            [BM].[delta_X],
            [BM].[delta_Y],
            [N1].[noG],
            [N2].[noG],
            [CS].[A],
            [CS].[I_y],
            [MT].[E_1]
        FROM [131:beams:topos]      AS [BM]
        LEFT JOIN [111:nodes:optim] AS [N1] ON [BM].[n1]   = [N1].[id]
        LEFT JOIN [111:nodes:optim] AS [N2] ON [BM].[n2]   = [N2].[id]
        LEFT JOIN [021:usec1:unics] AS [CS] ON [BM].[sect] = [CS].[id]
        LEFT JOIN [011:mates:umate] AS [MT] ON [CS].[mate] = [MT].[id]
        ''')

        for beam in beams:
            # unpack db data
            id,L,Δx,Δy,n1,n2,A,I_y,E_1 = beam

            # calculate sin,cos itd
            Cx,  Cy       = Δx/L   , Δy/L
            Cx2, Cy2, Cxy = Cx**2  , Cy**2 , Cx*Cy

            # calculate paramaeters for kg_local
            EAL  = ( E_1 * A   / L   )
            EIL3 = ( E_1 * I_y / L**3)
            EIL2 = ( E_1 * I_y / L**2)
            EIL1 = ( E_1 * I_y / L   )
            EIL0 = ( E_1 * I_y / L   )


            # create left upper part
            kg11 = np.array([
             [Cx2* EAL + 3*Cy2* EIL3, Cxy* EAL - 3*Cxy* EIL3, 3*Cy*EIL2],
             [Cxy* EAL - 3*Cxy* EIL3, Cy2* EAL + 3*Cx2* EIL3, -3*Cx*EIL2],
             [3*Cy*EIL2, -3*Cx*EIL2, 4*EIL1]
            ])

            # create right upper
            kg12 = np.array([
             [-Cx2* EAL - 3*Cy2* EIL3, -Cxy* EAL + 3*Cxy* EIL3, 3*Cy*EIL2],
             [-Cxy* EAL + 3*Cxy* EIL3, -Cy2* EAL - 3*Cx2* EIL3, -3*Cx*EIL2],
             [-3*Cy*EIL2, 3*Cx*EIL2, 2*EIL0]
            ])

            # left down parts
            kg21 = np.array([
             [-Cx2* EAL - 3*Cy2* EIL3, -Cxy* EAL + 3*Cxy* EIL3, -3*Cy*EIL2],
             [-Cxy* EAL + 3*Cxy* EIL3, -Cy2* EAL - 3*Cx2* EIL3, 3*Cx*EIL2],
             [3*Cy*EIL2, -3*Cx*EIL2, 2*EIL0]
            ])

            # create right down part
            kg22 = np.array([
             [Cx2* EAL + 3*Cy2* EIL3, Cxy* EAL - 3*Cxy* EIL3, -3*Cy*EIL2],
             [Cxy* EAL - 3*Cxy* EIL3, Cy2* EAL + 3*Cx2* EIL3, 3*Cx*EIL2],
             [-3*Cy*EIL2, 3*Cx*EIL2, 4*EIL1]
            ])

            # assembly local matrix to global stif matrix
            self._K_stif[
                n1*self._ndof:n1*self._ndof+self._ndof,
                n1*self._ndof:n1*self._ndof+self._ndof] += +kg11

            self._K_stif[
                n1*self._ndof:n1*self._ndof+self._ndof,
                n2*self._ndof:n2*self._ndof+self._ndof] += kg12

            self._K_stif[
                n2*self._ndof:n2*self._ndof+self._ndof,
                n1*self._ndof:n1*self._ndof+self._ndof] += kg21

            self._K_stif[
                n2*self._ndof:n2*self._ndof+self._ndof,
                n2*self._ndof:n2*self._ndof+self._ndof] += kg22


#$$$ ____________ def -K-beams-3d __________________________________________ #

    def _K_beams2(self):

        beams = self.dbase.get('''
        SELECT
            [BM].[id],
            [BM].[L],
            [BM].[delta_X],
            [BM].[delta_Y],
            [BM].[delta_z],
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
        LEFT JOIN [021:usec1:unics] AS [CS] ON [BM].[sect] = [CS].[id]
        LEFT JOIN [011:mates:umate] AS [MT] ON [CS].[mate] = [MT].[id]
        ''')

        for beam in beams:
            # unpack db data
            id,L,Δx,Δy,Δz,n1,n2,A,I_t,I_y,I_z,E_1,G_1 = beam

            # calculate sin,cos itd
            Cx,  Cy,  Cz  = Δx/L   , Δy/L  , Δz/L
            Cx2, Cy2, Cxy = Cx**2  , Cy**2 , Cx*Cy

            cxx=1
            cyx=0
            czx=0
            cxy=0
            cyy=1
            czy=0
            cxz=0
            cyz=0
            czz=1

            # calculate paramaeters for kg_local
            EAL  = ( E_1 * A   / L   )
            GKL  = ( G_1 * I_t / L   )

            EIY1 = ( E_1 * I_y / L   )
            EIY2 = ( E_1 * I_y / L**2)
            EIY3 = ( E_1 * I_y / L**3)

            EIZ1 = ( E_1 * I_z / L   )
            EIZ2 = ( E_1 * I_z / L**2)
            EIZ3 = ( E_1 * I_z / L**3)


            def List(*vals):
                return [val for val in vals]


            # create left upper part
            kg11 = np.array(List(List(cxx**2*EAL + 3*cxz**2*EIY3 +
              3*cxy**2*EIZ3,
             cxx*cyx*EAL + 3*cxz*cyz*EIY3 +
              3*cxy*cyy*EIZ3,
             cxx*czx*EAL + 3*cxz*czz*EIY3 +
              3*cxy*czy*EIZ3,
             -3*cxy*cxz*EIY2 + 3*cxy*cxz*EIZ2,
             -3*cxz*cyy*EIY2 + 3*cxy*cyz*EIZ2,
             -3*cxz*czy*EIY2 + 3*cxy*czz*EIZ2),
            List(cxx*cyx*EAL + 3*cxz*cyz*EIY3 +
              3*cxy*cyy*EIZ3,
             cyx**2*EAL + 3*cyz**2*EIY3 +
              3*cyy**2*EIZ3,
             cyx*czx*EAL + 3*cyz*czz*EIY3 +
              3*cyy*czy*EIZ3,
             -3*cxy*cyz*EIY2 + 3*cxz*cyy*EIZ2,
             -3*cyy*cyz*EIY2 + 3*cyy*cyz*EIZ2,
             -3*cyz*czy*EIY2 + 3*cyy*czz*EIZ2),
            List(cxx*czx*EAL + 3*cxz*czz*EIY3 +
              3*cxy*czy*EIZ3,
             cyx*czx*EAL + 3*cyz*czz*EIY3 +
              3*cyy*czy*EIZ3,
             czx**2*EAL + 3*czz**2*EIY3 +
              3*czy**2*EIZ3,
             -3*cxy*czz*EIY2 + 3*cxz*czy*EIZ2,
             -3*cyy*czz*EIY2 + 3*cyz*czy*EIZ2,
             -3*czy*czz*EIY2 + 3*czy*czz*EIZ2),
            List(-3*cxy*cxz*EIY2 + 3*cxy*cxz*EIZ2,
             -3*cxy*cyz*EIY2 + 3*cxz*cyy*EIZ2,
             -3*cxy*czz*EIY2 + 3*cxz*czy*EIZ2,
             4*cxy**2*EIY1 + 4*cxz**2*EIZ1 +
              cxx**2*GKL,
             4*cxy*cyy*EIY1 + 4*cxz*cyz*EIZ1 +
              cxx*cyx*GKL,
             4*cxy*czy*EIY1 + 4*cxz*czz*EIZ1 +
              cxx*czx*GKL),
            List(-3*cxz*cyy*EIY2 + 3*cxy*cyz*EIZ2,
             -3*cyy*cyz*EIY2 + 3*cyy*cyz*EIZ2,
             -3*cyy*czz*EIY2 + 3*cyz*czy*EIZ2,
             4*cxy*cyy*EIY1 + 4*cxz*cyz*EIZ1 +
              cxx*cyx*GKL,
             4*cyy**2*EIY1 + 4*cyz**2*EIZ1 +
              cyx**2*GKL,
             4*cyy*czy*EIY1 + 4*cyz*czz*EIZ1 +
              cyx*czx*GKL),
            List(-3*cxz*czy*EIY2 + 3*cxy*czz*EIZ2,
             -3*cyz*czy*EIY2 + 3*cyy*czz*EIZ2,
             -3*czy*czz*EIY2 + 3*czy*czz*EIZ2,
             4*cxy*czy*EIY1 + 4*cxz*czz*EIZ1 +
              cxx*czx*GKL,
             4*cyy*czy*EIY1 + 4*cyz*czz*EIZ1 +
              cyx*czx*GKL,
             4*czy**2*EIY1 + 4*czz**2*EIZ1 +
              czx**2*GKL)))

            # create right upper
            kg12 = np.array(List(List(-(cxx**2*EAL) - 3*cxz**2*EIY3 -
              cxy**2*EIZ3,
             -(cxx*cyx*EAL) - 3*cxz*cyz*EIY3 -
              cxy*cyy*EIZ3,
             -(cxx*czx*EAL) - 3*cxz*czz*EIY3 -
              cxy*czy*EIZ3,
             -3*cxy*cxz*EIY2 + 3*cxy*cxz*EIZ2,
             -3*cxz*cyy*EIY2 + 3*cxy*cyz*EIZ2,
             -3*cxz*czy*EIY2 + 3*cxy*czz*EIZ2),
            List(-(cxx*cyx*EAL) - 3*cxz*cyz*EIY3 -
              cxy*cyy*EIZ3,
             -(cyx**2*EAL) - 3*cyz**2*EIY3 -
              cyy**2*EIZ3,
             -(cyx*czx*EAL) - 3*cyz*czz*EIY3 -
              cyy*czy*EIZ3,
             -3*cxy*cyz*EIY2 + 3*cxz*cyy*EIZ2,
             -3*cyy*cyz*EIY2 + 3*cyy*cyz*EIZ2,
             -3*cyz*czy*EIY2 + 3*cyy*czz*EIZ2),
            List(-(cxx*czx*EAL) - 3*cxz*czz*EIY3 -
              cxy*czy*EIZ3,
             -(cyx*czx*EAL) - 3*cyz*czz*EIY3 -
              cyy*czy*EIZ3,
             -(czx**2*EAL) - 3*czz**2*EIY3 -
              czy**2*EIZ3,
             -3*cxy*czz*EIY2 + 3*cxz*czy*EIZ2,
             -3*cyy*czz*EIY2 + 3*cyz*czy*EIZ2,
             -3*czy*czz*EIY2 + 3*czy*czz*EIZ2),
            List(3*cxy*cxz*EIY2 - 3*cxy*cxz*EIZ2,
             3*cxy*cyz*EIY2 - 3*cxz*cyy*EIZ2,
             3*cxy*czz*EIY2 - 3*cxz*czy*EIZ2,
             2*cxy**2*EIY1 + 2*cxz**2*EIZ1 -
              cxx**2*GKL,
             2*cxy*cyy*EIY1 + 2*cxz*cyz*EIZ1 -
              cxx*cyx*GKL,
             2*cxy*czy*EIY1 + 2*cxz*czz*EIZ1 -
              cxx*czx*GKL),
            List(3*cxz*cyy*EIY2 - 3*cxy*cyz*EIZ2,
             3*cyy*cyz*EIY2 - 3*cyy*cyz*EIZ2,
             3*cyy*czz*EIY2 - 3*cyz*czy*EIZ2,
             2*cxy*cyy*EIY1 + 2*cxz*cyz*EIZ1 -
              cxx*cyx*GKL,
             2*cyy**2*EIY1 + 2*cyz**2*EIZ1 -
              cyx**2*GKL,
             2*cyy*czy*EIY1 + 2*cyz*czz*EIZ1 -
              cyx*czx*GKL),
            List(3*cxz*czy*EIY2 - 3*cxy*czz*EIZ2,
             3*cyz*czy*EIY2 - 3*cyy*czz*EIZ2,
             3*czy*czz*EIY2 - 3*czy*czz*EIZ2,
             2*cxy*czy*EIY1 + 2*cxz*czz*EIZ1 -
              cxx*czx*GKL,
             2*cyy*czy*EIY1 + 2*cyz*czz*EIZ1 -
              cyx*czx*GKL,
             2*czy**2*EIY1 + 2*czz**2*EIZ1 -
              czx**2*GKL)))

            # left down parts
            kg21 = np.array(List(List(-(cxx**2*EAL) - 3*cxz**2*EIY3 -
              cxy**2*EIZ3,
             -(cxx*cyx*EAL) - 3*cxz*cyz*EIY3 -
              cxy*cyy*EIZ3,
             -(cxx*czx*EAL) - 3*cxz*czz*EIY3 -
              cxy*czy*EIZ3,
             3*cxy*cxz*EIY2 - 3*cxy*cxz*EIZ2,
             3*cxz*cyy*EIY2 - 3*cxy*cyz*EIZ2,
             3*cxz*czy*EIY2 - 3*cxy*czz*EIZ2),
            List(-(cxx*cyx*EAL) - 3*cxz*cyz*EIY3 -
              cxy*cyy*EIZ3,
             -(cyx**2*EAL) - 3*cyz**2*EIY3 -
              cyy**2*EIZ3,
             -(cyx*czx*EAL) - 3*cyz*czz*EIY3 -
              cyy*czy*EIZ3,
             3*cxy*cyz*EIY2 - 3*cxz*cyy*EIZ2,
             3*cyy*cyz*EIY2 - 3*cyy*cyz*EIZ2,
             3*cyz*czy*EIY2 - 3*cyy*czz*EIZ2),
            List(-(cxx*czx*EAL) - 3*cxz*czz*EIY3 -
              cxy*czy*EIZ3,
             -(cyx*czx*EAL) - 3*cyz*czz*EIY3 -
              cyy*czy*EIZ3,
             -(czx**2*EAL) - 3*czz**2*EIY3 -
              czy**2*EIZ3,
             3*cxy*czz*EIY2 - 3*cxz*czy*EIZ2,
             3*cyy*czz*EIY2 - 3*cyz*czy*EIZ2,
             3*czy*czz*EIY2 - 3*czy*czz*EIZ2),
            List(-3*cxy*cxz*EIY2 + 3*cxy*cxz*EIZ2,
             -3*cxy*cyz*EIY2 + 3*cxz*cyy*EIZ2,
             -3*cxy*czz*EIY2 + 3*cxz*czy*EIZ2,
             2*cxy**2*EIY1 + 2*cxz**2*EIZ1 -
              cxx**2*GKL,
             2*cxy*cyy*EIY1 + 2*cxz*cyz*EIZ1 -
              cxx*cyx*GKL,
             2*cxy*czy*EIY1 + 2*cxz*czz*EIZ1 -
              cxx*czx*GKL),
            List(-3*cxz*cyy*EIY2 + 3*cxy*cyz*EIZ2,
             -3*cyy*cyz*EIY2 + 3*cyy*cyz*EIZ2,
             -3*cyy*czz*EIY2 + 3*cyz*czy*EIZ2,
             2*cxy*cyy*EIY1 + 2*cxz*cyz*EIZ1 -
              cxx*cyx*GKL,
             2*cyy**2*EIY1 + 2*cyz**2*EIZ1 -
              cyx**2*GKL,
             2*cyy*czy*EIY1 + 2*cyz*czz*EIZ1 -
              cyx*czx*GKL),
            List(-3*cxz*czy*EIY2 + 3*cxy*czz*EIZ2,
             -3*cyz*czy*EIY2 + 3*cyy*czz*EIZ2,
             -3*czy*czz*EIY2 + 3*czy*czz*EIZ2,
             2*cxy*czy*EIY1 + 2*cxz*czz*EIZ1 -
              cxx*czx*GKL,
             2*cyy*czy*EIY1 + 2*cyz*czz*EIZ1 -
              cyx*czx*GKL,
             2*czy**2*EIY1 + 2*czz**2*EIZ1 -
              czx**2*GKL)))

            # create right down part
            kg22 = np.array(List(List(cxx**2*EAL + 3*cxz**2*EIY3 +
              3*cxy**2*EIZ3,
             cxx*cyx*EAL + 3*cxz*cyz*EIY3 +
              3*cxy*cyy*EIZ3,
             cxx*czx*EAL + 3*cxz*czz*EIY3 +
              3*cxy*czy*EIZ3,
             3*cxy*cxz*EIY2 - 3*cxy*cxz*EIZ2,
             3*cxz*cyy*EIY2 - 3*cxy*cyz*EIZ2,
             3*cxz*czy*EIY2 - 3*cxy*czz*EIZ2),
            List(cxx*cyx*EAL + 3*cxz*cyz*EIY3 +
              3*cxy*cyy*EIZ3,
             cyx**2*EAL + 3*cyz**2*EIY3 +
              3*cyy**2*EIZ3,
             cyx*czx*EAL + 3*cyz*czz*EIY3 +
              3*cyy*czy*EIZ3,
             3*cxy*cyz*EIY2 - 3*cxz*cyy*EIZ2,
             3*cyy*cyz*EIY2 - 3*cyy*cyz*EIZ2,
             3*cyz*czy*EIY2 - 3*cyy*czz*EIZ2),
            List(cxx*czx*EAL + 3*cxz*czz*EIY3 +
              3*cxy*czy*EIZ3,
             cyx*czx*EAL + 3*cyz*czz*EIY3 +
              3*cyy*czy*EIZ3,
             czx**2*EAL + 3*czz**2*EIY3 +
              3*czy**2*EIZ3,
             3*cxy*czz*EIY2 - 3*cxz*czy*EIZ2,
             3*cyy*czz*EIY2 - 3*cyz*czy*EIZ2,
             3*czy*czz*EIY2 - 3*czy*czz*EIZ2),
            List(3*cxy*cxz*EIY2 - 3*cxy*cxz*EIZ2,
             3*cxy*cyz*EIY2 - 3*cxz*cyy*EIZ2,
             3*cxy*czz*EIY2 - 3*cxz*czy*EIZ2,
             4*cxy**2*EIY1 + 4*cxz**2*EIZ1 +
              cxx**2*GKL,
             4*cxy*cyy*EIY1 + 4*cxz*cyz*EIZ1 +
              cxx*cyx*GKL,
             4*cxy*czy*EIY1 + 4*cxz*czz*EIZ1 +
              cxx*czx*GKL),
            List(3*cxz*cyy*EIY2 - 3*cxy*cyz*EIZ2,
             3*cyy*cyz*EIY2 - 3*cyy*cyz*EIZ2,
             3*cyy*czz*EIY2 - 3*cyz*czy*EIZ2,
             4*cxy*cyy*EIY1 + 4*cxz*cyz*EIZ1 +
              cxx*cyx*GKL,
             4*cyy**2*EIY1 + 4*cyz**2*EIZ1 +
              cyx**2*GKL,
             4*cyy*czy*EIY1 + 4*cyz*czz*EIZ1 +
              cyx*czx*GKL),
            List(3*cxz*czy*EIY2 - 3*cxy*czz*EIZ2,
             3*cyz*czy*EIY2 - 3*cyy*czz*EIZ2,
             3*czy*czz*EIY2 - 3*czy*czz*EIZ2,
             4*cxy*czy*EIY1 + 4*cxz*czz*EIZ1 +
              cxx*czx*GKL,
             4*cyy*czy*EIY1 + 4*cyz*czz*EIZ1 +
              cyx*czx*GKL,
             4*czy**2*EIY1 + 4*czz**2*EIZ1 +
              czx**2*GKL)))

            # assembly local matrix to global stif matrix
            self._K_stif[
                n1*self._ndof:n1*self._ndof+self._ndof,
                n1*self._ndof:n1*self._ndof+self._ndof] += +kg11

            self._K_stif[
                n1*self._ndof:n1*self._ndof+self._ndof,
                n2*self._ndof:n2*self._ndof+self._ndof] += kg12

            self._K_stif[
                n2*self._ndof:n2*self._ndof+self._ndof,
                n1*self._ndof:n1*self._ndof+self._ndof] += kg21

            self._K_stif[
                n2*self._ndof:n2*self._ndof+self._ndof,
                n2*self._ndof:n2*self._ndof+self._ndof] += kg22


#$$$ ____________ def -K-beams-3d __________________________________________ #

    def _K_beams(self):

        beams = self.dbase.get('''
        SELECT
            [BM].[id],
            [BM].[L],
            [BM].[delta_X],
            [BM].[delta_Y],
            [BM].[delta_z],
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
        LEFT JOIN [021:usec1:unics] AS [CS] ON [BM].[sect] = [CS].[id]
        LEFT JOIN [011:mates:umate] AS [MT] ON [CS].[mate] = [MT].[id]
        ''')

        for beam in beams:
            # unpack db data
            id,L,Δx,Δy,Δz,n1,n2,A,I_t,I_y,I_z,E_1,G_1 = beam

            Lxy = (Δx**2+Δy**2)**0.5

            # calculate cos matrix
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

            # left down parts
            kg21 = np.array(List(List(-(cxx**2*EAL) - cxz**2*EIY3 -
              cxy**2*EIZ3,
             -(cxx*cyx*EAL) - cxz*cyz*EIY3 -
              cxy*cyy*EIZ3,
             -(cxx*czx*EAL) - cxz*czz*EIY3 -
              cxy*czy*EIZ3,
             -(cxy*cxz*EIY2) - cxy*cxz*EIZ2,
             -(cxz*cyy*EIY2) - cxy*cyz*EIZ2,
             -(cxz*czy*EIY2) - cxy*czz*EIZ2),
            List(-(cxx*cyx*EAL) - cxz*cyz*EIY3 -
              cxy*cyy*EIZ3,
             -(cyx**2*EAL) - cyz**2*EIY3 -
              cyy**2*EIZ3,
             -(cyx*czx*EAL) - cyz*czz*EIY3 -
              cyy*czy*EIZ3,
             -(cxy*cyz*EIY2) - cxz*cyy*EIZ2,
             -(cyy*cyz*EIY2) - cyy*cyz*EIZ2,
             -(cyz*czy*EIY2) - cyy*czz*EIZ2),
            List(-(cxx*czx*EAL) - cxz*czz*EIY3 -
              cxy*czy*EIZ3,
             -(cyx*czx*EAL) - cyz*czz*EIY3 -
              cyy*czy*EIZ3,
             -(czx**2*EAL) - czz**2*EIY3 -
              czy**2*EIZ3,
             -(cxy*czz*EIY2) - cxz*czy*EIZ2,
             -(cyy*czz*EIY2) - cyz*czy*EIZ2,
             -(czy*czz*EIY2) - czy*czz*EIZ2),
            List(cxy*cxz*EIY2 + cxy*cxz*EIZ2,
             cxy*cyz*EIY2 + cxz*cyy*EIZ2,
             cxy*czz*EIY2 + cxz*czy*EIZ2,
             cxy**2*EIY0 + cxz**2*EIZ0 - cxx**2*GKL,
             cxy*cyy*EIY0 + cxz*cyz*EIZ0 -
              cxx*cyx*GKL,
             cxy*czy*EIY0 + cxz*czz*EIZ0 -
              cxx*czx*GKL),
            List(cxz*cyy*EIY2 + cxy*cyz*EIZ2,
             cyy*cyz*EIY2 + cyy*cyz*EIZ2,
             cyy*czz*EIY2 + cyz*czy*EIZ2,
             cxy*cyy*EIY0 + cxz*cyz*EIZ0 -
              cxx*cyx*GKL,
             cyy**2*EIY0 + cyz**2*EIZ0 - cyx**2*GKL,
             cyy*czy*EIY0 + cyz*czz*EIZ0 -
              cyx*czx*GKL),
            List(cxz*czy*EIY2 + cxy*czz*EIZ2,
             cyz*czy*EIY2 + cyy*czz*EIZ2,
             czy*czz*EIY2 + czy*czz*EIZ2,
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

            # assembly local matrix to global stif matrix
            self._K_stif[
                n1*self._ndof:n1*self._ndof+self._ndof,
                n1*self._ndof:n1*self._ndof+self._ndof] += +kg11

            self._K_stif[
                n1*self._ndof:n1*self._ndof+self._ndof,
                n2*self._ndof:n2*self._ndof+self._ndof] += kg12

            self._K_stif[
                n2*self._ndof:n2*self._ndof+self._ndof,
                n1*self._ndof:n1*self._ndof+self._ndof] += kg21

            self._K_stif[
                n2*self._ndof:n2*self._ndof+self._ndof,
                n2*self._ndof:n2*self._ndof+self._ndof] += kg22


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

        # transpose into vertical vector
        # now we dont do it
        # self._F_load = self._F_load.reshape((-1,1))


#$$$ ____________ def -F-nodes _____________________________________________ #

    def _F_nodes(self, lcase):
        loads = self.dbase.get(f'''
        SELECT
            [NZ].[noG],
            [NZ].[id],
            [px],
            [py],
            [pz]
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
            # here must be if (no elif) because in one statment user can add
            # load in few directions
            if px:
                if self._ldof[0]:
                    self._F_load[adof+0] += px
                else:
                    prwarn('DX', node_id)
                    return False

            if py:
                if self._ldof[1]:
                    self._F_load[adof+1] += py
                else:
                    prwarn('DY', node_id)
                    return False

            if pz:
                if self._ldof[2]:
                    self._F_load[adof+2] += pz
                else:
                    prwarn('DZ', node_id)
                    return False







#$$ ________ boundary condition ____________________________________________ #

#$$$ ____________ def -bc-K ________________________________________________ #

    def _bc_K(self):
        '''
        Set boundary condition on the K matrix.
        '''

        nodes = self.dbase.get('''
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
            noG,fix, node_id = node

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

                    # insert zeros in full wide row and col
                    self._K_stif[add1,:] = 0  # zero row
                    self._K_stif[:,add1] = 0  # zero col

                    # insert unit at cross of row and col
                    self._K_stif[add1,add1] = 1



#$$$ ____________ def -bc-F ________________________________________________ #

    def _bc_F(self):
        '''
        Set boundary condition on the F vector.
        '''

        # loop over list created while bc_K set.
        for add1 in self._cdof:
            self._F_load[add1] = 0


#$$$ ____________ def -bc-pattern __________________________________________ #

    def _bc_pattern(self, name, node_id):
        '''
        Additional dof number depend on force load type.
        '''

        def prwarn(dof):
            # print warning
            print(f'warning bc-dof-101:\nThe support at node {node_id} is noneffective, because global {dof} dof is inactive')


        # if-block depend on static load type
        if   name == 'P0': return [0]
        elif name == 'P1': return [1]
        elif name == 'P2': return [2]
        elif name == 'P3': return [3]
        elif name == 'P4': return [4]
        elif name == 'P5': return [5]
        else: raise ValueError('Unknow boundary condition name')


#$$ ________ post-evaluate _________________________________________________ #

#$$$ ____________ def -displacement ________________________________________ #

    def _displacement(self):
        '''
        Calculate node displacement as result of system solve.
        '''
        # set displacement vector
        self._Q_disp = np.linalg.solve(self._K_stif, self._F_load)


#$$$ ____________ def -reactions ____________________________________________ #

    def _reactions(self):
        '''
        Calculate reaction in supports.
        R = K*Q - F
        '''

        # TODO: im not sure that below method are optimal... we need to create copy of K and F vector and then calculate full system, so maybe do not copy full matrix (vector), but copy only selected rows?

        # calculate reaction depend on unconstrained K and F data
        self._R_reac = self._K_free.dot(self._Q_disp) - self._F_free


#$$$ ____________ def -store-db ____________________________________________ #

    def _store_RQ(self, lcase):
        '''
        Store calculated data in db.
        '''

        # check dof of system
        cols,ndata=self._store_check()

        for noG in range(self.max_node_noG+1):

            adof = noG*self._ndof
            # TODO: get all elements at one kwerend, then get from matrix
            # find id of node
            id = self.dbase.get(f'''
                SELECT [id] FROM [111:nodes:optim] WHERE [noG] = {noG}
            ''')[0][0]

            cols,data = self._storeloc(
                cols  = cols,
                ndata = ndata,
                lcase = lcase,
                id    = id,
                adof  = adof)

            self.dbase.add(
                table = '[113:nodes:sresu]',
                cols  = cols,
                data  = data,
            )

    def _store_check(self):
        '''
        Check dof of system and return cols
        '''

        cols = '[lcase],[node],'
        if self._ldof[0]: cols += '[px],[dx],'
        if self._ldof[1]: cols += '[py],[dy],'
        if self._ldof[2]: cols += '[pz],[dz],'
        if self._ldof[3]: cols += '[mx],[rx],'
        if self._ldof[4]: cols += '[my],[ry],'
        if self._ldof[5]: cols += '[mz],[rz],'
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


#$$$ ____________ def -s-truss _____________________________________________ #

    def _p_truss(self, lcase):
        trusses = self.dbase.get('''
        SELECT
            [TS].[id],
            [TS].[L],
            [TS].[delta_X],
            [TS].[delta_Y],
            [TS].[delta_Z],
            [N1].[noG],
            [N1].[id],
            [N2].[noG],
            [N2].[id],
            [CS].[A],
            [MT].[E_1]
        FROM [121:truss:topos]      AS [TS]
        LEFT JOIN [111:nodes:optim] AS [N1] ON [TS].[n1]   = [N1].[id]
        LEFT JOIN [111:nodes:optim] AS [N2] ON [TS].[n2]   = [N2].[id]
        LEFT JOIN [021:usec1:unics] AS [CS] ON [TS].[sect] = [CS].[id]
        LEFT JOIN [011:mates:umate] AS [MT] ON [CS].[mate] = [MT].[id]
        ''')


        for truss in trusses:

            id, L, Δx, Δy, Δz, n1, n1id, n2, n2id, A, E_1 = truss

            # first node, must return only one node
            # TODO: validate return of 1 node
            q1 = self.dbase.get(f'''
            SELECT
                [dx],
                [dy],
                [dz]
            FROM [113:nodes:sresu] WHERE [lcase]="{lcase}" AND [node]="{n1id}"
            ''')[0]

            # second node, look upper comment
            q2 = self.dbase.get(f'''
            SELECT
                [dx],
                [dy],
                [dz]
            FROM [113:nodes:sresu] WHERE [lcase]="{lcase}" AND [node]="{n2id}"
            ''')[0]

            # calculate sin,cos itd
            Cx, Cy, Cz = Δx/L, Δy/L, Δz/L

            # change of length
            if self.pvars.get('system_dof') == '2t':
                # vector of local displacement sorted like dofs
                q_loc = np.array([q1[0], q1[1], q2[0], q2[1]])

                # change of length
                ΔL = np.array([-Cx, -Cy, Cx, Cy]).dot(q_loc)

            elif self.pvars.get('system_dof') == '3t':
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
            self.dbase.add(
                table = '[123:truss:sresu]',
                cols  = '[id],[lcase],[N],[delta_L],[eps_x]',
                data  = (id, lcase, N_x, ΔL, ε_x),
            )

            # send to design results
            self.dbase.add(
                table = '[124:truss:desig]',
                cols  = '[id],[lcase],[sig_x]',
                data  = (id, lcase, σ_x),
            )

