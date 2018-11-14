import unittest
import bacadra as bcdr
from bacadra.cunit.ce    import *
from bacadra.cunit.verrs import *

import numpy as np

#$ ____ class TestMe _______________________________________________________ #

class TestMe(unittest.TestCase):

#$$ ________ system ________________________________________________________ #

    def test_system_001(self):
        '''
        If user want to get from system nonexisted unit, then CunitSystemError occur.
        '''
        with self.assertRaises(CunitSystemError):
            bcdr.cunit('fake_m22')

    def test_system_002(self):
        '''
        If user get already existed unit, then type of return must be cunit!
        '''
        bcdr.cunit.system = 'si'
        m = bcdr.cunit('m')
        self.assertEqual(type(m), bcdr.cunit)
        self.assertEqual(m._value, 1)
        self.assertEqual(m._units, {'m':1})


    def test_system_003(self):
        '''
        Overwrite unit already exists in base should raise system error.
        '''
        with self.assertRaises(CunitSystemError):
            bcdr.cunit.add(name='μm', value=10**-9, units={'m':1})
            bcdr.cunit.add(name='μm', value=10**-9, units={'m':1})


    def test_system_004(self):
        '''
        Overwrite unit already exists in base should raise system error, but overwrite flag is start now, definition of value should change.
        '''
        with self.assertRaises(ValueError):
            mm = bcdr.cunit.add(name='μm', value=10**-9, units={'m':1}, overwrite=True)
            mm = bcdr.cunit.add(name='μm', value=2, units={'m':2}, overwrite=True)

            self.assertEqual(mm._value, 2)
            self.assertEqual(mm._units, {'m':2})
            raise ValueError()


    def test_system_005(self):
        '''
        User can change system during calculation. Of course he need to reinit variable.
        '''
        bcdr.cunit.system = 'ce'
        kPa = bcdr.cunit('kPa')
        self.assertEqual(kPa._value, 1)
        self.assertEqual(kPa._units, {'kN':1, 'm':-2})

        bcdr.cunit.system = 'si'
        kPa = bcdr.cunit('kPa') # remember! you need reinit variable
        self.assertEqual(kPa._value, 1000)
        self.assertEqual(kPa._units, {'kg':1, 'm':-1, 's':-2})

        bcdr.cunit.system = 'ce'
        kPa = bcdr.cunit('kPa')
        self.assertEqual(kPa._value, 1)
        self.assertEqual(kPa._units, {'kN':1, 'm':-2})


    def test_system_005(self):
        '''
        Accuracy .acc should change only print form of cunit!
        '''
        bcdr.cunit.acc = 1,1
        self.assertEqual((1564896.01236456*m)._value, 1564896.01236456)

    def test_system_006(self):
        '''
        '''
        bcdr.cunit.mode = 'pretty'
        bcdr.cunit.acc = 1,1
        self.assertEqual(repr(1564896.01236456*m), '2000000 [m]')

    def test_system_007(self):
        '''
        '''
        bcdr.cunit.mode = 'pretty'
        bcdr.cunit.acc = 1,100
        self.assertEqual(repr(1564896.01236456*m), '1564896 [m]')

    def test_system_008(self):
        '''
        '''
        bcdr.cunit.mode = 'pretty'
        bcdr.cunit.acc = 2,12
        self.assertEqual(repr(1564896.01236456*m), '1564896.01 [m]')

    def test_system_009(self):
        '''
        '''
        bcdr.cunit.mode = 'latex'
        bcdr.cunit.acc = 2,12
        self.assertEqual(repr(1564896.01236456*m), r'1564896.01~\textrm{m}')



#$$ ________ convert _______________________________________________________ #

    def test_convert_001(self):
        '''
        Simply convert units. It test primary function.
        '''
        bcdr.cunit.system = 'si'
        self.assertEqual(2*m, 2000*mm)
        self.assertEqual(1000*kPa, 1*MPa)

    def test_convert_003(self):
        '''
        Convert can be fully or nonfully. Here we test nonfully trade. If user convert X to Y, then him result is Y + rest.
        '''
        a = 151.55*MN
        a = a.convert('kPa')
        b = 151550*kPa*m**2
        self.assertEqual(a, b)


#$$ ________ equal / inequal _______________________________________________ #

    def test_inequal_001(self):
        self.assertTrue(2*m > 2*mm)

    def test_inequal_002(self):
        self.assertFalse(2*m > 2*m)

    def test_inequal_003(self):
        self.assertTrue(1*m >= 0.5*m)

    def test_inequal_004(self):
        '''
        Units with different primary cant be compare. cunit return CunitIncompatibleErorr exception..
        '''
        with self.assertRaises(CunitIncompatibleErorr):
            1*m >= 0.5*kPa


#$$ ________ power _________________________________________________________ #

    def test_power_001(self):
        '''
        cunit type in power is not supported. cunit package return CunitSystemError.
        '''
        with self.assertRaises(CunitSystemError): 2**m


#$$ ________ numpy _________________________________________________________ #

    def test_numpy_001(self):
        '''
        '''
        a = np.array([1,2,3])*kPa
        b = np.array([1*kPa,2*kPa,3*kPa])

        for check in a==b:
            self.assertTrue(check)

    def test_numpy_002(self):
        '''
        '''
        a = kPa*np.array([1,2,3])
        b = np.array([1*kPa,2*kPa,3*kPa])

        for check in a==b:
            self.assertTrue(check)


#$ ____ Run tests __________________________________________________________ #

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)


