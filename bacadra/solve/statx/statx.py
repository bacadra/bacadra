import numpy as np
from . import verrs
# from . import system
np.set_printoptions(suppress=True)

#$ ____ class statx ________________________________________________________ #

class statx:
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
        self._system_summary()

        # set the complete stiffnes matrix
        self._K_summary()

        # set boundary condition
        self._K_bc()


    #$$$ def solve
    def solve(self, lcase):
        # check if system is crated
        if self._K is None:
            verrs.f3SolveStatxSystemError()

        # set the complete vector
        self._L_sumary(lcase=lcase)

        # boundary condition on load vector
        self._L_bc()

        # calc displacement vector
        self._Q_solve()

        # calc reactions
        self._R_calc()

        self._store_sresu(lcase=lcase)


#$$ ________ system ________________________________________________________ #

    #$$$ def -system-summary
    def _system_summary(self):
        '''
        Central order tower to create system.
        '''

        # check dof in system
        self._dof_active()

        # crete global numertaion
        self._noG_create()

        # check active node count
        self._sdof_active()


    #$$$ def -dof-active
    def _dof_active(self):
        '''
        Set the correct list of dof and calculate count of dof in system.
        '''

        # dof list pattern:
        # [dx, dy, dz, rx, ry, rz, rw]

        # get the settings about dof system
        system_dof = self.core.mdata.setts.get('system_dof')

        if type(system_dof) is list:
            for dof in system_dof:
                if dof not in ['dx', 'dy', 'dz', 'rx', 'ry', 'rz', 'rw']:
                    verrs.f1SolveStatxSystemError(system_dof)
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
            verrs.f1SolveStatxSystemError(system_dof)


    #$$$ def -nog-create
    def _noG_create(self):
        '''
        Optimize nodes numbering.
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


    #$$$ def -sdof-active
    def _sdof_active(self):
        '''
        Count of nodal degree of freedom of our structure. Get the max node number in actual building.
        '''

        self.max_node_noG = self.core.dbase.get('''
        SELECT max([noG]) FROM [111:nodes:optim]
        ''')[0][0]

        # TODO: variable size of cell or autodefine dof size
        # +1 because matrix start from 0
        self._sdof = len(self._ldof) * (self.max_node_noG+1)


#$$ ________ stiffness matrix ______________________________________________ #

    #$$$ def -K-summary
    def _K_summary(self):
        # init stiffness matrix
        self._K = np.zeros((self._sdof, self._sdof))

        # call method to different type of elements
        self._K_truss() # +truss


    #$$$ def -K-assembly
    def _K_assembly(self, data):
        '''
        You can apply element with n-nodes.
        list[
        Struct:
            data(0) - node 1
            data(1) - node 2
            data(2) - local stiffness matrix in global coor
        ]

        data = [
            (1,1, kg11),
            (1,2, kg12),
            (2,1, kg21),
            (2,2, kg21),
        ]
        '''

        for subkg in data:
            d1,d2,kg = subkg
            ndof = len(self._ldof)

            # assembly local matrix to global stif matrix
            self._K[d1*ndof:d1*ndof+ndof, d2*ndof:d2*ndof+ndof] += kg


    #$$$ def -K-truss
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
            self._K_assembly([
                (n1, n1,  kg11),
                (n1, n2, -kg11),
                (n2, n1, -kg11),
                (n2, n2,  kg11),
            ])


    #$$$ deg -kg-truss
    def _kg_truss(self, E_1, A, L, Δx, Δy, Δz):

        # check system
        system = self.core.mdata.setts.get('system_dof')

        # calculate sin,cos itd
        Cx, Cy, Cz = Δx/L, Δy/L, Δz/L

        k0 = 10**-10 # TODO: what number?

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
                 [0,           0, k0]])

        elif system == '3d':
            kg11 = E_1 * A / L * np.array(
                [[+Cx*Cx, +Cx*Cy, +Cx*Cz,  0,  0,  0],
                 [+Cx*Cy, +Cy*Cy, +Cy*Cz,  0,  0,  0],
                 [+Cx*Cz, +Cy*Cz, +Cz*Cz,  0,  0,  0],
                 [     0,      0,      0, k0,  0,  0],
                 [     0,      0,      0,  0, k0,  0],
                 [     0,      0,      0,  0,  0, k0]])

        return kg11


#$$ ________ load vector ___________________________________________________ #

    #$$$ def -L-summary
    def _L_sumary(self, lcase):

        # init 1d vector for loads and imposed displacement
        # 1d vector is not horizontal and not vertical, just 1d
        # we can multiply array * 1d vector and we get 1d vector (only if cols count of matrix and element count in vector is the same)
        self._F = np.zeros(self._sdof)
        self._D = np.zeros(self._sdof)

        # add loads from nodes and elemenets
        self._L_nodes(lcase)


    #$$$ def -L-nodes
    def _L_nodes(self, lcase):
        loads = self.core.dbase.get(f'''
        SELECT
            [NL].[node],
            [NZ].[noG],
            [px],
            [py],
            [pz],
            [mx],
            [my],
            [mz],
            [dx],
            [dy],
            [dz],
            [rx],
            [ry],
            [rz]
        FROM [112:nodes:loads]      as [NL]
        LEFT JOIN [111:nodes:optim] as [NZ] ON [NL].[node] = [NZ].[id]
        WHERE [lcase] = "{lcase}"
        ''')

        for load in loads:
            # unpack row from db
            n1,noG,px,py,pz,mx,my,mz,dx,dy,dz,rx,ry,rz = load

            ndof = len(self._ldof)

            for forc in [(px,'dx'),
                         (py,'dy'),
                         (pz,'dz'),
                         (mx,'rx'),
                         (my,'ry'),
                         (mz,'rz')]:
                if forc[0]:
                    verrs.f2SolveStatxSystemError(self._ldof, forc[1])
                    self._F[noG*ndof +
                        self._ldof.index(forc[1])] += forc[0]

            for disp in [(dx,'dx'),
                         (dy,'dy'),
                         (dz,'dz'),
                         (rx,'rx'),
                         (ry,'ry'),
                         (rz,'rz')]:
                if disp[0]:
                    verrs.f2SolveStatxSystemError(self._ldof, disp[1])
                    # verrs.f4SolveStatxSystemError(self._ldof, disp[1])
                    self._D[noG*ndof +
                        self._ldof.index(disp[1])] += disp[0]



#$$ ________ boundary condition ____________________________________________ #

    #$$$ def -K-bc
    def _K_bc(self):
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
            adof = noG * len(self._ldof)

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

        self._K11 = np.delete(np.delete(self._K, self._cdof, axis=0),
            self._cdof, axis=1)

        self._K22 = self._K[np.ix_(self._cdof,self._cdof)]

        self._K21 = np.delete(self._K[np.ix_(self._cdof)],
            self._cdof, axis=1)

        self._K12 = self._K21.T


    #$$$ def -L-bc
    def _L_bc(self):
        '''
        Set boundary condition on the F vector.
        '''

        self._F = np.delete(self._F, self._cdof)
        self._D = self._D[np.ix_(self._cdof)]


    #$$$ def -bc-pattern
    def _bc_pattern(self, name, node_id):
        '''
        Additional dof number depend on force load type.
        '''

        def prwarn(name,dof):
            # print warning
            print(f'warning bc-dof-101:\nThe support at node {node_id} is noneffective, because global {dof} dof is inactive')


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



#$$ ________ solve system __________________________________________________ #

    #$$$ def -Q-solve
    def _Q_solve(self):
        '''
        Calculate node displacement as result of system solve.
        '''
        # set displacement vector
        self._Q = np.linalg.solve(self._K11, self._F - self._K12.dot(self._D))

    #$$$ def -R-calc
    def _R_calc(self):
        '''
        Calculate reaction in supports.
        '''

        # calculate reaction depend on unconstrained K and F data
        self._R = self._K21.dot(self._Q) + self._K22.dot(self._D)


#$$ ________ store results _________________________________________________ #


    def _store_sresu(self, lcase):
        '''
        Store calculated data in db.
        '''

        # create column name vector
        cols = self._store_cols()

        # loop over all nodes in curent system
        for noG in range(self.max_node_noG+1):

            # get id of node
            id = self.core.dbase.get(f'''
                SELECT [id] FROM [111:nodes:optim] WHERE [noG] = {noG}
            ''')[0][0]

            # create results vector
            data = self._storeloc(
                lcase = lcase,
                id    = id,
                noG   = noG)

            # add data to dbase
            self.core.dbase.add(
                table = '[113:nodes:sresu]',
                cols  = cols,
                data  = data,
            )



    def _store_cols(self):
        '''
        Check dof of system and return cols
        '''

        # first to column, as indicatior
        cols = '[lcase],[node],'

        # loop over dof in system and create in same dir cols
        for disp in self._ldof:
            if   disp == 'dx': cols += '[px],[dx],'
            elif disp == 'dy': cols += '[py],[dy],'
            elif disp == 'dz': cols += '[pz],[dz],'
            elif disp == 'rx': cols += '[mx],[rx],'
            elif disp == 'ry': cols += '[my],[ry],'
            elif disp == 'rz': cols += '[mz],[rz],'

        # delete last one comma
        cols  = cols[:-1]

        # return string
        return cols


    def _storeloc(self, lcase,id,noG):
        '''
        Generate input data
        '''

        # create first two data column
        data = [lcase,id]

        # loop over length of dofs list in current ndoe
        for i in range(len(self._ldof)):

            # if current dof was blocked then use pattern below
            if noG * len(self._ldof) + i in self._cdof:

                # find index list in cdof list
                index = self._cdof.index(noG * len(self._ldof) + i)

                # add to data vector reaction and imposed displacement
                data.append(self._R[index])
                data.append(self._D[index])

            else:
                # find how many dof was deleted from Q vector before current vector
                cdofn = (np.asarray(self._cdof) <
                    noG * len(self._ldof) + i).sum()

                # save index in cutted matrix
                index = noG * len(self._ldof) + i - cdofn

                # add to data vector None (reaction not occur) and displacement
                data.append(None)
                data.append(self._Q[index])

        return data





