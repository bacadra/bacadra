
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

def f1SolveStatxSystemError(system_space):
    raise SolveStatxSystemError(f'The unknown system_space <{system_space}>. Available dir of dof: dx, dy, dz, rx, ry, rz, rw. \nTip: You can try set one of already define system: 2t, 3t, 2d, 3d, 3d7, ss, sn, as.')


def f2SolveStatxSystemError(system_space, dof):
    if dof not in system_space:
        raise SolveStatxSystemError(f'The loaded DOF <{dof}> is not avaiable in system_space <{system_space}>.')

def f3SolveStatxSystemError():
        raise SolveStatxSystemError('At first build the system with method .build(<param>)')

def f4SolveStatxSystemError(ldof, noG):
        if noG not in ldof:
            raise SolveStatxSystemError('The DOF must be blocked if you want to input imposed displacement')


class SolveBConditionWarning(Warning):
    '''
    '''
    pass

def f1SolveBConditionWarning(ldof, dof):
    print(f'***** SolveBConditionWarning: The boundary condition <{dof}> can\'t be applied into system, because the corresponding to him dof is inactive.\nList of current active dofs <{ldof}>')
