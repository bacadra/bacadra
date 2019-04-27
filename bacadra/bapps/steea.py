'''
------------------------------------------------------------------------------
***** (b)acadra (app)lication(s) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''


from bacadra.unise.si import MPa,mm,m,Hz,cu,s,kN,N,unise
from bacadra.unise.umath import π,sqrt

#$ ____ class steea ________________________________________________________ #

class steea:

#$$ ________ def __init __ _________________________________________________ #

    def __init__(self, core=None, **kwargs):

        self.core = core

        self.η_bi_pl = η_bi_pl(core=core)

#$ ____ def α_imp __________________________________________________________ #

    @classmethod
    def α_imp(self, α_imp):
        '''
        Buckling imperfection parameter is equal to lateral torsional imperfection amplitude.
        '''
        if   α_imp=='a0': return 0.13
        elif α_imp=='a' : return 0.21
        elif α_imp=='b' : return 0.34
        elif α_imp=='c' : return 0.49
        elif α_imp=='d' : return 0.76
        else            : return α_imp

#$$ ________ def λ_ ________________________________________________________ #

    @classmethod
    def λ_(sellf, α_ult, α_cr):
        return sqrt((α_ult)/(α_cr))

#$$ ________ def χ _________________________________________________________ #

    @classmethod
    def χ(self, α_imp, α_ult, α_cr):
        '''
        Parameters
        ----------

            α_imp: [int or str] parametr imperefekcji, dany jako liczba z
            przedziału <0, 1> lub nazwa krzywej, np. 'a', 'b', 'c', 'd',

            α_ult: [1] odwrotność wytężenia punktu przekroju,

            α_cr: [1] współczynnik krytyczny postaci niestateczności.
        '''

        return self.χ_1(α_imp, self.λ_(α_ult, α_cr))

#$$ ________ def χ _________________________________________________________ #

    @classmethod
    def χ_1(self, α_imp, λ_):
        α_imp = self.α_imp(α_imp)
        φ = 0.5*(1+α_imp*(λ_-0.2)+λ_**2)
        return min(1, 1/(φ+sqrt(φ**2-λ_**2)))








class η_bi_pl:
    '''
    utilization level for (b)isymetrical (i)-section for 1-2 class (pl)astic
    '''

    def __init__(self, core):

        self.core = core


    def chp(self, text=None):

        tex = self.core.pinky.texme

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



    # def file(self, path, sheet, calc, output):
    #
    #     df = pd.read_excel(path, sheet_name=sheet)
    #
    #     data = df.to_numpy()
    #
    #     data_sliced = {
    #
    #         'lc='+str(row[0])+';'+str(row[1])+';beam='+str(row[2])+';x='+str(row[3]):
    #         [
    #             row[4]*1000,
    #             row[5]*1000,
    #             row[6]*1000,
    #             row[8]*1000,
    #             row[9]*1000,
    #         ]
    #
    #     for row in data}
    #
    #     return self.chm(data=data_sliced, calc=calc, output=output)
