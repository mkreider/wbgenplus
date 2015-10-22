# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 16:51:23 2015

@author: mkreider
"""
import math
from register import register
from register import internalregister
from stringtemplates import wbsVhdlStrGeneral
from stringtemplates import wbsVhdlStrRegister
from stringtemplates import wbsCStr
 

from textformatting import beautify as adj
from textformatting import setColsIndent as iN
from textformatting import commentLine as cline
from textformatting import commentBox as cbox


class wbslave(object):
    def __init__(self, unitname, version, date, slaveIfName, startaddress, selector, pages, ifwidth, sdbVendorID, sdbDeviceID, sdbname, clocks, genIntD, genMiscD, genPrefix):    
                
        self.unitname       = unitname
        self.version        = version        
        self.date           = date
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
        #Fill in string templates
        self.genIntD    = genIntD
        self.genMiscD   = genMiscD
        self.genPrefix  = genPrefix
        self.v          = wbsVhdlStrGeneral(unitname, slaveIfName, ifwidth, sdbVendorID, sdbDeviceID, sdbname, clocks, version, date, selector)
        self.vreg       = wbsVhdlStrRegister(slaveIfName)
        self.c          = wbsCStr(pages, unitname, slaveIfName, sdbVendorID, sdbDeviceID)
        
        self.stallReg   = self.createIntReg(self.name + "_stall", "flow control", "1", "d", self.clocks[0], 0)
        self.addIntReg(self.stallReg)  
        
                  
    def addReg(self, name, desc, bigMsk, flags, clkdomain="sys", rstvec=None, startAdr=None):
                                        #wbStr, pages, datawidth, addresswidth, name, desc, bigMsk, flags, clkbase="sys", clkdomain="sys", rstvec=None, startAdr=None, offs=4, genIntD=dict(), genMiscD=dict()):
        self.registers.append(register(self.vreg, self.pages, self.dataWidth, self.addressWidth, name, desc, bigMsk, flags,
                                       self.clocks[0], clkdomain, rstvec, self.getAddress(startAdr), self.offs, self.genIntD, self.genMiscD))    
        
    def createIntReg(self, name, desc, bigMsk, flags, clkdomain="sys", rstvec=None):
        return internalregister(self.vreg, self.pages, name, desc, bigMsk, flags, self.clocks[0], clkdomain, rstvec, self.genIntD, self.genMiscD)    
    
    def addIntReg(self, intreg):    
        self.registers.append(intreg)    
    
    def getGenPrefix(self):
        return self.genPrefix
    
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
            s += reg.getStrAddress("C")
        return s    
        
    def getAddressListVHDL(self):
        s = []        
        for reg in self.registers:
            s += reg.getStrAddress("VHDL")
        return s       

    def getAssignmentList(self):
        s = []
        for reg in self.registers:
            s += reg.getStrPortAssignment()
        #generate flow control code
        s.append("\n")
        s.append(self.v.wbsStall0)
#        for line in self.v.wbsStall1:
#            s.append(line % (self.stallReg.v.regname, self.stallReg.v.portsignamein))
#        s += self.v.wbsDat
#        for line in self.v.wbsErr:
#            s.append(line % self.errReg.v.portsignamein)    
        
        return adj(s, ['<=', "--"], 1)
    
    def getGenericList(self):
        tmp = []
        s = []
        for key in self.genIntD:
            (gtype, default, description) = self.genIntD[key] 
            tmp.append(wbsVhdlStrGeneral.generic % (self.getGenPrefix()+key, gtype, default, description))
        for line in tmp[:-1]:
            s.append(line % ";") 
        s.append(tmp[-1] % "")
        return adj(s, [':', ':=', '--'], 1)     

    
    def getPortList(self):
        s = []
        
        t = []
        
        sortedregs = sorted(self.registers, key=lambda x: (x.clkdomain, x.isWrite(), x.name), reverse=False)
        regold = sortedregs[0]        
        for reg in sortedregs:
            
            if( (regold.clkdomain != reg.clkdomain) or ( regold.isWrite() != reg.isWrite() )):
                t.append("\n")
            regold = reg
            s += reg.getStrPortDeclaration()
        s += self.v.slaveIf    
        s += t
        return adj(s, [':', ':=', '--'], 1)

    def getDeclarationList(self):
        s = []
                
        for reg in self.registers:
            s += reg.getStrSignalDeclaration()
        return adj(s, [' is ', ':', ':=', '--'], 1) 
        
        
    def getReadUpdateList(self):
        s = []        
        for reg in self.registers:
            s += reg.getStrReadUpdate()
        return s 
        

    def getResetList(self):
        s = []        
        for reg in self.registers:
            s += reg.getStrReset()
        return s        
        
        
    def getPulsedList(self):
        s = []        
        for reg in self.registers:
            s += reg.getStrPulsed()
        return s         
          

    def getFsmReadList(self):
        s = []        
        for reg in self.registers:
            s += reg.getStrFsmRead()
        return s         
        
            
    def getFsmWriteList(self):
        s = []        
        for reg in self.registers:
            s += reg.getStrFsmWrite()
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
        stall   = iN(self.v.wbsStall1 % self.stallReg.v.portsignamein, 4)
        pulsed  = adj(self.getPulsedList(), ['<=', '--'], 4)
        update  = adj(self.getReadUpdateList(), ['<=', '--'], 4)
        psel    =  iN(self.getPageSelect(), 4)
        hdr2    =  iN(self.v.wbs2, 4)  
        writes  = adj(self.getFsmWriteList(), ['=>', '<=', 'v_dat_i', "--"], 7)    
 
        mid0    =  iN(self.v.wbOthers, 7)
        mid1    =  iN(self.v.wbs3, 5)
        reads   = adj(self.getFsmReadList(), ['=>', '<=', "--"], 7)
        ftr     =  iN(self.v.wbs4, 1)
        
        
        
        s += (hdr0 + rst + hdr1 + stall + pulsed + update + psel +  hdr2 + writes + mid0 + mid1 + reads + mid0 + ftr)
        return s
    
   
    def getStrSDB(self):
        s = []
        s += self.v.sdb       
        return s 
        
    def getPageSelect(self):
        if(self.selector == ""):
            return ["\n"]
        else:    
            return [self.v.wbsPageSelect % self.selector]
            
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
        s += cbox(mark,"Register map", self.sdbname)
        s.append(mark + " " + sAdr + ' ' * ((len(sHex)+nibbles)+1 - len(sAdr)) + "D  Name : Width -> Comment\n")
        s.append(mark + '-' * 92 + '\n')
        
        for reg in self.registers:
            docList = reg.getInterfaceDocStrings(nibbles)            
            for line in docList:
                s.append("-- " + line)
        s.append('\n')        
        return s
        
