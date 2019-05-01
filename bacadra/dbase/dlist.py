'''
------------------------------------------------------------------------------
***** (d)atabase init (list) ****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
+ Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

#$ ######################################################################### #

#$ ____ sql ________________________________________________________________ #

sql = {}

'''
***** Variable *****

sql: [dict]
    dict of table properties

    *key: [str]
        table name, dont use square bracket [ ], it will be include automaticly.

    *val: [dict]
        dict of columns properties

        *key: [str]
            will treat as column name, dont use square bracket [ ], it will be include automaticly.

        *val: [dict]
            specify column properties, can be input as {}

            'sqltype': [str] (not occur)
                it will be used to define type in sqlite database

            'pytype': [list of strings] (not occur)
                it can be check if proper type inputed, please do not insert unise value into cell!

            'unise': [str] (not occur)
                it will be check if value is input in proper unit, but also can be input without unit -> then treat is as this unit

            'description': [dict] (not occur)
                description of column designing

                *key: [str]
                    represent language shortname like en,pl

                *val: [str]
                    description in proper language

        '*sql': [str]
            sqlcode, in most cases will be fullfill automaticly!

        '*pri': [list of strings]
            list of ids of primary columns

'''


#$$ ________ def table_i1 __________________________________________________ #

def table_i1(table_name, columns, primary=[]):
    '''
    ***** Parameters *****

    table_name: [str]
        name of sql table

    columns: [dict]
        dict of columns properties, for help please look at sql column description

    primary: [list of strings] (None)
        list of columns id's which will be treat as primary keys
    '''

    global sql

    # create table in sql
    sql.update({table_name:{}})

    # add table header to sql
    sql[table_name]['*sql'] = '\nCREATE TABLE IF NOT EXISTS ['+table_name+'] (''\n'
    sql[table_name]['*pri'] = primary

    # loop over columns
    for key,val in columns.items():

        sqltype = val['sqltype'] if 'sqltype' in val else ''

        # add sqlcode
        sql[table_name]['*sql'] += f'\t[{key}] {sqltype},\n'

        # add sql column data
        sql[table_name][key] = val

    # add primary keys
    if primary:
        sql[table_name]['*sql'] += 'PRIMARY KEY ('+', '.join(['['+key+']' for key in primary])+')'
    else:
        sql[table_name]['*sql'] = sql[table_name]['*sql'][:-3]

    # close table
    sql[table_name]['*sql'] += '\n'');\n'


#$ ######################################################################### #

#$ ____ mates ______________________________________________________________ #

#$$ ________ mates:umate ___________________________________________________ #

table_i1(

    table_name = 'mates:umate',
    primary    = ['id'],
    columns    = {

    'id': {
        'sqltype': 'text',
        'pytype' : ['str'],
        'description': {
            'en': 'identificator',
            'pl': 'identyfikator',
        },
    },

    'ρ_o': {
        'sqltype': 'real',
        'pytype' : ['int', 'float'],
        'unise'  : 'kg m**-3',
        'description': {
            'en': 'densinity',
            'pl': 'gęstość objętościowa materiału',
        },
    },

    'E': {
        'sqltype': 'real',
        'pytype' : ['int', 'float'],
        'unise'  : 'Pa',
        'description': {
            'en': 'young modulus',
            'pl': 'moduł odkształcalności podłużnej',
        },
    },

    'ν': {
        'sqltype': 'real',
        'pytype' : ['int', 'float'],
        'unise'  : '',
        'description': {
            'en': 'poisson ratio',
            'pl': 'współczynnik poissona',
        },
    },

    'G': {
        'sqltype': 'real',
        'pytype' : ['int', 'float'],
        'unise'  : 'Pa',
        'description': {
            'en': 'kirchoff modulus',
            'pl': 'moduł odkształcalności poprzecznej',
        },
    },

    't_e': {
        'sqltype': 'real',
        'pytype' : ['int', 'float'],
        'unise'  : '1 Δ°K**-1',
        'description': {
            'en': 'thermal extensions',
            'pl': 'współczynnik roszszerzalności termicznej',
        },
    },

    'ttl': {
        'sqltype': 'text',
        'pytype' : ['str'],
        'description': {
            'en': 'title',
            'pl': 'tytuł',
        },
    },

    'subclass': {
        'sqltype': 'text',
        'pytype' : ['str'],
        'description': {
            'en': 'material subclass',
            'pl': 'materiał pochodny',
        },
    },


})




#$ ######################################################################### #
