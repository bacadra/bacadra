#!/usr/bin/python
#-*-coding: UTF-8-*-
from .bsv import bsv

#$ ____ import _____________________________________________________________ #



#$ ____ function ___________________________________________________________ #
#$$ ________ def translate _________________________________________________ #

def translate(text, wordDict):
    '''Replace string by dict'''
    for key in wordDict:
        text = text.replace(str(key), str(wordDict[key]))
    return text
    # return text.format(**wordDict)
