'''
------------------------------------------------------------------------------
bacadra-dbase
==============================================================================
Database tools set, including table schema and parse functions.

--------------------------------------------------------------------------
Copyright (C) 2018 bacadra <bacadra@gmail.com>
Team members who develop this file:
- Sebastian Balcerowiak <asiloisad; asiloisad.93@gmail.com>

--------------------------------------------------------------------------
Changelog:
- ...

--------------------------------------------------------------------------
'''

import sqlite3

from ..cunit.units import cunit


#$ ____ class dbase ________________________________________________________ #

class dbase:
    '''
    Manage database SQLite3
    '''

    #$$ def --init--
    def __init__(self, path='main.bcdr'):
        self.path = path # can be ":memory:"

        # TODO: set path as the actual input file, impossible in ipython?

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    #$$ def connect
    def connect(self, clear=False):
        self.cb = sqlite3.connect(self.path)
        self.db = self.cb.cursor()
        if clear:
            self.delete_table()
        self.create_table()

    #$$ def close
    def close(self, save=True):
        # try:
        #     if save:
        #         self.com()
        #     self.cb.close()
        # except Exception as e:
        #     print(e)
        if save:
            self.com()
        self.cb.close()

    #$$ def clear-lock
    def clear_lock(self):
        try:
            self.close()
            self.connect()
        except:
            pass

    #$$ def exe
    def exe(self, code, data=None):
        if data:
            self.db.execute(code, data)
        else:
            self.db.execute(code)


    #$$ def exem
    def exem(self, code, data=None):
        self.db.executemany(code, data)

    #$$ def exes
    def exes(self, code):
        self.db.executescript(code)

    #$$ def get
    def get(self, code):
        return self.db.execute(code).fetchall()

    def add(self, table, cols, data):
        cols_noname = ''.join(['?,' for col in cols.split(',')])[:-1]
        self.exe(f"INSERT INTO {table}({cols}) VALUES({cols_noname})", data)

    def edit(self, table, cols, data, where):
        self.exe(f"UPDATE {table} SET {cols} WHERE {where}", data)


    #$$ def com
    def com(self):
        self.cb.commit()



    #$$ def parse
    @staticmethod
    def parse(parse_mode=1, **kwargs):
        def easy_cunit(**kwargs):
            for key,val in kwargs.items():
                if type(val)==cunit:
                    kwargs[key] = val.drop(system='si')
                elif type(val)==list:
                    kwargs[key] = [me.drop(system='si') if type(me) is cunit else me for me in val]
                elif type(val)==tuple:
                    kwargs[key] = (me.drop(system='si') if type(me) is cunit else me for me in val)
            return kwargs

        if parse_mode == 1:
            # return an data prepare to use with self.dbase.add
            kwargs = easy_cunit(**kwargs)

            # prepare string of cols names closed into square bracket with additional after commas
            A = ''
            for key in kwargs.keys():
                A += f'[{key}],'
            A = A[:-1]

            C = tuple([val for val in kwargs.values()])

            return A,C

        elif parse_mode == 2:
            # return also string with noname, it use with hand parsing like:
            # eg. A,B,C = self.dbase.parse(id=id, name=name)
            #     self.dbase.exe("INSERT INTO [011]" + A + " VALUES" + B ,C)

            kwargs = easy_cunit(**kwargs)

            A = str(tuple(['['+str(key)+']' for key,val in kwargs.items()]))
            A = A.replace('\'','')
            B = str('('+('?,'*len(kwargs))[:-1]+')')
            C = tuple([val for key,val in kwargs.items()])

            return A,B,C

        elif parse_mode == 'update':
            # use is if you write edit method
            # it somethink is none, then it is not in used

            kwargs = easy_cunit(**kwargs)

            J = ''
            C = []

            for key,val in kwargs.items():
                if val is not None:
                    J += f'[{key}] = ?,'
                    C.append(val)

            J = J[:-1]
            C = tuple(C)

            return J,C


    #$$ def delete-table
    def delete_table(self, mode=1):
        if mode==1:
            res = self.db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")
            res = res.fetchall()
            for name in res:
                name = name[0]
                code = f'DROP TABLE IF EXISTS [{name}];'
                self.exe(code)


    #$$ def create-table
    def create_table(self):


#$$ ________ ***** [000:---model-data--------] ***** ______________________ #

        code  = 'CREATE TABLE IF NOT EXISTS [000:---model-data--------] ('

        # nazwa porzadkowa
        code += '[info] TEXT'

        # close table def!
        code += ');'

        # push!
        self.exe(code)


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
        code  = 'CREATE TABLE IF NOT EXISTS [001:mdata:setts] ('

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

        # push!
        self.exe(code)


#$$$$ ________________ [002:mdata:annex] ___________________________________ #

        # tablica z rodzajem podpor
        code  = 'CREATE TABLE IF NOT EXISTS [002:mdata:annex] ('

        # nazwa porzadkowa
        code += '[id] TEXT PRIMARY KEY'

        # close table def!
        code += ');'

        # push!
        self.exe(code)


#$$$$ ________________ [003:mdata:suppe] ___________________________________ #

        # tablica z rodzajem podpor
        code  = 'CREATE TABLE IF NOT EXISTS [003:mdata:suppe] ('

        # nazwa porzadkowa
        code += '[id] TEXT PRIMARY KEY,'

        # nazwa uzytkownika
        code += '[ttl] TEXT'

        # close table def!
        code += ');'

        # push!
        self.exe(code)

#$$$$ ________________ [004:mdata:cords] ___________________________________ #

        # tablica z definicjami ukladow wspolrzednych
        code  = 'CREATE TABLE IF NOT EXISTS [004:mdata:cords] ('

        # nazwa porzadkowa
        code += '[id] TEXT PRIMARY KEY'

        # close table def!
        code += ');'

        # push!
        self.exe(code)


#$$$ ____________ [010:mates] ______________________________________________ #

        # all materials are summed in general table. so the natural constaint of sql topology is that, the number of different materials cant overhelming other one.

#$$$$ ________________ [011:mates:umate] ___________________________________ #

        # tablica materialy general
        code  = 'CREATE TABLE IF NOT EXISTS [011:mates:umate] ('

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
        code += '[texp] REAL,'

        # nazwa uzytkownika
        code += '[ttl] TEXT,'

        # ------------------------------------- #
        # below cols are calculated automaticly #
        # ------------------------------------- #

        # submaterial eg. concrete (C), steel (A) (S), wood (T)
        code += '[subcl] TEXT'

        # close table def!
        code += ');'

        # push!
        self.exe(code)


#$$$$ ________________ [012:mates:conce] ___________________________________ #

        # tablica materialy general
        code  = 'CREATE TABLE IF NOT EXISTS [012:mates:conce] ('

        # nazwa porzadkowa
        code += '[id] TEXT PRIMARY KEY'
        code += '   ON CONFLICT FAIL'
        code += '   NOT NULL REFERENCES [011:mates:umate] ([id]),'

        # klasa betonu
        code += '[cclass] TEXT,'

        # characteristic compressive strength
        code += '[f_ck] REAL,'

        # cubic characteristic compressive strength
        code +='[f_ck_cube] REAL,'

        # medium compressive strength
        code +='[f_cm] REAL,'

        # metdium tension strength of concrete due to bending test
        code +='[f_ctm] REAL,'

        # medium tension strength of concrete due to bending test 0.05% prob
        code +='[f_ctk_005] REAL,'

        # medium tension strength of concrete due to bending test 0.95% prob
        code +='[f_ctm_095] REAL,'

        # secant stiffness module
        code +='[E_cm] REAL,'

        # first plastic compresive strain
        code +='[ε_c1] REAL,'

        # first ultimate compressive strain
        code +='[ε_cu1] REAL,'

        # second plastic compresive strain
        code +='[ε_c2] REAL,'

        # second ultimate compressive strain
        code +='[ε_cu2] REAL,'

        # power of inelastic function
        code +='[n_c] REAL,'

        # third plastic compresive strain
        code +='[ε_c3] REAL,'

        # third ultimate compressive strain
        code +='[ε_cu3] REAL'


        # close table def!
        code += ');'

        # push!
        self.exe(code)


#$$$$ ________________ [012:mates:stees] ___________________________________ #


        # tablica materialy general
        code  = 'CREATE TABLE IF NOT EXISTS [012:mates:stees] ('

        # nazwa porzadkowa
        code += '[id] TEXT PRIMARY KEY'
        code += '   ON CONFLICT FAIL'
        code += '   NOT NULL REFERENCES [011:mates:umate] ([id]),'

        # charakterystyczna granica plastycznosci stali
        code += '[f_sk] REAL'

        # close table def!
        code += ');'

        # push!
        self.exe(code)


#$$$$ ________________ [012:mates:steep] ___________________________________ #


        # tablica materialy general
        code  = 'CREATE TABLE IF NOT EXISTS [012:mates:steep] ('

        # nazwa porzadkowa
        code += '[id] TEXT PRIMARY KEY'
        code += '   ON CONFLICT FAIL'
        code += '   NOT NULL REFERENCES [011:mates:umate] ([id]),'

        # charakterystyczna granica plastycznosci
        code += '[f_pk] REAL'

        # close table def!
        code += ');'

        # push!
        self.exe(code)


#$$$$ ________________ [013:mates:steea] ___________________________________ #

        # tablica materialy general
        code  = 'CREATE TABLE IF NOT EXISTS [013:mates:steea] ('

        # nazwa porzadkowa
        code += '[id] TEXT PRIMARY KEY'
        code += '   ON CONFLICT FAIL'
        code += '   NOT NULL REFERENCES [011:mates:umate] ([id]),'

        # charakterystyczna granica plastycznosci stali
        code += '[f_yk] REAL,'

        # charakterystyczna wytrzymalosc na rozciaganie
        code += '[f_uk] REAL'

        # close table def!
        code += ');'

        # push!
        self.exe(code)


#$$$$ ________________ [014:mates:shear] ___________________________________ #



#$$$$ ________________ [015:mates:timbr] ___________________________________ #

        # tablica materialy general
        code  = 'CREATE TABLE IF NOT EXISTS [015:mates:timbr] ('

        # nazwa porzadkowa
        code += '[id] TEXT PRIMARY KEY'
        code += '   ON CONFLICT FAIL'
        code += '   NOT NULL REFERENCES [011:mates:umate] ([id])'

        # close table def!
        code += ');'

        # push!
        self.exe(code)


#$$$$ ________________ [016:mates:brics] ___________________________________ #

        # tablica materialy general
        code  = 'CREATE TABLE IF NOT EXISTS [016:mates:brics] ('

        # nazwa porzadkowa
        code += '[id] TEXT PRIMARY KEY'
        code += '   ON CONFLICT FAIL'
        code += '   NOT NULL REFERENCES [011:mates:umate] ([id])'

        # close table def!
        code += ');'

        # push!
        self.exe(code)


#$$$$ ________________ [017:mates:soile] ___________________________________ #

        # tablica materialy general
        code  = 'CREATE TABLE IF NOT EXISTS [017:mates:soile] ('

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

        # push!
        self.exe(code)


#$$$ ____________ [020:usec1] ______________________________________________ #

#$$$$ ________________ [021:usec1:value] ___________________________________ #

        # tablica na wartosci charakterystyk przekrojowych preta
        code  = 'CREATE TABLE IF NOT EXISTS [021:usec1:value] ('

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

        # obwod przekroju
        code += '[u] REAL,'

        # masa jednostkowa, masa na metr dlugosci
        code += '[m_g] REAL,'

        # nazwa uzytkownika
        code += '[ttl] TEXT,'

        # ------------------------------------- #
        # below cols are calculated automaticly #
        # ------------------------------------- #

        # subclass, type of section
        code += '[subcl] TEXT'

        # close table def!
        code += ');'

        # push!
        self.exe(code)


#$$$$ ________________ [022:usec1:psect] ___________________________________ #



#$$$$ ________________ [023:usec1:point] ___________________________________ #

        # tablica na wartosci charakterystyk przekrojowych preta
        code  ='CREATE TABLE IF NOT EXISTS [021:usec1:point] ('

        # nazwa porzadkowa
        code += '[id] TEXT PRIMARY KEY,'

        # przekroj referencyjny
        code += '[sect] INTEGER REFERENCES [021:usec1:value] ([id]),'

        # material referencyjny
        code += '[mref] INTEGER REFERENCES [011:mates:umate] ([id]),'

        # wspolrzedna punktu
        code += '[y] REAL,'

        # wspolrzedna punktu
        code += '[z] REAL,'

        # nazwa uzytkownika
        code += '[ttl] TEXT'

        # close table def!
        code += ');'

        # push!
        self.exe(code)

#$$$ ____________ [030:usec2] ______________________________________________ #

#$$$ ____________ [030:usec3] ______________________________________________ #



#$$$ ____________ [050:loads] ______________________________________________ #

#$$$$ ________________ [051:loads:cates] ___________________________________ #

        # tablica na kategorie obciazen
        code  = 'CREATE TABLE IF NOT EXISTS [051:loads:cates] ('

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

        # push!
        self.exe(code)


#$$$$ ________________ [052:loads:lcase] ___________________________________ #

        # TODO: tutaj docelowo bedzie skopiowana definicja kategorii obciazenia, poniewaz dla kolejnych przypadkow w kategorii mozna bedzie modyfikowac lokalnie wartosci kombinacyjnie, more flexible...

        # tablica na przypadki obciazenia
        code  = 'CREATE TABLE IF NOT EXISTS [052:loads:lcase] ('

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

        # push!
        self.exe(code)




#$$ ________ ***** [100:---finite-elements---] ***** ______________________ #

        code  = 'CREATE TABLE IF NOT EXISTS [100:---finite-elements---] ('

        # nazwa porzadkowa
        code += '[info] TEXT'

        # close table def!
        code += ');'

        # push!
        self.exe(code)


#$$$ ____________ [110:nodes] ______________________________________________ #

#$$$$ ________________ [111:nodes:topos] ___________________________________ #

        # tablica z topologia wezlow w ukladzie
        code  = 'CREATE TABLE IF NOT EXISTS [111:nodes:topos] ('

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
        code += '[ucsi] TEXT,'

        # blokada stopni swobody
        code += '[fix] INTEGER,'

        # nazwa uzytkownika
        code += '[ttl] TEXT'

        # ------------------------------------- #
        # below cols are calculated automaticly #
        # ------------------------------------- #

        # close table def!
        code += ');'

        # push!
        self.exe(code)

#$$$$ ________________ [111:nodes:optim] ___________________________________ #

        # tablica z topologia wezlow w ukladzie
        code  = 'CREATE TABLE IF NOT EXISTS [111:nodes:optim] ('

        # numer wezla wprowadzany przez uzytkownika
        code += '[id] TEXT PRIMARY KEY ON CONFLICT FAIL REFERENCES [111:nodes:topos]([id]),'

        # temporary number in global matrix stiffness
        code += '[noG] integer UNIQUE'

        # close table def!
        code += ');'

        # push!
        self.exe(code)


#$$$$ ________________ [112:nodes:loads] ___________________________________ #

        # tablica z obciazeniem statycznym wezlowym
        code  = 'CREATE TABLE IF NOT EXISTS [112:nodes:loads] ('

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

        # push!
        self.exe(code)


#$$$$ ________________ [113:nodes:sresu] ___________________________________ #

        # wyniki wezlowe
        code  = 'CREATE TABLE IF NOT EXISTS [113:nodes:sresu] ('

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

        # push!
        self.exe(code)


#$$$ ____________ [120:truss] ______________________________________________ #

#$$$$ ________________ [121:truss:topos] ___________________________________ #

        # tablica z topologia pretow kratownicowych
        code  = 'CREATE TABLE IF NOT EXISTS [121:truss:topos] ('

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

        # ------------------------------------- #
        # below cols are calculated automaticly #
        # ------------------------------------- #

        # length
        code += '[L] REAL,'

        # difference projected length of element
        code += '[ΔX] REAL,'
        code += '[ΔY] REAL,'
        code += '[ΔZ] REAL'

        # close table def!
        code += ');'

        # push!
        self.exe(code)


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
        code  = 'CREATE TABLE IF NOT EXISTS [123:truss:sresu] ('

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

        # push!
        self.exe(code)


#$$$$ ________________ [124:truss:desig] ___________________________________ #

        # tablica z rezultatami dla kratownic
        code  = 'CREATE TABLE IF NOT EXISTS [124:truss:desig] ('

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

        # push!
        self.exe(code)




#$$$ ____________ [130:beams] ______________________________________________ #

#$$$$ ________________ [131:beams:topos] ___________________________________ #

        # tablica z topologia pretow kratownicowych
        code  = 'CREATE TABLE IF NOT EXISTS [131:beams:topos] ('

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

        # ------------------------------------- #
        # below cols are calculated automaticly #
        # ------------------------------------- #

        # length
        code += '[L] REAL,'

        # difference projected length
        code += '[ΔX] REAL,'
        code += '[ΔY] REAL,'
        code += '[ΔZ] REAL'

        # close table def!
        code += ');'

        # push!
        self.exe(code)


#$$$$ ________________ [130:beams:loads] ___________________________________ #

        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [122:trus:load] (
        #     [id]  INTEGER DEFAULT (0)
        #             NOT NULL REFERENCES [121:truss:topos] ([id]),
        #     [px]  REAL DEFAULT (0),
        #     [dt0] REAL DEFAULT (0)
        # );''')

#$$$$ ________________ [133:beams:sresu] ___________________________________ #

        # tablica z rezultatami dla kratownic
        code  = 'CREATE TABLE IF NOT EXISTS [133:beams:sresu] ('

        # numer preta kratownicowego
        code += '[id] TEXT REFERENCES [131:beams:topos] ([id]),'

        # numer przypadku obicazenia
        code += '[lcase] TEXT REFERENCES [052:loads:lcase] ([id]),'

        # axial force
        code += '[N_1] REAL,'

        # shear force Vy
        code += '[V_y_1] REAL,'

        # shear force Vz
        code += '[V_z_1] REAL,'

        # bending moment Mx
        code += '[M_x_1] REAL,'

        # shear force Mz
        code += '[M_y_1] REAL,'

        # shear force Mz
        code += '[M_z_1] REAL,'

        # axial force
        code += '[N_2] REAL,'

        # shear force Vy
        code += '[V_y_2] REAL,'

        # shear force Vz
        code += '[V_z_2] REAL,'

        # bending moment Mx
        code += '[M_x_2] REAL,'

        # shear force Mz
        code += '[M_y_2] REAL,'

        # shear force Mz
        code += '[M_z_2] REAL,'

        code += '[ΔL] REAL,'
        code += '[Δk_y] REAL,'
        code += '[ε_x_N] REAL,'





        # set primary key
        code += 'PRIMARY KEY ([id], [lcase]) ON CONFLICT REPLACE'

        # close table def!
        code += ');'

        # push!
        self.exe(code)


#$$$$ ________________ [134:beams:desig] ___________________________________ #

        # tablica z rezultatami dla kratownic
        code  = 'CREATE TABLE IF NOT EXISTS [134:beams:desig] ('

        # numer preta kratownicowego
        code += '[id] INTEGER REFERENCES [121:beams:topos] ([id]),'

        # numer przypadku obicazenia
        code += '[lcase] INTEGER REFERENCES [052:loads:lcase] ([id]),'

        # naprezenia osiowe w precie
        code += '[σ_x_N] REAL,'

        # set primary key
        code += 'PRIMARY KEY ([id], [lcase]) ON CONFLICT REPLACE'

        # close table def!
        code += ');'

        # push!
        self.exe(code)


#$$ ________ ***** [200:---struct-elements---] ***** ______________________ #

        code  = 'CREATE TABLE IF NOT EXISTS [200:---struct-elements---] ('

        # nazwa porzadkowa
        code += '[info] TEXT'

        # close table def!
        code += ');'

        # push!
        self.exe(code)


#$$ ________ ***** [300:---design-elements---] ***** ______________________ #

        code  = 'CREATE TABLE IF NOT EXISTS [300:---design-elements---] ('

        # nazwa porzadkowa
        code += '[info] TEXT'

        # close table def!
        code += ');'

        # push!
        self.exe(code)




#$$$ ____________ [310:gtech] ______________________________________________ #

#$$$$ ________________ [311:gtech:borep] ___________________________________ #

        # TODO: przekroj geotechniczny na poziomie warstwy powinien moc nadpisac I_L oraz I_D z materialu typu grunt, czesto sie zdarza

        # przekroj geotechniczny, numerowane sa kolejne przekroje, a w przekrojach warstwy liczone od wartswy gornej
        code  = 'CREATE TABLE IF NOT EXISTS [311:gtech:borep] ('

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

        # push!
        self.exe(code)


#$$$$ ________________ [312:gtech:piles] ___________________________________ #

        # obiekt pala, obliczeniowo przypisywany do wezla
        code  = 'CREATE TABLE IF NOT EXISTS [312:gtech:piles] ('

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

        # push!
        self.exe(code)