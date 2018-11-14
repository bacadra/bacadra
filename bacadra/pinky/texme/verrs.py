class BCDR_rstme_Error(Exception):
    pass

class BCDR_rstme_path_Error(Exception):
    pass

def pathError(path):
    raise BCDR_rstme_path_Error(f'Path <{path}> does not exists.')