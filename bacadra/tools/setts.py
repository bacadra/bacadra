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

            raise(BCDR_ERROR(
                f'e0001$$!$!$$Unknow setting <{name}>\n'
                'Tip: please check that init method set'
            ))

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

    def sgc(self, name, value, check):
        '''Set, get, check'''

        if check==None: check=self.check

        if value==None:
            return self.get(name)

        elif check==True:
            return value

        else:
            self.set(name, value)

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

    def __call__(self, master=True):

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

            return data

        else:

            return self.tools.data





















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
