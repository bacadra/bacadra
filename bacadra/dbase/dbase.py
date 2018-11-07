'''
------------------------------------------------------------------------------
bacadra-dbase
==============================================================================
Database tools set, including table rdbse and parse functions.

------------------------------------------------------------------------------
Copyright (C) 2018 bacadra <bacadra@gmail.com>
Team members who develop this file:
- Sebastian Balcerowiak <asiloisad; asiloisad.93@gmail.com>

------------------------------------------------------------------------------
'''

import sqlite3

from . import verrs
from . import rdbse
from . import parse


#$ ____ class dbase ________________________________________________________ #

class dbase:
    '''
    Manage database SQLite3
    '''

    #$$ def --init--
    def __init__(self):
        self.path        = ':memory:' # can be ":memory:"
        self.timeout     = 0.1        # None = lock will not interupt auto
        self.multithread = True       # multithread connection to db
                                      # please be becarefull - sql threat bool
                                      # negattve as we do it
        self.cb          = None       # database instant
        self.db          = None       # cursor instant
        self._connection = False      # flag (True|False) of database connection
                                      # init state is False of course

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass


    #$$ def connect
    def connect(self, path=None, clear=False):
        '''
        Create database system.
        '''

        # if user use path, then create local copy of db; otherwise :memory:
        if path:     self.path = path

        # first check if connection is established
        if not self._connection:
            # connect to database
            # use timeomet and multithread options
            self.cb = sqlite3.connect(
                database          = self.path,
                timeout           = self.timeout,
                check_same_thread = self.multithread is False
            )
            self._connection = True

            # create cursor object
            self.db = self.cb.cursor()

            # if clear is True, then redefine all table
            if clear:
                self.delete_table()

            # create tables if they not exists
            self.create_system()


    #$$ def close
    def close(self, save=True):
        '''
        Close connection to database. As defualt all changes will be commited (.save=True).
        '''

        # first check if connection is established
        if self._connection:
            if save:
                self.save()
            self.cb.close()
            self._connection = False


    #$$ def clear-lock
    def clear_lock(self):
        '''
        Clear lock of database. Locks occure if last quary was start and not finished yet (eg. side effects of python exception). Locks occure if dbase.timeout is set to None - then automaticly lock removes is disabled.
        '''
        # first check if connection is established
        if not self._connection:
            self.cb.interrupt()


    #$$ def exe
    def exe(self, code, data=None):
        '''
        Execution of single query. The method provide security interface with (?,?,?) and (a,b,c) data.
        '''
        self._check_connection()

        if data:
            self.db.execute(code, data)
        else:
            self.db.execute(code)


    #$$ def exem
    def exem(self, code, data=None):
        '''
        Execution of single query. The method provide security interface with (?,?,?) and (a,b,c) data. Data should be inserted in list, as [(a,b), (c,d)].
        '''
        self._check_connection()
        self.db.executemany(code, data)


    #$$ def exes
    def exes(self, code):
        '''
        Execution of multi querys. Query must be sepparated by ";" symbol.
        '''
        self._check_connection()
        self.db.executescript(code)


    #$$ def get
    def get(self, code):
        '''
        Get data from database. Dev need to write query with SELECT base. The data will be fetched in all quantity.
        '''
        self._check_connection()
        return self.db.execute(code).fetchall()


    def add(self, table, cols, data):
        '''
        Add data into system. Dev need to provide information about table, list of oclumns and data tuple eg. (a,b).
        '''
        self._check_connection()
        cols_noname = ''.join(['?,' for col in cols.split(',')])[:-1]
        self.exe(f"INSERT INTO {table}({cols}) VALUES({cols_noname})", data)


    def addm(self, table, cols, data):
        '''
        Add many data into system. Dev need to provide information about table, list of column and data list eg. [(a,b),(c,d)].
        '''
        self._check_connection()
        cols_noname = ''.join(['?,' for col in cols.split(',')])[:-1]
        self.exem(f"INSERT INTO {table}({cols}) VALUES({cols_noname})", data)


    def edit(self, table, cols, data, where):
        '''
        Edit data into system. Dev need to provide information about table, list of oclumns, data list and WHERE statment.
        '''
        self._check_connection()
        self.exe(f"UPDATE {table} SET {cols} WHERE {where}", data)


    #$$ def save
    def save(self):
        '''
        Commit changes.
        '''
        self._check_connection()
        self.cb.commit()


    #$$ def delete-table
    def delete_table(self, mode=1):
        '''
        Delete data in database
        '''
        self._check_connection()
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
        Call to rdbse class in rdbse.py file.
        '''
        self._check_connection()
        self.exes(rdbse.rdbse.code)

    #$$ def parse
    @staticmethod
    def parse(parse_mode=1, **kwargs):
        return parse.parse().run(parse_mode=parse_mode, **kwargs)

    #$$ def -check-connection
    def _check_connection(self):
        if not self._connection:
            verrs.openDatabaseError()
