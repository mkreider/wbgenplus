# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 16:51:23 2015

@author: mkreider
"""
import math
from register import Register
from register import WbRegister
from stringtemplates import wbsVhdlStrGeneral
from stringtemplates import wbsVhdlStrRegister
from stringtemplates import wbsCStr


from textformatting import beautify as adj
from textformatting import setColsIndent as iN
#from textformatting import commentLine as cline
from textformatting import commentBox as cbox


class wbslave(object):
    def __init__(self, unitname, version, date, slaveIfName, startaddress, selector, pages, ifwidth, sdbVendorID, sdbDeviceID, sdbname, clocks, genIntD, genMiscD, genPrefix):

        # pylint: disable=too-many-instance-attributes

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

        #create flow control 
        tmpReg = self._createWbReg(self.name + "_stall", "flow control", "1", "d", self.clocks[0], 0)
        tmpStrD = {'set'    : [self.v.wbsStall1 % (tmpReg.v.regname, tmpReg.v.regname, tmpReg.v.portsignamein)],
                   'assign' : [self.v.wbsStall0 % tmpReg.v.regname],
                   }
        tmpReg.setCustomStrDict(tmpStrD)
        self.stallReg = self._addReg(tmpReg)
       



    def _createWbReg(self, name, desc, bits, flags, clkdomain="sys", rstvec=None, startAdr=None):
        return WbRegister(self.dataWidth, self.addressWidth, self._getAddress(startAdr, name), self.offs,
                          self.vreg, self.genIntD, name, desc, flags, bits, rstvec, self.pages, self.clocks[0], clkdomain)



    def _createIntReg(self, name, desc, bits, flags, clkdomain="sys", rstvec=None):
        return Register(self.vreg, self.genIntD, name, desc, flags, bits, rstvec, self.pages, self.clocks[0], clkdomain)


    def addWbReg(self, name, desc, bits, flags, clkdomain="sys", rstvec=None, startAdr=None):
        
        #dummy so the int regs don't mess with
        tmpIntStrD = {'assign'  : [""]}
        customStrD = {'read'    : [],
                      'write'   : []}
                      
        
        reg = self._createWbReg(name, desc, bits, flags, clkdomain, rstvec, startAdr)
        
        #check for flags
        print "reg %s has %s" % (name, flags)
        if reg.hasEnableFlags():
            if reg.isWrite():
                
                tmpReg = self._createIntReg(reg.name + "_WR", "Write enable flag", "1", "wp", reg.clkdomain, 0)
                tmpReg.setCustomStrDict(tmpIntStrD) # prevent it from doing its own port assignment
                self._addReg(tmpReg)
                customStrD['write'] += [tmpReg.v.setHigh]
                
            if reg.isRead():
                tmpReg = self._createIntReg(reg.name + "_RD", "Read enable flag", "1", "wp", reg.clkdomain, 0)
                tmpReg.setCustomStrDict(tmpIntStrD) # prevent it from doing its own port assignment
                self._addReg(tmpReg)
                customStrD['read'] += [tmpReg.v.setHigh]
        if reg.isStalling():
            customStrD['read']  += [self.stallReg.v.setHigh]
            customStrD['write'] += [self.stallReg.v.setHigh]            
        
        
        reg.setCustomStrDict(customStrD)
        self._addReg(reg)
        return reg
        
    def addIntReg(self, name, desc, bits, flags, clkdomain="sys", rstvec=None):
         intreg = self._createIntReg(name, desc, bits, flags, clkdomain, rstvec)
         return self._addReg(intreg)

    def _addReg(self, reg):
         self.registers.append(reg)
         return reg

    def _getGenPrefix(self):
        return self.genPrefix

    def _getAddress(self, startAdr=None, regname=""):
        lastadr = self._getLastAddress()
        if(lastadr is not None):
            if startAdr is not None:
                if(startAdr >= lastadr + self.offs):
                    return startAdr
                else:
                    print "ERROR: Wrong address specified for Register %s: %08x must be greater %08x!" % (regname, int(startAdr), int(lastadr) + int(self.offs))
                    exit(2)
            else:
                #find the last valid address (skip internal registers)
                return lastadr + self.offs
        else:
            if(startAdr is not None):
                return startAdr
            return self.startaddress

    def _getLastAddress(self):
        regList = self.registers
        lastadr = None

        if len(regList) > 0:
            for reg in regList[::-1]:
                if(reg.getLastAdr() != None):
                    lastadr = reg.getLastAdr()
                    break

        return lastadr

    def getStubSignalList(self):
        s = []
        for reg in self.registers:
            s += reg.getStrStubDeclaration()
        #generate flow control code
        s.append("\n")
        return adj(s, [':', ':=', '--'], 1)

    def getStubInstanceList(self):
        s = []

        for clock in self.clocks:
            tmpClk = wbsVhdlStrGeneral.clkportname % (clock)
            tmpRst = wbsVhdlStrGeneral.rstportname % (clock)
            s.append(wbsVhdlStrGeneral.assignStub % (tmpClk, tmpClk))
            s.append(wbsVhdlStrGeneral.assignStub % (tmpRst, tmpRst))

        for reg in self.registers:
            s += reg.getStrStubInstance()
        s += self.v.slaveInst
        return adj(s, ['=>'], 1)


    def getAddressListPython(self):
        s = []
        for reg in self.registers:
            s += reg.getStrAddress("python")
        return adj(s, [':'], 0)

    def getAddressListC(self):
        s = []
        for reg in self.registers:
            s += reg.getStrAddress("C")
        return adj(s, ['0x', '//'], 1)

    def getAddressListVHDL(self):
        s = []
        for reg in self.registers:
            s += reg.getStrAddress("VHDL", self._getLastAddress())
        return adj(s, [':', ':=', '--'], 1)

    def getAssignmentList(self):
        s = []
        for reg in self.registers:
            s += reg.getStrPortAssignment()
        #generate flow control code
        

        return adj(s, ['<=', "--"], 1)

    def getGenericList(self):
        tmp = []
        s = []
        for key in self.genIntD:
            (gtype, default, description) = self.genIntD[key]
            tmp.append(wbsVhdlStrGeneral.generic % (self._getGenPrefix()+key, gtype, default, description))
        if len(tmp):
            for line in tmp[:-1]:
                s.append(line % ";")
            s.append(tmp[-1] % "")
        return adj(s, [':', ':=', '--'], 1)


    def getPortList(self):
        s = []
        for clock in self.clocks:
            s.append(wbsVhdlStrGeneral.clkport % (clock, clock))
            s.append(wbsVhdlStrGeneral.rstport % (clock, clock))
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


    def getSetList(self):
        s = []
        for reg in self.registers:
            s += reg.getStrSet()
        return s


    def getResetList(self):
        s = []
        for reg in self.registers:
            s += reg.getStrReset()
        return s



    def _getFsmReadList(self):
        s = []
        for reg in self.registers:
            s += reg.getStrFsmRead()
        return s


    def _getFsmWriteList(self):
        s = []
        for reg in self.registers:
            s += reg.getStrFsmWrite()
        return s


    def getFsmList(self):
        s = []

        hiAdr = self._getLastAddress()
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

        s +=  iN(self.v.wbs0, 1)
        s += adj(self.getResetList(), ['<='], 4)
        tmpV = self.v.wbs1_0 + [self.v.wbs1_adr % (msbIdx-1, lsbIdx, padding)] + self.v.wbs1_1 + [self.v.enable % self.stallReg.v.regname]
        s += iN(tmpV, 3)
        s += adj(self.getSetList(), ['<=', '--'], 4)
        s +=  iN(self._getPageSelect(), 4)
        s +=  iN(self.v.wbs2, 4)
        s += adj(self._getFsmWriteList(), ['=>', '<=', 'v_d', "--"], 7)

        s +=  iN(self.v.wbOthers, 7)
        s +=  iN(self.v.wbs3, 5)
        s += adj(self._getFsmReadList(), ['=>', '<=', "--"], 7)
        s +=  iN(self.v.wbs4, 1)

        return s


    def getStrSDB(self):
        s = []
        adrx = ("%016x")
        align = 1<<(self._getLastAddress()-1).bit_length()
        s += self.v.sdb0
        s.append(self.v.sdbAddrFirst % (adrx % int(self.startaddress)))
        s.append(self.v.sdbAddrLast  % (adrx % ( int(align-1) )))
        s += self.v.sdb1
        return s

    def _getPageSelect(self):
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

        adrHi = "%x" % self._getLastAddress()
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

