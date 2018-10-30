import numpy as np

class staqr:
    #$$ def --init--
    def __init__(self, core, prog, lcase):
        self.core = core
        self.prog = prog
        self.lcase = lcase

        # solver
        solver_type = '1'

        # if-block solver type
        # numpy linesolve
        if solver_type == '1':
            self._Q1_solve()
            self._R1_solve()

        # store results in dbase
        self._store_qr()


    #$$$ def -Q1-solve
    def _Q1_solve(self):
        '''
        Calculate node displacement as result of system solve.
        '''
        # set displacement vector
        self.prog._Q = np.linalg.solve(
            self.prog._K11, self.prog._F -
            self.prog._K12.dot(self.prog._D)
        )


    #$$$ def -R-calc
    def _R1_solve(self):
        '''
        Calculate reaction in supports.
        '''

        # calculate reaction depend on unconstrained K and F data
        self.prog._R = (
            self.prog._K21.dot(self.prog._Q) +
            self.prog._K22.dot(self.prog._D)
        )




    #$$$ def -store-qr
    def _store_qr(self):
        '''
        Store calculated data in db.
        '''

        # create column name vector
        cols = self._store_cols()

        # loop over all nodes in curent system
        for noG in range(self.prog.max_node_noG+1):

            # get id of node
            id = self.core.dbase.get(f'''
                SELECT [id] FROM [111:nodes:optim] WHERE [noG] = {noG}
            ''')[0][0]

            # create results vector
            data = self._store_loc(
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
        for disp in self.prog._ldof:
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


    def _store_loc(self,id,noG):
        '''
        Generate input data
        '''

        # create first two data column
        data = [self.lcase,id]

        # loop over length of dofs list in current ndoe
        for i in range(len(self.prog._ldof)):

            # if current dof was blocked then use pattern below
            if noG * len(self.prog._ldof) + i in self.prog._cdof:

                # find index list in cdof list
                index = self.prog._cdof.index(noG * len(self.prog._ldof) + i)

                # add to data vector reaction and imposed displacement
                data.append(self.prog._R[index])
                data.append(self.prog._D[index])

            else:
                # find how many dof was deleted from Q vector before current vector
                cdofn = (np.asarray(self.prog._cdof) <
                    noG * len(self.prog._ldof) + i).sum()

                # save index in cutted matrix
                index = noG * len(self.prog._ldof) + i - cdofn

                # add to data vector None (reaction not occur) and displacement
                data.append(None)
                data.append(self.prog._Q[index])

        return data









