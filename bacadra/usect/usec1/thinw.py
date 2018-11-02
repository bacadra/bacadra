import math
from . import value
from ...cunit import cunit

class thinw:
    #$$ def --init--
    def __init__(self, core):
        self.core = core
        self._value = value.value(core=core)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    def add(self, origin, eleme):
        self. _calc_properties(origin, eleme)

        pass

    #$$ def -calc
    def _calc_properties(self, origin, eleme):

        # add origin node as first element in list
        eleme = [origin] + eleme

        # numeracja wezlow od 0 do n
        jj = range(0, len(eleme))

        # numeracja elementow od 1 do n
        ii = range(1, len(eleme))

        y = [val[0] for val in eleme]
        z = [val[1] for val in eleme]
        t = [val[2] if len(val) > 2 else 0 for val in eleme]

        # jednostkowe pola przekroju
        dA = [0]+[t[i] * ((y[i]-y[i-1])**2 + (z[i]-z[i-1])**2)**0.5 for i in ii]
        print('dA', dA)

        # pole przekroju
        A = sum(dA)
        print('A', A)

        # Moment statyczny przekroju względem osi y-y
        Sy0 = sum([(z[i] + z[i-1]) * dA[i] /2 for i in ii])
        print('Sy0', Sy0)

        # Moment statyczny przekroju względem osi z-z
        Sz0 = sum([(y[i] + y[i-1]) * dA[i] /2 for i in ii])
        print('Sz0', Sz0)

        # współrzędna środka ciężkości
        z_gc = Sy0 / A
        print('z_gc', z_gc)
        y_gc = Sz0 / A
        print('y_gc', y_gc)

        # Moment bezwładności przekroju względem pierwotnej osi y-y
        Iy0 = sum([(z[i]**2 + z[i-1]**2 + z[i]*z[i-1])*dA[i]/3 for i in ii])
        print('Iy0', Iy0)

        # Moment bezwładności y-y przekroju względem osi centralnej
        Iy = Iy0 - A*z_gc**2
        print('Iy', Iy)

        # Moment bezwładności przekroju względem pierwotnej osi z-z
        Iz0 = sum([(y[i]**2 + y[i-1]**2 + y[i]*z[i-1])*dA[i]/3 for i in ii])
        print('Iz0', Iz0)

        # Moment bezwładności z-z przekroju względem osi centralnej
        Iz = Iz0 - A*y_gc**2
        print('Iz', Iz)

        # Odśrodkowe momenty bezwładności względem osi początkowych
        Iyz0 = sum([(2*y[i-1]*z[i-1] + 2*y[i]*z[i] + y[i-1]*z[i] + y[i]*z[i-1])*dA[i]/6 for i in ii])
        print('Iyz0', Iyz0)

        # Odśrodkowe momenty bezwładności względem osi centralnych
        Iyz = Iyz0 - Sy0*Sz0/A
        print('Iyz', Iyz)

        # Położenie głównych osi bezwładności oraz
        if Iz-Iy != 0:
            α = 1/2 * math.atan(2* Iyz / (Iz - Iy))
        else:
            α = 0
        print('α', α)

        # ekstremalne momenty bezwładności
        Iξ = 0.5*(Iy + Iz + ((Iz-Iy)**2 + 4*Iyz**2)**0.5)
        print('Iξ', Iξ)

        Iη = 0.5*(Iy + Iz - ((Iz-Iy)**2 + 4*Iyz**2)**0.5)
        print('Iη', Iη)

        # wspolrzedne wycinkowe
        ω0 = [0]+[y[i-1]*z[i] - y[i]*z[i-1] for i in ii]

        ω = [0]
        for i in ii:
            val = ω[i-1] + ω0[i]
            ω += [val]

        # Średnie współrzędne wycinkowe
        Iω = sum([(ω[i-1] + ω[i])*dA[i]/2])

        ω_mean = Iω/A

        # Stałe wycin kowe
        Iyω0 = sum([(2*y[i-1]*ω[i-1] + 2*y[i]*ω[i] + y[i-1]*ω[i] + y[i]*ω[i-1])*dA[i]/6 for i in ii])

        Izω0 = sum([(2*z[i-1]*ω[i-1] + 2*z[i]*ω[i] + z[i-1]*ω[i] + z[i]*ω[i-1])*dA[i]/6 for i in ii])

        Iωω0 = sum([(ω[i]**2 + ω[i-1]**2 + ω[i]*ω[i-1])*dA[i]/3 for i in ii])

        Iyω = Iyω0 - Sz0*Iω/A
        Izω = Izω0 - Sy0*Iω/A
        Iωω = Iωω0 - Iω**2/A

        # Środek ścinania _ współrzędne
        if Iy*Iz-Iyz**2 != 0:
            y_sc = (Izω*Iz - Iyω*Iyz)/(Iy*Iz-Iyz**2)
            z_sc = (-Iyω*Iy + Izω*Iyz)/(Iy*Iz-Iyz**2)

        # Wycinkowy moment bezwładności
        Iw = Iωω + z_sc*Iyω-y_sc*Izω
        print('Iw', Iw)

        # Moment bezwładności przy skręcaniu przekroju otwartego
        It = sum([dA[i]*t[i]**2 /3 for i in ii])
        print('It', It)

        # Wskażnik wytrzymałości przy skręcaniu przekroju otwartego
        Wt = It*min(t[1:])

        # Współrzędne wycinkowe względem środka ścinania
        ωs = [ω[j]-ω_mean+z_sc*(y[j]-y_gc)-y_sc*(z[j]-z_gc) for j in jj]

        # Maksymalne współrzędne wycinkowe i wycinkowy wskażnik wytrzymałości
        ω_max = max(list(map(abs, ωs)))

        Ww = Iw / ω_max
        print('Ww', Ww)

        # Współrzędne środka ścinania względem środka ciężkości
        y_s = y_sc - y_gc
        z_s = z_sc - z_gc

        # Biegunowy moment bezwładności względem środka ścinania
        Ip = Iy+Iz+A*(y_s**2+z_s**2)

        # współrzędne środków części przekroju względem środka ścinania
        y_c = [0]+[(y[i] + y[i-1])/2 - y_gc for i in ii]
        z_c = [0]+[(z[i] + z[i-1])/2 - z_gc for i in ii]

        # Współczynniki asymetrii z, i y,-
        z_j = z_s - 0.5/Iy * sum([(z_c[i]**3 + z_c[i]*(((z[i]-z[i-1])**2)/4 + y_c[i]**2 + ((y[i]-y[i-1])**2)/12) + y_c[i]*((y[i]-y[i-1])*(z[i]-z[i-1]))/6)*dA[i] for i in ii])

        y_j = y_s - 0.5/Iz * sum([(y_c[i]**3 + y_c[i]*(((y[i]-y[i-1])**2)/4 + z_c[i]**2 + ((z[i]-z[i-1])**2)/12) + z_c[i]*((z[i]-z[i-1])*(y[i]-y[i-1]))/6)*dA[i] for i in ii])
