

class BCDRsofixError(Exception):
    pass

def envcheckBCDRsofixError(path):
    raise BCDRsofixError('enviroment does not exists! path: ' + path)

def cdbcheckBCDRsofixError(path):
    raise BCDRsofixError('.cdb does not exists! path: ' + path)

def gracheckBCDRsofixError(path):
    raise BCDRsofixError('.gra does not exists! path: ' + path)