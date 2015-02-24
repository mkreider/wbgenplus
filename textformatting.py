# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 10:35:39 2014

@author: mkreider
"""

def setColIndent(sLine, level, tabsize=3):
    if(sLine == ""):
        s = ""
    else:    
        ind = ' ' * (tabsize * level)        
        s = ind + sLine#s = sLine.lstrip(' ')    
    return s      

def i1(sLine, level, tabsize=3):
    return setColIndent(sLine, level, tabsize)
    
def setColsIndent(sLines, level, tabsize=3):
    l = []    
    for i in range(0, len(sLines)):    
        l.append(setColIndent(sLines[i], level, tabsize))    
    return l

def iN(sLines, level, tabsize=3):
    return setColsIndent(sLines, level, tabsize)

def getMaxBlockColByMark(sLines, cMark, tabsize):
    offs = 0
    for line in sLines:
        if(line.find(cMark) > offs):
            offs = line.find(cMark)
            
    alignedOffs = ((offs + tabsize - 1) // tabsize) * tabsize;        
    
    return alignedOffs 

def adjColByMark(sLine, cMark, offs):
    pos = sLine.find(cMark)
    if(pos > -1):
        ins = ' ' * (offs - pos)
        s = sLine[:pos] + ins + sLine[pos:]
    else:
        s = sLine
    return s

def adjBlockByMarks(sLines, cMarks, indentLvl, tabsize=3):
    l  = setColsIndent(sLines, indentLvl, tabsize)
    
    for mark in cMarks:
        offs    = getMaxBlockColByMark(l, mark, tabsize)
        for i in range(0, len(l)):    
            sLine = l[i]
            sLine = adjColByMark(sLine, mark, offs)   
            l[i] = sLine    
    
    return l

def mskWidth(msk):
    result  = 0
    if(msk != 0): 
        aux     = bin(msk).split('b')
        tmpmsk  = aux[-1];
        hiIdx   = len(tmpmsk)-1 - tmpmsk.find('1')        
        tmpmsk  = tmpmsk[::-1]
        loIdx   = tmpmsk.find('1')
        result  = [hiIdx, loIdx]
    else:
        result = [0, 0]    
    return result
    
def parseNumeral(num, default = None):
    result = default 
    if(num.find('0x') == 0):       
        base = 16
    elif(num.find('0b') == 0):
        base = 2  
    else:
        base = 10
    
    try:
        result = int(num, base)
    except ValueError:
        result = default
    return result

    
def commentStrings(commentSym, label1=''):
    commBoxCont0    = commentSym +"| %s" % label1
    commBoxCont1    = "|\n"
    commBoxLine     = commentSym + '+' + '*' * 90 + "+\n"    
    return [commBoxLine, commBoxCont0, commBoxCont1]    

def commentLine(commentSym, label1, label2):
    l = []
    (commBoxLine, commBoxCont0, commBoxCont1) = commentStrings(commentSym, label1)       
    d = len(commBoxLine) - (len(commBoxCont0) + len(label2) + 3 + 2)
    pad0 = d // 2 - len(label1)
    pad1 = d - pad0
    cont = commBoxCont0 + ' ' + ('-' * pad0) + ' ' + label2 + ' ' + ('-' * pad1) + commBoxCont1   
    l.append(cont)
    return l 

def commentBox(commentSym, label1, label2):
    l = []
    (commBoxLine, commBoxCont0, commBoxCont1) = commentStrings(commentSym, label1)
    l.append(commBoxLine)
    l += commentLine(commentSym, label1, label2)
    l.append(commBoxLine)
    return l        