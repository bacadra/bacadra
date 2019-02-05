'''
------------------------------------------------------------------------------
***** (d)atabase init (list) ****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

sql_tables = (

#$$ ________ PRAGMA ________________________________________________________ #

# https://www.sqlite.org/pragma.html


# https://www.sqlite.org/pragma.html#pragma_journal_mode
# PRAGMA schema.journal_mode = DELETE | TRUNCATE | PERSIST | MEMORY | WAL | OFF
'PRAGMA journal_mode = $<journal_mode>$;'
# 'PRAGMA journal_mode = OFF;'

'PRAGMA synchronous = 0;'

# 'PRAGMA foreign_keys=OFF;'
# 'PRAGMA read_uncommitted = true;'
'PRAGMA synchronous=OFF;'
# 'PRAGMA locking_mode = NORMAL;'



#$$ ________ [000:model-data] ______________________________________________ #

#$$$ ____________ [010:mates] ______________________________________________ #

#$$$$ ________________ [011:mates:umate] ___________________________________ #

'CREATE TABLE IF NOT EXISTS [011:mates:umate] ('

# nazwa porzadkowa
'[id] TEXT PRIMARY KEY,'

# densinity \ gestosc materialu
'[ρ_o] REAL,'

# modul odksztalcalnosci podluznej, d=0deg
'[E_1] REAL,'

# wspolczynnik poissona
'[v_1] REAL,'

# shear modulus
'[G_1] REAL,'

# wspolczynnik rozszerzalnosci termicznej
'[t_e] REAL,'

# nazwa uzytkownika
'[ttl] TEXT,'

# submaterial eg. concrete (C), steel (A) (S), wood (T)
'[subcl] TEXT'

# close table def!
');'


#$$$$ ________________ [012:mates:conce] ___________________________________ #


'CREATE TABLE IF NOT EXISTS [012:mates:conce] ('

# nazwa porzadkowa
'[id] TEXT PRIMARY KEY REFERENCES [011:mates:umate] ([id]),'

# klasa betonu
'[grade] TEXT,'

# Characteristic compressive cylinder strength of concrete at 28 days
'[f_ck] REAL,'

# cubic characteristic compressive strength
'[f_ck_cube] REAL,'

# Mean value of concrete cylinder cornpressive strength
'[f_cm] REAL,'

# Mean value of axial tensile strength of concrete
'[f_ctm] REAL,'

# Characteristic axial tensile strength of concrete 0.05% prob
'[f_ctk_005] REAL,'

# Characteristic axial tensile strength of concrete 0.95% prob
'[f_ctk_095] REAL,'

# Secant modulus of elasticity of concrete
'[E_cm] REAL,'

# first ompressive strain in the concrete at the peak stress fc
'[ε_c1] REAL,'

# first ultimate compressive strain in the concrete
'[ε_cu1] REAL,'

# first ompressive strain in the concrete at the peak stress fc
'[ε_c2] REAL,'

# first ultimate compressive strain in the concrete
'[ε_cu2] REAL,'

# power of inelastic function
'[n_c] REAL,'

# first ompressive strain in the concrete at the peak stress fc
'[ε_c3] REAL,'

# first ultimate compressive strain in the concrete
'[ε_cu3] REAL,'

# Partial factor for a material property, taking account of uncertainties in the material property itself, in geometric deviation and in the design model used
'[γ_M] REAL'

');'


#$$$$ ________________ [013:mates:steea] ___________________________________ #

'CREATE TABLE IF NOT EXISTS [013:mates:steea] ('

# nazwa porzadkowa
'[id] TEXT PRIMARY KEY'
'   ON CONFLICT FAIL'
'   NOT NULL REFERENCES [011:mates:umate] ([id]),'

# klasa stali
'[grade] TEXT,'

# max thickness
'[t_max] REAL,'

# yield strength
'[f_yk] REAL,'

# ultimate strength
'[f_uk] REAL,'

# modulus of elasticity
'[E_a] REAL,'

# yield strain
'[ε_yk] REAL,'

# ultimate strain
'[ε_uk] REAL,'

# partial factor for resistance of cross-sections whatever the class is
'[γ_M0] REAL,'

# partial factor for resistance of members to instability assessed by member checks
'[γ_M1] REAL,'

# partial factor for resistance of cross-sections in tension to fracture
'[γ_M2] REAL,'

'[γ_M3] REAL,'
'[γ_M4] REAL,'
'[γ_M5] REAL,'
'[γ_M6] REAL'

');'


#$$$ ____________ [020:usecp] ______________________________________________ #

#$$$$ ________________ [021:usecp:value] ___________________________________ #

'CREATE TABLE IF NOT EXISTS [021:usecp:value] ('

# nazwa porzadkowa
'[id] TEXT PRIMARY KEY,'

# numer materialu bazowego dla profilu, w przypadku profili zespolonych ponownie mowa o materiale bazowym, ten jest brany do statyki
'[mate] INTEGER REFERENCES [011:mates:umate] ([id]),'

# pole przekroju poprzecznego
'[A] REAL,'

# pole czynne przy scinaniu po osi y
'[A_y] REAL,'

# pole czynne przy scinaniu po osi z
'[A_z] REAL,'

'[A_1] REAL,'
'[A_2] REAL,'

# moment bezwladnosci preta na zginanie wzgledem osi y-y
'[I_y] REAL,'

# moment bezwladnosci preta na zginanie wzgledem osi z-z
'[I_z] REAL,'

# moment bezwladnosci preta na skrecanie swobodne saint-venanta
'[I_t] REAL,'

'[y_c] REAL,'
'[z_c] REAL,'
'[y_sc] REAL,'
'[z_sc] REAL,'

# moment bezwladnosci preta na zginanie wzgledem osi y-y
'[I_1] REAL,'

# moment bezwladnosci preta na zginanie wzgledem osi z-z
'[I_2] REAL,'

'[y_min] REAL,'
'[z_min] REAL,'
'[y_max] REAL,'
'[z_max] REAL,'

# moment bezwladnosci preta na skrecanie skrepowane
'[C_m] REAL,'
'[C_ms] REAL,'

# kat obrotu osi glownych
'[α] REAL,'

# obwod przekroju
'[u] REAL,'

# masa jednostkowa, masa na metr dlugosci
'[m_g] REAL,'

# nazwa uzytkownika
'[ttl] TEXT,'

# subclass, type of section
'[subcl] TEXT'

');'





#$$$$ ________________ [023:usecp:point] ___________________________________ #

'CREATE TABLE IF NOT EXISTS [023:usecp:point] ('

# przekroj referencyjny
'[sect] TEXT REFERENCES [021:usecp:value] ([id]),'

# nazwa porzadkowa
'[id] TEXT,'

# material referencyjny
'[mate] TEXT REFERENCES [011:mates:umate] ([id]),'

# wspolrzedna punktu
'[y] REAL,'

# wspolrzedna punktu
'[z] REAL,'

# nazwa uzytkownika
'[ttl] TEXT,'

# set primary key
'PRIMARY KEY ([sect], [id])'

');'



#$$$$ ________________ [025:usecp:tsect] ___________________________________ #

'CREATE TABLE IF NOT EXISTS [025:usecp:tsect] ('

# przekroj referencyjny
'[id] TEXT PRIMARY KEY REFERENCES [021:usecp:value] ([id]),'

# section height
'[h] REAL,'

# section web height
'[h_w] REAL,'

# thickness of web
'[t_w] REAL,'

# thickness of upper flange
'[t_f_u] REAL,'

# width of upper flange
'[b_f_u] REAL,'

# thickness of lower flange
'[t_f_l] REAL,'

# width of lower flange
'[b_f_l] REAL'

');'















#$$$ ____________ [050:loads] ______________________________________________ #

# consider to add loads group
# then structure
# > cates 1
#   > group 1
#       > lc 1
#       > lc 2
#       > lc 3
#   > group 2
#       > lc 1
#       > lc 2
#       > lc 3
# > cates 2
#   > group 1
#       > lc 1
#       > lc 2
#       > lc 3
#   > group 2
#       > lc 1
#       > lc 2
#       > lc 3

#$$$$ ________________ [051:loads:cates] ___________________________________ #

'CREATE TABLE IF NOT EXISTS [051:loads:cates] ('

# nazwa porzadkowa
'[id] TEXT PRIMARY KEY,'

# wspolczynnik bezpieczenstwa niekorzystny
'[γ_u] REAL,'

# wspolczynnik bezpieczenstwa korzystny
'[γ_f] REAL,'

# wspolczynnik bezpieczenstwa wyjatkowy
'[γ_a] REAL,'

# wspolczynnik kombinacyjny ψ_0
'[ψ_0] REAL,'

# wspolczynnik kombinacyjny ψ_1
'[ψ_1] REAL,'

# wspolczynnik kombinacyjny ψ_1s
'[ψ_1s] REAL,'

# wspolczynnik kombinacyjny v2
'[ψ_2] REAL,'

# nazwa uzytkownika
'[ttl] TEXT'

');'


#$$$$ ________________ [052:loads:lcase] ___________________________________ #

'CREATE TABLE IF NOT EXISTS [052:loads:lcase] ('

# przynaleznosc do kategorii obciazen
'[cates] TEXT REFERENCES [051:loads:cates] ([id]),'

# nazwa porzadkowa
'[id] TEXT,'

# mnoznik calego obciazenia w przypadku
'[fact] REAL,'

# wspolczynnik bezpieczenstwa niekorzystny
'[γ_u] REAL,'

# wspolczynnik bezpieczenstwa korzystny
'[γ_f] REAL,'

# wspolczynnik bezpieczenstwa wyjatkowy
'[γ_a] REAL,'

# wspolczynnik kombinacyjny ψ_0
'[ψ_0] REAL,'

# wspolczynnik kombinacyjny ψ_1
'[ψ_1] REAL,'

# wspolczynnik kombinacyjny ψ_1s
'[ψ_1s] REAL,'

# wspolczynnik kombinacyjny v2
'[ψ_2] REAL,'

# nazwa uzytkownika
'[ttl] TEXT,'

# set primary key
'PRIMARY KEY ([id], [cates])'

');'




#$$ ________ [100:finit-elements] _________________________________________ #

#$$$ ____________ [110:nodes] ______________________________________________ #

#$$$$ ________________ [111:nodes:topos] ___________________________________ #

'CREATE TABLE IF NOT EXISTS [111:nodes:topos] ('

# numer wezla wprowadzany przez uzytkownika
'[id] TEXT PRIMARY KEY ON CONFLICT FAIL,'

# wspolrzedna wezla z ukladzie globalnym XYZ poczatkowym
# if you want get coor in local system (eg as reference type reft to
# object_id refi then calculate it manualy or edit node-add function
'[x] REAL,'

# wspolrzedna wezla z ukladzie globalnym XYZ poczatkowym
'[y] REAL,'

# wspolrzedna wezla z ukladzie globalnym XYZ poczatkowym
'[z] REAL,'

# coor reference type
'[ucst] TEXT,'

# coor reference id
'[ucid] TEXT,'

# blokada stopni swobody
'[fix] TEXT,'

# nazwa uzytkownika
'[ttl] TEXT'

');'



#$$$$ ________________ [112:nodes:loads] ___________________________________ #

'CREATE TABLE IF NOT EXISTS [112:nodes:loads] ('

# nazwa porzadkowa
'[lcase] TEXT REFERENCES [052:loads:lcase] ([id]),'

# numer obciazanego wezla
'[node] TEXT REFERENCES [111:nodes:topos] ([id]),'

# wartosc obciazenia statycznego
'[px] REAL,'
'[py] REAL,'
'[pz] REAL,'
'[mx] REAL,'
'[my] REAL,'
'[mz] REAL,'
'[mw] REAL,'

# wartosc obciazenia kinematycznego na podpore
'[dx] REAL,'
'[dy] REAL,'
'[dz] REAL,'
'[rx] REAL,'
'[ry] REAL,'
'[rz] REAL,'
'[rw] REAL,'

# nazwa uzytkownika
'[ttl] TEXT'

');'


#$$$$ ________________ [113:nodes:stati] ___________________________________ #

'CREATE TABLE IF NOT EXISTS [113:nodes:stati] ('

# numer przypadku obciazenia
'[lcase] TEXT REFERENCES [052:loads:lcase] ([id]),'

# numer obciazanego wezla
'[node] TEXT REFERENCES [111:nodes:topos] ([id]),'

# reakcje podpore dla wezlow z podparami
'[px] REAL,'
'[py] REAL,'
'[pz] REAL,'
'[mx] REAL,'
'[my] REAL,'
'[mz] REAL,'
'[mw] REAL,'

# przemieszczenia wezlowe
'[dx] REAL,'
'[dy] REAL,'
'[dz] REAL,'
'[rx] REAL,'
'[ry] REAL,'
'[rz] REAL,'
'[rw] REAL,'

# set primary key
'PRIMARY KEY ([lcase], [node]) ON CONFLICT REPLACE'

# close table def!
');'


#$$$ ____________ [120:truss] ______________________________________________ #

#$$$$ ________________ [121:truss:topos] ___________________________________ #

'CREATE TABLE IF NOT EXISTS [121:truss:topos] ('

# nazwa porzadkowa
'[id] TEXT PRIMARY KEY,'

# numer wezla poczatkowy preta
'[n1] TEXT REFERENCES [111:nodes:topos] ([id]),'

# numer wezla koncowegoy preta
'[n2] TEXT REFERENCES [111:nodes:topos] ([id]),'

# przekroj
'[sect] TEXT REFERENCES [021:usecp:value] ([id]),'

# group
'[grp] TEXT,'

'[ttl] TEXT,'


# ----- auto-zone ------------------------------------------- #

# length
'[L] REAL,'

# difference projected length of element
'[Δx] REAL,'
'[Δy] REAL,'
'[Δz] REAL'

');'


#$$$$ ________________ [123:truss:sresu] ___________________________________ #

'CREATE TABLE IF NOT EXISTS [123:truss:sresu] ('

# numer preta kratownicowego
'[id] TEXT REFERENCES [121:truss:topos] ([id]),'

# numer przypadku obciazenia
'[lcase] TEXT REFERENCES [052:loads:lcase] ([id]),'

# axial force in element
'[N] REAL,'

# change length of element
'[ΔL] REAL,'

# strain of element
'[ε] REAL,'

# set primary key
'PRIMARY KEY ([id], [lcase]) ON CONFLICT REPLACE'

');'


#$$$$ ________________ [124:truss:desig] ___________________________________ #

'CREATE TABLE IF NOT EXISTS [124:truss:desig] ('

# numer preta kratownicowego
'[id] INTEGER REFERENCES [121:truss:topos] ([id]),'

# numer przypadku obicazenia
'[lcase] INTEGER REFERENCES [052:loads:lcase] ([id]),'

# sila osiowa w precie
'[σ_x] REAL,'

# set primary key
'PRIMARY KEY ([id], [lcase]) ON CONFLICT REPLACE'

');'




# #$$$ ____________ [130:beams] ______________________________________________ #
#
# #$$$$ ________________ [131:beams:topos] ___________________________________ #
#
# 'CREATE TABLE IF NOT EXISTS [131:beams:topos] ('
#
# # numer porzadkowy
# '[id] TEXT PRIMARY KEY,'
#
# # numer wezla poczatkowy preta
# '[n1] INTEGER REFERENCES [111:nodes:topos] ([id]),'
#
# # numer wezla koncowegoy preta
# '[n2] INTEGER REFERENCES [111:nodes:topos] ([id]),'
#
# # przekroj
# '[sect] INTEGER REFERENCES [021:usecp:value] ([id]),'
#
# '[ttl] TEXT,'
#
#
# # ----- auto-zone ------------------------------------------- #
#
# # length
# '[L] REAL,'
#
# # difference projected length
# '[Δx] REAL,'
# '[Δy] REAL,'
# '[Δz] REAL'
#
# # close table def!
# ');'
#
#
# #$$$$ ________________ [133:beams:stati] ___________________________________ #
#
# # tablica z rezultatami dla belek
# 'CREATE TABLE IF NOT EXISTS [133:beams:stati] ('
#
# # numer przypadku obciazenia
# '[lcase] TEXT REFERENCES [052:loads:lcase] ([id]),'
#
# # numer preta
# '[id] TEXT REFERENCES [131:beams:topos] ([id]),'
#
# # x coor in x-local way
# '[x] REAL,'
#
# # axial force
# '[N] REAL,'
#
# # shear force Vy
# '[V_y] REAL,'
#
# # shear force Vz
# '[V_z] REAL,'
#
# # bending moment Mx
# '[M_x] REAL,'
#
# # shear force Mz
# '[M_y] REAL,'
#
# # shear force Mz
# '[M_z] REAL,'
#
# # set primary key
# 'PRIMARY KEY ([id], [lcase], [x]) ON CONFLICT REPLACE'
#
# ');'
#
#
# #$$$$ ________________ [134:beams:desig] ___________________________________ #
#
# 'CREATE TABLE IF NOT EXISTS [134:beams:desig] ('
#
# # numer przypadku obciazenia
# '[lcase] INTEGER REFERENCES [052:loads:lcase] ([id]),'
#
# # numer preta
# '[id] INTEGER REFERENCES [121:beams:topos] ([id]),'
#
# # x coor in x-local way
# '[x] REAL,'
#
# # naprezenia osiowe w precie
# '[σ_x_N] REAL,'
#
# # set primary key
# 'PRIMARY KEY ([id], [lcase]) ON CONFLICT REPLACE'
#
# ');'
#
#
# #$$$$ ________________ [190:nodes:optim] ___________________________________ #
#
# 'CREATE TABLE IF NOT EXISTS [190:nodes:optim] ('
#
# # numer wezla wprowadzany przez uzytkownika
# '[id] TEXT PRIMARY KEY REFERENCES [111:nodes:topos]([id]),'
#
# # temporary number in global matrix stiffness
# '[noG] integer UNIQUE'
#
# # close table def!
# ');'



#$$ ________ [200:struct-elements] ________________________________________ #

#$$ ________ [300:design-elements] ________________________________________ #




)