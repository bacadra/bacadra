import shutil
import datetime
import os


from ..cunit.units import cunit



#$ ____ class baclup _______________________________________________________ #

class bsv:
    '''
    bacadra.tools.bsv
    =================
    bacadra system version
    ----------------------
    '''

    def __init__(self, source='.', destination='backup', description=None, exclude=[''], name=None, active=True, gitignoreQ=True, dtime=cunit(0, 's'), id=None):
        self.active      = active
        self.source      = source
        self.destination = destination
        self.description = description
        self.exclude     = exclude
        self.name        = name
        self.gitignoreQ  = gitignoreQ
        self.dtime       = dtime
        self.id          = id

        self.exclude += [destination]
        self.timer(self.dtime)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, name):
        if name:
            name = '_' + str(name)
        else:
            name = ''
        self._id = '.bup' + name


    def nameF(self):
        name = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

        if self.name == None:
            if self.source == '.':
                name += '_root'
            else:
                name += '_' + os.path.basename(self.source).split('.')[0]
        else:
            name += '_' + self.name
        if self.description:
            name += '_' + self.description
        return name

    def gitignoreM(self):
        if os.path.isfile('.gitignore'):
            with open('.gitignore') as f:
                gitignore = f.readlines()
            self.exclude = self.exclude + gitignore

    def backup(self):
        if self.gitignoreQ:
            self.gitignoreM()
        dpath = os.path.join(self.destination, self.nameF())
        Ignore = shutil.ignore_patterns(*self.exclude)
        shutil.copytree(self.source, dpath, ignore=Ignore)

    def timer(self, DeltaTime):
        if DeltaTime.drop('s') == 0:
            return None
        if self.active:
            tcontrol = os.path.join(self.destination, self._id)
            if os.path.exists(tcontrol):
                f = open(tcontrol)
                tlast = eval(f.readline())
                f.close()
            else:
                tlast = datetime.datetime(2000,1,1)

            tnow = datetime.datetime.now()
            tdelta = tnow - tlast
            if tdelta.total_seconds() >= DeltaTime.drop('s'):
                self.backup()
                f = open(tcontrol, 'w')
                str1 = 'datetime.datetime(' + str(tnow.year) + ',' + str(tnow.month) + ','+str(tnow.day) + ','+str(tnow.hour) + ','+str(tnow.minute) + ','+str(tnow.second) + ')'
                f.writelines(str1)
                f.close()
