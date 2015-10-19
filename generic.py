# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/mkreider/.spyder2/.temp.py
"""
from xml.dom import minidom
import datetime
import textformatting
import os.path
import sys
import getopt
import math
import pdb

myVersion = "0.3"
myStart   = "15 Dec 2014"
myUpdate  = "10 Jan 2015"
myCreator = "M. Kreider <m.kreider@gsi.de>"


is_seq      = textformatting.is_sequence
i1          = textformatting.setColIndent
iN          = textformatting.setColsIndent    
adj         = textformatting.beautify
mskWidth    = textformatting.mskWidth
str2int     = textformatting.parseNumeral
commentLine = textformatting.commentLine
commentBox  = textformatting.commentBox
now = datetime.datetime.now()

class generic(object):

    def __init__(self, name, gtype, default, desc):
        self.name       = name
        self.vname      = "g_" + self.name 
        self.gtype      = gtype
        self.desc       = desc
        self.default    = default
        
        def getGenericEntityStrings(self):
            gen        = "%s : %s := %s -- %s\n"  % ( self.vname, self.gtype, self.default, self.desc)     
            return gen