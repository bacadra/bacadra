'''
------------------------------------------------------------------------------
BCDR += ***** (thin)-(w)alled 1d unit-sections *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

import math
from . import value
from ...cunit import cunit

class thinw:
    #$$ def __init__
    def __init__(self, core):
        self.core = core
        self._value = value.value(core=core)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exI_t--
    def __exit__(self, type, value, traceback):
        pass

    def add(self, id=None, mate=None, eleme=None, ttl=None):

        y_gc,z_gc,y_sc,z_sc,A,I_t,I_ω,I_y,I_z,I_ξ,I_η,I_p,u,α = self._prop_brutto(eleme, mate)

        # parse universal units section 1d data
        self._value.add(
            id     = id,
            mate   = mate,
            A      = A,
            A_y    = None,
            A_z    = None,
            I_t    = I_t,
            I_ω    = I_ω,
            I_y    = I_y,
            I_z    = I_z,
            I_ξ    = I_ξ,
            I_η    = I_η,
            I_p    = I_p,
            u      = u,
            ttl    = ttl,
            y_gc   = y_gc,
            z_gc   = z_gc,
            y_sc   = y_sc,
            z_sc   = z_sc,
            α      = α,
            _subcl = 'thinw',
        )


    #$$ def -calc
    def _prop_brutto(self, eleme, mate):

        # numeracja wezlow od 0 do n
        jj = range(0, len(eleme))

        # numeracja elementow od 1 do n
        ii = range(1, len(eleme))

        # create init list
        y,z,t = [],[],[]

        # loop over element and divide tuple into y,z,t list
        for row in eleme:

            # first element is coor y, if cunit then drop in si system
            y += [row[0].drop(system='si') if type(row[0])==cunit else row[0]]

            # second element is coor z, if cunit then drop in si system
            z += [row[1].drop(system='si') if type(row[1])==cunit else row[1]]

            # third element is thickness t, if cunit then drop in si system
            # but if line is juz move to other coor, then user insert only
            # len 2 tuple, so check it first
            if len(row)==3:
                t += [row[2].drop(system='si') if type(row[2])==cunit else row[2]]
            else:
                t += [0]

        # jednostkowe pola przekroju
        dA = [0]+[t[i] * ((y[i]-y[i-1])**2 + (z[i]-z[i-1])**2)**0.5 for i in ii]

        # obwod pola (suma dlugosci elementow o grubosci wiekszej od zera)
        u = sum([((y[i]-y[i-1])**2 + (z[i]-z[i-1])**2)**0.5 if t[i]>0 else 0 for i in ii])*2

        # pole przekroju
        A = sum(dA)

        # Moment statyczny przekroju względem osi y-y
        Sy0 = sum([(z[i] + z[i-1]) * dA[i] /2 for i in ii])

        # Moment statyczny przekroju względem osi z-z
        Sz0 = sum([(y[i] + y[i-1]) * dA[i] /2 for i in ii])

        # współrzędna środka ciężkości
        z_gc = Sy0 / A
        y_gc = Sz0 / A

        # Moment bezwładności przekroju względem pierwotnej osi y-y
        I_y0 = sum([(z[i]**2 + z[i-1]**2 + z[i]*z[i-1])*dA[i]/3 for i in ii])

        # Moment bezwładności y-y przekroju względem osi centralnej
        I_y = I_y0 - A*z_gc**2

        # Moment bezwładności przekroju względem pierwotnej osi z-z
        I_z0 = sum([(y[i]**2 + y[i-1]**2 + y[i]*y[i-1])*dA[i]/3 for i in ii])

        # Moment bezwładności z-z przekroju względem osi centralnej
        I_z = I_z0 - A*y_gc**2

        # Odśrodkowe momenty bezwładności względem osi początkowych
        I_yz0 = sum([(2*y[i-1]*z[i-1] + 2*y[i]*z[i] + y[i-1]*z[i] + y[i]*z[i-1])*dA[i]/6 for i in ii])

        # Odśrodkowe momenty bezwładności względem osi centralnych
        I_yz = I_yz0 - Sy0*Sz0/A

        # Położenie głównych osi bezwładności oraz
        if I_z-I_y != 0:
            α = 1/2 * math.atan(2* I_yz / (I_z - I_y))
        else:
            α = 0

        # ekstremalne momenty bezwładności
        I_ξ = 0.5*(I_y + I_z + ((I_z-I_y)**2 + 4*I_yz**2)**0.5)

        I_η = 0.5*(I_y + I_z - ((I_z-I_y)**2 + 4*I_yz**2)**0.5)

        # wspolrzedne wycinkowe
        ω0 = [0]+[y[i-1]*z[i] - y[i]*z[i-1] for i in ii]

        ω = [0]
        for i in ii:
            val = ω[i-1] + ω0[i]
            ω += [val]

        # Średnie współrzędne wycinkowe
        I_ωs = sum([(ω[i-1] + ω[i])*dA[i]/2])

        ω_mean = I_ωs/A

        # Stałe wycinkowe
        I_yω0 = sum([(2*y[i-1]*ω[i-1] + 2*y[i]*ω[i] + y[i-1]*ω[i] + y[i]*ω[i-1])*dA[i]/6 for i in ii])

        I_zω0 = sum([(2*z[i-1]*ω[i-1] + 2*z[i]*ω[i] + z[i-1]*ω[i] + z[i]*ω[i-1])*dA[i]/6 for i in ii])

        I_ωsω0 = sum([(ω[i]**2 + ω[i-1]**2 + ω[i]*ω[i-1])*dA[i]/3 for i in ii])

        I_yω = I_yω0 - Sz0*I_ωs/A
        I_zω = I_zω0 - Sy0*I_ωs/A
        I_ωsω = I_ωsω0 - I_ωs**2/A

        # Środek ścinania _ współrzędne
        if I_y*I_z-I_yz**2 != 0:
            y_sc = (I_zω*I_z - I_yω*I_yz)/(I_y*I_z-I_yz**2)
            z_sc = (-I_yω*I_y + I_zω*I_yz)/(I_y*I_z-I_yz**2)
        print(I_y*I_z-I_yz**2)


        # Wycinkowy moment bezwładności
        I_ω = I_ωsω + z_sc*I_yω-y_sc*I_zω

        # Moment bezwładności przy skręcaniu przekroju otwartego
        I_t = sum([dA[i]*t[i]**2 /3 for i in ii])

        # Wskażnik wytrzymałości przy skręcaniu przekroju otwartego
        Wt = I_t*min(t[1:])

        # Współrzędne wycinkowe względem środka ścinania
        ωs = [ω[j]-ω_mean+z_sc*(y[j]-y_gc)-y_sc*(z[j]-z_gc) for j in jj]

        # Maksymalne współrzędne wycinkowe
        ω_max = max(list(map(abs, ωs)))

        # wycinkowy wskażnik wytrzymałości
        Ww = I_ω / ω_max

        # Współrzędne środka ścinania względem środka ciężkości
        y_s = y_sc - y_gc
        z_s = z_sc - z_gc

        # Biegunowy moment bezwładności względem środka ścinania
        I_p = I_y+I_z+A*(y_s**2+z_s**2)

        # współrzędne środków części przekroju względem środka ścinania
        y_c = [0]+[(y[i] + y[i-1])/2 - y_gc for i in ii]
        z_c = [0]+[(z[i] + z[i-1])/2 - z_gc for i in ii]

        # Współczynniki asymetrii z, i y,-
        z_j = z_s - 0.5/I_y * sum([(z_c[i]**3 + z_c[i]*(((z[i]-z[i-1])**2)/4 + y_c[i]**2 + ((y[i]-y[i-1])**2)/12) + y_c[i]*((y[i]-y[i-1])*(z[i]-z[i-1]))/6)*dA[i] for i in ii])

        y_j = y_s - 0.5/I_z * sum([(y_c[i]**3 + y_c[i]*(((y[i]-y[i-1])**2)/4 + z_c[i]**2 + ((z[i]-z[i-1])**2)/12) + z_c[i]*((z[i]-z[i-1])*(y[i]-y[i-1]))/6)*dA[i] for i in ii])

        return y_gc,z_gc,y_sc,z_sc,A,I_t,I_ω,I_y,I_z,I_ξ,I_η,I_p,u,α