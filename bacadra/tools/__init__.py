from .bsver import bsver
from .rootx import rootx
from .utile import utile

#$ class index
class index(rootx):
    #$$ __init__
    def __init__(self, core):
        self.core = core
        self.sub_init('utile', True)

    def sub_add_pattern(self, module):
        '''
        Return new object of submodule.
        '''
        if module=='utile':
            return utile(core=self.core)



#$ module definition

#$$ def translate
def translate(text, wordDict):
    '''
    Replace string by dict.
    '''

    # loop over keys in dict
    for key in wordDict:
        # replace text
        text = text.replace(str(key), str(wordDict[key]))

    # return modyfied text
    return text
