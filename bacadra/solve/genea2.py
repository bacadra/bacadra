import random

class genea:
    def __init__(self, core):
        self.core     = core

        # initialize data input by user
        self._gd_init = {}

        # then from init data created are current object
        self.gd       = {}

        # result of current object
        self._obj     = None

        # create current line
        self.line    = []


    #$$ def --enter--
    def __enter__(self):
        return self


    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        self.run()


    def run(self):
        self._create_obj()
        self._create_line()
        self._create_weight()


    def gd_init(self, data):
        '''
        Parse and save init data inputed by user.
        '''
        self._gd_init = data


    def _genotype(self):
        '''
        Create random object of current line.
        '''
        for key,val in self._gd_init.items():
            type_val = type(val)
            if type_val is dict:
                self.gd[key] = random.randrange(val['min'], val['max'], val['step'])


    # def obj(self):
    #     # it will be redefined by user
    #     # return paramst of object
    #     pass


    def _create_obj(self):
        '''
        Save results of object'
        '''

        self._genotype()
        obj = self.obj()
        return obj

    def tree(self, tree):
        self._i = 0
        self._tree = tree

    def _get_generation_sett(self):
        self._i += 1
        return self._tree[self._i-1]

    def _create_line(self):
        line = self._get_generation_sett()
        for i in range(line['n']):
            self.line += [self._create_obj()]

    def _create_weight(self):
        result = self.goal()
        self._weight = [val/result for val in self.line]
        print(self._weight)
