class rstmeError(Exception):
    pass

def lvlrstmeError(lvl):
    raise rstmeError(f'The typped level <{lvl}> outside domain. The header level be defined as integer between <0,5>')