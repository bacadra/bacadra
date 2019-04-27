'''
------------------------------------------------------------------------------
***** (f)ast (c)ode (lib)rary | (civil) engineering *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ######################################################################### #

import os

import pandas as pd

from bacadra.tools.setts import sinit

from bacadra.unise.unise import unise

from bacadra.unise.si import MPa,mm,m,Hz,cu,s,kN,N

from bacadra.unise.umath import π,sqrt


#$ ____ class setts ________________________________________________________ #

class setts(sinit):
    pass

#$ ____ class lib __________________________________________________________ #

class lib:

    setts = setts()

#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, texme):

        self.texme = texme

        self.setts = setts(self.setts.tools, self)

        self.tools = tools(lib=self)

        self.loads = loads(lib=self)

        self.steea = steea(lib=self)

        self.footb = footb(lib=self)


#$ ____ class tools ________________________________________________________ #

class tools:

#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, lib):

        self.lib = lib

    def summary(self, η):

        if type(η)==unise: η = η.drop('')

        if η==False or η>1:
            text =  r'\b{\color{red} warunek niespełniony}'

        elif η<0:
            text = r'\b{\color{yellow} warunek błędny (!!!)}'

        else:
            text = r'\b{\color{green} warunek spełniony}'

        return text


    def isum(self, η):

        self.lib.texme.item('wnioski', self.summary(η), 't')


#$ ____ class loads ________________________________________________________ #

class loads:

#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, lib):

        self.lib = lib

    def act_fact_table_G(self, γ_G_sup, γ_G_inf):

        d_γ_G_sup = self.lib.texme.core.tools.clang(
            pl='współczynnik bezpieczeństwa, niekorzystny',
            en='safety factor, unfavourable',
        )

        d_γ_G_inf = self.lib.texme.core.tools.clang(
            pl='współczynnik bezpieczeństwa, korzystny',
            en='safety factor, favourable',
        )

        self.lib.texme.t(
            cols     = 'e{13.0cm}C',
            float    = 'long',
            stretchV = 1.3,
            data     = rf'''
        \hlineb
            {d_γ_G_sup}: $γ_G_sup=$ & {γ_G_sup:d2:td} \\
        \hline
            {d_γ_G_inf}: $γ_G_inf=$ & {γ_G_inf:d2:td} \\
        \hlineb
        ''')


    def act_fact_table_Q(self, γ_F_sup, γ_F_inf, ψ_0, ψ_1, ψ_2):

        d_γ_F_sup = self.lib.texme.core.tools.clang(
            pl='współczynnik bezpieczeństwa, niekorzystny',
            en='safety factor, unfavourable',
        )

        d_γ_F_inf = self.lib.texme.core.tools.clang(
            pl='współczynnik bezpieczeństwa, korzystny',
            en='safety factor, favourable',
        )

        d_ψ_0 = self.lib.texme.core.tools.clang(
            pl='współczynnik dla wartości kombinacyjnej oddziaływania zmiennego',
            en='coefficient for the combination value of the variable interaction',
        )

        d_ψ_1 = self.lib.texme.core.tools.clang(
            pl='współczynnik dla wartości częstej oddziaływania zmiennego',
            en='coefficient for the value of the frequent variable impact',
        )

        d_ψ_2 = self.lib.texme.core.tools.clang(
            pl='współczynnik dla wartości prawie stałej oddziaływania zmiennego',
            en='coefficient for quasi permanent value of a variable impact',
        )


        self.lib.texme.t(cols=' e{13.0cm} C ',
              float='long',
              stretchV=1.3,
              data=rf'''
        \hlineb
            {d_γ_F_sup}: $γ_F_sup=$ & {γ_F_sup:d2:td} \\
        \hline
            {d_γ_F_inf}: $γ_F_inf=$ & {γ_F_inf:d2:td} \\
        \hline
            {d_ψ_0}:     $ψ_0=$     & {ψ_0:d2:td}     \\
        \hline
            {d_ψ_1}:     $ψ_1=$     & {ψ_1:d2:td}     \\
        \hline
            {d_ψ_2}:     $ψ_2=$     & {ψ_2:d2:td}     \\
        \hlineb
        ''')




#$ ____ class steea ________________________________________________________ #

class steea:

#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, lib):

        self.lib = lib

        self.eqj2 = steea.eqj2(lib=lib)

        self.nkes = steea.nkes(lib=lib)

        self.sbmo = steea.sbmo(lib=lib)

        self.sbmn = steea.sbmn(lib=lib)

        self.η_bi_pl = steea.η_bi_pl(lib=lib)

    @staticmethod
    def α_imp(α_imp):
        '''
        Buckling imperfection parameter is equal to lateral torsional imperfection amplitude.
        '''
        if   α_imp=='a0': return 0.13
        elif α_imp=='a' : return 0.21
        elif α_imp=='b' : return 0.34
        elif α_imp=='c' : return 0.49
        elif α_imp=='d' : return 0.76
        else            : return α_imp

    @staticmethod
    def λ_(α_ult, α_cr):
        return sqrt((α_ult)/(α_cr))

    @staticmethod
    def χ_def1(α_imp, λ_):
        α_imp = steea.α_imp(α_imp)
        φ = 0.5*(1+α_imp*(λ_-0.2)+λ_**2)
        return min(1, 1/(φ+sqrt(φ**2-λ_**2)))

    @staticmethod
    def χ_def2(α_imp, α_ult, α_cr):
        return steea.χ_def1(α_imp, steea.λ_(α_ult, α_cr))

#$$ ________ class η_bi_pl _________________________________________________ #

    class η_bi_pl:
        '''
        utilization level for (b)isymetrical (i)-section for 1-2 class (pl)astic
        '''

        def __init__(self, lib):

            self.lib = lib


        def chp(self, text=None):

            tex = self.lib.texme

            if text:
                text = ' -- '+text
            else:
                text = ''

            tex.h(3, rf'Nośność przekroju z uwagi na kryterium J2'+text)


        def res(self, h, b, t_f, t_w, r, ΔA, f_yk, f_uk, η_ec, γ_M0, γ_M2, output='', ΔA_z=0, ΔA_y=0, ΓM_y=1, ΓM_z=1):

            h      = unise.drop(h    , 'm'  )
            b      = unise.drop(b    , 'm'  )
            t_f    = unise.drop(t_f  , 'm'  )
            t_w    = unise.drop(t_w  , 'm'  )
            r      = unise.drop(r    , 'm'  )
            ΔA     = unise.drop(ΔA   , 'm2' )
            ΔA_y   = unise.drop(ΔA_y , 'm2' )
            ΔA_z   = unise.drop(ΔA_z , 'm2' )
            f_yk   = unise.drop(f_yk , 'Pa' )
            f_uk   = unise.drop(f_uk , 'Pa' )
            η_ec   = unise.drop(η_ec , ''   )
            γ_M0   = unise.drop(γ_M0 , ''   )
            γ_M2   = unise.drop(γ_M2 , ''   )

            self.h = h

            self.b = b

            self.t_f = t_f

            self.t_w = t_w

            self.r = r

            self.f_yk = f_yk

            self.η_ec = η_ec

            self.γ_M0 = γ_M0


            # web height
            self.h_w = h_w = h-2*t_f

            # cross-section area
            self.A = A = h_w*t_w + 2*b*t_f + (r**2 - π*r**2)

            # cross-section effective shear area
            A_z = max(A - 2*b*t_f + (t_w+2*r)*t_f, η_ec*h_w*t_w) + ΔA_z
            A_y = A - h_w*t_w + ΔA_y

            # cross-section netto area
            A_net = A - ΔA

            # resistance to ultimate tension
            N_u_Rd = 0.9*A_net*f_uk/γ_M2

            # plastic axial resistance
            self.N_pl_Rd   = A*f_yk/γ_M0

            # section reistance to tension
            self.N_t_Rd = min(N_u_Rd, self.N_pl_Rd)

            # shear resistance
            self.V_y_pl_Rd = A_y * f_yk / sqrt(3) / γ_M0
            self.V_z_pl_Rd = A_z * f_yk / sqrt(3) / γ_M0

            # benidng resistnace
            self.M_y_pl_Rd = (b*t_f*(0.5*h-0.5*t_f) + 0.5*h_w*t_w*0.25*h_w)*2*f_yk/γ_M0 * ΓM_y

            self.M_z_pl_Rd = (b**2*t_f/4 * 2 + t_w**2 * h_w/4)*f_yk/γ_M0 * ΓM_z


            I_y = 2*b*t_f**3/12 + 2*b*t_f*(0.5*h-0.5*t_f)**2 + t_w*(h-t_f)**3/12

            S_y_max = b*t_f*(0.5*h-0.5*t_f)+0.5*t_w*(0.5*h-t_f)**2

            self.V_z_el_Rd = f_yk * I_y * t_w / sqrt(3) / S_y_max + f_yk/sqrt(3)*ΔA_z

            if output!='':

                data = {
                    'h_w'       : (h_w            *m)('umm'),
                    'A'         : (A              *m**2)('ucm2'),
                    'A_y'       : (A_y            *m**2)('ucm2'),
                    'A_z'       : (A_z            *m**2)('ucm2'),
                    'A_net'     : (A_net          *m**2)('ucm2'),
                    'N_u_Rd'    : (N_u_Rd         *N)('ukN'),
                    'N_pl_Rd'   : (self.N_pl_Rd   *N)('ukN'),
                    'N_t_Rd'    : (self.N_t_Rd    *N)('ukN'),
                    'V_y_pl_Rd' : (self.V_y_pl_Rd *N)('ukN'),
                    'V_z_pl_Rd' : (self.V_z_pl_Rd *N*m)('ukN m'),
                    'M_y_pl_Rd' : (self.M_y_pl_Rd *N*m)('ukN m'),
                    'M_z_pl_Rd' : (self.M_z_pl_Rd *N*m)('ukN m'),
                    'V_z_el_Rd' : (self.V_z_el_Rd *N)('ukN'),
                    'I_y'       : (I_y*m**4)('ucm4'),
                    'S_y_max'   : (S_y_max*m**3)('ucm3'),
                }

                if 't' in output:

                    pass

                if 'p' in output:

                    print(data)

                if 'r' in output:

                    return data


        def chk(self, N_Ed, V_y_Ed, V_z_Ed, M_y_Ed, M_z_Ed, calc, output=''):
            '''
            a -- tension,
            b -- compression,
            c -- bending yy,
            d -- bending zz,
            e -- shear yy,
            f -- shear zz,
            g -- bending yy with shear yy,
            h -- bending zz with shear zz,
            i -- bending yy with axial,
            j -- bending zz with axial,
            k -- bending yy+zz with axial,
            l -- bending yy with shear yy and axial,
            m -- bending zz with shear zz and axial,
            n -- bending yy+zz with shear yy+zz and axial,
            o -- bending yy+zz with shear yy+zz and axial - sofi,
            p -- linear summation of utilization,
            r -- linear summation of utilization - without shear,
            s -- linear summation of utilization - sofi,
            '''

            V_y_Ed = abs(unise.drop(V_y_Ed, 'N'))
            V_z_Ed = abs(unise.drop(V_z_Ed, 'N'))
            M_y_Ed = abs(unise.drop(M_y_Ed, 'N m'))
            M_z_Ed = abs(unise.drop(M_z_Ed, 'N m'))

            N_Ed   = unise.drop(N_Ed  , 'N')
            N_Ed_c = -N_Ed if N_Ed<0 else 0
            N_Ed_t =  N_Ed if N_Ed>0 else 0
            N_Ed   = abs(N_Ed)


            N_t_Rd = self.N_t_Rd

            N_pl_Rd = self.N_pl_Rd

            M_y_pl_Rd = self.M_y_pl_Rd

            M_z_pl_Rd = self.M_z_pl_Rd

            V_z_pl_Rd = self.V_z_pl_Rd

            V_y_pl_Rd = self.V_y_pl_Rd

            h_w = self.h_w

            t_w = self.t_w

            f_yk = self.f_yk

            γ_M0 = self.γ_M0

            A = self.A

            b = self.b

            t_f = self.t_f

            data = {'η':{}, 'other':{}}

            if calc==True: calc = 'abcdefghijklmnoprs'

            if 'a' in calc: # tension


                η_a = N_Ed_c/N_t_Rd

                data['η']['a'] = η_a

            if 'b' in calc: # compression


                η_b = N_Ed_t/N_pl_Rd

                data['η']['b'] = η_b

            if 'c' in calc: # bending yy

                η_c = M_y_Ed/M_y_pl_Rd

                data['η']['c'] = η_c

            if 'd' in calc: # bending zz

                η_d = M_z_Ed/M_z_pl_Rd

                data['η']['d'] = η_d

            if 'e' in calc: # shear yy

                η_e = V_z_Ed/V_z_pl_Rd

                data['η']['e'] = η_e

            if 'f' in calc: # shear zz

                η_f = V_y_Ed/V_y_pl_Rd

                data['η']['f'] = η_f

            if 'g' in calc: # bending yy with shear yy

                ρ_y = (2 * V_z_Ed / V_z_pl_Rd - 1)**2 if V_z_Ed / V_z_pl_Rd>= 0.5 else 0

                M_y_pl_V_Rd = M_y_pl_Rd - (0.5*h_w*t_w*0.25*h_w*(ρ_y))*2*f_yk/γ_M0

                η_g = M_y_Ed/M_y_pl_V_Rd

                data['η']['g'] = η_g

                data['other']['ρ_y'] = ρ_y *cu

                data['other']['M_y_pl_V_Rd'] = (M_y_pl_V_Rd *N*m)('ukN m')


            if 'h' in calc: # bending zz with shear zz

                ρ_z = (2 * V_y_Ed / V_y_pl_Rd - 1)**2 if V_y_Ed / V_y_pl_Rd>= 0.5 else 0

                M_z_pl_V_Rd = M_z_pl_Rd - (t_w**2 * h_w/4*ρ_z)*f_yk/γ_M0

                η_h = M_z_Ed/M_z_pl_V_Rd

                data['η']['h'] = η_h

                data['other']['ρ_z'] = ρ_z *cu

                data['other']['M_z_pl_V_Rd'] = (M_z_pl_V_Rd *N*m)('ukN m')

            if 'i' in calc: # bending yy with axial

                n = N_Ed/N_pl_Rd

                a = min((A-2*b*t_f)/A, 0.5)

                M_y_pl_N_Rd = M_y_pl_Rd if N_Ed <= 0.25*N_pl_Rd and N_Ed<=0.5*h_w*t_f*f_yk/γ_M0 else min(M_y_pl_Rd * (1-n)/(1-0.5*a), M_y_pl_Rd)

                η_i = M_y_Ed/M_y_pl_N_Rd

                data['η']['i'] = η_i

            if 'j' in calc: # bending zz with axial

                M_z_pl_N_Rd = M_z_pl_Rd if N_Ed<= h_w*t_w*f_yk/γ_M0 else M_z_pl_Rd if n<=a else M_z_pl_Rd*(1-((n-a)/(1-a))**2)

                η_j = M_z_Ed/M_z_pl_N_Rd

                data['η']['j'] = η_j

            if 'k' in calc: # bending yy+zz with axial

                α = 2

                β = max(5*n, 1)

                η_k = (M_y_Ed/M_y_pl_N_Rd)**α + (M_z_Ed/M_z_pl_N_Rd)**β

                data['η']['k'] = η_k

            if 'l' in calc: # bending yy with shear yy and axial

                M_y_pl_N_V_Rd = M_y_pl_V_Rd if N_Ed <= 0.25*N_pl_Rd and N_Ed<=0.5*h_w*t_f*f_yk/γ_M0 else min(M_y_pl_V_Rd * (1-n)/(1-0.5*a), M_y_pl_V_Rd)

                η_l = M_y_Ed/M_y_pl_N_V_Rd

                data['η']['l'] = η_l

            if 'm' in calc: # bending zz with shear zz and axial

                M_z_pl_N_V_Rd = M_z_pl_V_Rd if N_Ed<= h_w*t_w*f_yk/γ_M0 else M_z_pl_V_Rd if n<=a else M_z_pl_V_Rd*(1-((n-a)/(1-a))**2)

                η_m = M_z_Ed/M_z_pl_N_V_Rd

                data['η']['m'] = η_m

            if 'n' in calc: # bending yy+zz with shear yy+zz and axial

                η_n = (M_y_Ed/M_y_pl_N_V_Rd)**α + (M_z_Ed/M_z_pl_N_V_Rd)**β

                data['η']['n'] = η_n

            if 'o' in calc: # bending yy+zz with shear yy+zz and axial - sofi

                η_o = (
                    (M_y_Ed/M_y_pl_N_V_Rd)**α * (1-n)**(1-α) +
                    (M_z_Ed/M_z_pl_N_V_Rd)**β * (1-n)**(1-β) +
                    N_Ed / N_pl_Rd
                )

                data['η']['o'] = η_o

            if 'p' in calc: # linear summation of utilization

                η_p = N_Ed/N_pl_Rd + M_y_Ed/M_y_pl_V_Rd + M_z_Ed/M_z_pl_V_Rd

                data['η']['p'] = η_p

            if 'r' in calc: # linear summation of utilization - without shear

                η_r = N_Ed/N_pl_Rd + M_y_Ed/M_y_pl_Rd + M_z_Ed/M_z_pl_Rd

                data['η']['r'] = η_r

            if 's' in calc: # linear summation of utilization - sofi

                η_s = N_Ed/N_pl_Rd + M_y_Ed/M_y_pl_Rd + M_z_Ed/M_z_pl_Rd + V_y_Ed/V_y_pl_Rd + V_z_Ed/V_z_pl_Rd

                data['η']['s'] = η_s

            data['η']['max'] = max(data['η'].values())

            data['η']['min'] = min(data['η'].values())

            for key in data['η'].keys():

                data['η'][key] *= cu('u%')


            if output!='':

                if 't' in output:

                    pass

                if 'p' in output:

                    print(data['η'])

                if 'd' in output:

                    data1 = {
                    'a': 'pl: tension',
                    'b': 'pl: compression',
                    'c': 'pl: bending yy',
                    'd': 'pl: bending zz',
                    'e': 'pl: shear yy',
                    'f': 'pl: shear zz',
                    'g': 'pl: bending yy with shear yy',
                    'h': 'pl: bending zz with shear zz',
                    'i': 'pl: bending yy with axial',
                    'j': 'pl: bending zz with axial',
                    'k': 'pl: bending yy+zz with axial',
                    'l': 'pl: bending yy with shear yy and axial',
                    'm': 'pl: bending zz with shear zz and axial',
                    'n': 'pl: bending yy+zz with shear yy+zz and axial',
                    'o': 'pl: bending yy+zz with shear yy+zz and axial - sofi',
                    'p': 'pl: linear summation of utilization',
                    'r': 'pl: linear summation of utilization - without shear',
                    's': 'pl: linear summation of utilization - sofi',
                    'max': 'max',
                    'min': 'min',
                    'lc': 'load case',
                    }

                    nres = {}

                    for letter,ηdata in data['η'].items():

                        nres[letter+': '+data1[letter]] = ηdata

                    return nres

                if 'r' in output:

                    return data['η']


        def chm(self, data, calc, output):

            result = {}

            if calc==True: calc = 'abcdefghijklmnoprs'

            for lc, forces in data.items():

                res = self.chk(
                    N_Ed   = forces[0]  ,
                    V_y_Ed = forces[1]  ,
                    V_z_Ed = forces[2]  ,
                    M_y_Ed = forces[3]  ,
                    M_z_Ed = forces[4]  ,
                    calc   = calc       ,
                    output = 'r'        ,
                )

                result[lc] = res


            maxg = {}
            ming = {}

            for letter in calc:

                minl,maxl=[None]*2

                for lc, val in result.items():

                    if maxl==None or maxl[letter] < val[letter]:
                            maxl=val
                            maxl['lc']=lc

                    if minl==None or minl[letter] > val[letter]:
                            minl=val
                            minl['lc']=lc

                result['η_'+letter+'_max'] = maxl
                result['η_'+letter+'_min'] = minl

                maxg[letter] = maxl[letter]
                ming[letter] = minl[letter]


            result['η_max'] = maxg
            result['η_min'] = ming

            result['η_max']['max'] = max(result['η_max'].values())
            result['η_max']['min'] = min(result['η_max'].values())

            result['η_min']['max'] = max(result['η_min'].values())
            result['η_min']['min'] = min(result['η_min'].values())


            if 'p' in output:

                # for key,val in result.items():
                #     print('{'+key+':', val)
                # print(result)
                print("{" + "\n".join("{}: {}".format(k, v) for k, v in result.items()) + "}")

            if 'd' in output:

                data = {
                'a': 'pl: tension',
                'b': 'pl: compression',
                'c': 'pl: bending yy',
                'd': 'pl: bending zz',
                'e': 'pl: shear yy',
                'f': 'pl: shear zz',
                'g': 'pl: bending yy with shear yy',
                'h': 'pl: bending zz with shear zz',
                'i': 'pl: bending yy with axial',
                'j': 'pl: bending zz with axial',
                'k': 'pl: bending yy+zz with axial',
                'l': 'pl: bending yy with shear yy and axial',
                'm': 'pl: bending zz with shear zz and axial',
                'n': 'pl: bending yy+zz with shear yy+zz and axial',
                'o': 'pl: bending yy+zz with shear yy+zz and axial - sofi',
                'p': 'pl: linear summation of utilization',
                'r': 'pl: linear summation of utilization - without shear',
                's': 'pl: linear summation of utilization - sofi',
                'max': 'max',
                'min': 'min',
                'lc': 'load case',
                }

                nres = {}

                for key,val in result.items():

                    nres[key] = {}

                    for letter,ηdata in val.items():

                        nres[key][letter+': '+data[letter]] = ηdata

                return nres


            if 'r' in output:

                return result



        def file(self, path, sheet, calc, output):

            df = pd.read_excel(path, sheet_name=sheet)

            data = df.to_numpy()

            data_sliced = {

                'lc='+str(row[0])+';'+str(row[1])+';beam='+str(row[2])+';x='+str(row[3]):
                [
                    row[4]*1000,
                    row[5]*1000,
                    row[6]*1000,
                    row[8]*1000,
                    row[9]*1000,
                ]

            for row in data}

            return self.chm(data=data_sliced, calc=calc, output=output)


#$$ ________ class eqj2 ____________________________________________________ #

    class eqj2:

        def __init__(self, lib):

            self.lib = lib

        def chp(self, text=None):

            tex = self.lib.texme

            if text:
                text = ' -- '+text
            else:
                text = ''

            tex.h(3, rf'Nośność przekroju z uwagi na kryterium J2'+text)


        def res(self, us):

            tex = self.lib.texme

            tex.h(4, rf'(R) Warunek graniczny')

            self.σ_J2_Rd = σ_J2_Rd = (us.mate.f_yk/us.mate.γ_M0)

            tex.i(rf'nośność przekroju z uwagi na początek uplastycznienia',
                rf'σ_J2_Rd=f_yk/γ_M0=({us.mate.f_yk:uMPa})/({us.mate.γ_M0:d2:td} )={σ_J2_Rd:uMPa}')

            return {'σ_J2_Rd': self.σ_J2_Rd}


        def chk(self, image, σ_J2_Ed):

            tex = self.lib.texme

            tex.h(4, rf'(R) Kombinacja PT dla zestawu obciążenia gr1')

            if image:
                tex.p(image)

            tex.i('obliczeniowe naprężenia zredukowane w przekroju',
                rf'σ_J2_Ed = {σ_J2_Ed:uMPa}')

            η = σ_J2_Ed / self.σ_J2_Rd

            tex.i('poziom wytężenia',
                rf'η = (σ_x_Ed)/(σ_J2_Rd) = ({σ_J2_Ed:uMPa})/({self.σ_J2_Rd:uMPa}) = {η:u%:d2:td}')

            self.lib.tools.isum(η)

            return {'η': η('u%'), 'σ_J2_Ed':σ_J2_Ed}



#$$ ________ class nkes ____________________________________________________ #

    class nkes:

        def __init__(self, lib):

            self.lib = lib

        def chp(self):

            tex = self.lib.texme

            tex.h(3, 'Nośność krzyżowych elementów stężającyh')

        def res(self, us, p1, d_0, t, L, μ, n_L=3, n_P=1):

            tex = self.lib.texme

            def fβ_2(p1, d_0):
                if p1 <= 2.5*d_0:
                    return 0.4
                elif p1 >= 5.0*d_0:
                    return 0.7
                else:
                    return 0.4 + 0.3*(p1-2.5*d_0)/(2.5*d_0)

            def fβ_3(p1, d_0):
                if p1 <= 2.5*d_0:
                    return 0.5
                elif p1 >= 5.0*d_0:
                    return 0.7
                else:
                    return 0.5 + 0.2*(p1-2.5*d_0)/(2.5*d_0)

            if n_L>=3:
                β = fβ_3(p1, d_0)
            elif n_L ==2:
                β = fβ_2(p1, d_0)
            elif n_L==0:
                β = 1

            A_net = us.A - (d_0*t)*n_P

            self.N_u_Rd = (β * 0.9 * A_net * us.mate.f_uk)/(us.mate.γ_M2)


            N_cr = π**2 * us.mate.E_a * us.I_2 / (L*μ)**2

            N_pl_Rk = us.A*us.mate.f_yk

            χ = self.lib.steea.χ_def2(
                α_imp=us.α_imp, α_ult=N_pl_Rk, α_cr=N_cr)

            self.N_b_Rd = us.A*us.mate.f_yk/us.mate.γ_M1 * χ


            tex.h(4, '(R) Warunek graniczny')

            tex.i('współczynnik nośności przekroju na rozciąganie', rf'β={β}')

            tex.i('pole przekroju netto', rf'A_net={A_net("ucm**2")}')

            tex.i('nośność przekroju na rozciąganie', rf'N_u_Rd={self.N_u_Rd}')

            tex.i('rozpiętość teoretyczna elementów', rf'L={L}')

            tex.i('współczynnik długości wyboczeniowej', rf'μ={μ}')

            tex.i('główny centralny moment bezwładności', rf'I_2={us.I_2:ucm**4}')

            tex.i('siła krytyczna wyboczenia giętnego',
                rf'N_cr = (π**2*E_a*I_2)/((L*μ)**2) = {N_cr}')

            tex.i('nośność elementu na ściskanie z uwzględnieniem stateczności giętnej', rf'N_b_Rd={self.N_b_Rd}')

            return {
                'A_net'   : A_net>>'ucm2',
                'A_net/A' : A_net/us.A,
                'N_u_Rd'  : self.N_u_Rd,
                'N_b_Rd'  : self.N_b_Rd,
                'χ'       : χ,
                'β'       : β,
            }



        def _get_from_sofi(self, path, data=None, start=None, count=None):
            '''
            data  - list with tuples [(a,b), (c,d), ...]
            '''

            # create base list
            sofi_data = []

            if not os.path.exists(path):
                print('fcode.desi_steea_nkes_get: Path does not exists:', path)
                return {'F_c':0, 'F_t':0, 'F_s':0}

            if data==None and start and count:
                data = [(start*2+i*2+0, start*2+i*2+1) for i in range(count)]

            # open file with rset results and create sofi_data
            with open(path) as f:
                for line in f:
                    line = line[:-2] # delete new line symbol
                    if line[:2]=='>>':
                        sofi_data.append([])
                    else:
                        value = float(line) # convert to string
                        sofi_data[-1].append(value)

                sofi_data = sofi_data[:-1] # last one is empty

            f_c = +10e10 # max compresion in one bell
            f_t = -10e10 # max tension in one bell
            f_s = -10e10 # max tension without compresion

            for id1,id2 in data:
                for row in sofi_data:
                    maxt = max([row[id1]-min(0,row[id2]), row[id2]-min(0,row[id1])])
                    if maxt     > f_s  : f_s = maxt
                    if row[id1] > f_t  : f_t = row[id1]
                    if row[id2] > f_t  : f_t = row[id2]
                    if row[id1] < f_c  : f_c = row[id1]
                    if row[id2] < f_c  : f_c = row[id2]

            return {'F_c':f_c*kN, 'F_t':f_t*kN, 'F_s':f_s*kN}



        def chk_sofi(self, path, image, data=None, F_c=None, F_t=None, F_s=None, start=None, count=None):

            tex = self.lib.texme

            F_Ed = self._get_from_sofi(path, data, start=start, count=count)

            if F_c: F_Ed['F_c'] = F_c
            if F_t: F_Ed['F_t'] = F_t
            if F_s: F_Ed['F_s'] = F_s

            η_t = F_Ed['F_t']/self.N_u_Rd

            η_b = -F_Ed['F_c']/self.N_b_Rd

            η_t_c = F_Ed['F_s']/self.N_u_Rd


            η_s = max([η_t, η_b])

            η_w = η_t_c

            η = min([η_s, η_w])


            tex.h(4, rf'(R) Kombinacja PT dla zestawu obciążenia gr1')

            if image:
                tex.p(image)

            tex.i('obliczeniowa siła rozciągająca w przekroju',
                rf'N_t_Ed = {F_Ed["F_t"]}')

            tex.i('obliczeniowa siła ściskająca w przekroju',
                rf'N_c_Ed = {F_Ed["F_c"]}')

            tex.i('obliczeniowa siła rozciągające w grupie elementów',
                rf'N_s_Ed={F_Ed["F_s"]}')

            tex.i('poziom wytężenia przy założeniu elementów sztywnych',
                rf'η_s = {η_s:u%:d2:td}')

            tex.i('poziom wytężenia przy założeniu elementów wiotkich',
                rf'η_w = {η_w:u%:d2:td}')

            tex.i('poziom wytężenia', rf'η = min(η_s,\ η_w) = {η:u%:d2:td}')

            self.lib.tools.isum(η)

            return {
                'η'    : η('u%'),
                'η_s'  : η_s('u%'),
                'η_w'  : η_w('u%'),
                'F_Ed' : F_Ed,
            }


#$$ ________ class sbmo ____________________________________________________ #

    class sbmo:

        def __init__(self, lib):

            self.lib = lib

        def chp(self, text=None):

            tex = self.lib.texme

            if text:
                text = ' -- '+text
            else:
                text = ''

            tex.h(3, rf'Nośność elementu z uwagi na utratę stateczności ogólnej'+text)


        def res(self, image, us, α_cr, α_ult=None, σ_x=None, α_imp=None):

            tex = self.lib.texme

            tex.h(4, rf'(R) Warunek graniczny')

            # tex.x('''
            # W celu określenia stateczności elementu w zakresie giętnym, skrętnym, giętno-skrętnym oraz zwichrzenia, rozwiązuje się zlinearyzowane zagadnienie własne, zwane dalej LBA.
            # ''')

            if image:
                tex.p(image, caption='Postać utraty stateczności')

            tex.i('współczynnik krytyczny obciążenia', rf'α_cr = {α_cr}')

            if σ_x and not α_ult:  α_ult = us.mate.f_yk / σ_x

            tex.i('współczynnik plastyczny obciążenia', rf'α_ult = {α_ult}')

            tex.i('smukłość względna elementu',
                rf'λ_ = sqrt{{(α_ult)/(α_cr)}} = {self.lib.steea.λ_(α_ult, α_cr)}')

            if α_imp==None: α_imp = us.α_imp
            tex.i('parametr imperfekcji', rf'α_imp = {α_imp}')

            χ = self.lib.steea.χ_def2(α_imp=α_imp, α_ult=α_ult, α_cr=α_cr)

            tex.i('współczynnik niestateczności',
                [rf'φ = 0.5*(1 + α_imp*(λ_ - 0.2) + λ_**2)',
                 rf'χ = (1)/(φ + sqrt{{φ**2 - λ**2}}) = {χ}'])

            self.σ_1_b_Rd = us.mate.f_yk / us.mate.γ_M1 * χ

            tex.i('graniczne naprężenia główne ze względu na stateczność', rf'σ_1_b_Rd = (f_yk)/(γ_M1) * χ = {self.σ_1_b_Rd:uMPa}')

            return {
                'χ': χ,
                'σ_1_b_Rd' : self.σ_1_b_Rd('uMPa'),
            }


        def chk(self, image, σ_1_Ed):

            tex = self.lib.texme

            tex.h(4, rf'(R) Kombinacja PT dla zestawu obciążenia gr1')

            if image:
                tex.p(image)

            tex.i('obliczeniowe naprężenia główne w przekroju',
                rf'σ_1_Ed = {σ_1_Ed:uMPa}')

            η = σ_1_Ed / self.σ_1_b_Rd

            tex.i('poziom wytężenia',
                rf'η = (σ_1_Ed)/(σ_1_b_Rd) = ({σ_1_Ed:uMPa})/({self.σ_1_b_Rd:uMPa}) = {η:u%:d2:td}')

            self.lib.tools.isum(η)

            return {
                'η'        : η('u%'),
                'σ_1_Ed'   : σ_1_Ed('uMPa'),
            }


#$$ ________ class sbmn ____________________________________________________ #

    class sbmn:

        def __init__(self, lib):

            self.lib = lib

        def chp(self, text=None):

            tex = self.lib.texme

            if text:
                text = ' -- '+text
            else:
                text = ''

            tex.h(3, rf'Nośność ze względu na stateczność ogólną metodą nieliniową'+text)

        def res(self, image, us, EIη2crmax, α_cr, α_imp, η_max, σ_x=None, α_ult=None):

            tex = self.lib.texme

            tex.h(4, rf'(R) Warunek graniczny')

            N_Rk = us.A * us.mate.f_yk

            tex.i(rf'nośność przekroju z uwagi na siły osiowe', rf'N_Rk={N_Rk}')

            M_y_Rk = us.I_y / (0.5*us.h) * us.mate.f_yk

            tex.i(rf'nośność przekroju z uwagi na zginanie względem silnej osi', rf'M_y_Rk={M_y_Rk:ukN m}')

            if σ_x and not α_ult:  α_ult = us.mate.f_yk / σ_x

            λ_ = self.lib.steea.λ_(α_ult, α_cr)

            α_imp = self.lib.steea.α_imp(α_imp)

            χ = self.lib.steea.χ_def2(α_imp=α_imp, α_ult=α_ult, α_cr=α_cr)

            e_0 = α_imp*(λ_-0.2)*M_y_Rk/N_Rk*(1-χ*λ_**2/us.mate.γ_M1)/(1-χ*λ_**2)

            tex.i(rf'wstępna amplituda zintegrowanej imperfekcji zastępczej', rf'e_0 = α_imp*(λ_-0.2)*(M_y_Rk)/(N_Rk)*(1-(χ*λ_**2)/γ_M1)/(1-χ*λ_**2) = {e_0}','a')

            η_init = (e_0/λ_**2)*(N_Rk/EIη2crmax)*η_max

            tex.i(rf'deformacja skalująca postać imperfekcji', rf'η_init_max=(e_0)/(λ_**2)*(N_Rk)/(EIη2crmax)*η_max={η_init:umm}','a')

            self.σ_J2_Rd = us.mate.f_yk / us.mate.γ_M0
            tex.i('graniczne naprężenia zredukowane ze względu na stateczność', rf'σ_J2_Rd = (f_yk)/(γ_M0) = {self.σ_J2_Rd:uMPa}')

            return {
                'N_Rk'   : N_Rk,
                'M_y_Rk' : M_y_Rk,
                'λ_'     : λ_,
                'α_imp'  : α_imp,
                'χ'      : χ,
                'e_0'    : e_0,
                'η_init' : η_init,
            }




        def chk(self, image, σ_J2_Ed):

            tex = self.lib.texme

            tex.h(4, rf'(R) Kombinacja PT dla zestawu obciążenia gr1')

            if image:
                tex.p(image)

            tex.i('obliczeniowe naprężenia zredukowane w przekroju z uwzględnieniem imperfekcji i efektów geometrycznych',
                rf'σ_J2_Ed = {σ_J2_Ed:uMPa}')

            η = σ_J2_Ed / self.σ_J2_Rd

            tex.i('poziom wytężenia',
                rf'η = (σ_J2_Ed)/(σ_J2_Rd) = ({σ_J2_Ed:uMPa})/({self.σ_J2_Rd:uMPa}) = {η:u%:d2:td}')

            self.lib.tools.isum(η)




#$ ____ class footb ________________________________________________________ #

class footb:

#$$ ________ def __init__ __________________________________________________ #

    def __init__(self, lib):

        self.lib = lib


    @staticmethod
    def sync_z_fact(q_r, f_v, N_r):
        # random stream of low density pedestrian bridhe
        if q_r <= 0.6/m**2:
            if 1.50*Hz <= f_v <= 2.5*Hz:
                return 0.225*N_r
            elif f_v < 1.50*Hz or 2.50*Hz < f_v <= 3.50*Hz:
                return sqrt(N_r)
            elif 3.50*Hz < f_v <= 4.50*Hz:
                return 0.225*0.5*N_r

    def acc_z_simply(self, f_v, z_1p, ncps, φ_a, A_ref, α_a=0.1*cu, δ = 0.01*cu, q_r=0.1/m**2, K=0.6):

        η = 5*Hz / f_v

        ζ = δ / (2*π)

        a_z_1 = 4 * π**2 * f_v**2 * z_1p * α_a * φ_a

        N_r = q_r * A_ref * K # 5.7

        a_S = footb.sync_z_fact(q_r, f_v, N_r)

        a_z = a_S * a_z_1

        a_z_lim = min(0.50*sqrt(f_v/Hz), 0.70)*m/s**2

        η = a_z / a_z_lim


        tex = self.lib.texme

        tex.i('częstotliwość drgań pionowych', rf'f_v = {f_v:uHz}')

        tex.i('warunek minimalnej częstotliwości drgań pionowych',
            rf'η = (5*Hz)/(f_v)={η:u%}')

        tex.i('ugięcie od jednej osoby (P=0.7~kN) w miejscu krytycznym formy drgań',
            rf'z_1p = {z_1p:umm}')

        tex.i(rf'współczynnik furiera odpowiedzi harmonicznej', rf'α_a={α_a}')

        tex.i(rf'logarytmiczny dekrement tłumienia', rf'δ={δ}')

        tex.i(rf'współczynnik tłumienia', rf'ζ = δ / (2*π) = {ζ}')

        tex.i(rf'liczba cykli dla przęsła', rf'ncps={ncps}')

        tex.i(rf'dynamiczny współczynnik aplifikacji przejścia pieszego', rf'φ_a={φ_a}')

        tex.i(rf'przyśpieszenia pionowe pomostu od pojedynczego pieszego', rf'a_z_1={a_z_1}')

        tex.i('natężenie ruchu pieszych', rf'q_r={q_r}')

        tex.i(rf'współczynnik uwzględniający rozmieszczenie pieszych na pomoście', rf'')
        # weighting factor to take into account the variable point of application for loading (simple beam: K = 0.6 according to [54])

        tex.i('zastępcza ilość osób na pomoście', rf'N_r={N_r}')

        tex.i(rf'współczynnik synchronizacji tłumu pieszych', rf'a_S={a_S}')

        tex.i(rf'przyspieszenia pomostu dla grupy osób', rf'a_z={a_z}')

        tex.i(rf'graniczne przyśpieszenia pomostu z uwagi na komfort pieszych', rf'a_z_lim={a_z_lim}')

        tex.i(rf'poziom wytężenia', rf'η={η}')

        return {'η': η('u%')}

