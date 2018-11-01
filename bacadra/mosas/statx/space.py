from . import verrs



class space:
    def __init__(self, othe):

        # check dof in system
        self._dof_active(othe)

        # div ekenent and crete global numeration
        self._mesh(othe)

        # check active node count
        self._sdof_active(othe)


    #$$$ def -dof-active
    def _dof_active(self, othe):
        '''
        Set the correct list of dof and calculate count of dof in system.
        '''

        # dof list pattern:
        # [dx, dy, dz, rx, ry, rz, rw]

        # get the settings about dof system
        system_space = othe.core.mdata.setts.get('system_space')

        if type(system_space) is list:
            for dof in system_space:
                if dof not in ['dx', 'dy', 'dz', 'rx', 'ry', 'rz', 'rw']:
                    verrs.f1SolveStatxSystemError(system_space)
            othe._ldof = system_space

        elif system_space == '2t':
            # planar truss
            othe._ldof = ['dx','dz']

        elif system_space == '3t':
            # space truss
            othe._ldof = ['dx','dy','dz']

        elif system_space == '2d':
            # planar beams
            othe._ldof = ['dx','dz','ry']

        elif system_space == '3d':
            # space beams
            othe._ldof = ['dx','dy','dz','rx','ry','rz']

        elif system_space == '3d7':
            # space beams with warping dof
            othe._ldof = ['dx','dy','dz','rx','ry','rz','rw']

        elif system_space == 'ss':
            # plain stress
            othe._ldof = ['dx','dz','rz']

        elif system_space == 'sn':
            # plain strain
            othe._ldof = ['dx','dz','rz']

        elif system_space == 'as':
            # axial symetry
            othe._ldof = ['dx','dz','rz']

        else:
            verrs.f1SolveStatxSystemError(system_space)


    #$$$ def -nog-create
    def _mesh(self, othe):
        '''
        Optimize nodes numbering.
        '''

        nodes = othe.core.dbase.get('SELECT [id] FROM [111:nodes:topos]')

        # TODO: optimize numbering
        # now the optimize is in sort order number ...

        noG = 0
        for node in nodes:
            othe.core.dbase.add(
                table = '[111:nodes:optim]',
                cols  = '[id],[noG]',
                data  = (node[0], noG)
            )
            noG += 1


    #$$$ def -sdof-active
    def _sdof_active(self, othe):
        '''
        Count of nodal degree of freedom of our structure. Get the max node number in actual building.
        '''

        othe.max_node_noG = othe.core.dbase.get('''
        SELECT max([noG]) FROM [111:nodes:optim]
        ''')[0][0]

        # TODO: variable size of cell or autodefine dof size
        # +1 because matrix start from 0
        othe._sdof = len(othe._ldof) * (othe.max_node_noG+1)