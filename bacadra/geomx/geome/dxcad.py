'''
------------------------------------------------------------------------------
BCDR += ***** load (dx)f/w geometry from (cad) system *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''

import dxfgrabber

from .. import geomf

# TODO: add transfrom XY plane to 3d plane,
# constrain it with global system settings

#$ ____ class dxcad ________________________________________________________ #

class dxcad:
    #$$ def __init__
    def __init__(self, core):
        self.core = core

        self._pack = {}
        self._geomf = geomf.index(core=core)



    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    #$$ def parse
    def parse(self, path=None, type='dxf'):
        if type=='dxf':
            self._dxf(path)

    #$$ def layer
    def layer(self, lay, **kwargs):
        self._pack.update({lay:kwargs})

    #$$ def -dxf
    def _dxf(self,path):
        self.file = dxfgrabber.readfile(path, {"assure_3d_coords": True})
        self._parse_nodes()
        self._parse_lines()

    #$$ def parse-nodes
    def _parse_nodes(self):
        all_insert = [entity for entity in self.file.entities if entity.dxftype=='INSERT']

        node_name = 'a'
        node_nami = 1
        for insert in all_insert:
            if insert.name == 'bcdr-node':
                attributes = {}
                for attribute in insert.attribs:
                    attributes.update({attribute.tag:attribute.text})

                if attributes['id']:
                    id = attributes['id']
                else:
                    id = node_name + str(node_nami)
                    node_nami += 1

                if self.setts.get('system_space') in ['2d','2t'] and self.setts.get('2dXY2XZ'):
                    self._geomf.nodes.add(
                        id  = id,
                        x   = +insert.insert[0],
                        z   = -insert.insert[1],
                        fix = attributes['fix'],
                        ttl = attributes['ttl'],
                    )

                else:
                    self._geomf.nodes.add(
                        id  = id,
                        x   = +insert.insert[0],
                        y   = +insert.insert[1],
                        z   = -insert.insert[2],
                        fix = attributes['fix'],
                        ttl = attributes['ttl'],
                    )

    #$$ def -parse-lines
    def _parse_lines(self):
        all_lines = [entity for entity in self.file.entities if entity.dxftype=='LINE']

        line_name = 'a'
        line_nami = 1
        for line in all_lines:
            if line.layer[:5] == 'bcdr-':

                ε = self.setts.get('node_tol').drop('m')

                l1 = line.start

                if self.setts.get('system_space') in ['2d','2t'] and self.setts.get('xy->xz'):
                    node1 = self.core.dbase.get(f'''
                    SELECT [id] FROM [111:nodes:topos]
                    WHERE
                        ([x] BETWEEN ''' + str(l1[0]-ε) + ' AND ' + str(l1[0]+ε) + ''')
                    AND
                        ([z] BETWEEN ''' + str(-l1[1]-ε) + ' AND ' + str(-l1[1]+ε) + ''')
                    ''')

                else:
                    node1 = self.core.dbase.get(f'''
                    SELECT [id] FROM [111:nodes:topos]
                    WHERE
                        ([x] BETWEEN ''' + str(l1[0]-ε) + ' AND ' + str(l1[0]+ε) + ''')
                    AND
                        ([y] BETWEEN ''' + str(l1[1]-ε) + ' AND ' + str(l1[1]+ε) + ''')
                    AND
                        ([z] BETWEEN ''' + str(-l1[2]-ε) + ' AND ' + str(-l1[2]+ε) + ''')
                    ''')

                if len(node1) > 1:
                    print(node1)
                    raise ValueError('Nodes too small distance between self')
                elif len(node1) == 0:
                    raise ValueError(f'Node misses, coor: {l1}')
                else:
                    node1 = node1[0]


                l2 = line.end
                if self.setts.get('system_space') in ['2d','2t'] and self.setts.get('2dXY2XZ'):
                    node2 = self.core.dbase.get(f'''
                    SELECT [id] FROM [111:nodes:topos]
                    WHERE
                        ([x] BETWEEN ''' + str(l2[0]-ε) + ' AND ' + str(l2[0]+ε) + ''')
                    AND
                        ([z] BETWEEN ''' + str(-l2[1]-ε) + ' AND ' + str(-l2[1]+ε) + ''')
                    ''')

                else:
                    node2 = self.core.dbase.get(f'''
                    SELECT [id] FROM [111:nodes:topos]
                    WHERE
                        ([x] BETWEEN ''' + str(l2[0]-ε) + ' AND ' + str(l2[0]+ε) + ''')
                    AND
                        ([y] BETWEEN ''' + str(l2[1]-ε) + ' AND ' + str(l2[1]+ε) + ''')
                    AND
                        ([z] BETWEEN ''' + str(-l2[2]-ε) + ' AND ' + str(-l2[2]+ε) + ''')
                    ''')

                if len(node2) > 1:
                    print(node2)
                    raise ValueError('Nodes too small distance between self')
                elif len(node2) == 0:
                    raise ValueError(f'Node misses, coor: {l2}')
                else:
                    node2 = node2[0]


                pack = self._pack[line.layer[5:]]

                if pack['etype'] == 'truss':
                    self._geomf.truss.add(
                        id   = line_name + str(line_nami),
                        n1   = node1[0],
                        n2   = node2[0],
                        sect = pack['sect'],
                    )

                elif pack['etype'] == 'beams':
                    self._geomf.beams.add(
                        id   = line_name + str(line_nami),
                        n1   = node1[0],
                        n2   = node2[0],
                        sect = pack['sect'],
                    )

                else:
                    raise ValueError('Unknow element type')

                line_nami += 1




