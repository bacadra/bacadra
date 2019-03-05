'''
------------------------------------------------------------------------------
***** bacadra (d)ata(base) *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ######################################################################### #

import sqlite3

from ..tools.setts import setts_init
from ..tools.fpack import translate

from . import verrs


#$ ____ class setts ________________________________________________________ #

class setts(setts_init):

#$$ ________ def path ______________________________________________________ #

    def path(self, value=None, check=None, reset=None):
        '''
        path to database
        can be ":memory:" or just path to file, with extension!
        '''
        return self.tools.gst('path', value, check, reset)


#$$ ________ def multithread _______________________________________________ #

    def multithread(self, value=None, check=None, reset=None):
        return self.tools.gst('multithread', value, check, reset)

#$$ ________ def journal_mode ______________________________________________ #

    def journal_mode(self, value=None, check=None, reset=None):
        return self.tools.gst('journal_mode', value, check, reset)

#$$ ________ def auto_commit _______________________________________________ #

    def auto_commit(self, value=None, check=None, reset=None):
        return self.tools.gst('auto_commit', value, check, reset)

#$$ ________ def write _____________________________________________________ #

    def write(self, value=None, check=None, reset=None):

        if value in [True, 'insert', 'i']:
            value = 'insert'

        elif value in ['insert or replace','replace','ior']:
            value = 'insert or replace'

        elif value in ['insert or ignore','ignore','ioi']:
            value = 'insert or ignore'

        else:
            raise ValueError('Unknow where type')

        return self.tools.gst('write', value, check, reset)

    __write = 'insert'


#$$ ________ def echo ______________________________________________________ #

    def echo(self, value=None, x=None, check=None, reset=None):
        '''
        Atribute <echo> set the output of base methods in texme class. It provide letters interface "+" which can turn on/off

        > "+" -- plain sql code.

        User can type value as True then will be set "+" configuration or False then no output will be produced.
        '''

        return self.tools.let('echo', value, check, reset,
            x=x,
            full={'True':'x', 'False':''}
        )


#$ ____ class dbase ________________________________________________________ #

class dbase:
    '''
    Important links:
    https://docs.python.org/3.7/library/sqlite3.html
    '''

    setts = setts()
    setts.path(':memory:')
    setts.multithread(True)
    setts.journal_mode('OFF')
    setts.auto_commit(True)
    setts.write('insert')
    setts.echo(False)


#$$ ________ def __init __ __________________________________________________ #

    def __init__(self, core=None):

        self.core = core

        self.setts = setts(self.setts, self)

        # sqlite3 connection
        self.db = None

        # sqlite3 connection.cursor
        self.cr = None

        # structure and constraint of database
        self.chk = {}

        # connection flags
        # variable is False or string with connected database name
        self._connQ = False


#$$ ________ def connect ____________________________________________________ #

    def connect(self, path=None, clear=True):
        '''
        Create and connect to database system.
        '''

        # if user type path, then set it as atribute
        if path:
            self.setts.path(path)

        # if connection is not established or other database was selected
        if self._connQ != self.setts.path():

            # create sqlite.connection object
            self.db = sqlite3.connect(
                database          = self.setts.path(),
                timeout           = 0,
                check_same_thread = not self.setts.multithread(),
                isolation_level   = None,
            )

            # set connection flags as True
            self._connQ = self.setts.path()

            # set row_factory
            self.db.row_factory = sqlite3.Row

            # create cursor instance
            self.cr = self.db.cursor()

            # if clear is True, then redefine all table
            if clear:
                self.interrupt()
                self.clear()

            # create tables if they not exists
            self._create_system()

        # if connection to current database is established and clear flags
        elif clear:

            # then redefine all table
            self.clear()

            # create tables if they not exists
            self._create_system()


#$$ ________ def cloase _____________________________________________________ #

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


#$$ ________ def commit _____________________________________________________ #

    def commit(self):
        '''
        Commit changes.
        '''

        # check if connection is established
        self._check_connection()

        # commit journal files
        self.db.commit()


#$$ ________ def _check_connection __________________________________________ #

    def _check_connection(self):
        '''
        Raise ERROR if connection is not established.
        '''

        # if connection is not established
        if not self._connQ:

            # then raise error with tips
            verrs.BCDR_dbase_ERROR_Open_Database()


#$$ ________ def interupt ___________________________________________________ #

    def interrupt(self):
        self.db.interrupt()


#$$ ________ def exe ________________________________________________________ #

    def exe(self, mode, code, data=None):
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

        if '+' in self.setts.echo():
            print('[dbase]\n'+code)

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

        if self.setts.auto_commit():
            self.commit()


#$$ ________ def add ________________________________________________________ #

    def add(self, mode, table, cols, data, write=None):
        '''
        mode='r'
        Add data into system. Dev need to provide information about table, list of oclumns and data tuple eg. (a,b).

        mode='m'
        Add many data into system. Dev need to provide information about table, list of column and data list eg. [(a,b),(c,d)].

        cols = [..
            [table, column name, alias],
        ..]

        '''

        # connection is checked in exe method
        write = self.setts.check_loc('write', write)

        _table = []
        for row in table:
            if type(row)==str:
                _table.append('['+row+']')
            elif type(row)==list and len(row)==2:
                _table.append('['+row[0]+']'+' as ['+row[2]+']')
        table = ','.join(_table)

        _cols = []
        for row in cols:
            if type(row)==str:
                _cols.append('['+row+']')
            elif type(row)==list and len(row)==2:
                _cols.append('['+row[0]+'].['+row[1]+']')
            elif type(row)==list and len(row)==3:
                _cols.append('['+row[0]+'].['+row[1]+']'+' as ['+row[2]+']')
        cols = ',\n'.join(_cols)

        # create noname vector
        cole = ','.join(['?' for col in range(len(_cols))])

        # call to exe method
        self.exe(
            code = f"{self.setts.write()} INTO {table}({cols}) VALUES({cole})",
            data = data,
            mode = mode,
        )


#$$ ________ def get ________________________________________________________ #

    def get(self, mode, table, cols=None, where=None, join=None, formula=1):
        '''
        mode='s'

        connection is checked in exe method
        '''

        # prepare tables
        _table = []
        for row in table:
            if type(row)==str:
                _table.append('['+row+']')
            elif type(row)==list and len(row)==2:
                _table.append('['+row[0]+']'+' as ['+row[2]+']')
        table = ','.join(_table)

        # prepare where
        if where==None:
            where = ''
        elif type(where)==str:
            where = '\nwhere ' + where
        else:
            where = '\nwhere ' + ' AND '.join(['('+row+')' for row in where])

        # prepare joins
        _join = []
        if join==None:
            join=''
        else:
            for row in join:
                if type(row)==str:
                    _join.append(row)
                elif type(row)==list and len(row)==3:
                    _join.append(row[0]+' '+row[1]+' on '+row[2])
            join = '\n' + '\n'.join(_join)

        # prepare columns
        if cols==None:
            cols = '*'
        else:
            _cols = []
            for row in cols:
                if type(row)==str:
                    _cols.append('['+row+']')
                elif type(row)==list and len(row)==2:
                    _cols.append('['+row[0]+'].['+row[1]+']')
                elif type(row)==list and len(row)==3:
                    _cols.append('['+row[0]+'].['+row[1]+']'+' as ['+row[2]+']')
            cols = ',\n'.join(_cols)

        # select statment
        if formula==1:
            self.exe('r',
                f'SELECT\n{cols}\nfrom {table} {join} {where}'
            )

        elif formula==2:
            self.exe('r',
                f'SELECT* FROM (SELECT\n{cols}\nfrom {table} {join}) {where}'
            )

        if  mode=='i':
            return self.cr

        elif mode=='r':
            return self.cr.fetchone()

        elif mode=='m':
            return self.cr.fetchall()

        elif mode=='s':
            return self.cr.fetchone()[0]

        else:
            raise ValueError()


#$$ ________ def obj ________________________________________________________ #

    from .getdb import obj

#$$ ________ def edit _______________________________________________________ #

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


#$$ ________ def _create_system _____________________________________________ #

    def _create_system(self):
        from . import dlist

        self.chk = dlist.chk

        code = translate(dlist.sql, {
            '$<journal_mode>$': self.setts.journal_mode(),
        })

        self.exe(code=code, mode='s')


#$$ ________ def clear ______________________________________________________ #

    def clear(self):
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
        self.exe(code=code, mode='s')

#$ ######################################################################### #
