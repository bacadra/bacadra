'''
------------------------------------------------------------------------------
BCDR += ***** (parse) input data *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

from . import verrs
from ..cunit import cunit


#$ class parse
class parse:

#$$ ________ organize ______________________________________________________ #

    #$$$ def run
    def run(self, parse_mode, **kwargs):
        '''
        Prepare data to add into database.
        '''

        # first parse data
        kwargs = self.easy_cunit(**kwargs)

        # if-block to detect work mode
        if parse_mode == 1:
            return self.prep_add(**kwargs)

        elif parse_mode == 2:
            return self.prep_add_full(**kwargs)

        elif parse_mode == 'update':
            return self.prep_edit(**kwargs)

        elif parse_mode == 'addm':
            return self.prep_addm(**kwargs)

        else:
            verrs.f1ParseErorr(parse_mode)


#$$ ________ parse data ____________________________________________________ #

    #$$$ def easy-cunit
    def easy_cunit(self, **kwargs):
        # user input data as **kwargs, then loop over them
        for key,val in kwargs.items():

            # if data is cunit
            if type(val)==cunit:
                # then drop value due to SI system
                kwargs[key] = val.drop(system='si')

            # if data is list
            elif type(val)==list:
                # then loop over list and recursive call to parse method
                kwargs[key] = [me.drop(system='si') if type(me) is cunit else me for me in val]

            # if data is tuple
            elif type(val)==tuple:
                # the same like list
                kwargs[key] = (me.drop(system='si') if type(me) is cunit else me for me in val)

        # return parsed data
        return kwargs


#$$ ________ prepare data __________________________________________________ #

    #$$$ def prep-add
    def prep_add(self, _data=None, **kwargs):
        '''
        Return an data prepare to use with self.dbase.add
        '''

        # prepare string of cols names closed into square bracket with additional after commas
        A = ''
        for key in kwargs.keys():
            A += f'[{key}],'

        # delete last one comma (too much)
        A = A[:-1]

        # convert kwargs into tuple
        # for key,val in kwargs.items():
        #     if val is None and key in _data:
        #             kwargs[key] = _data[key]
        C = tuple([val if val is not None else '' for val in kwargs.values()])

        # return cols and data
        return A,C


    #$$$ def prep-add-full
    def prep_add_full(self, **kwargs):
        '''
        Return also string with noname, it use with hand parsing like:
        eg. A,B,C = self.dbase.parse(id=id, name=name)
            self.dbase.exe("INSERT INTO [011]" + A + " VALUES" + B ,C)
        '''

        # create col name
        A = str(tuple(['['+str(key)+']' for key,val in kwargs.items()]))
        A = A.replace('\'','')

        # create ?,? list
        B = str('('+('?,'*len(kwargs))[:-1]+')')

        # convert kwargs into tuple
        C = tuple([val for key,val in kwargs.items()])

        # return cols, ?? and data
        return A,B,C


    #$$$ def prep-edit
    def prep_edit(self, **kwargs):
        '''
        Use is if you write edit method. If somethink is none, then it is not in used.
        '''

        J,C = '', []

        for key,val in kwargs.items():
            if val is not None:
                J += f'[{key}] = ?,'
                C.append(val)

        J = J[:-1]
        C = tuple(C)

        return J,C


    #$$$ def prer-addm
    def prep_addm(self, cols, data, defs={}):
        ldict = []

        #save length of cols header
        cols_len = len(cols)

        # loop over data row in data argument
        for i in range(len(data)):

            # at first check consist of data, like length
            if len(data[i]) != cols_len:
                verrs.f1ParseMultiError(len(data[i]), cols_len, data[i])

            idict = {}
            # loop over data in row
            for j in range(cols_len):

                # if factor of col is defined
                if cols[j]+'+f' in defs:
                    # check that value is valid form
                    if data[i][j] not in [True, False, None] and data[i][j]:
                        # if value is valid then multiply it by factor
                        # factor can consist of units
                        # TODO: how to miss doubled unit by factor
                        #       method should or not multiply cunit?
                        data[i][j] *= defs[cols[j]+'+f']

                # if default value of col is defined then replace None value
                if cols[j]+'+d' in defs:
                    # then check that val is undefined (None)
                    if data[i][j] in [None]:
                        # if it is, then replace it with default value
                        data[i][j] = defs[cols[j]+'+d']

                idict.update({cols[j]:data[i][j]})

            ldict.append(idict)

        return tuple(cols),ldict
