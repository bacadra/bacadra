'''
bacadra.dbase
=============
Database tools set, including table schema and parse functions.
'''

#!/usr/bin/python
#-*-coding: UTF-8-*-

import sqlite3

from ..cunit.cmath import cunit
# from ..cunit.cmath import *



#$ ____ class dbase ________________________________________________________ #

class dbase:
    '''
    Manage database SQLite3
    '''

    #$$ def --init--
    def __init__(self, path='main.bcdr', scope=[]):
        self.path = path # can be ":memory:"
        self.scope = scope

        # TODO: set path as the actual input file, possibly impossible

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

#$$ ________ ***** model data ************* ________________________________ #

#$$$ ____________ [002:mdata] ______________________________________________ #

#$$$$ ________________ [002:mdata:suppe] ___________________________________ #

        # tablica z rodzajem podpor
        code  = 'CREATE TABLE IF NOT EXISTS [002:mdata:suppe] ('

        # nazwa porzadkowa
        code += '[id] TEXT PRIMARY KEY,'

        # nazwa uzytkownika
        code += '[ttl] TEXT'

        # close table def!
        code += ');'

        # push!
        self.exe(code)

#$$$$ ________________ [003:mdata:cords] ___________________________________ #

        # tablica z definicjami ukladow wspolrzednych
        code  = 'CREATE TABLE IF NOT EXISTS [003:mdata:cords] ('

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
        code += '[rho] REAL,'

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

        # charakterystyczna granica plastycznosci stali
        code += '[f_ck] REAL'

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
        code += '[fsk] REAL'

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
        code += '[fpk] REAL'

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
        code += '[fyk] REAL,'

        # charakterystyczna wytrzymalosc na rozciaganie
        code += '[fuk] REAL'

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
        code += '[phi_u] REAL,'

        # spojnosc
        code += '[c_u]   REAL,'

        # wspolczynnik konsolidacji
        code += '[beta]  REAL'

        # close table def!
        code += ');'

        # push!
        self.exe(code)


#$$$ ____________ [020:usec1] ______________________________________________ #

#$$$$ ________________ [021:usec1:unics] ___________________________________ #

        # tablica na wartosci charakterystyk przekrojowych preta
        code  = 'CREATE TABLE IF NOT EXISTS [021:usec1:unics] ('

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
        code += '[I_w] REAL,'

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
        code += '[sect] INTEGER REFERENCES [021:usec1:unics] ([id]),'

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
        code += '[gamu] REAL,'

        # wspolczynnik bezpieczenstwa korzystny
        code += '[gamf] REAL,'

        # wspolczynnik bezpieczenstwa wyjatkowy
        code += '[gama] REAL,'

        # wspolczynnik bezpieczenstwa v1
        code += '[gam1] REAL,'

        # wspolczynnik bezpieczenstwa v2
        code += '[gam2] REAL,'

        # wspolczynnik bezpieczenstwa v3
        code += '[gam3] REAL,'

        # wspolczynnik bezpieczenstwa v4
        code += '[gam4] REAL,'

        # wspolczynnik kombinacyjny psi0
        code += '[psi0] REAL,'

        # wspolczynnik kombinacyjny psi1
        code += '[psi1] REAL,'

        # wspolczynnik kombinacyjny psi1s
        code += '[psi1s] REAL,'

        # wspolczynnik kombinacyjny v2
        code += '[psi2] REAL,'

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

#$$ ________ ***** finit elements ********* ________________________________ #

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
        code += '[sect] TEXT REFERENCES [021:usec1:unics] ([id]),'

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
        code += '[delta_X] REAL,'
        code += '[delta_Y] REAL,'
        code += '[delta_Z] REAL'

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
        code += '[delta_L] REAL,'

        # strain of element
        code += '[eps_x] REAL,'

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
        code += '[sig_x] REAL,'

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
        code += '[sect] INTEGER REFERENCES [021:usec1:unics] ([id]),'

        # nazwa uzytkownika
        code += '[ttl] TEXT,'

        # ------------------------------------- #
        # below cols are calculated automaticly #
        # ------------------------------------- #

        # length
        code += '[L] REAL,'

        # difference projected length
        code += '[delta_X] REAL,'
        code += '[delta_Y] REAL,'
        code += '[delta_Z] REAL'

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

        code += '[delta_L] REAL,'
        code += '[delta_ky] REAL,'
        code += '[eps_x_N] REAL,'





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
        code += '[sig_x_N] REAL,'

        # set primary key
        code += 'PRIMARY KEY ([id], [lcase]) ON CONFLICT REPLACE'

        # close table def!
        code += ');'

        # push!
        self.exe(code)


#$$ ________ ***** structural elements **** ________________________________ #

#$$ ________ ***** design elements ******** ________________________________ #

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
        code += '[usec1]  INTEGER REFERENCES [021:usec1:unics] ([id]),'

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


#$ old


        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [312:gtech:piles] (
        #     [id]     INTEGER,
        #     [name]   TEXT UNIQUE,
        #     [tech]   TEXT,
        #     [bore]   INTEGER REFERENCES [311:gtech:borep] ([id]),
        #     [z_0]    REAL,
        #     [L_t]    REAL,
        #     [usec1]  INTEGER REFERENCES [021:usec1:unics] ([id]),
        #     [i]      INTEGER,
        #     [x]      REAL,
        #     [y]      REAL,
        #     [title]  TEXT,
        #     PRIMARY KEY ([id],[i])
        # );''') # TODO: wprowadzic przekroj specjalny dla pala
        #
        # self.com()
        #
        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [311:gtech:borep] (
        #     [id]     INTEGER,
        #     [name]   TEXT,
        #     [i]      INTEGERY,
        #     [soil]   INTEGER REFERENCES [017:mates:soile] ([id]),
        #     [h]      REAL,
        #     [title]  TEXT,
        #     PRIMARY KEY ([id],[i])
        # );''')





        #
        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [102:loads:handy] (
        #     [lcase]  INTEGER REFERENCES [052:loads:lcase] ([id]),
        #     [usec1]  INTEGER,
        #     [px]     REAL,
        #     [py]     REAL,
        #     [pz]     REAL,
        #     [mx]     REAL,
        #     [my]     REAL,
        #     [mz]     REAL,
        #     [dx]     REAL,
        #     [dy]     REAL,
        #     [dz]     REAL,
        #     [rx]     REAL,
        #     [ry]     REAL,
        #     [rz]     REAL
        # );''')










        #
        #
        #
        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [001:syst] (
        #     [name]  STRING PRIMARY KEY ON CONFLICT FAIL
        #             NOT NULL,
        #     [val1]  STRING,
        #     [val2]  STRING,
        #     [val3]  STRING,
        #     [val4]  STRING,
        #     [val5]  STRING,
        #     [val6]  STRING
        # );''')
        #
        # data = []
        #
        # '''
        # [name] head      :
        # [val1] author    :
        # [val2] proj-nam1 :
        # [val3] proj-nam2 :
        # [val4] company   :
        # [val5] phoney    :
        # '''
        # data.append(('head',    1,    1,    1,    1,    1,    1))
        #
        # '''
        # [name] ndof      : avaiable dof of fem system
        # [val1] dof-px    : value 1 (dof exists) or 0 (dof don't exists)
        # [val2] dof-py    : value 1 (dof exists) or 0 (dof don't exists)
        # [val3] dof-pz    : value 1 (dof exists) or 0 (dof don't exists)
        # [val4] dof-mx    : value 1 (dof exists) or 0 (dof don't exists)
        # [val5] dof-my    : value 1 (dof exists) or 0 (dof don't exists)
        # [val6] dof-mz    : value 1 (dof exists) or 0 (dof don't exists)
        # '''
        # data.append(('ndof',    1,    1,    1,    1,    1,    1))
        #
        # '''
        # [name] lang      : language settings of project
        # [val1] lang-gene : general language in project
        # [val2] lang-pink : language in pinky project
        # '''
        # data.append(('lang', 'en', None, None, None, None, None))
        #
        # self.exem('''INSERT OR IGNORE INTO [001:syst] VALUES
        #          (?,?,?,?,?,?,?)''', data)
        #
        #
        # #$$$ ____________ [002:supp] _______________________________________ #
        #
        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [002:supp] (
        #     [id]   INTEGER PRIMARY KEY ON CONFLICT FAIL
        #             NOT NULL,
        #     [kdx]  REAL   DEFAULT (0),
        #     [kdy]  REAL   DEFAULT (0),
        #     [kdz]  REAL   DEFAULT (0),
        #     [krx]  REAL   DEFAULT (0),
        #     [kry]  REAL   DEFAULT (0),
        #     [krz]  REAL   DEFAULT (0)
        # );''')
        #
        # val = []; i = 0
        # for j in range(2):
        #     for k in range(2):
        #         for l in range(2):
        #             for m in range(2):
        #                 for n in range(2):
        #                     for o in range(2):
        #                         val.append((-i,  -j, -k, -l,  -m, -n, -o))
        #                         i += 1
        #
        # self.exem('''INSERT OR IGNORE INTO [002:supp] VALUES (?,  ?, ?, ?,  ?, ?, ?)''', val)
        #
        # #$$$ ____________ [003:cord] _______________________________________ #
        #
        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [003:cord] (
        #     [id]   INTEGER PRIMARY KEY ON CONFLICT FAIL
        #             NOT NULL,
        #     [type] STRING,
        #     [e11]  REAL   DEFAULT (0),
        #     [e12]  REAL   DEFAULT (0),
        #     [e13]  REAL   DEFAULT (0),
        #     [e21]  REAL   DEFAULT (0),
        #     [e22]  REAL   DEFAULT (0),
        #     [e23]  REAL   DEFAULT (0),
        #     [e31]  REAL   DEFAULT (0),
        #     [e32]  REAL   DEFAULT (0),
        #     [e33]  REAL   DEFAULT (0)
        # );''')
        #
        # self.exe('''INSERT OR IGNORE INTO [003:cord] VALUES (0, "CART",
        #     1, 0, 0,
        #     0, 1, 0,
        #     0, 0, 1)''')
        #
        #
        # #$$$ ____________ [010:mate] _______________________________________ #
        # #$$$$ ___________ [011:mates:umate] __________________________________ #
        #
        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [011:mates:umate] (
        #     [id] INTEGER PRIMARY KEY ON CONFLICT FAIL
        #             NOT NULL,
        #     [E]  REAL DEFAULT (0)
        # );''')
        #
        #
        # #$$$$ ___________ [013:mates:steea] __________________________________ #
        #
        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [013:mates:steea] (
        #     [id] INTEGER PRIMARY KEY ON CONFLICT FAIL
        #             NOT NULL REFERENCES [011:mates:umate] ([id]),
        #     [fyk] REAL DEFAULT (0)
        # );''')
        #
        # #$$$$ ___________ [012:mates:stees] __________________________________ #
        #
        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [012:mates:stees] (
        #     [id] INTEGER PRIMARY KEY ON CONFLICT FAIL
        #             NOT NULL REFERENCES [011:mates:umate] ([id]),
        #     [fsk] REAL DEFAULT (0)
        # );''')
        #
        # #$$$$ ___________ [012:mates:conce] __________________________________ #
        #
        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [012:mates:conce] (
        #     [id] INTEGER PRIMARY KEY ON CONFLICT FAIL
        #             NOT NULL REFERENCES [011:mates:umate] ([id]),
        #     [fck] REAL DEFAULT (0)
        # );''')
        #
        # #$$$$ ___________ [015:mates:timbr] __________________________________ #
        #
        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [015:mates:timbr] (
        #     [id] INTEGER PRIMARY KEY ON CONFLICT FAIL
        #             NOT NULL REFERENCES [011:mates:umate] ([id]),
        #     [test] REAL DEFAULT (0)
        # );''')
        #
        # #$$$$ ___________ [017:mates:soile] __________________________________ #
        #
        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [017:mates:soile] (
        #     [id] INTEGER PRIMARY KEY ON CONFLICT FAIL
        #             NOT NULL REFERENCES [011:mates:umate] ([id]),
        #     [test] REAL DEFAULT (0)
        # );''')
        #
        #
        # #$$$ ____________ [020:sec1] _______________________________________ #
        # #$$$$ ___________ [021:usec1:unics] __________________________________ #
        #
        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [021:usec1:unics] (
        #     [id] INTEGER PRIMARY KEY ON CONFLICT FAIL
        #             NOT NULL REFERENCES [011:mates:umate] ([id]),
        #     [mate] INTEGER,
        #     [A]  REAL NOT NULL,
        #     [IY] REAL NOT NULL,
        #     [IZ] REAL NOT NULL,
        #     [IW] REAL NOT NULL,
        #     [IT] REAL NOT NULL
        # );''')
        #
        #
        # #$$$$ ___________ [022:sec1:poin] __________________________________ #
        #
        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [022:sec1:poin] (
        #     [id] INTEGER PRIMARY KEY ON CONFLICT FAIL
        #             NOT NULL REFERENCES [021:usec1:unics] ([id]),
        #     [mate] INTEGER,
        #     [x] REAL NOT NULL,
        #     [z] REAL NOT NULL
        # );''')
        #
        #
        # #$$$ ____________ [030:sec2] _______________________________________ #
        #
        #
        #
        # #$$$ ____________ [110:node] _______________________________________ #
        # #$$$$ ___________ [111:nodes:topos] __________________________________ #
        #
        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [111:nodes:topos] (
        #     [id]   INTEGER PRIMARY KEY ON CONFLICT FAIL NOT NULL,
        #     [x]    REAL    DEFAULT (0),
        #     [y]    REAL    DEFAULT (0),
        #     [z]    REAL    DEFAULT (0),
        #     [fix]  INTEGER DEFAULT (0)
        #                 REFERENCES [002:supp] ([id]),
        #     [ref]  INTEGER DEFAULT (0),
        #     [ucs]  INTEGER DEFAULT (0)
        #                 REFERENCES [003:cord] ([id]),
        #     [noG]  INTEGER UNIQUE
        # );''')
        #
        # self.exe('''INSERT OR IGNORE INTO [111:nodes:topos] VALUES
        #          (0, 0, 0, 0, 0, 0, 0, 0)''')
        #
        # #$$$$ ___________ [112:node:load] __________________________________ #
        #
        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [112:node:load] (
        #     [id] INTEGER DEFAULT (0),
        #     [px] REAL DEFAULT (0),
        #     [py] REAL DEFAULT (0),
        #     [pz] REAL DEFAULT (0),
        #     [mx] REAL DEFAULT (0),
        #     [my] REAL DEFAULT (0),
        #     [mz] REAL DEFAULT (0),
        #     [dx] REAL DEFAULT (0),
        #     [dy] REAL DEFAULT (0),
        #     [dz] REAL DEFAULT (0),
        #     [rx] REAL DEFAULT (0),
        #     [ry] REAL DEFAULT (0),
        #     [rz] REAL DEFAULT (0)
        # );''')
        #
        # #$$$$ ___________ [113:node:stat] __________________________________ #
        #
        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [113:node:stat] (
        #     [id] INTEGER PRIMARY KEY ON CONFLICT FAIL
        #             NOT NULL,
        #     [px] REAL DEFAULT (0),
        #     [py] REAL DEFAULT (0),
        #     [pz] REAL DEFAULT (0),
        #     [mx] REAL DEFAULT (0),
        #     [my] REAL DEFAULT (0),
        #     [mz] REAL DEFAULT (0),
        #     [dx] REAL DEFAULT (0),
        #     [dy] REAL DEFAULT (0),
        #     [dz] REAL DEFAULT (0),
        #     [rx] REAL DEFAULT (0),
        #     [ry] REAL DEFAULT (0),
        #     [rz] REAL DEFAULT (0)
        # );''')
        #
        #
        #
        #
        #
        #
        # #$$$ ____________ [120:trus] _______________________________________ #
        # #$$$$ ___________ [121:truss:topos] __________________________________ #
        #
        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [121:truss:topos] (
        #     [id]    INTEGER PRIMARY KEY,
        #     [n1] INTEGER REFERENCES [111:nodes:topos] ([id]),
        #     [n2] INTEGER REFERENCES [111:nodes:topos] ([id]),
        #     [sect]  INTEGER REFERENCES [011:mates:umate] ([id]),
        #     [fix]   INTEGER REFERENCES [002:supp]      ([id]),
        #     [div]   INTEGER DEFAULT (1)
        # );''')
        #
        # #$$$$ ___________ [122:trus:load] __________________________________ #
        #
        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [122:trus:load] (
        #     [id]  INTEGER DEFAULT (0)
        #             NOT NULL REFERENCES [121:truss:topos] ([id]),
        #     [px]  REAL DEFAULT (0),
        #     [dt0] REAL DEFAULT (0)
        # );''')
        #
        # #$$$$ ___________ [123:truss:sresu] __________________________________ #
        #
        # self.exe('''
        # CREATE TABLE IF NOT EXISTS [123:truss:sresu] (
        #     [id] INTEGER PRIMARY KEY ON CONFLICT FAIL
        #             NOT NULL REFERENCES [121:truss:topos] ([id]),
        #     [px] REAL NOT NULL
        # );''')
        #
        # #$$$ ____________ commit ___________________________________________ #
        # self.com()
        #
        #

    # #$$ def parsedatan
    # def parsedatan(self, count):
    #     base = '('
    #     for i in range(count):
    #         base += '?,'
    #     return base[:-1] + ')'
    #
    # #$$ def parsedata
    # def parsedata(self, no=None, **kwargs):
    #     if type(no) is int or type(no) is float or no is None:
    #         l1, l2 = [], []
    #         if no: l1.append('no'); l2.append(no)
    #         for key, val in kwargs.items():
    #             if val:
    #                 l1.append(key)
    #                 l2.append(val)
    #         return tuple(l1), self.parsedatan(len(l1)), [tuple(l2)]
    #
    #     elif type(no) == list:
    #         if type(no[0]) == list:
    #             return tuple(no[0]), self.parsedatan(len(no[0])), list(map(tuple, no[1:]))
    #
    #         elif type(no[0]) == tuple:
    #             return no[0], self.parsedatan(len(no[0])), no[1:]
    #
    #     elif type(no) == dict:
    #         res = [tuple(no.keys())]
    #         t1  = list(no.values())
    #
    #         if type(t1[0]) == list or type(t1[0]) == tuple:
    #             n = len(t1[0])
    #             for val1 in range(n):
    #                 temp = []
    #                 for list1 in t1:
    #                     temp.append(list1[val1])
    #                 res.append(temp)
    #         else:
    #             temp = []
    #             for val in t1:
    #                 temp.append(val)
    #             res.append(temp)
    #
    #         return res[0], self.parsedatan(len(res[0])), list(map(tuple, res[1:]))
    #
    #
    # $ parsedata
    # @staticmethod
    # def parsedata(inputs, settings, dbunit, data):
    #
    #     sett0 = {}
    #     for key,val in settings.items():
    #         try:
    #             dbunit1 = cunit.project.data[dbunit[key]]
    #         except KeyError:
    #             dbunit1 = {}
    #
    #         try:
    #             unitfactor = (cunit.xunit.init(settings[key]['unit'])).xdrop(dbunit1)
    #         except:
    #             unitfactor = 1
    #
    #         try:
    #             defaultval = settings[key]['default']
    #             if type(defaultval)==cunit.xunit:
    #                 defaultval = defaultval.xdrop(dbunit1)
    #             else:
    #                 defaultval *= unitfactor
    #         except:
    #             defaultval = None
    #
    #         sett0.update({key:[dbunit1, unitfactor, defaultval]})
    #     # print(sett0)
    #
    #     if not data:
    #         input_maxlen = 1
    #         input = inputs.copy()
    #         for key,val in input.items():
    #             if type(val) == list:
    #                 if len(val) > input_maxlen:
    #                     input_maxlen = len(val)
    #
    #         dA, dB = '(', '('
    #         for key,val in input.items():
    #             try:
    #                 settings[key]['default']
    #                 s1 = True
    #             except:
    #                 s1 = False
    #             if val!=None or s1:
    #                 dA += '[' + key + '],'
    #                 dB += '?,'
    #         dA = dA[:-1] + ')'
    #         dB = dB[:-1] + ')'
    #
    #         dC = []
    #
    #         for i in range(input_maxlen):
    #             temp = []
    #             for key,val in input.items():
    #                 try:
    #                     settings[key]['default']
    #                     s1 = True
    #                 except:
    #                     s1 = False
    #                 if val!=None or s1:
    #                     if type(val) == list:
    #                         val0 = val[i]
    #                     else:
    #                         val0 = val
    #
    #                     if type(val0) == cunit.xunit:
    #                         val0 = val0.xdrop(sett0[key][0])
    #                     elif val0 == None:
    #                         val0 = sett0[key][2]
    #                     else:
    #                         val0 *= sett0[key][1]
    #                     temp.append(val0)
    #             dC.append(tuple(temp))
    #         return dA, dB, dC
    #
    #     else:
    #         input_maxlen = len(data)-1
    #
    #         dA, dB = '(', '('
    #         for key in data[0]:
    #             dA += '[' + key + '],'
    #             dB += '?,'
    #         dA = dA[:-1] + ')'
    #         dB = dB[:-1] + ')'
    #
    #         dC = []
    #
    #         data_head = data[0]
    #         data_nrow = len(data)-1
    #         data_len  = len(data_head)
    #
    #         for j in range(data_nrow):
    #             temp = []
    #             for i in range(data_len):
    #                 key  = data_head[i]
    #                 val0 = data[j+1][i]
    #                 if type(val0) == cunit.xunit:
    #                     val0 = val0.xdrop(sett0[key][0])
    #                 elif val0 == None:
    #                     val0 = sett0[key][2]
    #                 else:
    #                     val0 *= sett0[key][1]
    #                 temp.append(val0)
    #             dC.append(tuple(temp))
    #
    #         return dA, dB, dC







