'''
------------------------------------------------------------------------------
***** module & local (sett)ing(s) *****
==============================================================================

There are few rules:

- settings can not be None. value==None is work as property, value!=None working as setter.

- method name "tools" is prohibited!

- to simply set value please use method "tools.set"

- to simply get value please use method "tools.get"

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ######################################################################### #

from . import fpack

#$ ____ class BCDR_ERROR ___________________________________________________ #

class BCDR_ERROR(Exception):

    pass


#$ ____ class tools ________________________________________________________ #

class tools:

#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, master=None, root=None):

        self.master = master

        self.data   = {}

        self.root = root

        self.check = False

#$$ ________ def get _______________________________________________________ #

    def get(self, name):

        # if value is set for current object
        if name in self.data:

            return self.data[name]

        elif self.master:

            return self.master.get(name)

        else:

            from . import verrs

            verrs.BCDR_tools_ERROR_setts_get_unknow(name)

            # raise(BCDR_ERROR(
            #     'e0001'
            #     '$$!$!$$'
            #     f'Unknow setting <{name}>\n'
            #     'Tip: please check that init method set'
            # ))

#$$ ________ def set _______________________________________________________ #

    def set(self, name, value):

        self.data[name] = value

#$$ ________ def chk _______________________________________________________ #

    def chk(self, name, value):
        '''Check'''

        if value==None:
            return self.get(name)

        else:
            return value

#$$ ________ def gst _______________________________________________________ #

    def gst(self, name, value=None):
        '''Get, set'''

        if value==None:
            return self.get(name)

        else:
            self.set(name, value)

#$$ ________ def sgc _______________________________________________________ #

    def sgc(self, name, value, check, return_always=False):
        '''Set, get, check'''

        if check==None: check=self.check

        if value==None:
            return self.get(name)

        elif check==True:
            return value

        else:
            self.set(name, value)
            if return_always: return value


#$$ ________ def multiname _________________________________________________ #

    def multiname(self, _get, _check, _base, _driver=None, _sub={}, **kwargs):
        '''

        ***** Parameters *****

        _get: [str, list with strings]
            can be given as string or list with strings, then return subname value or list with subnames value's

        _check: [bool]

        _base: [str]
            base name for subnames, then it can be found as {base}.{subname}

        _driver: [letters via string]
            letchk can be applied if multiname is used to manage letters via string values.
            ref: bcdr.core.tools.fpack.letchk

        _sub: [dict]:

            *key*: [letter via string]
                shortcut name given as single letter

            *val*: [string]
                original name, which will be passed instead of letter given as key


        **kwargs:
            optional value to check by multiname methods. if value will be None, then the element will be skipped

            *key*:
                given subname

            *val*:
                value for subname

        '''

        if _check==None: _check=self.check

        out = []

        get_list = [_sub[val] if val in _sub else val for val in _get]

        for key,val in kwargs.items():

            if _driver!=None and val!=None:
                fpack.letchk(_driver, letters=val, mode='valid')

            if val==None and key in get_list:

                out.append(self.get(f'{_base}:{key}'))

            elif val==None:

                continue

            elif key in get_list:

                out.append(val)

            if val!=None and _check!=True:
                self.set(f'{_base}:{key}', val)

        if len(out)==1:
            return out[0]

        else:
            return out


#$$ ________ def pop _______________________________________________________ #

    def pop(self, name):
        '''Pop value from data'''

        self.data.pop(name)

#$$ ________ def create_slave ______________________________________________ #

    def create_slave(self):
        '''Return new tools with auto self-mastering'''

        return tools(master=self, root=self.root)



#$ ____ class sinit ________________________________________________________ #

class sinit:

#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, master=None, root=None):

        self.tools = tools(master=master, root=root)

#$$ ________ def __call__ __________________________________________________ #

    def __call__(self, master=True, pretty=False):

        if master:

            # create list to append data
            data_temp = []

            # init loop
            othe = self.tools

            # loop
            while othe.master:

                othe = othe.master

                data_temp.append(othe.data)

            data = {}

            for i in range(len(data_temp)):

                data.update(data_temp[-i-1])

            data.update(self.tools.data)

        else:
            data = self.tools.data

        if pretty:
            print(fpack.btable('bacadra settings', data))

        else:
            return data





















#$ ######################################################################### #





    # def getin(self, name):
    #
    #     if name in self.data:
    #
    #         return True, self.data[name]
    #
    #     elif self.master:
    #
    #         for mst in self.master:
    #
    #             value = mst.getin(name)
    #
    #             if value!=(None,None):
    #
    #                 return value
    #
    #         return None, None
    #
    #     else:
    #
    #         return None, None
    #
    #
    # def get(self, name):
    #
    #     flag, value = self.getin(name)
    #
    #     if flag: return value
    #
    #     else:
    #
    #         raise(BCDR_ERROR(
    #             f'Unknow setting <{name}>\n'
    #             'Tip: please check that init method set'
    #         ))
