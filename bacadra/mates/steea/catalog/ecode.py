
from .. import verrs

from ....cunit.cunit import cunit

m   = cunit(1, 'm')
mm  = cunit(1, 'mm')
MPa = cunit(1, 'MPa')
GPa = cunit(1, 'GPa')


class ecode:
    def __init__(self):
        self.cdata = None

    @classmethod
    def set(self, grade, **kwargs):
        '''
        '''

        if grade[0].lower() == 's':
            self.cdata = self._en_1993_S(grade=grade, **kwargs)

        else:
            verrs.f1_BCDR_mates_steea_Error(grade)


    @classmethod
    def get(self, var, name):
        if var is None:
            if name in self.cdata:
                return self.cdata[name]
        else:
            return var


#$$ ________ en 1993 _______________________________________________________ #

    @classmethod
    def _en_1993_S(self, grade, t_max=40*mm, f_yk=None):

        if grade == 'S 235':
            if           t_max <= 40*mm: data = {'f_yk':235*MPa, 'f_uk':360*MPa}
            elif 40*mm < t_max <= 80*mm: data = {'f_yk':215*MPa, 'f_uk':360*MPa}




        if t_max <= 40*mm:
            data = {
                'S 235'         :{'f_yk':235*MPa, 'f_uk':360*MPa},
                'S 275'         :{'f_yk':275*MPa, 'f_uk':430*MPa},
                'S 355'         :{'f_yk':355*MPa, 'f_uk':510*MPa},
                'S 450'         :{'f_yk':440*MPa, 'f_uk':550*MPa},
                'S 275 N/NL'    :{'f_yk':275*MPa, 'f_uk':390*MPa},
                'S 355 N/NL'    :{'f_yk':355*MPa, 'f_uk':490*MPa},
                'S 420 N/NL'    :{'f_yk':420*MPa, 'f_uk':520*MPa},
                'S 460 N/NL'    :{'f_yk':460*MPa, 'f_uk':540*MPa},
                'S 275 M/ML'    :{'f_yk':275*MPa, 'f_uk':370*MPa},
                'S 355 M/ML'    :{'f_yk':355*MPa, 'f_uk':470*MPa},
                'S 420 M/ML'    :{'f_yk':420*MPa, 'f_uk':520*MPa},
                'S 460 M/ML'    :{'f_yk':460*MPa, 'f_uk':540*MPa},
                'S 235 W'       :{'f_yk':235*MPa, 'f_uk':360*MPa},
                'S 355 W'       :{'f_yk':355*MPa, 'f_uk':510*MPa},
                'S 460 Q/Q:/QL1':{'f_yk':460*MPa, 'f_uk':570*MPa},
                'S 235 H'       :{'f_yk':235*MPa, 'f_uk':360*MPa},
                'S 275 H'       :{'f_yk':275*MPa, 'f_uk':430*MPa},
                'S 355 H'       :{'f_yk':355*MPa, 'f_uk':510*MPa},
                'S 275 NH/NLH'  :{'f_yk':275*MPa, 'f_uk':390*MPa},
                'S 355 NH/NLH'  :{'f_yk':355*MPa, 'f_uk':490*MPa},
                'S 420 NH/NLH'  :{'f_yk':420*MPa, 'f_uk':540*MPa},
                'S 460 NH/NLH'  :{'f_yk':460*MPa, 'f_uk':560*MPa},
            }[grade]

            data.update({
                't_max': 40*mm,
            })

        else:
            raise ValueError('baza niedkonczona dla wyzszych t')


        data.update({
                'E_a'  : 210*GPa,
                'ε_yk' : (f_yk if f_yk else data['f_yk']) / (210*GPa),
                'ε_uk' : 0.05,
                'γ_M0' : 1.00,
                'γ_M1' : 1.10,
                'γ_M2' : 1.25,
        })

        # return dict with values
        return data