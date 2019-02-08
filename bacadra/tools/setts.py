'''
------------------------------------------------------------------------------
***** module & local (sett)ing(s) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ____ module _____________________________________________________________ #

from .color import colored


#$ ____ class settsmeta ____________________________________________________ #

class settsmeta(type):


#$$ ________ atributes _____________________________________________________ #

    __temp__ = None
    __save__ = True
    __addp__ = []

#$$ ________ def __setattr__ _______________________________________________ #

    def __setattr__(self, name, value):
        '''
        Method do not allow create new variable in class. It is provide more control over user correctly or spell-checker.
        '''

        if not hasattr(self, name):
            raise AttributeError(f"Creating new attributes <{name}> is not allowed!")

        type.__setattr__(self, name, value)


#$$ ________ def set _______________________________________________________ #

    def set(self, **value):
        '''
        Type of value is dict.
        '''

        for key,val in value.items():
            setattr(self, key, val)


#$$ ________ def check _____________________________________________________ #

    def check(self, name, value=None, subname=None):
        try:
            return self.check_loc(name=name, value=value, subname=subname)
        except:
            return self.check_cls(name=name, value=value, subname=subname)

#$$ ________ def check_cls _________________________________________________ #

    @classmethod
    def check_cls(self, name, value=None, subname=None):
        if value == None:
            if subname:
                return getattr(self, name)[subname]
            else:
                return getattr(self, name)
        else:
            if hasattr(self, '_setts__'+name):
                self.__save__ = False
                if subname:
                    setattr(self, name, {subname:value})
                else:
                    setattr(self, name, value)
                self.__save__ = True
                return self.__temp__ if subname==None else self.__temp__[subname]
            else:
                return value


#$$ ________ def check_loc _________________________________________________ #

    def check_loc(self, name, value=None, subname=None):
        if value == None:
            if subname:
                return getattr(self, name)[subname]
            else:
                return getattr(self, name)
        else:
            if hasattr(self, '_setts__'+name):
                self.__save__ = False
                if subname:
                    setattr(self, name, {subname:value})
                else:
                    setattr(self, name, value)
                self.__save__ = True
                return self.__temp__ if subname==None else self.__temp__[subname]
            else:
                return value





#$$ ________ def print _____________________________________________________ #

    def print(self, inherit=False, get_cls=True):
        try:
            return self.print_loc(inherit=inherit, get_cls=get_cls)
        except:
            return self.print_cls(inherit=inherit)

#$$ ________ def print_cls _________________________________________________ #

    @classmethod
    def print_cls(self, inherit=False):

        data = {}

        for key in dir(self):
            if key[:8]=='_setts__':
                val = getattr(self, key)
                data.update({key[8:]:val})

        if self.__addp__:
            data.update(self.__addp__)

        if inherit:
            return data


        pdata = [colored('---------------------------------------------------------------------------\n''***** bacadra class settings *****', 'magenta')]

        for key,val in data.items():
            if type(val) is str: val = "'" + str(val) + "'"
            pdata.append('> {:14s} : {}'.format(key, val))

        if len(pdata)==1: pdata+=['There are no atributes.']
        print('\n'.join(pdata))


#$$ ________ def print_loc _________________________________________________ #

    def print_loc(self, inherit=False, get_cls=True):

        if get_cls:
            try:
                data = self.print_cls(inherit=True)

            except:
                data = {}
        else:
            data = {}

        for key in dir(self):
            if key[:8]=='_setts__':
                val = getattr(self, key)
                data.update({key[8:]:val})

        if self.__addp__:
            data.update(self.__addp__)

        if inherit:
            return data


        pdata = [colored('---------------------------------------------------------------------------\n''***** bacadra object settings *****', 'magenta')]

        for key,val in data.items():
            if type(val) is str: val = "'" + str(val) + "'"
            pdata.append('> {:14s} : {}'.format(key, val))

        if len(pdata)==1: pdata+=['There are no atributes (maybe overwritten).']
        print('\n'.join(pdata))


#$$ ________ def me ________________________________________________________ #

    @property
    def me(self):

        try:
            data = self.print_loc(inherit=True, get_cls=True)
            name = 'object'
        except:
            data = self.print_cls(inherit=True)
            name = 'class'

        pdata = [colored('---------------------------------------------------------------------------\n''***** bacadra '+name+' settings *****', 'magenta')]

        for key,val in data.items():
            if type(val) is str: val = "'" + str(val) + "'"
            pdata.append('> {:14s} : {}'.format(key, val))

        if len(pdata)==1: pdata+=['There are no atributes (maybe overwritten).']
        print('\n'.join(pdata))



#$$ ________ def me ________________________________________________________ #

    def __call__(self, *args):
        if args:
            return type.__call__(self, *args)

        try:
            data = self.print_loc(inherit=True, get_cls=True)
            name = 'object'
        except:
            data = self.print_cls(inherit=True)
            name = 'class'

        pdata = [colored('---------------------------------------------------------------------------\n''***** bacadra '+name+' settings *****', 'magenta')]

        for key,val in data.items():
            if type(val) is str: val = "'" + str(val) + "'"
            pdata.append('> {:14s} : {}'.format(key, val))

        if len(pdata)==1: pdata+=['There are no atributes (maybe overwritten).']
        print('\n'.join(pdata))
