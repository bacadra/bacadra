class BCDR_mates_conce_Error(Exception):
    pass

def f1_BCDR_mates_conce_Error(grade):
    raise BCDR_mates_conce_Error(f'Material grade <{grade}> can not be assigned to any one of already defined code patterns.')


class BCDR_mates_conce_Error(Warning):
    pass

def f1_BCDR_mates_conce_Warning(limit, f):
    pass