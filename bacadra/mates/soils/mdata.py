
class mdata:
    def __init__(self):
        pass

    def get(self, soil):
        return self._pn_b(soil=soil)


    def _pn_b(self, soil):
        return {
            'KW':
                {'name':'KW',
                 'fullname':'zwietrzelina'},
            'KWg':
                {'name':'KWg',
                'fullname':'zwietrzelina gliniasta'},
            'KR':
                {'fullname':'rumosz'},
            'KRg':
                {'fullname':'rumosz gliniasty'},
            'KO':
                {'fullname':'otoczaki'},
            'Ż':
                {'fullname':'żwir'},
            'Żg':
                {'fullname':'żwir gliniasty'},
            'Po':
                {'fullname':'posółka'},
            'Pog':
                {'fullname':'pospółka gliniasta'},
            'Pr':
                {'fullname':'Piasek gruby'},
            'Ps':
                {'fullname':'Piasek średni'},
            'Pd':
                {'fullname':'Piasek drobny'},
            'Pπ':
                {'fullname':'Piasek pylasty'},
            'Pg':
                {'fullname':'piasek gliniasty'},
            'πp':
                {'fullname':'pył piaszczysty'},
            'π':
                {'fullname':'pył'},
            'Gp':
                {'fullname':'glina piaszczysta'},
            'G':
                {'fullname':'glina'},
            'Gπ':
                {'fullname':'glina pylasta'},
            'Gpz':
                {'fullname':'glina piaszczysta zwięzła'},
            'Gz':
                {'fullname':'glina zwięzła'},
            'Gπz':
                {'fullname':'glina pylasta zwięzła'},
            'Ip':
                {'fullname':'ił piaszczysty'},
            'I':
                {'fullname':'ił'},
            'Iπ':
                {'fullname':'ił pylasty'},
        }[soil]