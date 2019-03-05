'''
------------------------------------------------------------------------------
***** module & local (sett)ing(s) *****
==============================================================================

There are few rules:

- settings can not be None. value==None is work as property, value!=None working as setter.

- value==None and check==True working as setter, but return checked value, do not set is to data storage!

- there are globals flags like check and reset, which work on global zone to mass check or mass reset.

- reset delete variable from slave data and return value from master data. This way slave is again trace master data.

- reset work only if value==None.

- in tools there are methods: get, set and gst (get and set). All working with data should be done via this methods.

- to show data table call to object without arugment, eg. .setts().

- master setts is under tools.master.

- method name "tools" is prohibited!

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ######################################################################### #

#$ ____ import _____________________________________________________________ #

from .fpack import btable

#$ ____ class BCDR_ERROR ___________________________________________________ #

class BCDR_ERROR(Exception):
    pass

#$ ____ class tools ________________________________________________________ #

class tools:

#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, master=None, other=None):
        if master:
            self.master = master.tools
        else:
            self.master = None

        self.data  = {}
        self.other = other
        self.check = False
        self.reset = False

#$$ ________ def exists ____________________________________________________ #

    def exists(self, name):
        if name in self.data or (self.master!=None and name in self.master.data):
            return True
        else:
            return False

#$$ ________ def get _______________________________________________________ #

    def get(self, name, reset=None):
        '''
        Get value. Value can be erase from local dict and returned from master dict
        '''

        # if reset is not given, then load global settings
        if reset==None: reset=self.reset

        # if resset i True
        if reset==True and name in self.data:

            # then pop value from local
            self.data.pop(name)

            # and return from master
            return self.master.data[name]

        # elif flag is False and name occur in local data:
        elif name in self.data:

            # then return local version
            return self.data[name]

        # elif flag is False and name dont occur in local
        elif self.master :

            # then return value from master
            return self.master.data[name]

#$$ ________ def set _______________________________________________________ #

    def set(self, name, value, check=None):
        if check==None: check=self.check

        if check==True:
            if value==None:
                return self.get(name)
            else:
                return value
        else:
            self.data[name] = value
            # return self.data[name]

#$$ ________ def gst _______________________________________________________ #

    def gst(self, name, value, check=None, reset=None):
        if check==None: check=self.check

        if value==None and check==False:
            return self.get(name, reset)
        else:
            return self.set(name, value, check)

#$$ ________ def let _______________________________________________________ #

    def let(self, name, value, check=None, reset=None, full={}, **kwargs):
        '''
        let(value==True) -> set new full string
        let(value==False) -> set new empty string
        let(value='a') -> set value='a'
        let(a=True) -> set value+='a'
        let(a=False) -> set value-='a'

        let(value=None, a=None) -> return full string
        let(value=None, a=None, check='a') return True or False
        let(check='a') return True or False
        let(check=True) return full string
        '''

        if check==None: check=self.check

        chk1 = True not in [True if val!=None else False for val in kwargs.values()]

        if value==None and chk1 and check==False:
            return self.get(name, reset)

        else:

            all_letters = kwargs.keys()

            if value==True:
                if 'True' in full:
                    value = full['True']
                else:
                    value = ''.join(all_letters)

            elif value==False:
                if 'False' in full:
                    value = full['False']
                else:
                    value = ''

            elif value==None:
                value = self.get(name)

            elif type(value)==str:
                for key in value:
                    if key not in all_letters:
                        raise(BCDR_ERROR(
                            f'Unknow letter <{key}> in string.\n'
                            f'Tip: allowable letter: {"".join(list(all_letters))}'
                        ))

            for key,val in kwargs.items():
                if   val==True  and key not in value: value+=key
                elif val==False and key in     value: value = value.replace(key,'')

            if type(check)==str:
                for key in check:
                    if key not in all_letters:
                        raise(BCDR_ERROR(
                            f'Unknow letter <{key}> in string.\n'
                            f'Tip: allowable letter: {"".join(list(all_letters))}'
                        ))
                return False not in [True if letter in value else False for letter in check]
            else:
                return self.set(name, value, check)

#$$ ________ def dct _______________________________________________________ #

    def dct(self, name, value, check=None, reset=None, full={}, **kwargs):
        '''
        dct(value==True) -> set all as True
        dct(value==False) -> set all as False
        dct('a':1) -> set 'a' as 1
        dct(value==True, b=False) -> set all but no b as True, b set as False

        dct(check=True) -> return all dict
        dct(check='a') -> return value for key a

        dct(value=False, check='b') -> first run method and return 'b' without set'

        '''

        if check==None: check=self.check

        chk1 = True not in [True if val!=None else False for val in kwargs.values()]

        if value==None and chk1 and check==False:
            return self.get(name, reset)

        else:

            if value==True:
                value = {key: True if val==None else val for key,val in kwargs.items()}

            elif value==False:
                value = {key: False if val==None else val for key,val in kwargs.items()}

            elif type(value)==str:
                value = {key:value for key in kwargs.keys()}

            elif value==None:
                value = self.get(name)

            for key,val in kwargs.items():
                if val!=None:
                    value.update({key:val})

            if type(check)==str:
                return value[check]
            else:
                return self.set(name, value, check)

#$$ ________ class setts_init ______________________________________________ #

class setts_init:

    def __init__(self, master=None, other=None):
        self.tools = tools(master, other=other)


    def __call__(self, inherit=False, force_get_cls=False):

        if self.tools.master and force_get_cls==False:
            data = { **self.tools.master.data, **self.tools.data}
        else:
            data = self.tools.data

        popkeys = []
        for key in data.keys():
            if key[0]=='_':
                popkeys.append(key)
        for key in popkeys:
            data.pop(key)

        if inherit==True: return data

        print(btable('bacadra settings', data))

#$ ######################################################################### #
