# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 10:35:39 2014

@author: mkreider
"""
import math

_TAB_SIZE_ = 3

def is_sequence(arg):
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))

def srepr(arg):
    if is_sequence(arg):
        return "\n".join(srepr(x) for x in arg)
    return arg

def setColIndent(sLine, level, tabsize=_TAB_SIZE_):
    #provide a solution for list
    line = ""
    s = ""    
    if(is_sequence(sLine)):    
        #print sLine        
        for line in sLine:
            setColIndent(line, level, tabsize)
    else:
        line += sLine
        #print "line = %s" % line
        #if(line != ""):
        ind = ' ' * (tabsize * level)        
        s = ind + line    
    return s      

  
def setColsIndent(sLines, level, tabsize=_TAB_SIZE_):
    l = []
    if(is_sequence(sLines)):    
        for i in range(0, len(sLines)):    
            l.append(setColIndent(sLines[i], level, tabsize))
    else:
         l.append(setColIndent(sLines, level, tabsize))       
    return l

def getMaxBlockColByMark(sLines, cMark, tabsize=_TAB_SIZE_, offs=0):
    for line in sLines:
        if(is_sequence(line)):
           #print "seq"     
           offs = getMaxBlockColByMark(line, cMark, tabsize, offs)
        else:   
            #print line            
            if(line.find(cMark) > offs):
                offs = line.find(cMark)
    
    
        
    alignedOffs = ((offs + tabsize - 1) // tabsize) * tabsize;        
    
    return alignedOffs 

def adjColByMark(sLine, cMark, offs):
    s = []    
    if(is_sequence(sLine)):
       #print "seq"    
       s += sLine 
       for i in range(0, len(sLine)):    
            s[i] = adjColByMark(s[i], cMark, offs)   
       return s
    else:
                    
        pos = sLine.find(cMark)
        if(pos > -1):
            ins = ' ' * (offs - pos)
            s = sLine[:pos] + ins + sLine[pos:]
        else:
            s = sLine
        #print "A: %s" % s     
        return s

def adjBlockByMarks(sLines, cMarks, tabsize=_TAB_SIZE_):
    l = []
    l += sLines    
    for mark in cMarks:
        offs    = getMaxBlockColByMark(l, mark, tabsize)
        for i in range(0, len(l)):    
            sLine = l[i]
            sLine = adjColByMark(sLine, mark, offs)   
            l[i] = sLine    
      
    return l
    
def beautify(sLines, cMarks, indentLvl, tabsize=_TAB_SIZE_):
    l = []    
    
    l   += adjBlockByMarks(sLines, cMarks, tabsize)
    #print "*!*"    
    #print "l: %s" % l
    l   = setColsIndent(l, indentLvl, tabsize)
    #print "*!!*"    
    #print "l: %s" % l
    return l

def mskWidth(msk):
    result  = 0
    inp = str(msk)
    if(inp != 0):
        aux     = parseNumeral(inp)
        if(aux > 1):
            width = (math.ceil(math.log( aux) / math.log( 2 )))
        else:
            width = 1
        print "Breite: %s, inout %s" % (width, aux)
        result  = int( width)
    else:
        result = 0    
    return result
    
def parseNumeral(num, default = None):
    result = default
    x = str(num)
    if(x.find('0x') == 0):       
        base = 16
    elif(x.find('0b') == 0):
        base = 2  
    else:
        base = 10
    
    try:
        result = int(x, base)
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