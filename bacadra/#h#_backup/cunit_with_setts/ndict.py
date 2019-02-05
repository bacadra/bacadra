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
    def str2dict(txt, othe=None):
        cdict = {}
        txt = txt.replace('**','^').replace('*',' ')
        txt = txt.split(' ')
        for val in txt:
            if val == '':
                continue

            n = val.find('^')
            if n == -1:
                txt1 = [val, '1']
            else:
                txt1 = val.split('^')

            # here is convert if user want to present unit of multiple same val
            # first find and save position of last slash
            # this way - slash is protected symbol in package!!!
            lvl = txt1[0].rfind('/')

            # if othe object is defined and if base key (without slash) is defined then go to procedure
            if othe and txt1[0][lvl+1:] in othe.base:

                # here is clue, if slash unit is not defined, then define it
                if not txt1[0] in othe.base:

                    # first get base-non-slash unit
                    inherit_unit = othe.base[txt1[0][lvl+1:]]

                    # if base-non-slash unit is base unit, then create pattern to call exacly base unit
                    if inherit_unit is None:
                        othe.add(
                            name=txt1[0],
                            value=1,
                            units={txt1[0][lvl+1:]:1},
                        )
                        inherit_unit = (1, None)

                    # if unit is not base unit, then copy definition of non-slash cunit
                    else:
                        othe.add(
                            name=txt1[0],
                            value=inherit_unit[0],
                            units=inherit_unit[1],
                        )

            if txt1[0] in cdict:
                cdict[txt1[0]] += eval(txt1[1])
            else:
                cdict.update({txt1[0]:eval(txt1[1])})

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