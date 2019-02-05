'''
------------------------------------------------------------------------------
***** general use (f)unction (pack) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''


#$ ____ def translate ______________________________________________________ #

def translate(text, ndict):
    '''
    Replace string by dict.
    '''

    # loop over keys in dict
    for key in ndict:
        # replace text
        text = text.replace(key, str(ndict[key]))

    # return modyfied text
    return text