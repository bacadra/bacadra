
class SolveStatxError(Exception):
    '''
    General Solve exception.
    '''
    pass


class SolveStatxSystemError(Exception):
    '''
    System exception.
    '''
    pass

def f1SolveStatxSystemError(system_dof):
    raise SolveStatxSystemError(f'The unknown system_dof <{system_dof}>. Available dir of dof: dx, dy, dz, rx, ry, rz, rw. \nTip: You can try set one of already define system: 2t, 3t, 2d, 3d, 3d7, ss, sn, as.')


def f2SolveStatxSystemError(system_dof, dof):
    if dof not in system_dof:
        raise SolveStatxSystemError(f'The loaded DOF <{dof}> is not avaiable in system_dof <{system_dof}>.')

def f3SolveStatxSystemError():
        raise SolveStatxSystemError('At first build the system with method .build(<param>)')

def f4SolveStatxSystemError(ldof, noG):
        if noG not in ldof:
            raise SolveStatxSystemError('The DOF must be blocked if you want to input imposed displacement')