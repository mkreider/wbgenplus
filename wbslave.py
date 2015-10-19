# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 16:51:23 2015

@author: mkreider
"""
from register import * 


class wbslave(object):
    def __init__(self, unitname, slaveIfName, startaddress, selector, pages, ifwidth, sdbVendorID, sdbDeviceID, sdbname, clocks, genIntD, genMiscD):    
                
        self.unitname       = unitname
        self.name           = slaveIfName
        self.dataWidth      = ifwidth
        self.addressWidth   = 32
        self.clocks         = clocks  
        self.pages          = pages
        self.selector       = selector
        self.registers      = []
        self.startaddress   = startaddress
        self.sdbVendorID    = sdbVendorID
        self.sdbDeviceID    = sdbDeviceID
        self.sdbname        = sdbname        
        self.offs           = int(math.ceil(ifwidth/8))
        self.v = wbsVhdlStr(pages, unitname, slaveIfName, ifwidth, sdbVendorID, sdbDeviceID, sdbname, clocks)        
        self.c = wbsCStr(pages, unitname, slaveIfName, sdbVendorID, sdbDeviceID)
        self.addIntReg("wb_stall", "flow control", "1", "r")
        self.addIntReg("wb_err", "signal unsuccessful wb op", "1", "r")      
        
        
        
    def addReg(self, name, desc, bigMsk, flags, clkdomain="sys", rstvec=None, startAdr=None):
        self.registers.append(register(self.name, self.pages, self.dataWidth, self.addressWidth, name, desc, bigMsk, flags, self.clocks[0], clkdomain, rstvec, self.getAddress(startAdr), self.offs))    
        
    def addIntReg(self, name, desc, bigMsk, flags, clkdomain="sys", rstvec=None):
        self.registers.append(internalregister(self.name, self.pages, name, desc, bigMsk, flags, self.clocks[0], clkdomain, rstvec))    
    
    def getAddress(self, startAdr=None):
        regList = self.registers
        lastadr = 0
      
        if len(regList) > 0:        
            for reg in regList[::-1]:            
                if(reg.getLastAdr() != None):
                    lastadr = reg.getLastAdr()
                    break        
            if(startAdr):
                if(startAdr >= lastadr + self.offs):
                    return startAdr
                else:
                    print "ERROR: Wrong address specified for Register %s_%s: %08x must be greater %08x!" % (self.name, reg.name, int(startAdr), int(lastadr) + int(reg.offs))
                    exit(2)
            else:
                #find the last valid address (skip internal registers)
                return lastadr + self.offs
        else:
            if(startAdr):
                return startAdr
            return self.startaddress    
    
    def getLastAddress(self):
        regList = self.registers
        lastadr = self.startaddress
      
        if len(regList) > 0:
            for reg in regList[::-1]:            
                if(reg.getLastAdr() != None):
                    lastadr = reg.getLastAdr()
                    break        
        
        return lastadr    
    
    def getAddressListC(self):
        s = []        
        for reg in self.registers:
            s += reg.getAdrStrings("C")
        return s
        
    def getAddressListVHDL(self):
        s = []        
        for reg in self.registers:
            tmp = reg.getAdrStrings("VHDL")
            if is_seq(tmp):
                for line in tmp:
                    s.append(line)
            else:
                s.append(tmp)
        return s       
    
    def getInterfacePortList(self):
        return None    
        
    def getRegisterPortList(self):
        s = []
        s += self.v.slaveIf
        t = []
        
        sortedregs = sorted(self.registers, key=lambda x: (x.clkdomain, x.isWrite(), x.name), reverse=False)
        regold = sortedregs[0]        
        for reg in sortedregs:
            
            if( (regold.clkdomain != reg.clkdomain) or ( regold.isWrite() != reg.isWrite() )):
                t.append("\n")
            regold = reg
            tmp = reg.getPortStrings()
            if is_seq(tmp):
                for line in tmp:
                    t.append(line)
            else:
                t.append(tmp)  
        
        s += t
        return s

    def getRegisterDefinitionList(self):
        s = []        
        for reg in self.registers:
            tmp = reg.getRegisterStrings()
            
            if is_seq(tmp):
                for line in tmp:
                    s.append(line)
            else:
                s.append(tmp)
        
        return s

#    def getRegisterTypeList(self):
#        s = []        
#        for reg in self.registers:
#            tmp = reg.getTypeStrings()
#            
#            if is_seq(tmp):
#                for line in tmp:
#                    s.append(line)
#            else:
#                s.append(tmp)    
#        return s

    def getResetList(self):
        s = []        
        for reg in self.registers:
            tmp = reg.getResetStrings()
            
            if is_seq(tmp):
                for line in tmp:
                    s.append(line)
            else:
                s.append(tmp)
        return s
        
    def getPulsedList(self):
        s = []        
        for reg in self.registers:
            tmp = reg.getPulsedStrings()
            
            if is_seq(tmp):
                for line in tmp:
                    s.append(line)
            else:
                s.append(tmp)
        return s    

    def getFsmReadList(self, showComment=False):
        s = []        
        for reg in self.registers:
            tmp = reg.getFsmReadStrings(showComment)
            
            if is_seq(tmp):
                for line in tmp:
                    s.append(line)
            else:
                s.append(tmp)
        return s
            
    def getFsmWriteList(self, showComment=False):
        s = []        
        for reg in self.registers:
            tmp = reg.getFsmWriteStrings(showComment)
            if is_seq(tmp):
                for line in tmp:
                    s.append(line)
            else:
                s.append(tmp)
        return s
    
    def getFsmList(self, showComment=False):
        s = []
        
        hiAdr = self.getLastAddress()
        #if there's only a single register, hiAdr would be 0. Doesnt work with log2, change to highest non-aligned value 
        if(hiAdr == 0):
           msbIdx = 0
        else:   
            msbIdx = (math.ceil(math.log( hiAdr ) / math.log( 2 )))
        lsbIdx = (math.ceil(math.log( self.dataWidth/8 ) / math.log( 2 )))
        if lsbIdx > 0:
            padding = '& "%s"' % ('0' * int(lsbIdx))
        else:
            padding = ''
        adrMsk = 2**msbIdx-1 
        print "%s" % ('*' * 80) 
        print "Slave <%s>: Found %u register names, last Adr is %08x, Adr Range is %08x, = %u downto %u\n" % (self.name, len(self.registers), hiAdr, adrMsk, msbIdx-1, lsbIdx)
        print "\n%s" % ('*' * 80) 
        
        hdr0    =  iN(self.v.wbs0, 1) 
        rst     = adj(self.getResetList(), ['<='], 4)         
        hdr1    =  iN(self.v.wbs1_0 + [self.v.wbs1_adr % (msbIdx-1, lsbIdx, padding)] + self.v.wbs1_1, 3)
        pulsed  = adj(self.getPulsedList(), ['<=', '--'], 4)        
        psel    =  iN(self.getPageSelectStrings(), 4)
        hdr2    =  iN(self.v.wbs2, 4)  
        writes  = adj(self.getFsmWriteList(showComment), ['=>', '<=', 'v_dat_i', "--" if showComment else ""], 7)    
 
        mid0    =  iN(self.v.wbOthers, 7)
        mid1    =  iN(self.v.wbs3, 5)
        reads   = adj(self.getFsmReadList(showComment), ['=>', '<=', "--" if showComment else ""], 7)
        ftr     =  iN(self.v.wbs4, 1)
        con     = adj(self.v.wbs5, ['<=', "--"], 1)
        
        s += (hdr0 + rst + hdr1 + pulsed + psel +  hdr2 + writes + mid0 + mid1 + reads + mid0 + ftr + con)
        return s
    
       
    def getInstanceList(self):     
        s = []        
        for reg in self.registers:
            tmp = reg.getInstanceStrings()
            if is_seq(tmp):
                for line in tmp:
                    s.append(line)
            else:
                s.append(tmp)
        return s
        
    def getPageSelectStrings(self):
        if(self.selector == ""):
            return "\n"
        else:    
            return self.v.wbsPageSelect % self.selector
            
    def getDocList(self, language):
        if language == "VHDL":
           mark = "--"     
        elif language == "C":
            mark = "//"
        else:
            mark = ""
            
        adrHi = "%x" % self.getLastAddress()
        nibbles = len(adrHi)
        sHex = "0x"
        sAdr = "Adr"        
        
        s = []
        s += commentBox(mark,"Register map", self.sdbname)
        s.append(mark + " " + sAdr + ' ' * ((len(sHex)+nibbles)+1 - len(sAdr)) + "D  Name : Width -> Comment\n")
        s.append(mark + '-' * 92 + '\n')
        
        for reg in self.registers:
            docList = reg.getInterfaceDocStrings(nibbles)            
            for line in docList:
                s.append("-- " + line)
        s.append('\n')        
        return s
        
