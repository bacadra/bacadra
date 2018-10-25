

#$ ____ class lcase ________________________________________________________ #

class lcase:
    #$$ def --init--
    def __init__(self, dbase, pinky, pvars):
        self.dbase = dbase
        self.pinky = pinky
        self.pvars = pvars

    #$$ def --enter--
    def __enter__(self):
        return self

    #$$ def --exit--
    def __exit__(self, type, value, traceback):
        pass

    def add(self, id=None, cates=None, fact=None, ttl=None):
        '''
        Add new load case to database. If lc already exists raise error. To modify value in db just use edit method.
        '''

    # TODO: behaviour in add funtion? delete old loads asgined to lcase?

    # TODO: in compare to sofistik, imho to apply dead load we should make special loads, like "special load" ("eg. nodal loads") wher we can apply load like dead load, wind, snow etcself. In modal analysis we can apply this load by default, but i think it is bad idea, we want provide soft fot more clever users.

    # TODO: add method should provide interface to modify coefficient gamu-psi etc. In DB now cols should be created.

        # overwrite last one defined lcase
        self.pvars.set({'_lcase_ldef':id})

        # if cates is not defined then use cat last one defined
        if cates is None:
            cates = self.pvars.get('_cates_ldef')

        # parse data
        cols,data = self.dbase.parse(
            id    = id,
            cates = cates,
            fact  = fact,
            ttl   = ttl,
        )

        # add data
        self.dbase.add(
            table = '[052:loads:lcase]',
            cols  = cols,
            data  = data,
        )

    def edit():
        pass

    def rem():
        pass

    def get():
        # TODO: orm here?
        # method should return object mapped special table of LC
        # probably is not easy to create realy nice conn ...
        pass

    def _clear():
        '''
        Clear depending loads while the replacement lc occure.
        '''
        pass