from .texme import texme

class texpj:

    def __init__(self, core=None, tex=None):

        self.core = core

        self.tex  = tex

        self.data = {}


    def add(self, id, **kwargs):
        if type(id)==tuple:
            sid,sub = id
            self.data[sid].setts.mbuff = sub, kwargs

        else:
            self.data.update({id:texme(core=self.core, **kwargs)})


    def join(self, id=None, tex=None, clear=True):
        if type(id) in [str, tuple]:
            id = [id]

        elif type(id)==list:
            pass

        elif id==None:
            id = self.data.keys()

        if tex==None:
            tex = self.tex

        for name in id:
            if type(name)==tuple:
                self.data[name[0]].join(tex,mbuff=name[1])

            else:
                self.data[name].join(tex)

        if clear:
            tex.clear()


#$$$ ____________ def push _________________________________________________ #

    def push(self, id=None, active=None):
        '''
        Push method is connection of save and clear methods.
        '''
        if type(id)==str:
            id = [id]
        elif type(id)==list:
            pass
        elif id==None:
            id = self.data.keys()

        for name in id: self.data[name].push(active=active)

