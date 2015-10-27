# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 16:36:49 2015

@author: mkreider
"""
from stringtemplates import registerVhdlStr
from stringtemplates import wbsVhdlStrGeneral
from textformatting import mskWidth as mskWidth


class Register(object):


    def __init__(self, wbStr, genIntD, name, desc, flags, bits, rstvec, pages, clkBase, clkDom):
    

        #print "Adding WbRegister %s to domain %s" % (name, clkdomain)
        self.genIntD    = genIntD
        self.name       = name
        self.desc       = desc
        self.flags      = flags
        self.width      = bits
        self.customStrD = dict()
        if not self.isGenericWidth():
            self.width  = mskWidth(bits)
        self.pages      = pages
        if not self.isGenericPaged():
            self.pages  = mskWidth(pages)
        self.rstvec     = rstvec    
        if rstvec is not None:
            if not self.isGenericReset():
                self.rstvec = mskWidth(rstvec)     
        
        self.clkbase    = clkBase
        self.clkdomain  = clkDom
        self.v = registerVhdlStr(wbStr, self.name, self.desc, self.rstvec, self.getGenResetPrefix(), self.width,
                                 self.getGenWidthPrefix(), int(self.isPaged()) * self.pages, # 0 if this reg has no pages
                                 self.getGenPagePrefix(), self.clkdomain, self.clkbase)

        
        print "Reg %s Flags %s" % (self.name, self.flags)
        

    def setCustomStrDict(self, customD):
        self.customStrD = customD

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

    def getStrSignalDeclaration(self):
        s = []
        s.append(self.v.declarationReg)
        if self.isWrite():
            #s.append(self.v.declarationPortSigOut)
            s += self.getSyncSignalDeclaration("out") #will only be generated if sync

        if self.isDrive():
            s.append(self.v.declarationPortSigIn)
            s += self.getSyncSignalDeclaration("in")  #will only be generated if sync

        s.append
        return s


    def getStrPortDeclaration(self):
        s = []
        if self.isWrite():
            s.append(self.v.declarationPortOut)

        if self.isDrive():
            s.append(self.v.declarationPortIn)
        return s

    #generate sync signal delcarations if neeeded
    def getSyncSignalDeclaration(self, direction):
        s = []
        if self.clkbase != self.clkdomain:
            if direction == "out" or direction == "in":
                for line in self.syncSigsTemplate:
                    s.append(line % direction)
        return s
    
    def getStrPortAssignment(self):
        s = []
        if self.customStrD.has_key('assign'):
            s += self.customStrD['assign']
        else:
            if self.isDrive():
                s += self._getPortAssignment("in")
            if self.isWrite():
                s += self._getPortAssignment("out")
        return s    
    
    #generate simple or synced (FIFO) port assignment
    def _getPortAssignment(self, direction):
        s = []
        
        if self.clkbase != self.clkdomain:
            matrixPageStr   = ""
            sigInWrapper    = "%s%s%s"
            sigOutWrapper   = "%s%s%s"
            if self.pages > 0:
                matrixPageStr   = "%s%s * " % self.genPagePrefix, self.pages
                sigInWrapper    = "mflat(%s)"
                sigOutWrapper   = "minfl(%s)"
            syncwidth = "%s%s%s" % (matrixPageStr, self.genWidthPrefix, self.width)
            
            if direction == "out":
                sigin   = sigInWrapper  % self.v.regname
                sigout  = sigOutWrapper % self.v.portnameout
                clkin   = wbsVhdlStrGeneral.clkportname % (self.clkbase, self.clkbase)
                clkout  = wbsVhdlStrGeneral.clkportname % (self.clkdomain, self.clkdomain)
            elif direction == "in":
                sigin   = sigInWrapper  % self.v.portnamein
                sigout  = sigOutWrapper % self.v.portsignamein
                clkin   = wbsVhdlStrGeneral.clkportname % (self.clkdomain, self.clkdomain)
                clkout  = wbsVhdlStrGeneral.clkportname % (self.clkbase, self.clkbase)        
            else:
                print "ERROR: Port direction <%s> of Register <%s> is unknown. Choose <in> or <out>" % (direction, self.name)
            
                        
            #construct sync assignments            
            for line in self.v.syncInstTemplate0_dir2:
                s.append(line % (direction, direction))
            s.append(self.v.syncInstTemplate1_dir % (direction))
            s.append(self.v.syncInstTemplate2)
            s.append(self.v.syncInstTemplate3_sw % syncwidth)
            s += self.v.syncInstTemplate4
            for line in self.v.syncInstTemplate5_dir:
                s.append(line % direction)
            s.append(self.v.syncInstTemplate6_ci % clkin)
            s.append(self.v.syncInstTemplate7_co % clkout)
            s.append(self.v.syncInstTemplate8_si % sigin)
            s.append(self.v.syncInstTemplate9_so % sigout)
                                       
            return s                           
        else:
            if direction == "out":
                s.append(self.v.portAssignTemplate % (self.v.portnameout, self.v.regname))
            elif direction == "in":
                s.append(self.v.portAssignTemplate % (self.v.portsignamein, self.v.portnamein))
            else:
                print "ERROR: Port direction <%s> of Register <%s> is unknown. Choose <in> or <out>" % (direction, self.name)    
        return s        
        

    def getStrStubDeclaration(self):
        s = []
        if self.isWrite():
            s.append(self.v.declarationStubOut)

        if self.isDrive():
            s.append(self.v.declarationStubIn)
        return s


    def getStrStubInstance(self):
        s = []
        if self.isWrite():
            s.append(self.v.assignStubOut)

        if self.isDrive():
            s.append(self.v.assignStubIn)
        return s



    def getStrReset(self):
        s = []
        s.append(self.v.reset)
        return s



    def getStrSet(self):
        s = []        
        if self.customStrD.has_key('set'):
            s += self.customStrD['set']
        else:
            if self.isDrive():
                s.append(self.v.readUpdate)
                
            if self.isWrite() and self.isPulsed():
                s.append(self.v.wbPulseZero)   
        return s

    #implement in derived class
    def getLastAdr(self):
        return None

    def getStrAddress(self, language="VHDL", lastAdr=0):
        return []
    
    def getStrFsmRead(self):
        return []
    
    def getStrFsmWrite(self):
        return []
        
    def addToGroup(self, reg):
        pass
        
        

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
                #Show comment only the first occurrance of a WbRegister name
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



    

class WbRegister(Register):
    def __init__(self, dataBits=32, adrBits=32, sAdr=0x0, offs=4, *args):
        super(WbRegister, self).__init__(*args)
        self.dwidth     = dataBits
        self.awidth     = adrBits
        self.startAdr   = sAdr
        self.offs       = offs
        self.opList     = []
        #add operations according to WbRegister flags
        adr = sAdr
        if self.isAtomic():
            if self.isRead():
                self._addOp(adr, '_GET')
                adr = None
            if self.isWrite():
                self._addOp(adr, '_CLR')
                adr = None
                self._addOp(adr, '_SET')
        else:
            if self.isRead() and self.isWrite():
                self._addOp(adr, '_RW')
            elif self.isRead():
                self._addOp(adr, '_GET')
            elif self.isWrite():
                self._addOp(adr, '_OWR')                         


    def addToGroup(self, reg):
        self.groupList.append(reg)

    def _sliceMsk(self):
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


    def _addOp(self, adr, op):
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

        mskList = self._sliceMsk()
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
            
            
    def getStrAddress(self, language="VHDL", lastAdr=0):
        s = []
        adrHi = lastAdr
        idxHi = mskWidth(adrHi) -1
        adrx = ("%0" + str((idxHi+1+3)/4) + "x")
        mskx = ("%0" + str(self.dwidth/4) + "x")

        lang = str(language)

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

                if(lang.lower() == "c"):
                    s.append(self.v.cConstRegAdr        % (op + idx, adrx % adr, rw, bitmask))
                elif(lang.lower() == "vhdl"):
                    s.append(self.v.vhdlConstRegAdr     % (op + idx, adrx % adr, rw, bitmask))
                elif(lang.lower() == "python"):
                    s.append(self.v.pythonConstRegAdr    % (op + idx, adrx % adr, rw, bitmask))
                else:
                    print "<%s> is not a valid output language!" % language

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

                    
                if self.customStrD.has_key('read'):
                    s += self.customStrD['read']
                    
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

                if self.customStrD.has_key('write'):
                    s += self.customStrD['write']    
                opIdx += 1
        return s


