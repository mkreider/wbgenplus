# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 16:36:49 2015

@author: mkreider
"""
from stringtemplates import registerVhdlStr
from textformatting import mskWidth as mskWidth 

class register(object):

    def __init__(self, wbStr, pages, datawidth, addresswidth, name, desc, bigMsk, flags, clkbase="sys", clkdomain="sys", rstvec=None, startAdr=None, offs=4, genIntD=dict(), genMiscD=dict(), genPrefix='g_'):
        #print "Adding REgister %s to domain %s" % (name, clkdomain)        
        self.pages      = pages         
        self.dwidth     = datawidth
        self.awidth     = addresswidth       
        self.name       = name
        self.desc       = desc
        self.startAdr   = startAdr
        self.offs       = offs
        self.clkbase    = clkbase
        self.clkdomain  = clkdomain
        self.rstvec     = rstvec        
        self.flags      = flags
        self.width      = bigMsk
        self.genIntD    = genIntD
        self.genMiscD   = genMiscD
        self.genPrefix  = genPrefix
        if not self.isGenericWidth():
            self.width  = mskWidth(bigMsk)
        self.opList     = []
        self.v = registerVhdlStr(wbStr, self.name, self.desc, self.rstvec, self.getGenResetPrefix(), self.width,
                                 self.getGenWidthPrefix(), int(self.isPaged()) * self.pages, # 0 if this reg has no pages
                                 self.getGenPagePrefix(), self.clkdomain, self.clkbase)    
        
        adr = startAdr
        print "Reg %s Flags %s" % (self.name, self.flags)
        #add operations according to register flags
        if self.isAtomic():
            if self.isRead():
                self.addOp(adr, '_GET')
                adr = None 
            if self.isWrite():    
                self.addOp(adr, '_CLR')
                adr = None    
                self.addOp(adr, '_SET')
        else:
            if self.isRead() and self.isWrite():
                self.addOp(adr, '_RW ')
            elif self.isRead():    
                self.addOp(adr, '_GET')
            elif self.isWrite():
                self.addOp(adr, '_OWR')

    def isWrite(self):
        if(self.flags.find('w') > -1):
            return True
        return False
        
    def isRead(self):
        if(self.flags.find('r') > -1):
            return True
        return False
    
    def isDrive(self):
        if(self.flags.find('d') > -1):
            return True
        return False 
    
    def isPaged(self):
        if(self.flags.find('m') > -1):
            return True
        return False
        
    def isAtomic(self):
        if(self.flags.find('a') > -1):
            return True
        return False
        
    def isPulsed(self):
        if(self.flags.find('p') > -1):
            return True
        return False
        
    def hasEnableFlags(self):
        if(self.flags.find('f') > -1):
            return True
        return False
        
    def isStalling(self):
        if(self.flags.find('s') > -1):
            return True
        return False    

     

    def isGeneric(self):          
        return self.isGenericPaged() or self.isGenericWidth()
    
    def isGenericPaged(self):
        if self.isPaged():
            if(self.genIntD.has_key(self.pages)):
                return True
        return False  
        
    def isGenericWidth(self):
        if(self.genIntD.has_key(self.width)):
            return True
        return False    

    def isGenericReset(self):
        if(self.genIntD.has_key(self.rstvec)):
            return True
        return False     

    def getGenWidthPrefix(self):
        if self.isGenericWidth():
            return self.genPrefix
        return ""
        
    def getGenResetPrefix(self):
        if self.isGenericReset():
            return self.genPrefix
        return ""    
    
    def getGenPagePrefix(self):
        if self.isGenericPaged():
            return self.genPrefix
        return ""     

    def addOp(self, adr, op):
        adrList = []
        if adr == None:
            if len(self.opList) ==  0:
                adr = self.startAdr
            else:
                if len(self.opList) >  0:
                    adr = self.getLastAdr() + self.offs
                else:            
                    adr = adr + self.offs
        else:
            adr = (self.startAdr // self.offs) * self.offs          
       
        mskList = self.sliceMsk()
        #print "msk: %s %u" % (mskList, len(mskList))
        for msk in mskList:
            adrList.append([msk, adr])
            #print "Reg: %s msk: %s adr: %s offs: %s" % (self.name, msk, adr, self.offs)
            adr += self.offs
        self.opList.append([op, adrList])    

        
        
    def getLastAdr(self):
        if len(self.opList) >  0:
            (_, adrList) = self.opList[-1]
            (_, adr)     = adrList[-1]
            return adr
        else:            
            return self.startAdr
            
    def sliceMsk(self):
        mskList = []
        regWidth    = self.width
        if not self.isGenericWidth():
            words       = int(regWidth / self.dwidth)           
            for i in range(0, words):
                mskList.append(self.dwidth)                
                regWidth %= self.dwidth
        if(regWidth):
            mskList.append(regWidth)
        return (mskList)


    def getStrSignalDeclaration(self):
        s = []
        s.append(self.v.declarationReg)
        if self.isWrite():
            s += self.v.declarationSyncOutList #will only be generated if sync 
                 
        if self.isRead():
            s.append(self.v.declarationPortSigIn)
            s += self.v.declarationSyncInList #will only be generated if sync    
        
        s.append
        return s
    
    def getStrPortDeclaration(self):
        s = []
        if self.isWrite():
            s.append(self.v.declarationPortOut)
            if self.hasEnableFlags():
                s.append(self.v.portWEOut)
                 
        if self.isRead():
            if self.hasEnableFlags():
                s.append(self.v.portRDOut)

        if self.isDrive():
            s.append(self.v.declarationPortIn)
                
        return s             
    
            
    
    def getStrPortAssignment(self):
        s = []
        if self.isWrite():
            s += self.v.portAssignOutList
        if self.isDrive():
            s += self.v.portAssignInList
        return s        

            
    def getStrReset(self):
        s = []
                
        if self.hasEnableFlags():
            if self.isRead():
                s.append(self.v.wbRdZero) 
            if self.isWrite():
                s.append(self.v.wbWeZero)
                
        s.append(self.v.reset)
        
        return s


    def getStrReadUpdate(self):
        s = []        
        
        if self.isDrive():
            s.append(self.v.readUpdate)
        return s 

    def getStrPulsed(self):
        s = []        
        
        if self.isWrite():
            if self.isPulsed():
                s.append(self.v.wbPulseZero)
            if self.hasEnableFlags():
                s.append(self.v.wbWeZero)
        if self.isRead() and self.hasEnableFlags():
            s.append(self.v.wbRdZero)        
        
        return s       
    
    def getStrAddress(self, language="VHDL"):
        adrC = ""         
        adrV = "constant c_%s_%s : natural := 16#%s#;\n"            
        
        s = []
        adrHi = self.getLastAdr()
        idxHi = mskWidth(adrHi) -1
        adrx = ("%0" + str((idxHi+1+3)/4) + "x")
        mskx = ("0x%0" + str(self.dwidth/4) + "x")
        
        opIdx = 0            
        for opLine in self.opList:
            (op, adrList) = opLine
            if(op.find('_GET') > -1):
                rw = 'ro'
            elif (op.find('_SET') > -1) or (op.find('_CLR') > -1) or (op.find('_OWR') > -1):
                rw = 'wo'    
            elif(op.find('_RW') > -1):
                rw = 'rw'
                
            adrIdx = 0
            for adrLine in adrList:
                #if this reg has multiple words, add the index to the name                    
                if(len(adrList) > 1):                
                    idx = '_%u' % adrIdx
                else:
                    idx = ''
                (msk, adr) = adrLine
                
                if(self.genIntD.has_key(msk)):
                    bitmask = "g_%s" % msk
                else:
                    bitmask = mskx % int(2**msk-1)
                if(language == "C"):
                    s.append(adrC % (self.slaveIf, self.name + op + idx, adrx % adr))
                else:    

                    s.append(self.v.constRegAdr % (op + idx, adrx % adr))
                
                adrIdx += 1
            opIdx += 1
        
        return s        
        
    def getStrInterfaceDoc(self, adressNibbles):
        doc = "0x%s %s %s_%s : %s -> %s\n" #adr, rw, name_operation_(idx), bitwidth, description           
        
        s = []
        adrx = ("%0" + str(adressNibbles) + "x")       
        
        opIdx = 0            
        for opLine in self.opList:
            (op, adrList) = opLine
            if(op.find('_GET') > -1):
                rw = 'ro'
            elif (op.find('_SET') > -1) or (op.find('_CLR') > -1) or (op.find('_OWR') > -1):
                rw = 'wo'    
            elif(op.find('_RW') > -1):
                rw = 'rw'
                
            adrIdx = 0
            for adrLine in adrList:
                #if this reg has multiple words, add the index to the name                    
                if(len(adrList) > 1):                
                    idx = '_%u' % adrIdx
                else:
                    idx = ''
                (msk, adr) = adrLine
                #Show comment only the first occurrance of a register name                    
                if((opIdx == 0) and (adrIdx == 0)):
                    comment = self.desc
                else:
                    comment = '\"\"'
                
                if(self.genIntD.has_key(msk)):
                    bitmask = "g_%s" % msk
                else:
                    bitmask = msk
                s.append(doc % (adrx % adr, rw, self.slaveIf, self.name + op + idx, bitmask, comment))
                
                adrIdx += 1
            opIdx += 1
        
        return s    
            

        
    def getStrFsmRead(self):
       
             
        s = []    
        
        for opLine in self.opList:
            (op, adrList) = opLine
            if((op == "_GET") or (op == "_RW ")):                    
                #this is sliced
                
                    
                
                adrIdx = 0            
                for adrLine in adrList:
                    (msk, adr) = adrLine
                    
                    sliceWidth       = msk
                    if self.isGenericWidth():
                        curSlice         = "%s downto %u" % (self.getGenWidthPrefix() + sliceWidth + "-1", 0)
                        baseSlice        = "%s downto %u" % (self.getGenWidthPrefix() + sliceWidth + "-1", 0) 
                    else:        
                        curSliceHigh     = sliceWidth + adrIdx*self.dwidth -1
                        curSliceLow      = adrIdx*self.dwidth
                        curSlice         = "%u downto %u" % (curSliceHigh, curSliceLow)
                        baseSlice        = "%u downto %u" % (sliceWidth-1, 0)
                        
                                        
                    regSlice         = ""    
                    enum = ""
                    
                    if len(adrList) > 1:
                        regSlice         = "(%s)" % curSlice
                        enum = "_%s" % adrIdx
                    adrIdx += 1
                    s.append(self.v.wbRead % (op + enum, baseSlice, regSlice))
                    
                if self.isStalling():             
                    s.append(self.v.wbStall % self.name)    
        return s

    def getStrFsmWrite(self):
        s = []    
        
        opIdx = 0    
        for opLine in self.opList:
            (op, adrList) = opLine
            adrIdx = 0
            if(op != "_GET"):                    
               
                #this is sliced
                adrIdx=0            
                for adrLine in adrList:
                    (msk, adr) = adrLine
                    sliceWidth       = msk 
                    if self.isGenericWidth():
                        curSlice         = "%s downto %u" % (self.getGenWidthPrefix() + sliceWidth + "-1", 0) 
                    else:        
                        curSliceHigh     = sliceWidth + adrIdx*self.dwidth -1
                        curSliceLow      = adrIdx*self.dwidth
                        curSlice         = "%u downto %u" % (curSliceHigh, curSliceLow)
                    regSlice         = ""
                    enum = ""
                    if len(adrList) > 1:
                        regSlice         = "(%s)" % curSlice
                        enum = "_%s" % adrIdx
                    adrIdx += 1
                   
                    s.append(self.v.wbWrite % (op + enum, regSlice, regSlice, registerVhdlStr.wrModes[op]))
                
                if self.hasEnableFlags() and self.isWrite:
                    s.append(self.v.wbWe)
                if self.isStalling():             
                    s.append(self.v.wbStall)     
                opIdx += 1
        return s  
    
class internalregister(register):
    def __init__(self, wbStr, pages, name, desc, bigMsk, flags, clkbase="sys", clkdomain="sys", rstvec=None, genIntD=dict(), genMiscD=dict()):
        print "Adding internal Register %s" % name        
        self.pages      = pages         
        self.name       = name
        self.desc       = desc
        self.clkbase  = clkbase
        self.clkdomain  = clkdomain
        self.rstvec     = rstvec        
        self.flags     = flags
        self.width      = mskWidth(bigMsk)
        self.opList     = []
        self.genIntD    = genIntD
        self.genMiscD   = genMiscD
        if not self.isGenericWidth():
            self.width  = mskWidth(bigMsk)
        self.v = registerVhdlStr(wbStr, self.name, self.desc, self.rstvec, self.getGenResetPrefix(), self.width, self.getGenWidthPrefix(), int(self.isPaged()) * self.pages, # 0 if this reg has no pages
                                 self.getGenPagePrefix(), self.clkdomain, self.clkbase)          
    
  
    
    def getLastAdr(self):
        pass 
       
    def getStrAddress(self, language="VHDL"):
        return []      
            
    def getStrFsmRead(self):
        return []

    def getStrFsmWrite(self):
        return []   

    def getStrInterfaceDoc(self, addressNibbles):
        return []
        
    def getStrReadUpdate(self):
        return []