
import inspect
import copy

#$ ____ metaclass settsmeta ________________________________________________ #

class settsmeta(type):

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    #$$ def --setattr--
    def __setattr__(self, name, value):
        '''
        Method do not allow create new variable in class. It is provide more control over user correctly or spell-checker.
        '''

        if not hasattr(self, name) and inspect.stack()[1][3] != '__init__':
            raise AttributeError(f"Creating new attributes <{name}> is not allowed!")

        type.__setattr__(self, name, value)


    #$$ def --repr--
    def __repr__(self):
        '''
        Print only overwritten parameters and only not "private" atributes and methods.
        '''

        data = []
        for key in dir(self):
            if (key[0] == '_' and key[1] != '_' and key[-1] != '_' and key not in ['_scope', '_scope_']):
                val = eval('self.' + key)
                if type(val) is str: val = '"' + str(val) + '"'
                data.append('> {:14s} : {}'.format(key[1:], val))

        return '\n'.join(data) if len(data) > 0 else 'There are no overwritten atributes :-)'

    #$$ def test
    def test(self, name, value=None, subname=None):
        '''
        Methods provide interface to get local variable of settings. It does not change class atribute, only return as inherited.
        '''

        if subname is None:
            if value is None:
                return eval(f'self.{name}')
            else:
                return eval(f'self._{name}_')(value)

        elif subname is not None:
            if value is None:
                return eval(f'self.{name}')[subname]
            else:
                return (eval(f'self._{name}_')({subname:value}))[subname]

    #$$ def set
    def set(self, **kwargs):
        '''
        Methods provide interface to get local variable of settings. It does not change class atribute, only return as inherited.
        '''

        for key,val in kwargs.items():
            setattr(eval('self'), key, val)
