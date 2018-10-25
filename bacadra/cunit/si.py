#$ definicja stalych
import math
pi  = math.pi
π   = math.pi
e   = math.e
del math

#$ definicja jednostek
from .units import cunit # przypisanie klasy do zmiennej, mniej pisania
cunit.system = 'si'
kN   = cunit('kN')
m    = cunit('m')
rad  = cunit('rad')
mrad = cunit('mrad')
C    = cunit('C')
s    = cunit('s')
deg  = cunit('deg')
kNm  = cunit('kNm')
MNm  = cunit('MNm')
kg   = cunit('kg')
ton  = cunit('t')
K    = cunit('K')
km   = cunit('km')
dm   = cunit('dm')
cm   = cunit('cm')
mm   = cunit('mm')
GN   = cunit('GN')
MN   = cunit('MN')
N    = cunit('N')
yr   = cunit('yr')
day  = cunit('day')
hr   = cunit('hr')
mn   = cunit('min')
GPa  = cunit('GPa')
MPa  = cunit('MPa')
kPa  = cunit('kPa')
Pa   = cunit('Pa')
Hz   = cunit('Hz')
del cunit
