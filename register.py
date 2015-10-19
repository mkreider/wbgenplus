# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 16:36:49 2015

@author: mkreider
"""
from textformatting import mskWidth as mskWidth 

class register(object):

    def __init__(self, slaveIf, pages, datawidth, addresswidth, name, desc, bigMsk, flags, clkbase="sys", clkdomain="sys", rstvec=None, startAdr=None, offs=4, genIntD=dict(), genMiscD=dict()):
        #print "Adding REgister %s to domain %s" % (name, clkdomain)        
        self.slaveIf    = slaveIf
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
        if not self.isGenericWidth():
            self.width  = mskWidth(bigMsk)
            
        self.opList     = []
        
        adr = startAdr
        
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
        if self.hasWriteEnableFlag():    
            self.addOp(None, '_WE')   

    def isWrite(self):
        if(self.flags.find('w') > -1):
            return True
        return False
        
    def isRead(self):
        if(self.flags.find('r') > -1):
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
        
    def hasWriteEnableFlag(self):
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

    def getGenWidthPrefix(self):
        if self.isGenericWidth():
            return "g_"
        return ""    
    
    def getGenPagePrefix(self):
        if self.isGenericPaged():
            return "g_"
        return ""     

    def addOp(self, adr, op):
        #print "myop %s" % op        
        adrList = []
        #print "addop adr: %s" % adr        
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

#    def getTypeStrings(self):
#        slvSubType   = "subtype t_slv_%s_%s is std_logic_vector(%s-1 downto 0);\n" % (self.slaveIf, self.name, self.width) #name, idxHi
#        slvArrayType = "type    t_slv_%s_%s_array is array(natural range <>) of t_slv_%s_%s;\n" % ( self.slaveIf, self.name, self.slaveIf, self.name)  #name, #name
#       
#        s = []
#        if(self.flags.find('m') > -1):        
#            s.append('\n')
#            s.append(slmArray)
#        return s
    
    def getRegisterName(self):
        regname = "r_%s_%s" % (self.slaveIf, self.name)
        return regname
    
    def getRegisterStrings(self, showComment=False):
        syncsigs     = ["signal s_%s_%s_push  : std_logic; -- Sync signals\n" % (self.slaveIf, self.name),
                        "signal s_%s_%s_pop   : std_logic;\n" % (self.slaveIf, self.name),
                        "signal s_%s_%s_full  : std_logic;\n" % (self.slaveIf, self.name),
                        "signal s_%s_%s_empty : std_logic;\n" % (self.slaveIf, self.name)
                        ]
        comment = (" -- " +  self.desc) if showComment else ""
        reg          = "signal %s : std_logic_vector(%s%s-1 downto 0);%s\n" % (self.getRegisterName(), self.getGenWidthPrefix(), self.width, comment)
        regArray     = "signal %s : t_slm(%s%s-1 downto 0)(%s%s-1 downto 0);%s\n"  % (self.getRegisterName(), self.getGenPagePrefix(), self.pages, self.getGenWidthPrefix(), self.width, comment) #name, name, idxHi, desc
       
        s = []
        if(self.clkdomain != self.clkbase):
            s += syncsigs
        
        if self.isPaged(): 
            s.append(regArray)
        else:
            s.append(reg)
        return s    
        
    
    def getPortName(self):
        if self.isWrite():
            suffix      = "_o"    
        else:
            suffix      = "_i"
            
        portname = "%s_%s_%s%s" % (self.slaveIf, self.name, self.clkdomain, suffix)
        return portname
        
    def getPortStrings(self):
        if self.isWrite():
            direction   = "out"   
        else:
            direction   = "in"
        
        port        = "%s : %s std_logic_vector(%s%s-1 downto 0); -- %s\n" % (self.getPortName(), direction, self.getGenWidthPrefix(), self.width, self.desc)     
        portArray   = "%s : %s t_slm(%s%s-1 downto 0, %s%s-1 downto 0); -- %s\n" % (self.getPortName(), direction, self.getGenPagePrefix(), self.pages, self.getGenWidthPrefix(), self.width, self.desc)
        
        if self.isPaged():
            return portArray            
        else:
            return port             
            
           
            
    def getResetStrings(self):
        resetSignal       = "r_%s_%s <= %s;\n"                  % (self.slaveIf, self.name, self.rstvec)
        resetSignalArray  = "r_%s_%s <= (others =>%s);\n"       % (self.slaveIf, self.name, self.rstvec)       
        
        if self.isWrite():
            if self.isPaged():
               return resetSignalArray
            else:
               return resetSignal
        else:
            return []

    def getPulsedStrings(self):
        wbWritePulseZero        = "r_%s_%s <= (others => '0'); -- %s pulse\n" % (self.slaveIf, self.name, self.desc) #registerName        
        wbWritePulseZeroArray   = "r_%s_%s <= (others => (others => '0')); -- %s pulse\n" % (self.slaveIf, self.name, self.desc) #registerName             
        
        if( self.isWrite() and ( self.hasWriteEnableFlag() or self.isPulsed()  )):
            if self.isPaged():
               return wbWritePulseZeroArray
            else:
               return wbWritePulseZero
        else:
            return []       
    
    def getAdrStrings(self, language="VHDL"):
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
                #Show comment only the first occurrance of a register name                    
                if((opIdx == 0) and (adrIdx == 0)):
                    comment = self.desc
                else:
                    comment = '\"\"'
                
                if(genIntD.has_key(msk)):
                    bitmask = "g_%s" % msk
                else:
                    bitmask = mskx % int(2**msk-1)
                if(language == "C"):
                    s.append(adrC % (self.slaveIf, self.name + op + idx, adrx % adr))
                else:    
                    s.append(adrV % (self.slaveIf, self.name + op + idx, adrx % adr))
                
                adrIdx += 1
            opIdx += 1
        
        return s        
        
    def getInterfaceDocStrings(self, adressNibbles):
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
                
                if(genIntD.has_key(msk)):
                    bitmask = "g_%s" % msk
                else:
                    bitmask = msk
                s.append(doc % (adrx % adr, rw, self.slaveIf, self.name + op + idx, bitmask, comment))
                
                adrIdx += 1
            opIdx += 1
        
        return s    
            
            
    def getInstanceStrings(self):
        if self.isWrite():
            #it's an output of our entity
            sigin  = self.getRegisterName() 
            sigout = self.getPortName()
            clkin  = self.clkbase
            clkout = self.clkdomain
        else:
            sigin  = self.getPortName() 
            sigout = self.getRegisterName()
            clkin  = self.clkdomain
            clkout = self.clkbase           
            #it's an input to our entity        
#TODO

       
        
        sync_fifo   = ["\n%s_%s_FIFO : generic_async_fifo\n" % (self.slaveIf, self.name),
                       "generic map(\n",
                       "  g_data_width   => %s,\n" % (self.getGenWidthPrefix() + str(self.width)), 
                       "  g_size         => %s,\n" % (8),
                       "  g_show_ahead   => true,\n",
                       "  g_with_rd_empty   => true,\n",
                       "  g_with_wr_full    => true)\n",
                       "port map(\n",
                       "  rst_n_i  => rst_n_i,\n",
                       "  clk_wr_i => clk_%s_i,\n" % clkin,                        
                       "  clk_rd_i => clk_%s_i,\n" % clkout,
                       "  we_i     => s_fifo_push_%s_%s,\n" % (self.slaveIf, self.name),
                       "  rd_i     => s_fifo_pop_%s_%s,\n" % (self.slaveIf, self.name),
                       "  d_i      => %s,\n" % sigin,
                       "  q_o      => %s,\n" % sigout,
                       "  rd_empty_o  => s_fifo_empty_%s_%s,\n" % (self.slaveIf, self.name),
                       "  wr_full_o   => s_fifo_full_%s_%s);\n" % (self.slaveIf, self.name),
                       "  s_fifo_pop_%s_%s    <= not s_fifo_empty_%s_%s;\n" % (self.slaveIf, self.name, self.slaveIf, self.name),
                       "  s_fifo_push_%s_%s   <= not s_fifo_full_%s_%s;\n\n" % (self.slaveIf, self.name, self.slaveIf, self.name)
                      ]     
        
        simple_assign = "%s <= %s;\n" % (sigout, sigin)
        
        if(self.clkdomain != self.clkbase):
            s = sync_fifo
        else:
            s = simple_assign
        
        
        return s   
        
    def getFsmReadStrings(self, showComment=False):
        wbReadMatrix    = "when c_%s_%%s => r_%s_out_dat0(%%s) <= mrs2slv(r_%s_%%s, v_page, %%s, %%s);\n" % (self.slaveIf, self.slaveIf, self.slaveIf) #registerName, registerName, desc
        wbRead          = "when c_%s_%%s => r_%s_out_dat0(%%s) <= r_%s_%%s;\n" % (self.slaveIf, self.slaveIf, self.slaveIf) #registerName, registerName, desc
        wbStall         = "r_%s_out_stall  <= '1'; --    %%s auto stall\n" % (self.slaveIf)
             
        s = []    
        
        for opLine in self.opList:
            (op, adrList) = opLine
            if((op == "_GET") or (op == "_RW ")):                    
                #this is sliced
                adrIdx = 0            
                for adrLine in adrList:
                    (msk, adr) = adrLine
                    #Show comment only the first occurrance of a register name                    
                    if(adrIdx == 0):
                        comment  = self.desc
                    else:
                        comment  = '\"\"'
                   
                    #calculate register bitslice from adr idx    
                    sliceWidth       = msk
                    curSliceHigh     = sliceWidth + adrIdx*self.dwidth -1
                    curSliceLow      = adrIdx*self.dwidth
                    curSlice         = "(%u downto %u)" % (curSliceHigh, curSliceLow)
                    baseSlice        = "%u downto %u" % ( sliceWidth -1, 0)
                    adrIdx += 1
                    if showComment:
                        s.append("-- %s\n" % comment)
                    if self.isPaged():
                        s.append(wbReadMatrix % (self.name + op, baseSlice, self.name, curSliceHigh, curSliceLow) )
                    else:    
                        s.append(wbRead % (self.name + op, baseSlice, self.name + curSlice))
                    
                if self.isStalling():             
                    s.append(wbStall % self.name)    
        return s

    def getFsmWriteStrings(self, showComment=False):
        wbWrite            = "when c_%s_%%s => r_%s_%%s <= f_wb_wr(r_%s_%%s, v_dat_i, v_sel, \"%%s\");\n" % (self.slaveIf, self.slaveIf, self.slaveIf) #registerName, registerName, (set/clr/owr), desc
        wbWriteMatrix      = "when c_%s_%%s => slv2mrowslice(r_%s_%%s, f_wb_wr(r_%s_%%s, v_dat_i, v_sel, \"%%s\"), (v_page), %%s, %%s);\n" % (self.slaveIf, self.slaveIf, self.slaveIf) #registerName, registerName, (set/clr/owr), desc
   
        
        wbWriteWe          = "r_%s_%%s_WE <= '1'; --    %%s write enable\n" % (self.slaveIf) 
        wbWriteWeZero      = "r_%s_%%s_WE <= '0'; -- %%s pulse\n" % (self.slaveIf)
        wbStall            = "r_%s_out_stall  <= '1'; --    %%s auto stall\n" % (self.slaveIf)
        wbWritePulseZero   = "r_%s_%%s <= (others => '0'); -- %%s pulse\n" % (self.slaveIf) #registerName        
        wbWritePulseZeroArray = "r_%s_%%s <= (others => (others => '0')); -- %%s pulse\n" % (self.slaveIf) #registerName        
        wbStall            = "r_%s_out_stall  <= '1'; --    %%s auto stall\n" % (self.slaveIf)
     
        
        s = []    
        
        opIdx = 0    
        for opLine in self.opList:
            (op, adrList) = opLine
            adrIdx = 0
            if(op != "_GET"):                    
               
                #this is sliced
                adrIdx=0            
                for adrLine in adrList:
                    if((opIdx == 0) and (adrIdx == 0)):
                        comment = self.desc
                    else:
                        comment = '\"\"'
                    (msk, adr) = adrLine
                    
                    (idxHi, idxLo) = mskWidth(msk)
                    sliceWidth   = (idxHi-idxLo+1) 
                    curSliceHigh     = sliceWidth + adrIdx*self.dwidth -1
                    curSliceLow      = adrIdx*self.dwidth
                    curSlice         = "(%u downto %u)" % (curSliceHigh, curSliceLow)
                    adrIdx += 1
                    if showComment:                        
                        s.append("-- %s\n" % comment)
                    if self.isPaged():
                        s.append(wbWriteMatrix % (self.name + op, self.name + curSlice, self.name + curSlice, self.wrModes[op]))
                
                    else:
                        s.append(wbWrite % (self.name + op, self.name + curSlice, self.name + curSlice, self.wrModes[op], curSliceHigh, curSliceLow))
                
                if self.hasWriteEnableFlag():
                    s.append(wbWriteWe % (self.name, self.name))
                if self.isStalling():             
                    s.append(wbStall % self.name)     
                opIdx += 1
        
        if self.hasWriteEnableFlag():
            s.append(wbWriteWeZero % (self.name, self.name))
            if self.isPulsed():
                if self.isPaged():
                    s.append(wbWritePulseZeroArray % (self.name, self.name))
                else:                
                    s.append(wbWritePulseZero % (self.name, self.name))
        
        return s  
    
class internalregister(register):
    def __init__(self, slaveIf, pages, name, desc, bigMsk, flags, clkbase="sys", clkdomain="sys", rstvec=None):
        print "Adding internal Register %s" % name        
        self.slaveIf    = slaveIf
        self.pages      = pages         
        self.name       = name
        self.desc       = desc
        self.clkbase  = clkbase
        self.clkdomain  = clkdomain
        self.rstvec     = rstvec        
        self.flags     = flags
        self.width      = mskWidth(bigMsk)
        self.opList     = []        
    
    def getInstanceStrings(self):
        return [] 
    
    def getLastAdr(self):
        pass 
       
    def getAdrStrings(self, language="VHDL"):
        return []      
            
    def getFsmReadStrings(self, showComment=False):
        return []

    def getFsmWriteStrings(self, showComment=False):
        return []   

    def getInterfaceDocStrings(self, addressNibbles):
        return []
        
class pagedregister(register):
    def __init__(self, slaveIf, pages, datawidth, addresswidth, name, desc, bigMsk, flags, clkbase="sys", clkdomain="sys", rstvec=None, startAdr=None, offs=4):
        #print "Adding REgister %s to domain %s" % (name, clkdomain)        
        self.slaveIf    = slaveIf
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
        if not self.isGenericWidth():
            self.width  = mskWidth(bigMsk)
        self.checkGeneric()
        self.opList     = []
        
        adr = startAdr
        
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
        if self.hasWriteEnableFlag():    
            self.addOp(None, '_WE')   

    def isWrite(self):
        if(self.flags.find('w') > -1):
            return True
        return False
        
    def isRead(self):
        if(self.flags.find('r') > -1):
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
        
    def hasWriteEnableFlag(self):
        if(self.flags.find('f') > -1):
            return True
        return False
        
    def isStalling(self):
        if(self.flags.find('s') > -1):
            return True
        return False    

    def checkGeneric(self):
         if( self.isPaged() and self.genIntD.has_key(self.width)):
             print "\n\nERROR: Register %s has a generic width AND is part of a memory page! This is impossible, hardcode the width instead!" % self.name
             exit(2)
            
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

    def getGenWidthPrefix(self):
        if self.isGenericWidth():
            return "g_"
        return ""    
    
    def getGenPagePrefix(self):
        if self.isGenericPaged():
            return "g_"
        return ""     

    def addOp(self, adr, op):
        #print "myop %s" % op        
        adrList = []
        #print "addop adr: %s" % adr        
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

#    def getTypeStrings(self):
#        slvSubType   = "subtype t_slv_%s_%s is std_logic_vector(%s-1 downto 0);\n" % (self.slaveIf, self.name, self.width) #name, idxHi
#        slvArrayType = "type    t_slv_%s_%s_array is array(natural range <>) of t_slv_%s_%s;\n" % ( self.slaveIf, self.name, self.slaveIf, self.name)  #name, #name
#       
#        s = []
#        if(self.flags.find('m') > -1):        
#            s.append('\n')
#            s.append(slmArray)
#        return s
    
    def getRegisterName(self):
        regname = "r_%s_%s" % (self.slaveIf, self.name)
        return regname
    
    def getRegisterStrings(self, showComment=False):
        syncsigs     = ["signal s_%s_%s_push  : std_logic; -- Sync signals\n" % (self.slaveIf, self.name),
                        "signal s_%s_%s_pop   : std_logic;\n" % (self.slaveIf, self.name),
                        "signal s_%s_%s_full  : std_logic;\n" % (self.slaveIf, self.name),
                        "signal s_%s_%s_empty : std_logic;\n" % (self.slaveIf, self.name)
                        ]
        comment = (" -- " +  self.desc) if showComment else ""
        reg          = "signal %s : std_logic_vector(%s%s-1 downto 0);%s\n" % (self.getRegisterName(), self.getGenWidthPrefix(), self.width, comment)
        regArray     = "signal %s : t_slm(%s%s-1 downto 0)(%s%s-1 downto 0);%s\n"  % (self.getRegisterName(), self.getGenPagePrefix(), self.pages, self.getGenWidthPrefix(), self.width, comment) #name, name, idxHi, desc
       
        s = []
        if(self.clkdomain != self.clkbase):
            s += syncsigs
        
        if self.isPaged(): 
            s.append(regArray)
        else:
            s.append(reg)
        return s    
        
    
    def getPortName(self):
        if self.isWrite():
            suffix      = "_o"    
        else:
            suffix      = "_i"
            
        portname = "%s_%s_%s%s" % (self.slaveIf, self.name, self.clkdomain, suffix)
        return portname
        
    def getPortStrings(self):
        if self.isWrite():
            direction   = "out"   
        else:
            direction   = "in"
        
        port        = "%s : %s std_logic_vector(%s%s-1 downto 0); -- %s\n" % (self.getPortName(), direction, self.getGenWidthPrefix(), self.width, self.desc)     
        portArray   = "%s : %s t_slm(%s%s-1 downto 0, %s%s-1 downto 0); -- %s\n" % (self.getPortName(), direction, self.getGenPagePrefix(), self.pages, self.getGenWidthPrefix(), self.width, self.desc)
        
        if self.isPaged():
            return portArray            
        else:
            return port             
            
           
            
    def getResetStrings(self):
        resetSignal       = "r_%s_%s <= %s;\n"                  % (self.slaveIf, self.name, self.rstvec)
        resetSignalArray  = "r_%s_%s <= (others =>%s);\n"       % (self.slaveIf, self.name, self.rstvec)       
        
        if self.isWrite():
            if self.isPaged():
               return resetSignalArray
            else:
               return resetSignal
        else:
            return []

    def getPulsedStrings(self):
        wbWritePulseZero        = "r_%s_%s <= (others => '0'); -- %s pulse\n" % (self.slaveIf, self.name, self.desc) #registerName        
        wbWritePulseZeroArray   = "r_%s_%s <= (others => (others => '0')); -- %s pulse\n" % (self.slaveIf, self.name, self.desc) #registerName             
        
        if( self.isWrite() and ( self.hasWriteEnableFlag() or self.isPulsed()  )):
            if self.isPaged():
               return wbWritePulseZeroArray
            else:
               return wbWritePulseZero
        else:
            return []       
    
    def getAdrStrings(self, language="VHDL"):
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
                #Show comment only the first occurrance of a register name                    
                if((opIdx == 0) and (adrIdx == 0)):
                    comment = self.desc
                else:
                    comment = '\"\"'
                
                if(genIntD.has_key(msk)):
                    bitmask = "g_%s" % msk
                else:
                    bitmask = mskx % int(2**msk-1)
                if(language == "C"):
                    s.append(adrC % (self.slaveIf, self.name + op + idx, adrx % adr))
                else:    
                    s.append(adrV % (self.slaveIf, self.name + op + idx, adrx % adr))
                
                adrIdx += 1
            opIdx += 1
        
        return s        
        
    def getInterfaceDocStrings(self, adressNibbles):
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
                
                if(genIntD.has_key(msk)):
                    bitmask = "g_%s" % msk
                else:
                    bitmask = msk
                s.append(doc % (adrx % adr, rw, self.slaveIf, self.name + op + idx, bitmask, comment))
                
                adrIdx += 1
            opIdx += 1
        
        return s    
            
            
    def getInstanceStrings(self):
        if self.isWrite():
            #it's an output of our entity
            sigin  = self.getRegisterName() 
            sigout = self.getPortName()
            clkin  = self.clkbase
            clkout = self.clkdomain
        else:
            sigin  = self.getPortName() 
            sigout = self.getRegisterName()
            clkin  = self.clkdomain
            clkout = self.clkbase           
            #it's an input to our entity        
#TODO

       
        
        sync_fifo   = ["\n%s_%s_FIFO : generic_async_fifo\n" % (self.slaveIf, self.name),
                       "generic map(\n",
                       "  g_data_width   => %s,\n" % (self.getGenWidthPrefix() + str(self.width)), 
                       "  g_size         => %s,\n" % (8),
                       "  g_show_ahead   => true,\n",
                       "  g_with_rd_empty   => true,\n",
                       "  g_with_wr_full    => true)\n",
                       "port map(\n",
                       "  rst_n_i  => rst_n_i,\n",
                       "  clk_wr_i => clk_%s_i,\n" % clkin,                        
                       "  clk_rd_i => clk_%s_i,\n" % clkout,
                       "  we_i     => s_fifo_push_%s_%s,\n" % (self.slaveIf, self.name),
                       "  rd_i     => s_fifo_pop_%s_%s,\n" % (self.slaveIf, self.name),
                       "  d_i      => %s,\n" % sigin,
                       "  q_o      => %s,\n" % sigout,
                       "  rd_empty_o  => s_fifo_empty_%s_%s,\n" % (self.slaveIf, self.name),
                       "  wr_full_o   => s_fifo_full_%s_%s);\n" % (self.slaveIf, self.name),
                       "  s_fifo_pop_%s_%s    <= not s_fifo_empty_%s_%s;\n" % (self.slaveIf, self.name, self.slaveIf, self.name),
                       "  s_fifo_push_%s_%s   <= not s_fifo_full_%s_%s;\n\n" % (self.slaveIf, self.name, self.slaveIf, self.name)
                      ]     
        
        simple_assign = "%s <= %s;\n" % (sigout, sigin)
        
        if(self.clkdomain != self.clkbase):
            s = sync_fifo
        else:
            s = simple_assign
        
        
        return s   
        
    def getFsmReadStrings(self, showComment=False):
        wbReadMatrix    = "when c_%s_%%s => r_%s_out_dat0(%%s) <= mrs2slv(r_%s_%%s, v_page, %%s, %%s);\n" % (self.slaveIf, self.slaveIf, self.slaveIf) #registerName, registerName, desc
        wbRead          = "when c_%s_%%s => r_%s_out_dat0(%%s) <= r_%s_%%s;\n" % (self.slaveIf, self.slaveIf, self.slaveIf) #registerName, registerName, desc
        wbStall         = "r_%s_out_stall  <= '1'; --    %%s auto stall\n" % (self.slaveIf)
             
        s = []    
        
        for opLine in self.opList:
            (op, adrList) = opLine
            if((op == "_GET") or (op == "_RW ")):                    
                #this is sliced
                adrIdx = 0            
                for adrLine in adrList:
                    (msk, adr) = adrLine
                    #Show comment only the first occurrance of a register name                    
                    if(adrIdx == 0):
                        comment  = self.desc
                    else:
                        comment  = '\"\"'
                   
                    #calculate register bitslice from adr idx    
                    sliceWidth       = msk
                    curSliceHigh     = sliceWidth + adrIdx*self.dwidth -1
                    curSliceLow      = adrIdx*self.dwidth
                    curSlice         = "(%u downto %u)" % (curSliceHigh, curSliceLow)
                    baseSlice        = "%u downto %u" % ( sliceWidth -1, 0)
                    adrIdx += 1
                    if showComment:
                        s.append("-- %s\n" % comment)
                    if self.isPaged():
                        s.append(wbReadMatrix % (self.name + op, baseSlice, self.name, curSliceHigh, curSliceLow) )
                    else:    
                        s.append(wbRead % (self.name + op, baseSlice, self.name + curSlice))
                    
                if self.isStalling():             
                    s.append(wbStall % self.name)    
        return s

    def getFsmWriteStrings(self, showComment=False):
        wbWrite            = "when c_%s_%%s => r_%s_%%s <= f_wb_wr(r_%s_%%s, v_dat_i, v_sel, \"%%s\");\n" % (self.slaveIf, self.slaveIf, self.slaveIf) #registerName, registerName, (set/clr/owr), desc
        wbWriteMatrix      = "when c_%s_%%s => slv2mrowslice(r_%s_%%s, f_wb_wr(r_%s_%%s, v_dat_i, v_sel, \"%%s\"), (v_page), %%s, %%s);\n" % (self.slaveIf, self.slaveIf, self.slaveIf) #registerName, registerName, (set/clr/owr), desc
   
        
        wbWriteWe          = "r_%s_%%s_WE <= '1'; --    %%s write enable\n" % (self.slaveIf) 
        wbWriteWeZero      = "r_%s_%%s_WE <= '0'; -- %%s pulse\n" % (self.slaveIf)
        wbStall            = "r_%s_out_stall  <= '1'; --    %%s auto stall\n" % (self.slaveIf)
        wbWritePulseZero   = "r_%s_%%s <= (others => '0'); -- %%s pulse\n" % (self.slaveIf) #registerName        
        wbWritePulseZeroArray = "r_%s_%%s <= (others => (others => '0')); -- %%s pulse\n" % (self.slaveIf) #registerName        
        wbStall            = "r_%s_out_stall  <= '1'; --    %%s auto stall\n" % (self.slaveIf)
     
        
        s = []    
        
        opIdx = 0    
        for opLine in self.opList:
            (op, adrList) = opLine
            adrIdx = 0
            if(op != "_GET"):                    
               
                #this is sliced
                adrIdx=0            
                for adrLine in adrList:
                    if((opIdx == 0) and (adrIdx == 0)):
                        comment = self.desc
                    else:
                        comment = '\"\"'
                    (msk, adr) = adrLine
                    
                    (idxHi, idxLo) = mskWidth(msk)
                    sliceWidth   = (idxHi-idxLo+1) 
                    curSliceHigh     = sliceWidth + adrIdx*self.dwidth -1
                    curSliceLow      = adrIdx*self.dwidth
                    curSlice         = "(%u downto %u)" % (curSliceHigh, curSliceLow)
                    adrIdx += 1
                    if showComment:                        
                        s.append("-- %s\n" % comment)
                    if self.isPaged():
                        s.append(wbWriteMatrix % (self.name + op, self.name + curSlice, self.name + curSlice, self.wrModes[op]))
                
                    else:
                        s.append(wbWrite % (self.name + op, self.name + curSlice, self.name + curSlice, self.wrModes[op], curSliceHigh, curSliceLow))
                
                if self.hasWriteEnableFlag():
                    s.append(wbWriteWe % (self.name, self.name))
                if self.isStalling():             
                    s.append(wbStall % self.name)     
                opIdx += 1
        
        if self.hasWriteEnableFlag():
            s.append(wbWriteWeZero % (self.name, self.name))
            if self.isPulsed():
                if self.isPaged():
                    s.append(wbWritePulseZeroArray % (self.name, self.name))
                else:                
                    s.append(wbWritePulseZero % (self.name, self.name))
        
        return s    