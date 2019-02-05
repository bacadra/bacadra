'''
------------------------------------------------------------------------------
***** bacadra (d)ata(base) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

import sqlite3

from ..tools.setts import settsmeta
from ..tools.fpack import translate

from . import mdata
from . import verrs
from . import dlist


#$ ____ class setts ________________________________________________________ #

class setts(settsmeta):

#$$ ________ def path ______________________________________________________ #

    # path to database
    # can be ":memory:" or just path to file, with extension!

    __path = ':memory:'

    @property
    def path(self): return self.__path

    @path.setter
    def path(self, value):
        if self.__save__: self.__path   = value
        else:             self.__temp__ = value


#$$ ________ def multithread _______________________________________________ #

    __multithread = True

    @property
    def multithread(self): return self.__multithread

    @multithread.setter
    def multithread(self, value):
        if self.__save__: self.__multithread = value
        else:             self.__temp__ = value


#$$ ________ def journal_mode ______________________________________________ #

    __journal_mode = 'OFF'

    @property
    def journal_mode(self): return self.__journal_mode

    @journal_mode.setter
    def journal_mode(self, value):
        if not value.lower() in ['delete', 'truncate', 'persist', 'memory', 'wal', 'off']:
            verrs.BCDR_dbase_ERROR_General('e0111',
                'Unsupported parameter of journal_mode!\n'
                "Tip: try use 'delete' or 'truncate' or 'persist' or 'memory' or 'wal' or 'off'\n"
                'Tip: https://www.sqlite.org/pragma.html#pragma_journal_mode'
            )
            value = value.upper()
        if self.__save__: self.__journal_mode = value
        else:             self.__temp__ = value


#$$ ________ def auto_commit _______________________________________________ #

    __auto_commit = True

    @property
    def auto_commit(self): return self.__auto_commit

    @auto_commit.setter
    def auto_commit(self, value):

        if self.__save__: self.__auto_commit = value
        else:             self.__temp__ = value


#$$ ________ def asolve ____________________________________________________ #

    __asolve = 'INSERT'

    @property
    def asolve(self): return self.__asolve

    @asolve.setter
    def asolve(self, value):

        if value==None:
            value = 'INSERT'
        elif type(value)==str:
            value = value.upper()
        else:
            raise ValueError('Unknow where type')

        if value in ['INSERT OR REPLACE','REPLACE','IOR','R']:
            value = 'INSERT OR REPLACE'

        elif value in ['INSERT OR IGNORE','IGNORE','IOI','I']:
            value = 'INSERT OR IGNORE'

        else:
            raise ValueError('Unknow where type')

        if self.__save__: self.__asolve = value
        else:             self.__temp__ = value






#$ ____ class dbase ________________________________________________________ #

class dbase:
    '''
    Important links:
    https://docs.python.org/3.7/library/sqlite3.html
    '''

    # class setts
    setts = setts('setts', (setts,), {})



    #$$ def __init__
    def __init__(self, core=None):

        self.core = core

        # object setts
        self.setts = self.setts('setts',(),{})

        # sqlite3 connection
        self.db = None

        # sqlite3 connection.cursor
        self.cr = None

        # connection flags
        # variable is False or string with connected database name
        self._connQ = False



    #$$ def connect
    def connect(self, path=None, clear=True):
        '''
        Create and connect to database system.
        '''

        # if user type path, then set it as atribute
        if path:
            self.setts.path = path

        # if connection is not established or other database was selected
        if self._connQ != self.setts.path:

            # create sqlite.connection object
            self.db = sqlite3.connect(
                database          = self.setts.path,
                timeout           = 0,
                check_same_thread = not self.setts.multithread,
                isolation_level   = None,
            )

            # set connection flags as True
            self._connQ = self.setts.path

            # set row_factory
            self.db.row_factory = sqlite3.Row

            # create cursor instance
            self.cr = self.db.cursor()

            # if clear is True, then redefine all table
            if clear:
                self.interrupt()
                self.cleardb()

            # create tables if they not exists
            self.create_system()

        # if connection to current database is established and clear flags
        elif clear:

            # then redefine all table
            self.cleardb()

            # create tables if they not exists
            self.create_system()


    #$$ def close
    def close(self, commit=True, push_rstme=True):
        '''
        Close connection to database. As defualt all changes will be commited (.commit=True).
        '''

        # first check if connection is established
        if self._connQ:

            # if commit flag is True
            if commit==True:
                # then commit journal
                self.commit()

            # close all links
            self.interrupt()

            # close database
            self.db.close()

            # change connection flag
            self._connQ = False

        else:

            verrs.BCDR_dbase_WARN_Already_Closed()

        if self.core and push_rstme:
            self.core.pinky.rstme.push()


    #$$ def commit
    def commit(self):
        '''
        Commit changes.
        '''

        # check if connection is established
        self._check_connection()

        # commit journal files
        self.db.commit()



    #$$ def _check_connection
    def _check_connection(self):
        '''
        Raise ERROR if connection is not established.
        '''

        # if connection is not established
        if not self._connQ:

            # then raise error with tips
            verrs.BCDR_dbase_ERROR_Open_Database()

    #$$ def interrupt
    def interrupt(self):
        self.db.interrupt()


    #$$ def exe
    def exe(self, mode, code, data=None, auto_commit=None):
        '''
        mode='r'
        Execution of single query. The method provide security interface with (?,?,?) and (a,b,c) data.

        mode='m'
        Execution of single query. The method provide security interface with (?,?,?) and (a,b,c) data. Data should be inserted in list, as [(a,b), (c,d)].

        mode='s'
        Execution of multi querys. Query must be sepparated by ";" symbol.
        '''

        # check if connection is established
        self._check_connection()

        auto_commit = self.setts.check_loc('auto_commit', auto_commit)

        if mode=='r' and data:
            self.cr.execute(code, data)

        elif mode=='r':
            self.cr.execute(code)

        elif mode=='m':
            self.cr.executemany(code, data)

        elif mode=='s':
            self.cr.executescript(code)

        else:
            verrs.BCDR_dbase_ERROR_General('e0110',
                'Undefined transaction mode!\n'
                "Tip: use 'r', 'm' or 's'"
            )

        self.commit()


    #$$ def add
    def add(self, mode, table, cols, data, asolve=None):
        '''
        mode='r'
        Add data into system. Dev need to provide information about table, list of oclumns and data tuple eg. (a,b).

        mode='m'
        Add many data into system. Dev need to provide information about table, list of column and data list eg. [(a,b),(c,d)].
        '''

        # connection is checked in exe method

        asolve = self.setts.check_loc('asolve', asolve)

        # if user type cols name as one string, then divide it into list
        if type(cols) == str:

            cols = cols.split(',')

        # create noname vector
        cole = ','.join(['?' for col in range(len(cols))])

        # add bracket to column names
        cols = [col if col[0]=='[' else '['+col+']' for col in cols]

        # join to string form
        cols = ','.join(cols)

        # call to exe method
        self.exe(
            code = f"{self.setts.asolve} INTO {table}({cols}) VALUES({cole})",
            data = data,
            mode = mode,
        )



    #$$ def get
    def get(self, mode, table, cols=None, where=None, join=None, formula=1):
        '''
        mode='s'
        '''

        # connection is checked in exe method

        # prepare tables
        if type(table)==list:
            table = ','.join(table)
        elif type(table)==str:
            pass
        else:
            raise ValueError('Unknow where type')

        # prepare where
        if where==None:
            where = ''
        elif type(where)==list:
            where = 'where ' + ' AND '.join(['('+row+')' for row in where])
        elif type(where)==str:
            where = 'where ' + where
        else:
            raise ValueError('Unknow where type')

        # prepare joins
        if join==None:
            join = ''
        elif type(join)==list:
            join = ' '.join(join)
        elif type(where)==str:
            pass
        else:
            raise ValueError('Unknow where type')


        # prepare columns
        if cols==None:
            cols = '*'
        elif type(cols) == list:
            cols = ','.join(cols)
        elif type(cols)==str:
            pass
        else:
            raise ValueError()

        # select statment
        if formula==1:
            self.exe('r',f'''
                SELECT {cols} from {table} {join} {where}
            ''')

        elif formula==2:
            self.exe('r', f'''
                SELECT * FROM (SELECT {cols} from {table} {join}) {where}
            ''')

        else:
            raise ValueError()


        if  mode=='+':
            return self.cr

        elif mode=='r':
            return self.cr.fetchone()

        elif mode=='m':
            return self.cr.fetchall()

        elif mode=='s':
            return self.cr.fetchone()[0]

        else:
            raise ValueError()

    #$$ def obj
    obj = mdata.obj

    #$$ def edit
    def edit(self, table, cols, data, where):
        '''
        Edit data into system. Dev need to provide information about table, list of oclumns, data list and WHERE statment.
        '''

        # check if connection is established
        self._check_connection()

        self.exe(
            code = f"UPDATE {table} SET {cols} WHERE {where}",
            data = data,
            mode = 'r',
        )


    #$$ def create_system
    def create_system(self):

        code = translate(dlist.sql_tables,
        {
            '$<journal_mode>$':self.setts.journal_mode,
        })

        self.exe(code=code, mode='s')


    #$$ def cleardb
    def cleardb(self):
        '''
        Delete data in database.

        Here is small tutorial about drop table, pragma statment involved.
        http://www.sqlitetutorial.net/sqlite-drop-table/
        '''

        # check if connection is established
        self._check_connection()

        # get all existed tables
        res = self.db.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")

        # fetchall thems
        res = res.fetchall()

        # create code
        code = 'PRAGMA foreign_keys = OFF;'
        for name in res:
            code += f'DROP TABLE [{name[0]}];'
        code += 'PRAGMA foreign_keys = ON;'

        # drop it
        self.exe(code = code,mode = 's')

        # self.exe('s','''
        #     SQLITE_DBCONFIG_RESET_DATABASE=1;
        #     VACUUM;
        #     SQLITE_DBCONFIG_RESET_DATABASE=0;
        # ''')
