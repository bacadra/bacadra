import numpy as np


class lvect:
    def __init__(self, core, prog, lcase):
        self.core = core
        self.prog = prog
        self.lcase = lcase

        # run build
        self._build_L(prog)


    #$$$ def -build-L
    def _build_L(self, prog):
        '''
        Create load and imposed discplament vector.
        '''

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
        WHERE [lcase] = "{self.lcase}"
        ''')

        for load in loads:
            # unpack row from db
            n1,noG,px,py,pz,mx,my,mz,dx,dy,dz,rx,ry,rz = load

            for forc in [(px, dx,'dx'),
                         (py, dy,'dy'),
                         (pz, dz,'dz'),
                         (mx, rx,'rx'),
                         (my, ry,'ry'),
                         (mz, rz,'rz')]:
                if forc[0]: self.prog._F_assembly(noG, forc[2], forc[0])
                if forc[1]: self.prog._D_assembly(noG, forc[2], forc[1])
