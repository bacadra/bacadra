'''
------------------------------------------------------------------------------
bacadra-dbase
==============================================================================
Database tools set, including table schema and parse functions.

------------------------------------------------------------------------------
Copyright (C) 2018 bacadra <bacadra@gmail.com>
Team members who develop this file:
- Sebastian Balcerowiak <asiloisad; asiloisad.93@gmail.com>

------------------------------------------------------------------------------
Changelog:
- ...

------------------------------------------------------------------------------
'''

import sqlite3

from . import schema
from . import parse
from ..cunit.units import cunit


#$ ____ class dbase ________________________________________________________ #

class dbase:
    '''
    Manage database SQLite3
    '''

    #$$ def --init--
    def __init__(self):
        self.path = ':memory:' # can be ":memory:"

        # TODO: set path as the actual input file, impossible in ipython?

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    #$$ def connect
    def connect(self, path=None, clear=False):
        if path:
            self.path = path
        self.cb = sqlite3.connect(self.path)
        self.db = self.cb.cursor()
        if clear:
            self.delete_table()
        self.create_system()

    #$$ def close
    def close(self, save=False):
        # try:
        #     if save:
        #         self.save()
        #     self.cb.close()
        # except Exception as e:
        #     print(e)
        if save:
            self.save()
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
        '''
        Execution of single query. The method provide security interface with (?,?,?) and (a,b,c) data.
        '''
        if data:
            self.db.execute(code, data)
        else:
            self.db.execute(code)

    #$$ def exem
    def exem(self, code, data=None):
        '''
        Execution of single query. The method provide security interface with (?,?,?) and (a,b,c) data. Data should be inserted in list, as [(a,b), (c,d)].
        '''
        self.db.executemany(code, data)

    #$$ def exes
    def exes(self, code):
        '''
        Execution of multi querys. Query must be sepparated by ";" symbol.
        '''
        self.db.executescript(code)

    #$$ def get
    def get(self, code):
        '''
        Get data from database. Dev need to write query with SELECT base. The data will be fetched in all quantity.
        '''
        return self.db.execute(code).fetchall()

    def add(self, table, cols, data):
        '''
        Add data into system. Dev need to provide information about table, list of oclumns and data tuple eg. (a,b).
        '''
        cols_noname = ''.join(['?,' for col in cols.split(',')])[:-1]
        self.exe(f"INSERT INTO {table}({cols}) VALUES({cols_noname})", data)

    def addm(self, table, cols, data):
        '''
        Add many data into system. Dev need to provide information about table, list of column and data list eg. [(a,b),(c,d)].
        '''
        cols_noname = ''.join(['?,' for col in cols.split(',')])[:-1]
        self.exem(f"INSERT INTO {table}({cols}) VALUES({cols_noname})", data)

    def edit(self, table, cols, data, where):
        '''
        Edit data into system. Dev need to provide information about table, list of oclumns, data list and WHERE statment.
        '''
        self.exe(f"UPDATE {table} SET {cols} WHERE {where}", data)

    #$$ def save
    def save(self):
        '''
        Commit changes.
        '''
        self.cb.commit()

    #$$ def delete-table
    def delete_table(self, mode=1):
        '''
        Delete data in database
        '''
        if mode==1:
            res = self.db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")
            res = res.fetchall()
            for name in res:
                name = name[0]
                code = f'DROP TABLE IF EXISTS [{name}];'
                self.exe(code)


    #$$ def create-system
    def create_system(self):
        '''
        Call to schema class in schema.py file.
        '''
        self.exes(schema.schema.code)

    #$$ def parse
    @staticmethod
    def parse(parse_mode=1, **kwargs):
        return parse.parse().run(parse_mode=parse_mode, **kwargs)

