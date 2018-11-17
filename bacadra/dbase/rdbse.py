'''
------------------------------------------------------------------------------
BCDR += ***** (r)elational (d)ata(b)ase (s)chem(e) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

class rdbse:

    # init code variable
    code = ''

#$$ ________ *** [000:---model-data--------] *** __________________________ #

    code += 'CREATE TABLE IF NOT EXISTS [000:---model-data--------] ('

    # nazwa porzadkowa
    code += '[info] TEXT'

    # close table def!
    code += ');'



#$$$ ____________ [000:mdata] ______________________________________________ #


#$$$$ ________________ [001:mdata:setts] ___________________________________ #


    '''
    Here is the list of existed setts rows.

    [name] head      :
    [pval1] author    :
    [pval2] company   :
    [pval3] phone     :
    [pval4] email     :
    [pval5] proj-nam1 :
    [pval6] proj-nam2 :

    [name] ldof      : avaiable dof of fem system
    [pval1] dof-dx    : value 1 (dof exists) or 0 (dof don't exists)
    [pval2] dof-dy    : value 1 (dof exists) or 0 (dof don't exists)
    [pval3] dof-dp    : value 1 (dof exists) or 0 (dof don't exists)
    [pval4] dof-rx    : value 1 (dof exists) or 0 (dof don't exists)
    [pval5] dof-ry    : value 1 (dof exists) or 0 (dof don't exists)
    [pval6] dof-rz    : value 1 (dof exists) or 0 (dof don't exists)
    '''


    # crate system table
    code += 'CREATE TABLE IF NOT EXISTS [001:mdata:setts] ('

    # nazwa porzadkowa
    code += '[id] TEXT PRIMARY KEY'
    code += '   ON CONFLICT FAIL,'

    # data cell
    code += '''[pval1]  TEXT,
               [pval2]  TEXT,
               [pval3]  TEXT,
               [pval4]  TEXT,
               [pval5]  TEXT,
               [pval6]  TEXT,
               [pval7]  TEXT,
               [pval8]  TEXT,
               [pval9]  TEXT
    '''

    # close table def!
    code += ');'


#$$$$ ________________ [002:mdata:annex] ___________________________________ #

    # tablica z rodzajem podpor
    code += 'CREATE TABLE IF NOT EXISTS [002:mdata:annex] ('

    # nazwa porzadkowa
    code += '[id] TEXT PRIMARY KEY'

    # close table def!
    code += ');'


#$$$$ ________________ [003:mdata:suppe] ___________________________________ #

    # tablica z rodzajem podpor
    code += 'CREATE TABLE IF NOT EXISTS [003:mdata:suppe] ('

    # nazwa porzadkowa
    code += '[id] TEXT PRIMARY KEY,'

    # nazwa uzytkownika
    code += '[ttl] TEXT'

    # close table def!
    code += ');'

#$$$$ ________________ [004:mdata:cords] ___________________________________ #

    # tablica z definicjami ukladow wspolrzednych
    code += 'CREATE TABLE IF NOT EXISTS [004:mdata:cords] ('

    # nazwa porzadkowa
    code += '[id] TEXT PRIMARY KEY'

    # close table def!
    code += ');'


#$$$ ____________ [010:mates] ______________________________________________ #

    # all materials are summed in general table. so the natural constaint of sql topology is that, the number of different materials cant overhelming other one.

#$$$$ ________________ [011:mates:umate] ___________________________________ #

    # tablica materialy general
    code += 'CREATE TABLE IF NOT EXISTS [011:mates:umate] ('

    # nazwa porzadkowa
    code += '[id] TEXT PRIMARY KEY,'

    # densinity \ gestosc materialu
    code += '[ρ_o] REAL,'

    # modul odksztalcalnosci podluznej, d=0deg
    code += '[E_1] REAL,'

    # wspolczynnik poissona
    code += '[v_1] REAL,'

    # shear modulus
    code += '[G_1] REAL,'

    # wspolczynnik rozszerzalnosci termicznej
    code += '[t_e] REAL,'

    # nazwa uzytkownika
    code += '[ttl] TEXT,'

    # ----- auto-zone ------------------------------------------- #

    # submaterial eg. concrete (C), steel (A) (S), wood (T)
    code += '[subcl] TEXT'

    # close table def!
    code += ');'


#$$$$ ________________ [012:mates:conce] ___________________________________ #

    # tablica materialy general
    code += 'CREATE TABLE IF NOT EXISTS [012:mates:conce] ('

    # nazwa porzadkowa
    code += '[id] TEXT PRIMARY KEY'
    code += '   ON CONFLICT FAIL'
    code += '   NOT NULL REFERENCES [011:mates:umate] ([id]),'

    # klasa betonu
    code += '[grade] TEXT,'

    # Characteristic compressive cylinder strength of concrete at 28 days
    code += '[f_ck] REAL,'

    # cubic characteristic compressive strength
    code +='[f_ck_cube] REAL,'

    # Mean value of concrete cylinder cornpressive strength
    code +='[f_cm] REAL,'

    # Mean value of axial tensile strength of concrete
    code +='[f_ctm] REAL,'

    # Characteristic axial tensile strength of concrete 0.05% prob
    code +='[f_ctk_005] REAL,'

    # Characteristic axial tensile strength of concrete 0.95% prob
    code +='[f_ctk_095] REAL,'

    # Secant modulus of elasticity of concrete
    code +='[E_cm] REAL,'

    # first ompressive strain in the concrete at the peak stress fc
    code +='[ε_c1] REAL,'

    # first ultimate compressive strain in the concrete
    code +='[ε_cu1] REAL,'

    # first ompressive strain in the concrete at the peak stress fc
    code +='[ε_c2] REAL,'

    # first ultimate compressive strain in the concrete
    code +='[ε_cu2] REAL,'

    # power of inelastic function
    code +='[n_c] REAL,'

    # first ompressive strain in the concrete at the peak stress fc
    code +='[ε_c3] REAL,'

    # first ultimate compressive strain in the concrete
    code +='[ε_cu3] REAL,'

    # Partial factor for a material property, taking account of uncertainties in the material property itself, in geometric deviation and in the design model used
    code +='[γ_M] REAL'

    # close table def!
    code += ');'


#$$$$ ________________ [012:mates:stees] ___________________________________ #

    # tablica materialy general
    code += 'CREATE TABLE IF NOT EXISTS [012:mates:stees] ('

    # nazwa porzadkowa
    code += '[id] TEXT PRIMARY KEY'
    code += '   ON CONFLICT FAIL'
    code += '   NOT NULL REFERENCES [011:mates:umate] ([id]),'

    # charakterystyczna granica plastycznosci stali
    code += '[f_sk] REAL'

    # close table def!
    code += ');'


#$$$$ ________________ [012:mates:steep] ___________________________________ #


    # tablica materialy general
    code += 'CREATE TABLE IF NOT EXISTS [012:mates:steep] ('

    # nazwa porzadkowa
    code += '[id] TEXT PRIMARY KEY'
    code += '   ON CONFLICT FAIL'
    code += '   NOT NULL REFERENCES [011:mates:umate] ([id]),'

    # charakterystyczna granica plastycznosci
    code += '[f_pk] REAL'

    # close table def!
    code += ');'


#$$$$ ________________ [013:mates:steea] ___________________________________ #

    # tablica materialy general
    code += 'CREATE TABLE IF NOT EXISTS [013:mates:steea] ('

    # nazwa porzadkowa
    code += '[id] TEXT PRIMARY KEY'
    code += '   ON CONFLICT FAIL'
    code += '   NOT NULL REFERENCES [011:mates:umate] ([id]),'

    # klasa stali
    code += '[grade] TEXT,'

    # max thickness
    code += '[max_t] REAL,'

    # yield strength
    code += '[f_yk] REAL,'

    # ultimate strength
    code += '[f_uk] REAL,'

    # modulus of elasticity
    code += '[E_a] REAL,'

    # yield strain
    code += '[ε_yk] REAL,'

    # ultimate strain
    code += '[ε_uk] REAL,'

    # partial factor for resistance of cross-sections whatever the class is
    code += '[γ_M0] REAL,'

    # partial factor for resistance of members to instability assessed by member checks
    code += '[γ_M1] REAL,'

    # partial factor for resistance of cross-sections in tension to fracture
    code += '[γ_M2] REAL,'

    # partial factor for silos
    code += '[γ_M3] REAL,'
    code += '[γ_M4] REAL,'
    code += '[γ_M5] REAL,'
    code += '[γ_M6] REAL'

    # close table def!
    code += ');'


#$$$$ ________________ [014:mates:shear] ___________________________________ #

    # tablica materialy general
    code += 'CREATE TABLE IF NOT EXISTS [015:mates:timbe] ('

    # nazwa porzadkowa
    code += '[id] TEXT PRIMARY KEY'

    # close table def!
    code += ');'


#$$$$ ________________ [015:mates:timbe] ___________________________________ #

    # tablica materialy general
    code += 'CREATE TABLE IF NOT EXISTS [015:mates:timbe] ('

    # nazwa porzadkowa
    code += '[id] TEXT PRIMARY KEY'
    code += '   ON CONFLICT FAIL'
    code += '   NOT NULL REFERENCES [011:mates:umate] ([id])'

    # close table def!
    code += ');'


#$$$$ ________________ [016:mates:brics] ___________________________________ #

    # tablica materialy general
    code += 'CREATE TABLE IF NOT EXISTS [016:mates:brics] ('

    # nazwa porzadkowa
    code += '[id] TEXT PRIMARY KEY'
    code += '   ON CONFLICT FAIL'
    code += '   NOT NULL REFERENCES [011:mates:umate] ([id])'

    # close table def!
    code += ');'


#$$$$ ________________ [017:mates:soile] ___________________________________ #

    # tablica materialy general
    code += 'CREATE TABLE IF NOT EXISTS [017:mates:soile] ('

    # nazwa porzadkowa
    code += '[id] TEXT PRIMARY KEY'
    code += '   ON CONFLICT FAIL'
    code += '   REFERENCES [011:mates:umate] ([id]),'

    # nazwa wlasna materialu
    code += '[soil] TEXT NOT NULL,'

    # wspolczynnik zageszczenia ID lub plastycznosci IL
    code += '[I_DL]  REAL,'

    # wilgotnosc materialu
    code += '[w_n]   REAL,'

    # kat tarcia wewnetrznego
    code += '[φ_u] REAL,'

    # spojnosc
    code += '[c_u]   REAL,'

    # wspolczynnik konsolidacji
    code += '[β]  REAL'

    # close table def!
    code += ');'


#$$$ ____________ [020:usec1] ______________________________________________ #

#$$$$ ________________ [021:usec1:value] ___________________________________ #

    # tablica na wartosci charakterystyk przekrojowych preta
    code += 'CREATE TABLE IF NOT EXISTS [021:usec1:value] ('

    # nazwa porzadkowa
    code += '[id] TEXT PRIMARY KEY,'

    # numer materialu bazowego dla profilu, w przypadku profili zespolonych ponownie mowa o materiale bazowym, ten jest brany do statyki
    code += '[mate] INTEGER REFERENCES [011:mates:umate] ([id]),'

    # pole przekroju poprzecznego
    code += '[A] REAL,'

    # pole czynne przy scinaniu po osi y
    code += '[A_y] REAL,'

    # pole czynne przy scinaniu po osi z
    code += '[A_z] REAL,'

    # moment bezwladnosci preta na skrecanie swobodne saint-venanta
    code += '[I_t] REAL,'

    # moment bezwladnosci preta na skrecanie skrepowane
    code += '[I_ω] REAL,'

    # moment bezwladnosci preta na zginanie wzgledem osi y-y
    code += '[I_y] REAL,'

    # moment bezwladnosci preta na zginanie wzgledem osi z-z
    code += '[I_z] REAL,'

    # moment bezwladnosci preta na zginanie wzgledem osi y-y
    code += '[I_ξ] REAL,'

    # moment bezwladnosci preta na zginanie wzgledem osi z-z
    code += '[I_η] REAL,'

    # Biegunowy moment bezwładności względem środka ścinania
    code += '[I_p] REAL,'

    # kat obrotu osi glownych
    code += '[α] REAL,'

    # obwod przekroju
    code += '[u] REAL,'

    # masa jednostkowa, masa na metr dlugosci
    code += '[m_g] REAL,'

    # nazwa uzytkownika
    code += '[ttl] TEXT,'

    # ----- auto-zone ------------------------------------------- #

    # współrzędna środka ciężkości
    code += '[y_gc] REAL,'
    code += '[z_gc] REAL,'

    # współrzędna środka ścinania
    code += '[y_sc] REAL,'
    code += '[z_sc] REAL,'

    # subclass, type of section
    code += '[subcl] TEXT'

    # close table def!
    code += ');'


#$$$$ ________________ [022:usec1:psect] ___________________________________ #



#$$$$ ________________ [023:usec1:point] ___________________________________ #

    # tablica na wartosci charakterystyk przekrojowych preta
    code +='CREATE TABLE IF NOT EXISTS [023:usec1:point] ('

    # przekroj referencyjny
    code += '[sect] TEXT REFERENCES [021:usec1:value] ([id]),'

    # nazwa porzadkowa
    code += '[id] TEXT,'

    # material referencyjny
    code += '[mate] TEXT REFERENCES [011:mates:umate] ([id]),'

    # wspolrzedna punktu
    code += '[y] REAL,'

    # wspolrzedna punktu
    code += '[z] REAL,'

    # nazwa uzytkownika
    code += '[ttl] TEXT,'

    # set primary key
    code += 'PRIMARY KEY ([sect], [id])'

    # close table def!
    code += ');'


#$$$ ____________ [030:usec2] ______________________________________________ #

#$$$ ____________ [030:usec3] ______________________________________________ #



#$$$ ____________ [050:loads] ______________________________________________ #

#$$$$ ________________ [051:loads:cates] ___________________________________ #

    # tablica na kategorie obciazen
    code += 'CREATE TABLE IF NOT EXISTS [051:loads:cates] ('

    # nazwa porzadkowa
    code += '[id] TEXT PRIMARY KEY,'

    # wspolczynnik bezpieczenstwa niekorzystny
    code += '[γ_u] REAL,'

    # wspolczynnik bezpieczenstwa korzystny
    code += '[γ_f] REAL,'

    # wspolczynnik bezpieczenstwa wyjatkowy
    code += '[γ_a] REAL,'

    # wspolczynnik bezpieczenstwa v1
    code += '[γ_1] REAL,'

    # wspolczynnik bezpieczenstwa v2
    code += '[γ_2] REAL,'

    # wspolczynnik bezpieczenstwa v3
    code += '[γ_3] REAL,'

    # wspolczynnik bezpieczenstwa v4
    code += '[γ_4] REAL,'

    # wspolczynnik kombinacyjny ψ_0
    code += '[ψ_0] REAL,'

    # wspolczynnik kombinacyjny ψ_1
    code += '[ψ_1] REAL,'

    # wspolczynnik kombinacyjny ψ_1s
    code += '[ψ_1s] REAL,'

    # wspolczynnik kombinacyjny v2
    code += '[ψ_2] REAL,'

    # nazwa uzytkownika
    code += '[ttl] TEXT'

    # close table def!
    code += ');'


#$$$$ ________________ [052:loads:lcase] ___________________________________ #

    # TODO: tutaj docelowo bedzie skopiowana definicja kategorii obciazenia, poniewaz dla kolejnych przypadkow w kategorii mozna bedzie modyfikowac lokalnie wartosci kombinacyjnie, more flexible...

    # tablica na przypadki obciazenia
    code += 'CREATE TABLE IF NOT EXISTS [052:loads:lcase] ('

    # nazwa porzadkowa
    code += '[id] TEXT PRIMARY KEY,'

    # przynaleznosc do kategorii obciazen
    code += '[cates] INTEGER REFERENCES [051:loads:cates] ([id]),'

    # mnoznik calego obciazenia w przypadku
    code += '[fact] REAL,'

    # nazwa uzytkownika
    code += '[ttl] TEXT'

    # close table def!
    code += ');'




#$$ ________ *** [100:---finite-elements---] *** __________________________ #

    code += 'CREATE TABLE IF NOT EXISTS [100:---finite-elements---] ('

    # nazwa porzadkowa
    code += '[info] TEXT'

    # close table def!
    code += ');'


#$$$ ____________ [110:nodes] ______________________________________________ #

#$$$$ ________________ [111:nodes:topos] ___________________________________ #

    # tablica z topologia wezlow w ukladzie
    code += 'CREATE TABLE IF NOT EXISTS [111:nodes:topos] ('

    # numer wezla wprowadzany przez uzytkownika
    code += '[id] TEXT PRIMARY KEY ON CONFLICT FAIL,'

    # wspolrzedna wezla z ukladzie globalnym XYZ poczatkowym
    # if you want get coor in local system (eg as reference type reft to
    # object_id refi then calculate it manualy or edit node-add function
    code += '[x] REAL DEFAULT (0),'

    # wspolrzedna wezla z ukladzie globalnym XYZ poczatkowym
    code += '[y] REAL DEFAULT (0),'

    # wspolrzedna wezla z ukladzie globalnym XYZ poczatkowym
    code += '[z] REAL DEFAULT (0),'

    # reference type, eg. 'node', 'coor' etc
    code += '[ucst] TEXT,'

    # reference number, eg. 1001, 'lala'
    code += '[ucid] TEXT,'

    # blokada stopni swobody
    code += '[fix] INTEGER,'

    # nazwa uzytkownika
    code += '[ttl] TEXT'

    # ----- auto-zone ------------------------------------------- #

    # close table def!
    code += ');'

#$$$$ ________________ [111:nodes:optim] ___________________________________ #

    # tablica z topologia wezlow w ukladzie
    code += 'CREATE TABLE IF NOT EXISTS [111:nodes:optim] ('

    # numer wezla wprowadzany przez uzytkownika
    code += '[id] TEXT PRIMARY KEY ON CONFLICT FAIL REFERENCES [111:nodes:topos]([id]),'

    # temporary number in global matrix stiffness
    code += '[noG] integer UNIQUE'

    # close table def!
    code += ');'



#$$$$ ________________ [112:nodes:loads] ___________________________________ #

    # tablica z obciazeniem statycznym wezlowym
    code += 'CREATE TABLE IF NOT EXISTS [112:nodes:loads] ('

    # nazwa porzadkowa
    code += '[lcase] TEXT REFERENCES [052:loads:lcase] ([id]),'

    # numer obciazanego wezla
    code += '[node] TEXT REFERENCES [111:nodes:topos] ([id]),'

    # wartosc obciazenia statycznego
    code += '[px] REAL,'
    code += '[py] REAL,'
    code += '[pz] REAL,'
    code += '[mx] REAL,'
    code += '[my] REAL,'
    code += '[mz] REAL,'
    code += '[mw] REAL,'

    # wartosc obciazenia kinematycznego na podpore
    code += '[dx] REAL,'
    code += '[dy] REAL,'
    code += '[dz] REAL,'
    code += '[rx] REAL,'
    code += '[ry] REAL,'
    code += '[rz] REAL,'
    code += '[rw] REAL,'

    # nazwa uzytkownika
    code += '[ttl] TEXT'

    # close table def!
    code += ');'


#$$$$ ________________ [113:nodes:sresu] ___________________________________ #

    # wyniki wezlowe
    code += 'CREATE TABLE IF NOT EXISTS [113:nodes:sresu] ('

    # numer przypadku obciazenia
    code += '[lcase] TEXT REFERENCES [052:loads:lcase] ([id]),'

    # numer obciazanego wezla
    code += '[node] TEXT REFERENCES [111:nodes:topos] ([id]),'

    # reakcje podpore dla wezlow z podparami
    code += '[px] REAL,'
    code += '[py] REAL,'
    code += '[pz] REAL,'
    code += '[mx] REAL,'
    code += '[my] REAL,'
    code += '[mz] REAL,'
    code += '[mw] REAL,'

    # przemieszczenia wezlowe
    code += '[dx] REAL,'
    code += '[dy] REAL,'
    code += '[dz] REAL,'
    code += '[rx] REAL,'
    code += '[ry] REAL,'
    code += '[rz] REAL,'
    code += '[rw] REAL,'

    # set primary key
    code += 'PRIMARY KEY ([lcase], [node]) ON CONFLICT REPLACE'

    # close table def!
    code += ');'


#$$$ ____________ [120:truss] ______________________________________________ #

#$$$$ ________________ [121:truss:topos] ___________________________________ #

    # tablica z topologia pretow kratownicowych
    code += 'CREATE TABLE IF NOT EXISTS [121:truss:topos] ('

    # nazwa porzadkowa
    code += '[id] TEXT PRIMARY KEY,'

    # numer wezla poczatkowy preta
    code += '[n1] TEXT REFERENCES [111:nodes:topos] ([id]),'

    # numer wezla koncowegoy preta
    code += '[n2] TEXT REFERENCES [111:nodes:topos] ([id]),'

    # przekroj
    code += '[sect] TEXT REFERENCES [021:usec1:value] ([id]),'

    # group
    code += '[grp] TEXT,'

    # nazwa uzytkownika
    code += '[ttl] TEXT,'

    # ----- auto-zone ------------------------------------------- #

    # length
    code += '[L] REAL,'

    # difference projected length of element
    code += '[ΔX] REAL,'
    code += '[ΔY] REAL,'
    code += '[ΔZ] REAL'

    # close table def!
    code += ');'


#$$$$ ________________ [122:truss:loads] ___________________________________ #

    # self.exe('''
    # CREATE TABLE IF NOT EXISTS [122:trus:load] (
    #     [id]  INTEGER DEFAULT (0)
    #             NOT NULL REFERENCES [121:truss:topos] ([id]),
    #     [px]  REAL DEFAULT (0),
    #     [dt0] REAL DEFAULT (0)
    # );''')

#$$$$ ________________ [123:truss:sresu] ___________________________________ #

    # tablica z rezultatami dla kratownic
    code += 'CREATE TABLE IF NOT EXISTS [123:truss:sresu] ('

    # numer preta kratownicowego
    code += '[id] TEXT REFERENCES [121:truss:topos] ([id]),'

    # numer przypadku obciazenia
    code += '[lcase] TEXT REFERENCES [052:loads:lcase] ([id]),'

    # axial force in element
    code += '[N] REAL,'

    # change length of element
    code += '[ΔL] REAL,'

    # strain of element
    code += '[ε_x] REAL,'

    # set primary key
    code += 'PRIMARY KEY ([id], [lcase]) ON CONFLICT REPLACE'

    # close table def!
    code += ');'


#$$$$ ________________ [124:truss:desig] ___________________________________ #

    # tablica z rezultatami dla kratownic
    code += 'CREATE TABLE IF NOT EXISTS [124:truss:desig] ('

    # numer preta kratownicowego
    code += '[id] INTEGER REFERENCES [121:truss:topos] ([id]),'

    # numer przypadku obicazenia
    code += '[lcase] INTEGER REFERENCES [052:loads:lcase] ([id]),'

    # sila osiowa w precie
    code += '[σ_x] REAL,'

    # set primary key
    code += 'PRIMARY KEY ([id], [lcase]) ON CONFLICT REPLACE'

    # close table def!
    code += ');'




#$$$ ____________ [130:beams] ______________________________________________ #

#$$$$ ________________ [131:beams:topos] ___________________________________ #

    # tablica z topologia pretow kratownicowych
    code += 'CREATE TABLE IF NOT EXISTS [131:beams:topos] ('

    # numer porzadkowy
    code += '[id] TEXT PRIMARY KEY,'

    # numer wezla poczatkowy preta
    code += '[n1] INTEGER REFERENCES [111:nodes:topos] ([id]),'

    # numer wezla koncowegoy preta
    code += '[n2] INTEGER REFERENCES [111:nodes:topos] ([id]),'

    # przekroj
    code += '[sect] INTEGER REFERENCES [021:usec1:value] ([id]),'

    # nazwa uzytkownika
    code += '[ttl] TEXT,'

    # ----- auto-zone ------------------------------------------- #

    # length
    code += '[L] REAL,'

    # difference projected length
    code += '[ΔX] REAL,'
    code += '[ΔY] REAL,'
    code += '[ΔZ] REAL'

    # close table def!
    code += ');'


#$$$$ ________________ [130:beams:loads] ___________________________________ #

    # self.exe('''
    # CREATE TABLE IF NOT EXISTS [122:trus:load] (
    #     [id]  INTEGER DEFAULT (0)
    #             NOT NULL REFERENCES [121:truss:topos] ([id]),
    #     [px]  REAL DEFAULT (0),
    #     [dt0] REAL DEFAULT (0)
    # );''')

#$$$$ ________________ [133:beams:sresu] ___________________________________ #

    # tablica z rezultatami dla belek
    code += 'CREATE TABLE IF NOT EXISTS [133:beams:sresu] ('

    # numer przypadku obciazenia
    code += '[lcase] TEXT REFERENCES [052:loads:lcase] ([id]),'

    # numer preta
    code += '[id] TEXT REFERENCES [131:beams:topos] ([id]),'

    # x coor in x-local way
    code += '[x] REAL,'

    # axial force
    code += '[N_x] REAL,'

    # shear force Vy
    code += '[V_y] REAL,'

    # shear force Vz
    code += '[V_z] REAL,'

    # bending moment Mx
    code += '[M_x] REAL,'

    # shear force Mz
    code += '[M_y] REAL,'

    # shear force Mz
    code += '[M_z] REAL,'

    code += '[ΔL] REAL,'
    code += '[Δk_y] REAL,'
    code += '[ε_x_N] REAL,'

    # set primary key
    code += 'PRIMARY KEY ([id], [lcase], [x]) ON CONFLICT REPLACE'

    # close table def!
    code += ');'


#$$$$ ________________ [134:beams:desig] ___________________________________ #

    # tablica z rezultatami
    code += 'CREATE TABLE IF NOT EXISTS [134:beams:desig] ('

    # numer przypadku obciazenia
    code += '[lcase] INTEGER REFERENCES [052:loads:lcase] ([id]),'

    # numer preta
    code += '[id] INTEGER REFERENCES [121:beams:topos] ([id]),'

    # x coor in x-local way
    code += '[x] REAL,'

    # naprezenia osiowe w precie
    code += '[σ_x_N] REAL,'

    # set primary key
    code += 'PRIMARY KEY ([id], [lcase]) ON CONFLICT REPLACE'

    # close table def!
    code += ');'


#$$ ________ *** [200:---struct-elements---] *** __________________________ #

    code += 'CREATE TABLE IF NOT EXISTS [200:---struct-elements---] ('

    # nazwa porzadkowa
    code += '[info] TEXT'

    # close table def!
    code += ');'


#$$ ________ *** [300:---design-elements---] *** __________________________ #

    code += 'CREATE TABLE IF NOT EXISTS [300:---design-elements---] ('

    # nazwa porzadkowa
    code += '[info] TEXT'

    # close table def!
    code += ');'




#$$$ ____________ [310:gtech] ______________________________________________ #

#$$$$ ________________ [311:gtech:borep] ___________________________________ #

    # TODO: przekroj geotechniczny na poziomie warstwy powinien moc nadpisac I_L oraz I_D z materialu typu grunt, czesto sie zdarza

    # przekroj geotechniczny, numerowane sa kolejne przekroje, a w przekrojach warstwy liczone od wartswy gornej
    code += 'CREATE TABLE IF NOT EXISTS [311:gtech:borep] ('

    # numer przekroju
    code += '[id]     TEXT,'

    # unikatowa nazwa przekroju
    code += '[name]   TEXT,'

    # numer warstwy w przekroju, liczone od gory, numeracja nie musi byc ciagla
    code += '[i]      INTEGERY,'

    # numer materialu typu grunt stosowanego w danej warswie
    code += '[soil]   INTEGER REFERENCES [017:mates:soile] ([id]),'

    # wysokosc warstwy
    code += '[h]      REAL,'

    # nazwa uzytkownika
    code += '[ttl] TEXT,'

    # close table def!
    code += 'PRIMARY KEY ([id],[i])'
    code += ');'



#$$$$ ________________ [312:gtech:piles] ___________________________________ #

    # obiekt pala, obliczeniowo przypisywany do wezla
    code += 'CREATE TABLE IF NOT EXISTS [312:gtech:piles] ('

    # numer grupy pala
    code += '[id]     TEXT,'

    # unikatowa nazwa grupy pala
    code += '[name]   TEXT UNIQUE,'

    # technologia wykonywania grupy pala
    code += '[tech]   TEXT,'

    # numer przekroju geotechnicznego
    code += '[bore]   INTEGER REFERENCES [311:gtech:borep] ([id]),'

    # poczatek pala wzgledem ukladu w przekroju geotechnicznym
    code += '[z_0]    REAL,'

    # dlugosc pala
    code += '[L_t]    REAL,'

    # przekroj pala
    code += '[usec1]  INTEGER REFERENCES [021:usec1:value] ([id]),'

    # numer pala w grupie
    code += '[i]      INTEGER,'

    # wspolrzedna x pala w grupie, wzgledem srodka grupy
    code += '[x]      REAL,'

    # wspolrzedna y pala w grupie, wzgledem srodka grupy
    code += '[y]      REAL,'

    # nazwa uzytkownika
    code += '[ttl] TEXT,'

    # close table def!
    code += 'PRIMARY KEY ([id],[i])'
    code += ');'

