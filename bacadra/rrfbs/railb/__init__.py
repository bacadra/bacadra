from ...tools.rootx import rootx

from .en155 import en155

#$ class index
class index(rootx):
    def __init__(self, core=None):

        self.en155 = en155(core=core)