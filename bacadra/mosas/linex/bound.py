import numpy as np

class bound:
    #$$ def --init--
    def __init__(self, core, prog):
        self.core = core
        self.prog = prog

    #$$$ def stiff
    def stiff(self):
        '''
        Set boundary condition on the K matrix.
        '''

        # create cdof list
        self.prog._cdof = []

        # build constrained dof list
        self._build_cdof()

        # create active stiffness
        self.prog._K11 = np.delete(
            np.delete(self.prog._K, self.prog._cdof, axis=0),
            self.prog._cdof, axis=1
        )

        # create passive stiffness
        self.prog._K22 = self.prog._K[np.ix_(self.prog._cdof,self.prog._cdof)]

        # create mixed 21
        self.prog._K21 = np.delete(self.prog._K[np.ix_(self.prog._cdof)],
            self.prog._cdof, axis=1)

        # create mixed 12
        self.prog._K12 = self.prog._K21.T


    #$$$ def -L-bc
    def lvect(self):
        '''
        Set boundary condition on the F vector.
        '''

        # create active load
        self.prog._F = np.delete(self.prog._F, self.prog._cdof)

        # create imposed displacement
        self.prog._D = self.prog._D[np.ix_(self.prog._cdof)]



    def _build_cdof(self):
        # TODO: check node with assigned noG, other nodes are not needed!
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
            adof = noG * len(self.prog._ldof)

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
                    self.prog._cdof.append(add1)



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
            return [self.prog._ldof.index('dx')]

        elif name == 'PY':
            return [self.prog._ldof.index('dy')]

        elif name == 'PZ':
            return [self.prog._ldof.index('dz')]


        elif name == 'XP':
            return [self.prog._ldof.index('dy'),
                    self.prog._ldof.index('dz')]

        elif name == 'YP':
            return [self.prog._ldof.index('dx'),
                    self.prog._ldof.index('dz')]

        elif name == 'ZP':
            return [self.prog._ldof.index('dx'),
                    self.prog._ldof.index('dy')]

        elif name == 'PP':
            return [self.prog._ldof.index('dx'),
                    self.prog._ldof.index('dy'),
                    self.prog._ldof.index('dz')]


        elif name == 'MX':
            return [self.prog._ldof.index('rx')]

        elif name == 'MY':
            return [self.prog._ldof.index('ry')]

        elif name == 'MZ':
            return [self.prog._ldof.index('rz')]


        elif name == 'XM':
            return [self.prog._ldof.index('ry'),
                    self.prog._ldof.index('rz')]

        elif name == 'YM':
            return [self.prog._ldof.index('rx'),
                    self.prog._ldof.index('dz')]

        elif name == 'ZM':
            return [self.prog._ldof.index('rx'),
                    self.prog._ldof.index('ry')]

        elif name == 'MM':
            return [self.prog._ldof.index('rx'),
                    self.prog._ldof.index('ry'),
                    self.prog._ldof.index('rz')]

        elif name == 'FF':
            return [self.prog._ldof.index('dx'),
                    self.prog._ldof.index('dy'),
                    self.prog._ldof.index('dz'),
                    self.prog._ldof.index('rx'),
                    self.prog._ldof.index('ry'),
                    self.prog._ldof.index('rz')]

        else:
            raise ValueError('Unknow boundary condition name')