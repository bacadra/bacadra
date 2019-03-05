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

#$ ____ sql & chk __________________________________________________________ #

sql = ''
chk = {}

#$ ____ def tab1 ___________________________________________________________ #

def tab1(t, d, p=None):
    '''
    t - table
    d - data
        n - column name
        d - description as dict with language
        s - sql column type
        c - python allowed types (in list [..])
        u - unise unit string or dict
    p - primary
    '''

    # add to global space
    global sql,chk

    # create table in chk
    chk.update({t:{}})

    # add table header to sql
    sql+='\nCREATE TABLE IF NOT EXISTS ['+t+'] (''\n'

    # loop over columns
    for row in d:

        # add to sql
        sql+='\t['+row['n']+'] ' + row['s'] + ', ''\n'

        # add to chk
        chk[t].update({row['n']:{
            'd':row['d'],
            'u':row['u'],
            'c':row['c'],
        }})

    # add primary keys
    if p:
        sql+='PRIMARY KEY ('+', '.join(['['+key+']' for key in p])+')'
    else:
        sql = sql[:-3]

    # close table
    sql+='\n'');\n'


#$ ######################################################################### #

#$ ____ pragma _____________________________________________________________ #

# https://www.sqlite.org/pragma.html

# https://www.sqlite.org/pragma.html#pragma_journal_mode
# PRAGMA schema.journal_mode = DELETE | TRUNCATE | PERSIST | MEMORY | WAL | OFF
sql+='PRAGMA journal_mode = $<journal_mode>$;\n'

sql+='PRAGMA synchronous = 0;\n'

sql+='PRAGMA synchronous = OFF;\n'

#$ ____ [000:model-data] ___________________________________________________ #

#$$ ________ [010:mates] ___________________________________________________ #

#$$$ ____________ [011:mates:umate] ________________________________________ #

tab1(

    t = '011:mates:umate',

    p = ['id'],

    d = [

        {'n':'id',
            'd':{'en':'identificator',
                 'pl': 'identyfikator'},
            's':'TEXT', 'c':None, 'u':None},

        {'n':'ρ_o',
            'd':{'en':'densinity',
                 'pl': 'gęstość objętościowa materiału'},
            's':'REAL', 'c':[int,float], 'u':'kg m**-3'},

        {'n':'E_1',
            'd':{'en':'young modulus 1st',
            'pl': 'moduł odkształcalności podłużnej 1st'},
            's':'REAL', 'c':[int,float], 'u':'Pa'},

        {'n':'v_1',
            'd':{'en':'poisson ratio 1st',
            'pl': 'współczynnik poissona 1st'},
            's':'REAL', 'c':[int,float], 'u':''},

        {'n':'G_1',
            'd':{'en':'kirchoff modulus 1st',
            'pl': 'moduł odkształcalności poprzecznej 1st'},
            's':'REAL', 'c':[int,float], 'u':'Pa'},

        {'n':'t_e',
            'd':{'en':'temperature extensions',
            'pl': 'roszszerzalność termiczna'},
            's':'REAL', 'c':[int,float], 'u':'°C**-1'},

        {'n':'ttl',
            'd':{'en':'title',
            'pl': 'tytuł'},
            's':'TEXT', 'c':[str], 'u':None},

        {'n':'subcl',
            'd':{'en':'material subclass',
            'pl': 'materiał pochodny'},
            's':'TEXT', 'c':[str], 'u':None},

])


#$$$ ____________ [013:mates:steea] ________________________________________ #

tab1(

    t = '013:mates:steea',

    p = ['id'],

    d = [

        {'n':'id',
            'd':{'en':'identificator',
                 'pl': 'identyfikator'},
            's':'TEXT REFERENCES [011:mates:umate] ([id])',
            'c':None, 'u':None},

        {'n':'family',
            'd':{'en':'grade',
                 'pl': 'gradacja'},
            's':'TEXT', 'c':[str], 'u':None},

        {'n':'grade',
            'd':{'en':'grade',
                 'pl': 'gradacja'},
            's':'TEXT', 'c':[str], 'u':None},

        {'n':'t_max',
            'd':{'en':'max thickness',
                 'pl': 'maksymalna grubość'},
            's':'REAL', 'c':[int, float], 'u':'m'},

        {'n':'f_yk',
            'd':{'en':'characteritic yield strength',
                 'pl': 'charakterystyczna granica plastyczności'},
            's':'REAL', 'c':[int, float], 'u':'Pa'},

        {'n':'f_uk',
            'd':{'en':'characteritic ultimate strength',
                 'pl': 'charakterystyczna wytrzymałość na rozciąganie'},
            's':'REAL', 'c':[int, float], 'u':'Pa'},

        {'n':'E_a',
            'd':{'en':'modulus of elasticity',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':'Pa'},

        {'n':'ε_yk',
            'd':{'en':'yield strain',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':''},

        {'n':'ε_uk',
            'd':{'en':'ultimate strain',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':''},

        {'n':'γ_M0',
            'd':{'en':'partial factor for resistance of cross-sections whatever the class is',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':''},

        {'n':'γ_M1',
            'd':{'en':'partial factor for resistance of members to instability assessed by member checks',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':''},

        {'n':'γ_M2',
            'd':{'en':'partial factor for resistance of cross-sections in tension to fracture',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':''},

        {'n':'γ_M3',
            'd':{'en':'',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':''},

        {'n':'γ_M4',
            'd':{'en':'',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':''},

        {'n':'γ_M5',
            'd':{'en':'',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':''},

        {'n':'γ_M6',
            'd':{'en':'',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':''},

        {'n':'γ_M_ser',
            'd':{'en':'',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':''},

])


#$$$ ____________ [012:mates:conce] ________________________________________ #

tab1(

    t = '012:mates:conce',

    p = ['id'],

    d = [

        {'n':'id',
            'd':{'en':'identificator',
                 'pl': 'identyfikator'},
            's':'TEXT REFERENCES [011:mates:umate] ([id])',
            'c':None, 'u':None},

        {'n':'grade',
            'd':{'en':'grade',
                 'pl': 'gradacja'},
            's':'TEXT', 'c':[str], 'u':None},

        {'n':'f_ck',
            'd':{'en':'characteristic compressive cylinder strength of concrete at 28 days',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':'Pa'},

        {'n':'f_ck_cube',
            'd':{'en':'cubic characteristic compressive strength',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':'Pa'},

        {'n':'f_cm',
            'd':{'en':'mean value of concrete cylinder cornpressive strength',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':'Pa'},

        {'n':'f_ctm',
            'd':{'en':'mean value of axial tensile strength of concrete',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':'Pa'},

        {'n':'f_ctk_005',
            'd':{'en':'characteristic axial tensile strength of concrete 0.05% prob',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':'Pa'},

        {'n':'f_ctk_095',
            'd':{'en':'characteristic axial tensile strength of concrete 0.95% prob',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':'Pa'},

        {'n':'E_cm',
            'd':{'en':'cecant modulus of elasticity of concrete',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':'Pa'},

        {'n':'ε_c1',
            'd':{'en':'',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':''},

        {'n':'ε_cu1',
            'd':{'en':'',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':''},

        {'n':'ε_c2',
            'd':{'en':'',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':''},

        {'n':'ε_cu2',
            'd':{'en':'',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':''},

        {'n':'n_c',
            'd':{'en':'power of inelastic function',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':''},

        {'n':'ε_c3',
            'd':{'en':'',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':''},

        {'n':'ε_cu3',
            'd':{'en':'',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':''},

        {'n':'γ_M',
            'd':{'en':'partial factor for a material property, taking account of uncertainties in the material property itself, in geometric deviation and in the design model used',
                 'pl': ''},
            's':'REAL', 'c':[int, float], 'u':''},

])


#$ ____ [300:design-data] __________________________________________________ #

#$$ ________ [310:bapps] ___________________________________________________ #

#$$ ________ [311:bapps:check] _____________________________________________ #

tab1(

    t = '311:bapps:check',

    p = [],

    d = [

        {'n':'lvl',
            'd':{'en':'',
                 'pl':''},
            's':'TEXT', 'c':[int], 'u':None},

        {'n':'id',
            'd':{'en':'',
                 'pl':''},
            's':'TEXT', 'c':[str], 'u':None},

        {'n':'x',
            'd':{'en':'speed of train',
                 'pl':'prędkość pojazdu'},
            's':'INTEGER', 'c':[int], 'u':'km hr**-1'},

        {'n':'η',
            'd':{'en':'utilization level',
                 'pl':'poziom wytężenia'},
            's':'REAL', 'c':[int,float], 'u':''},

])

#$ ######################################################################### #
