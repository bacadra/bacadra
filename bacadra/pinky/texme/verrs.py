'''
------------------------------------------------------------------------------
BCDR += ***** (v)arious (err)or(s) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

import os

class BCDR_rstme_Error(Exception):
    pass

class BCDR_rstme_path_Error(Exception):
    pass




def pathError(path):
    '''
    Simple return info about path.
    '''
    raise BCDR_rstme_path_Error(f'Path <{path}> does not exists.')


def pathTemplateError(path, template_dir):
    '''
    Return info that template does not exists and print all avaiable template.
    '''

    dirlist = [name for name in os.listdir(template_dir) if os.path.isdir(os.path.join(template_dir, name)) ]

    name = '\n'.join(['>> ' + val for val in dirlist])

    raise BCDR_rstme_path_Error(f'Folder <{path}> does not exists. \nTip: try to use on of avaiable templates:\n{name}')