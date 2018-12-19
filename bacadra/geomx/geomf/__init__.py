from . import nodes
from . import truss
from . import beams

#$ class index
class index:
    #$$ __init__
    def __init__(self, core):
        self.nodes = nodes.nodes(core=core)
        self.truss = truss.truss(core=core)
        self.beams = beams.beams(core=core)

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

# import sqlite3
# import pandas as pd
#
#
# data_units = {
#     'node(x)':{'m':1},
#     'node(y)':{'m':1},
#     'node(z)':{'m':1},
# }
#
#
# #$ main
# class main():
#     #$$ __init__
#     def __init__(self, dbase, pinky):
#         self.sett = sett(dbase, pinky)
#         self.node = node(dbase, pinky)
#         # self.trus = trus(dbase)
#         # self.beam = beam(dbase)
#         # self.quad = quad(dbase)
#
#
# #$ sett
# class sett():
#     #$$ __init__
#     def __init__(self, dbase):
#         self.dbase = dbase
#
#     def __clear_data(self):
#         self.dbase.exes(
#             "DELETE FROM [111:node:topo];"
#             "DELETE FROM [112:node:load];"
#             "DELETE FROM [113:node:stat];"
#         )
#
#     def system(self):
#         self.__clear_data()
#
#
# #$ node
# class node():
#     #$$ __init__
#     def __init__(self, dbase, pinky):
#         self.dbase = dbase
#         self.pinky = pinky
#
#     #$$ add
#     def add(self,
#             no    = None,
#             x     = None,
#             y     = None,
#             z     = None,
#             fix   = None,
#             ref   = None,
#             ucs   = None,
#             data  = None,
#             no_   = None,
#             x_    = None,
#             y_    = None,
#             z_    = None,
#             fix_  = None,
#             ref_  = None,
#             ucs_  = None):
#         '''
#         bacadra.geomf.node.add
#         ----------------------
#         Add new nodes into fem system.
#         '''
#
#
#         parseddata = self.dbase.parsedata(
#             {'no'  : no,
#              'x'   : x,
#              'y'   : y,
#              'z'   : z,
#              'fix' : fix,
#              'ref' : ref,
#              'ucs' : ucs},
#
#             {'no'  : no_,
#              'x'   : x_,
#              'y'   : y_,
#              'z'   : z_,
#              'fix' : fix_,
#              'ref' : ref_,
#              'ucs' : ucs_},
#
#             {'x'   : 'geomf.node.[x]',
#              'y'   : 'geomf.node.[y]',
#              'z'   : 'geomf.node.[z]'},
#
#             data
#         )
#
#         # print(parseddata)
#
#         try:
#             self.dbase.exem(
#             "INSERT INTO [111:node:topo]"
#             "{0}"
#             "VALUES"
#             "{1}"
#             .format(parseddata[0], parseddata[1]), parseddata[2])
#
#         except sqlite3.IntegrityError:
#             print(
#             "[warning][bcdr.geomf.node.add] "
#             "there is a problem with node adding, node already exists"
#             .format(no))


    # #$$ shw
    # def shw(self, val,
    #     no=True,  x=True, y=True, z=True, fix=True, ref=True, ucs=True):
    #
    #     sett1, sett2 = '', []
    #     if no:  sett1 += '[111:node:topo].[id],'  ; sett2.append('[id]')
    #     if x:   sett1 += '[111:node:topo].[x],'   ; sett2.append('[x]')
    #     if y:   sett1 += '[111:node:topo].[y],'   ; sett2.append('[y]')
    #     if z:   sett1 += '[111:node:topo].[z],'   ; sett2.append('[z]')
    #     if fix: sett1 += '[111:node:topo].[fix],' ; sett2.append('[fix]')
    #     if ref: sett1 += '[111:node:topo].[ref],' ; sett2.append('[ref]')
    #     if ucs: sett1 += '[111:node:topo].[ucs],' ; sett2.append('[ucs]')
    #
    #     if len(sett1) > 0 : sett1 = sett1[:-1]
    #
    #     if type(val)==int:
    #         val = '[id] = ({0})'.format(val)
    #
    #     self.dbase.exe('''
    #         SELECT
    #         {0}
    #         FROM [111:node:topo]
    #         WHERE {1}
    #         '''.format(sett1, val))
    #
    #     res = self.dbase.db.fetchall()
    #
    #     if len(res) == 0:
    #         print(
    #         "[warning][bcdr.geomf.node.shw] "
    #         "There is no node where {0}"
    #         .format(no))
    #
    #     else:
    #         df = pd.DataFrame(data=res, columns=sett2)
    #         return df
    #
    #
    # #$$ rem
    # def rem(self, val):
    #     if type(val)==int:
    #         val = '[id] = ({0})'.format(val)
    #
    #     self.dbase.exe('''SELECT COUNT(*) FROM [111:node:topo]
    #                              WHERE {0};'''.format(val))
    #
    #     if self.dbase.db.fetchall()[0][0] > 0:
    #         self.dbase.exe('''DELETE FROM [111:node:topo]
    #                              WHERE {0};'''.format(val))
    #     else:
    #         print(
    #         "[warning][bcdr.geomf.node.del] "
    #         "There is no node where {0}"
    #         .format(val))
    #
    # #$$ mod
    # def mod(self, val, no=None, x=None, y=None, z=None, fix=None, ref=None, ucs=None):
    #     if type(val)==int:
    #         val = '[id] = ({0})'.format(val)
    #
    #     self.dbase.exe('''SELECT COUNT(*) FROM [111:node:topo]
    #                              WHERE {0};'''.format(val))
    #
    #     if self.dbase.db.fetchall()[0][0] == 1:
    #         sett = ''
    #         if no:  sett += '[id]='  + str(no)  + ','
    #         if x:   sett += '[x]='   + str(x)   + ','
    #         if y:   sett += '[y]='   + str(y)   + ','
    #         if z:   sett += '[z]='   + str(z)   + ','
    #         if fix: sett += '[fix]=' + str(fix) + ','
    #         if ref: sett += '[ref]=' + str(ref) + ','
    #         if ucs: sett += '[ucs]=' + str(ucs) + ','
    #         if len(sett) > 0 : sett = sett[:-1]
    #
    #         self.dbase.exe('''UPDATE [111:node:topo] SET {1}
    #                        WHERE {0}'''.format(val, sett))
    #
    #     if self.dbase.db.fetchall()[0][0] > 1:
    #         print(
    #         "[warning][bcdr.geomf.node.mod] "
    #         "There is too much nodes where {0}"
    #         .format(val))
    #
    #     else:
    #         print(
    #         "[warning][bcdr.geomf.node.mod] "
    #         "There is no node where {0}"
    #         .format(val))
    #
# #$ trus
# class trus():
#     #$$ __init__
#     def __init__(self, dbase):
#         self.dbase = dbase
#
# #$ beam
# class beam():
#     #$$ __init__
#     def __init__(self, dbase):
#         self.dbase = dbase
#
# #$ quad
# class quad():
#     #$$ __init__
#     def __init__(self, dbase):
#         self.dbase = dbase
