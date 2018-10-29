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

from . import schema
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
        self.exes(schema.schema.code)