'''
------------------------------------------------------------------------------
***** general use (f)unction (pack) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ____ def translate _______________________________________________________ #

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


#$ ____ def dprint _________________________________________________________ #

def dprint(d, indent=0, style='1'):
    '''
    Dictonary print
    '''

    if style=='1':

        code=''
        for key, value in d.items():
            code+=('\t' * indent + str(key)+':')
            if isinstance(value, dict):
                code+='\n'+dprint(value, indent+1)
            else:
                code+=(' '+str(value)+'\n')
        return code


