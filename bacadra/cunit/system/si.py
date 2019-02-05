#$ definicja jednostek
from ..cunit import cunit # przypisanie klasy do zmiennej, mniej pisania
cunit.system = 'si'
cu   = cunit(1, {})
kN   = cunit('kN')
m    = cunit('m')
rad  = cunit('rad')
mrad = cunit('mrad')
C    = cunit('°C')
s    = cunit('s')
deg  = cunit('deg')
kNm  = kN*m
kg   = cunit('kg')
ton  = cunit('t')
K    = cunit('K')
km   = cunit('km')
dm   = cunit('dm')
cm   = cunit('cm')
mm   = cunit('mm')
GN   = cunit('GN')
MN   = cunit('MN')
MNm  = MN*m
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
