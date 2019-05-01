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

import re

from ..tools.setts import sinit

from ..tools.fpack import translate, mdata

from . import verrs

import pickle
sqlite3.register_converter('LIST' , pickle.loads)
sqlite3.register_adapter  ( list  , pickle.dumps)
sqlite3.register_converter('TUPLE', pickle.loads)
sqlite3.register_adapter  ( tuple , pickle.dumps)
sqlite3.register_converter('DICT' , pickle.loads)
sqlite3.register_adapter  ( dict  , pickle.dumps)
sqlite3.register_converter('SET'  , pickle.loads)
sqlite3.register_adapter  ( set   , pickle.dumps)

import dill, types
sqlite3.register_converter('FUN'             , dill.loads)
sqlite3.register_adapter  (types.FunctionType, dill.dumps)


#$ ____ class sqldata ______________________________________________________ #

class sqldata(sqlite3.Row):

    def __call__(self):
        mdata(dict(self))()

    def __repr__(self):
        return str(dict(self))


#$ ____ class setts ________________________________________________________ #

class setts(sinit):

#$$ ________ def path ______________________________________________________ #

    def path(self, value=None, check=None):
        '''
        path to database
        can be ":memory:" or just path to file, with extension!
        '''
        return self.tools.sgc('path', value, check)


#$$ ________ def multithread _______________________________________________ #

    def multithread(self, value=None, check=None):
        return self.tools.sgc('multithread', value, check)

#$$ ________ def journal_mode ______________________________________________ #

    def journal_mode(self, value=None, check=None):
        return self.tools.sgc('journal_mode', value, check)

#$$ ________ def auto_commit _______________________________________________ #

    def auto_commit(self, value=None, check=None):
        return self.tools.sgc('auto_commit', value, check)

#$$ ________ def write _____________________________________________________ #

    def write(self, value=None, check=None):

        if value in [True, 'insert', 'i', 'ioe', 'e']:
            value = 'insert'

        elif value in ['insert or replace','replace','ior', 'r']:
            value = 'insert or replace'

        elif value in ['insert or ignore','ignore','ioi', 'i']:
            value = 'insert or ignore'

        elif value!=None:
            raise ValueError('Unknow where type')

        return self.tools.sgc('write', value, check)

#$$ ________ def echo ______________________________________________________ #

    def echo(self, code=None, check=None):
        '''
        Atribute <echo> set the output of base methods in texme class. It provide letters interface "+" which can turn on/off

        > "x" -- plain sql code.

        User can type value as True then will be set "+" configuration or False then no output will be produced.
        '''

        if   code==True : code='x'
        elif code==False: code=''

        return self.tools.sgc(name='echo', value=code, check=check)



#$ ____ class dbase ________________________________________________________ #

class dbase:
    '''
    Important links:
    https://docs.python.org/3.7/library/sqlite3.html
    '''

    # structure and constraint of database
    # from . import dlist as sql
    from .dlist import sql

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

        self.setts = setts(master=self.setts.tools, root=self)

        # sqlite3 connection
        self.db = None

        # sqlite3 connection.cursor
        self.cr = None

        # connection flags
        # variable is False or string with connected database name
        self._connQ = False

#$$ ________ def connect ____________________________________________________ #

    def connect(self, clear=True, path=None):
        '''
        Create and connect database system.

        ***** Parameters *****

        clear: [bool] (True)

        path: [str] (None)
        '''

        # if user type path, then set it as atribute
        if path==None: path = self.setts.path(path, check=True)

        # if connection is not established or other database was selected
        if self._connQ != path:

            # create sqlite.connection object
            self.db = sqlite3.connect(
                database          = path,
                timeout           = 0,
                check_same_thread = not self.setts.multithread(),
                isolation_level   = None,
                detect_types      = sqlite3.PARSE_DECLTYPES,
            )

            # set connection flags as True
            self._connQ = path

            # set row_factory
            # self.db.row_factory = sqlite3.Row
            self.db.row_factory = sqldata

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


#$$ ________ def close ______________________________________________________ #

    def close(self, commit_all=True):
        '''
        Close connection to database. As defualt all changes will be commited (.commit_all=True).

        ***** Parameters *****

        commit_all: [bool] (True)
        '''


        # first check if connection is established
        if self._connQ:

            # if commit flag is True
            if commit_all==True:
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


#$$ ________ def exe ________________________________________________________ #

    def exe(self, mode, code, data=None):
        '''
        Execute sql statment. Before use it connection must be established.

        ***** Parameters *****

        mode: {...}

            mode: {'execute', 'row', 'r''}
                Execution of single query. The method provide security interface with (?,?,?) and (a,b,c) data.

            mode: {'executemany', 'many', 'm'}
                Execution of single query. The method provide security interface with (?,?,?) and [(a,b,c), ...] data.

            mode: {'executescript', 'script', 's'}
                Execution multiquerys. Query must be sepparated by ";" symbol.

        code: [str]
            valid sqlite3 code which will be executed by database

        data: [tuple or list with tuples] (None)
            depend on mode, please refere it

        '''

        # check if connection is established
        self._check_connection()

        if 'x' in self.setts.echo():
            print('***** dbase.exe *****\n'+code)
            print(f'***** dbase.exe:data *****\n{data}')

        if mode in ['execute', 'row', 'r']:
            if data:
                self.cr.execute(code, data)

            else:
                self.cr.execute(code)

        elif mode in ['executemany', 'many', 'm']:
            self.cr.executemany(code, data)

        elif mode in ['executescript', 'script', 's']:
            self.cr.executescript(code)

        else:
            verrs.BCDR_dbase_ERROR_undefined_transaction_mode(
                command = 'exe',
                mode    = mode,
                allow   = "{'execute', 'row', 'r'} or {'executemany', 'many', 'm'} or {'executescript', 'script', 's'}"
            )

        if self.setts.auto_commit():
            self.commit()



#$$ ________ def add ________________________________________________________ #

    def add(self, mode, table, cols, data, write=None):
        '''
        Add new data into database. Before use it connection must be established.

        ***** Parameters *****

        mode: reference to .exe(mode=..)

        table: [str, list[str or dict or tuple(len=2)]]
            tuple[0], dict['n']: [str] name of table
            tuple[1], dict['a']: [str] alias

            ex: 'tab:1'
            ex: ['tab:1']
            ex: ['tab:1', 'tab:2']
            ex: ['tab:1', ('tab:2', 't2')
            ex: ['tab:1', {'n':'tab:2', 'a':'t2'}]

        cols:
            tuple[0], dict['t']: [str] name of table, optional
            tuple[1], dict['n']: [str] name of column
            tuple[2], dict['a']: [str] alias, optional

            ex: ['a','b','c']
            ex: ['tab:1.a?actor','b','c']
            ex: [{'t':'tab:1', 'n':'a', 'a':'actor'}, 'b', 'c'}
            ex: [{'t':'tab:1', 'n':'a'}, 'b', 'c'}
            ex: [('tab:1', 'a', 'actor'), 'b', 'c']
            ex: [('tab:1', 'a'), 'b', 'c']

            # ex: {'a':{}, 'b':{}, 'c':{}}
            # ex: {'a':{'a':'actor', 't':'tab:1'}, 'b':{}, 'c':{}}

        data:

        '''

        table = self._parse_table_name(table)

        cols, cole = self._parse_cols_name(cols)

        self.exe(
            mode = mode,
            code = f"{self.setts.write()} INTO {table}(\n{cols}\n)\nVALUES({cole})",
            data = data,
        )


#$$ ________ def get ________________________________________________________ #

    def get(self, mode, table, cols=None, where=None, join=None, formula=1):
        '''
        Get data from database.

        ***** Parameters *****

            mode: reference to .exe(mode=..). Method is extended of ...

            table:

            cols:

            where:

            join:

            formula: [int] (1)

        '''

        table = self._parse_table_name(table)

        cols, cole = self._parse_cols_name(cols)

        join = self._parse_join_name(join)

        where = self._parse_where_name(where)

        # select statment
        if formula==1:
            self.exe('r',
                f'SELECT\n{cols}\nfrom {table} {join} {where}'
            )

        elif formula==2:
            self.exe('r',
                f'SELECT* FROM (SELECT\n{cols}\nfrom {table} {join}) {where}'
            )

        if  mode in ['iterate', 'iterator', 'iter', 'i']:
            return self.cr

        elif mode in ['fetchone', 'one', 'o', 'row', 'r']:
            return self.cr.fetchone()

        elif mode in ['fetchall', 'all', 'a', 'many', 'm']:
            return self.cr.fetchall()

        elif mode in ['single', 's']:
            return self.cr.fetchone()[0]

        else:
            raise ValueError()


#$$ ________ def edit ______________________________________________________ #

    def edit(self, table, cols, data, where):
        '''
        ***** Parameters *****

        table:

        cols:

        data:

        where:


        '''


        table = self._parse_table_name(table)

        cols, cole = self._parse_cols_name(cols)

        where = self._parse_where_name(where)

        self.exe(
            code = f"UPDATE {table} SET {cols} WHERE {where}",
            data = data,
            mode = 'r',
        )


#$$ ________ def commit _____________________________________________________ #

    def commit(self):
        '''
        Commit changes.
        '''

        # check if connection is established
        self._check_connection()

        # commit journal files
        self.db.commit()

#$$ ________ def interupt ___________________________________________________ #

    def interrupt(self):
        self.db.interrupt()

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


#$$ ________ def _create_system _____________________________________________ #

    def _create_system(self):
        '''
        Load database sctructure
        '''

        self.exe(

            code = translate(

                ';\n'.join(table['*sql'] for table in self.sql.values()),

                {

                '$<journal_mode>$': self.setts.journal_mode(),

            }),

            mode = 'script',

        )


#$$ ________ def _check_connection __________________________________________ #

    def _check_connection(self):
        '''
        Raise ERROR if connection is not established.
        '''

        # if connection is not established
        if not self._connQ:

            # then raise error with tips
            verrs.BCDR_dbase_ERROR_Open_Database()


    def _parse_table_name(self, table):
        '''
        table: [str, list[str or dict or tuple(len=2)]]
            tuple[0], dict['n']: [str] name of table
            tuple[1], dict['a']: [str] alias

            ex: 'tab:1'
            ex: ['tab:1']
            ex: ['tab:1', 'tab:2']
            ex: ['tab:1', ('tab:2', 't2')
            ex: ['tab:1', {'n':'tab:2', 'a':'t2'}]
        '''

        if table==None: return ''

        if type(table)==str:
            table = f'[{table}]'

        elif type(table)==list:

            table_list = []

            for table1 in table:

                if type(table1)==str:
                    table_list.append(f'[{table1}]')

                elif type(table1)==dict:
                    name = None
                    if   'name'  in table1: name = table1['name']
                    elif 'n'     in table1: name = table1['n']

                    alias = None
                    if   'alias' in table1: alias = table1['alias']
                    elif 'a'     in table1: alias = table1['a']


                    if alias:
                        table_list.append(f'[{name}] as [{alias}]')
                    else:
                        table_list.append(f'[{name}]')

                elif type(table1)==tuple and len(table1)==2:
                    table_list.append(f'[{table1[0]}] as [{table1[1]}]')

                else:
                    pass # error raise

            table = ','.join(table_list)

        return table


    def _parse_cols_name(self, cols):
        '''
        cols:
            tuple[0], dict['t']: [str] name of table, optional
            tuple[1], dict['n']: [str] name of column
            tuple[2], dict['a']: [str] alias, optional

            ex: ['a','b','c']
            ex: ['tab:1.a?actor','b','c']
            ex: [{'t':'tab:1', 'n':'a', 'a':'actor'}, 'b', 'c'}
            ex: [{'t':'tab:1', 'n':'a'}, 'b', 'c'}
            ex: [('tab:1', 'a', 'actor'), 'b', 'c']
            ex: [('tab:1', 'a'), 'b', 'c']

            *

            # ex: {'a':{}, 'b':{}, 'c':{}}
            # ex: {'a':{'a':'actor', 't':'tab:1'}, 'b':{}, 'c':{}}
        '''

        if cols==None: return ''

        if cols=='*':
            return cols, ''

        if type(cols)==list:

            cols_list = []

            for col1 in cols:

                if type(col1)==str:

                    position = col1.find('?')

                    if position > 0:
                        alias = col1[position+1:]
                        table_and_cols = col1[:position]
                    else:
                        alias=''
                        table_and_cols = col1

                    position = table_and_cols.find('.')
                    if position > 0:
                        tab1, name = table_and_cols.split('.')
                    else:
                        tab1 = ''
                        name = table_and_cols

                    if tab1!='': tab1= f'[{tab1}].'
                    name = f'[{name}]'
                    if alias!='': alias= f' as [{alias}]'

                    cols_list.append(tab1 + name + alias)

                elif type(col1)==dict:
                    tab1 = None
                    if   'table' in col1: tab1 = col1['table']
                    elif 't'     in col1: tab1 = col1['t']

                    name = None
                    if   'name'  in col1: name = col1['name']
                    elif 'n'     in col1: name = col1['n']

                    alias = None
                    if   'alias' in col1: alias = col1['alias']
                    elif 'a'     in col1: alias = col1['a']

                    if tab1!='': tab1= f'[{tab1}].'
                    name = f'[{name}]'
                    if alias!='': alias= f' as [{alias}]'

                    cols_list.append(tab1 + name + alias)


                elif type(col1)==tuple and len(col1)==2:
                    tab1, name = tuple
                    cols_list.append(tab1 + name)

                elif type(col1)==tuple and len(col1)==3:
                    tab1, name, alias = tuple
                    cols_list.append(tab1 + name + alias)


            cols = ',\n'.join(cols_list)

        elif type(cols)==dict:
            pass

        cole = ','.join(['?' for col in range(len(cols_list))])

        return cols,cole


    def _parse_join_name(self, join):
        '''

        ix: INNER JOIN albums ON albums.albumid = tracks.albumid as ab
        ex: ('inner', 'albums', 'albumid', 'tracks', 'albumid')
        ex: ('inner', 'albums', 'albumid', 'tracks', 'albumid', 'ab')
        ex: {
            'm','mode' : 'inner',
            't','table': ('albums', 'albumid'),
            'o','on'   : ('tracks', 'albumid'),
            'a','alias': 'ab',
            }

        ex: [('inner', 'albums', 'albumid', 'tracks', 'albumid'), ...]
        '''

        if join==None: return ''

        if type(join)==tuple:

            if len(join)==5:
                mode, table_name, table_col, on_name, on_col = tuple
                alias = ''

            if len(join)==6:
                mode, table_name, table_col, on_name, on_col, alias = tuple

        elif type(join)==dict:

            mode       = join['m']
            table_name = join['t'][0]
            table_col  = join['t'][1]
            on_name    = join['o'][0]
            on_col     = join['o'][1]
            alias      = join['a'] if 'a' in join else ''

        elif type(join)==list:

            return '\n'.join([self._parse_join_names(join1) for join1 in join])


        alias = f' as [{alias}]'

        return f'{mode} JOIN {table_name} ON [{table_name}].[{table_col}]=[{on_name}].[{on_name}].[{on_col}]{alias}'


    def _parse_where_name(self, where, full=True):
        '''

        ex: ('a', '=', 5)
        ex: [('a', '=', 5), ...] (and)


        # ex: 'id=5'
        # ex: 'id="5"'
        # ex: 'tab:1.id=tab:2.b'
        # ex: 'tab:1.id="18"'
        # ex: ('id', '=', 5)
        # ex: ('id', '>', '5')
        # ex: ('tab1','id', '=', 5)
        # ex: ('tab1','id', '=', 'tab2', 'b')
        # ex: [('id', '>', '5'), ...]   (and)
        '''

        full = 'WHERE ' if full else ''

        if where==None: return ''

        if type(where)==str:
            left, operator, right = re.split('(\>\=|\<=|\=|\<|\>)+', where)

            left, right = left.split('.'), right.split('.')

            left = f'[{left[0]}].[{left[1]}]' if len(left)==2 and left[0]!='' else f'[{left[1]}]' if len(left)==2 else left[0]

            right = f'[{right[0]}].[{right[1]}]' if len(right)==2 else right[0]

            return f'{full}{left}{operator}{right}'

        if type(where)==tuple:

            left, operator, right = where

            if type(left)==str:
                left = left.split('.')
                left = f'[{left[0]}].[{left[1]}]' if len(left)==2 and left[0]!='' else f'[{left[1]}]' if len(left)==2 else left[0]

            if type(right)==str:
                right = right.split('.')
                right = f'[{right[0]}].[{right[1]}]' if len(right)==2 and right[0]!='' else f'[{right[1]}]' if len(right)==2 else right[0]

            return f'{full}({left}{operator}{right})'

        elif type(where)==list:

            return f'{full}'+' AND '.join([
                self._parse_where_name(where1, full=False)[0] for where1 in where
            ])