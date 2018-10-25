

#$ ____ class ndict ________________________________________________________ #

class ndict:
    @staticmethod
    def clear_empty(o1):
        for key, val in o1.copy().items():
            if o1[key] == 0: o1.pop(key)

#$$ ________ def dsum ______________________________________________________ #

    @staticmethod
    def dsum(o1, o2):
        '''
        Wzajemne dodawanie wartosci w slownikach.
        '''
        onew = o1.copy()
        for key, val in o2.items():
            try:
                onew[key] += val
            except:
                onew.update({key:val})
        ndict.clear_empty(onew)
        return onew


#$$ ________ def dsub ______________________________________________________ #

    @staticmethod
    def dsub(o1, o2):
        '''
        Wzajemne odejmowanie wartosci w slownikach.
        '''
        onew = o1.copy()
        for key, val in o2.items():
            try:
                onew[key] -= val
            except:
                onew.update({key:-val})
        ndict.clear_empty(onew)
        return onew


#$$ ________ def vmul ______________________________________________________ #

    @staticmethod
    def vmul(o1, val):
        return {k:l*val for k,l in o1.items()}

#$$ ________ def str2dict __________________________________________________ #

    @staticmethod
    def str2dict(txt):
        cdict = {}
        txt = txt.split(' ')
        for val in txt:
            n = val.find('**')
            if n == -1:
                txt1 = [val, '1']
            else:
                txt1 = val.split('**')
            cdict.update({txt1[0]:txt1[1]})
        for key,value in cdict.items():
            cdict[key] = eval(value)
        return cdict


#$$ ________ def add_new ___________________________________________________ #

    @staticmethod
    def add_new(o1, o2):
        '''
        Extend dictonary o1 only if keys o2 does not exists in o1!
        '''

        for key,val in o2.items():
            if key in o1:
                raise ValueError(f'Key {key} alredy exists!')
            else:
                o1.update({key:val})
        return o1