'''
------------------------------------------------------------------------------
BCDR += ***** rolled (s)teel profile 1d unit-sections *****
==============================================================================

------------------------------------------------------------------------------
Copyright (C) 2018 <bacadra@gmail.com> <https://github.com/bacadra>
Team members developing this package:
    - Sebastian Balcerowiak <asiloisad> <asiloisad.93@gmail.com>
------------------------------------------------------------------------------
'''


import os
import importlib

from .. import value

rootdir = os.path.dirname(os.path.realpath(__file__))


class sprof:
    #$$ def __init__
    def __init__(self, core):
        self.core = core
        self._value = value.value(core=core)
        self.catalog = r'ArcelorMittal_V2018_1'

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    #$$ def add
    def add(self, **kwargs):
        self._load_catalog()
        catalog.catalog(core=self.core, value=self._value).add(**kwargs)

    def open(self, **kwargs):
        self._load_catalog()
        catalog.catalog(core=self.core, value=self._value).open(**kwargs)

    def _load_catalog(self):
        catpath = os.path.join(rootdir, self.catalog, 'catalog.py')
        spec = importlib.util.spec_from_file_location('catalog', catpath)
        global catalog
        catalog = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(catalog)