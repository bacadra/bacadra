import math

from . import verrs

from ...cunit.system.ce import MPa


class pbase:
    def __init__(self):
        self.cdata = None

    @classmethod
    def set(self, grade, **kwargs):
        '''
        User input name pattern, eg. C30, then method return valide dict with parametrs.
        '''

        # if name start with C then return en-1992 concrete params.
        if grade.lower() == 'c':
            self.cdata = self._en_1992_C(**kwargs)

        else:
            verrs.f1_BCDR_mates_conce_Error(grade)


    @classmethod
    def get(self, var, name):
        if var is None:
            if name in self.cdata:
                return self.cdata[name]
        else:
            return var


#$$ ________ en 1992 _______________________________________________________ #

    @classmethod
    def _en_1992_C(self, f_ck=None, f_ck_cube=None):
        '''
        Return standard concrete (Cnn/nn) parameters according to EN 1992.
        '''

        # resolve what user input
        # if user input f_ck and f_ck_cube then there is nothing to resolve
        # if user input only f_ck, then calc f_ck_cube
        if f_ck and not f_ck_cube:
            f_ck_cube = 1.25 * f_ck

        # elif user input only f_ck_cube
        elif f_ck_cube and not f_ck:
            f_ck = f_ck_cube / 1.25


        # print error if value of compressive strength is over max value
        if f_ck > 90*MPa:
            pass

        if f_ck_cube > 105*MPa:
            pass


        # medium compressive strength
        f_cm = f_ck + 8*MPa

        # secant stiffness module
        E_cm = (22*(0.1*f_cm.drop('MPa'))**0.3)*MPa

        # first plastic compresive strain
        ε_c1 = min(0.7*(f_cm.drop('MPa'))**0.31, 2.8)/1000

        if 90*MPa >= f_ck >= 50*MPa:
            # metdium tension strength of concrete due to bending test
            f_ctm = (2.12*math.log(1+0.1*f_cm.drop('MPa'),math.e))*MPa

            # first ultimate compressive strain
            ε_cu1 = (2.8+27*(0.01*(98-f_cm.drop('MPa')))**4)/1000

            # second plastic compresive strain
            ε_c2  = (2.0+0.085*(f_ck.drop('MPa') - 50)**0.53)/1000

            # second ultimate compressive strain
            ε_cu2 = (2.6+35*(0.01*(90 - f_ck.drop('MPa')))**4)/1000

            # power of inelastic function
            n_c   = 1.4+23.4*(0.01*(90-f_ck.drop('MPa')))**4

            # third plastic compresive strain
            ε_c3  = (1.75 + 0.01375*(f_ck.drop('MPa') - 50))/1000

            # third ultimate compressive strain
            ε_cu3 = (2.60 + 35*(0.01*(90-f_ck.drop('MPa')))**4)/1000

        elif 50*MPa > f_ck > 0*MPa:
            # description as above
            f_ctm = (0.30*f_ck.drop('MPa')**(2/3))*MPa
            ε_cu1 = 3.50/1000
            ε_c2  = 2.00/1000
            ε_cu2 = 3.50/1000
            n_c   = 2.00
            ε_c3  = 1.75/1000
            ε_cu3 = 3.50/1000

        # medium tension strength of concrete due to bending test 0.05% prob
        f_ctk_005 = 0.7*f_ctm

        # medium tension strength of concrete due to bending test 0.95% prob
        f_ctk_095 = 1.3*f_ctm

        # return dict with values
        return {
            'f_ck'      : f_ck,
            'f_ck_cube' : f_ck_cube,
            'f_cm'      : f_cm,
            'f_ctm'     : f_ctm,
            'f_ctk_005' : f_ctk_005,
            'f_ctk_095' : f_ctk_095,
            'E_cm'      : E_cm,
            'ε_c1'      : ε_c1,
            'ε_cu1'     : ε_cu1,
            'ε_c2'      : ε_c2,
            'ε_cu2'     : ε_cu2,
            'n_c'       : n_c,
            'ε_c3'      : ε_c3,
            'ε_cu3'     : ε_cu3,
        }

