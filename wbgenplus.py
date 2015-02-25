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


myVersion = "0.3"
myStart   = "15 Dec 2014"
myUpdate  = "10 Jan 2015"
myCreator = "M. Kreider <m.kreider@gsi.de>"



i1          = textformatting.setColIndent
iN          = textformatting.setColsIndent    
adj         = textformatting.adjBlockByMarks
mskWidth    = textformatting.mskWidth
str2int     = textformatting.parseNumeral
commentLine = textformatting.commentLine
commentBox  = textformatting.commentBox
now = datetime.datetime.now()

 

class wbsCStr(object):
   

    def __init__(self, pages, unitname, slaveIfName, sdbVendorID, sdbDeviceID):
        self.unitname     = unitname
        self.slaveIfName  = slaveIfName        
        self.pages        = pages
        self.sdbVendorID  = '#define %s_%s_VENDOR_ID 0x%016xull\n' % (unitname.upper(), slaveIfName.upper(), sdbVendorID)
        self.sdbDeviceID  = '#define %s_%s_DEVICE_ID 0x%08x\n' % (unitname.upper(), slaveIfName.upper(), sdbDeviceID)
        #################################################################################        
        #Strings galore        
        self.constRegAdr    = "#define %s_%%s   0x%%s // %%s _0x%%s, %%s\n" % slaveIfName.upper() #name, adrVal,  rw, msk, desc

class gCStr(object):
    def __init__(self, filename, unitname, author, email, version, date):
        self.unitname   = unitname     
        self.author     = author
        self.email      = email
        self.version    = version
        self.date       = date
        self.header         = [] 
        self.hdrfileStart   = ["#ifndef _%s_H_\n"   % unitname.upper(),
                               "#define _%s_H_\n\n" % unitname.upper()]
        self.hdrfileEnd     =  "#endif\n"        
       

class wbsVhdlStr(object):
   

    def __init__(self, pages, unitname, slaveIfName, dataWidth, vendId, devId, sdbname, clocks):
        self.unitname       = unitname
        self.slaveIfName    = slaveIfName        
        self.pages          = pages
        self.dataWidth      = dataWidth
        self.clocks         = clocks
        #################################################################################        
        #Strings galore        
        self.slaveIf    = ["%s_i : in  t_wishbone_slave_in;\n" % slaveIfName,
                           "%s_o : out t_wishbone_slave_out" % slaveIfName] #name
                           
                           
        self.slaveSigsRegs = "signal s_%s_regs_clk_%%s_%%s : t_%s_regs_clk_%%s_%%s;\n" % (slaveIfName, slaveIfName)
        self.slaveInstRegs = "%s_regs_clk_%%s_%%s => s_%s_regs_clk_%%s_%%s,\n" % (slaveIfName, slaveIfName)
                          
        self.slaveSigs = ["signal s_%s_i : t_wishbone_slave_in;\n" % slaveIfName,
                          "signal s_%s_o : t_wishbone_slave_out;\n" % slaveIfName]
        
        self.slaveInst = ["%s_i => s_%s_i,\n" % (slaveIfName, slaveIfName),
                          "%s_o => s_%s_o" % (slaveIfName, slaveIfName)] #name        
        
        self.wbs0       = ["%s : process(clk_%s_i)\n" % (slaveIfName, clocks[0]),
                           "   variable v_dat_i  : t_wishbone_data;\n",
                           "   variable v_dat_o  : t_wishbone_data;\n",
                           "   variable v_adr    : natural;\n",
                           "   variable v_page   : natural;\n",
                           "   variable v_sel    : t_wishbone_byte_select;\n",
                           "   variable v_we     : std_logic;\n",
                           "   variable v_en     : std_logic;\n",
                           "begin\n",
                           "   if rising_edge(clk_%s_i) then\n" % clocks[0],
                           "      if(rst_n_i = '0') then\n"]
       
        self.wbs1_0     = ["else\n",
                           "   -- short names\n",
                           "   v_dat_i           := %s_i.dat;\n" % slaveIfName,
                           "   v_adr             := to_integer(unsigned(%s_i.adr(%%s)) %%s);\n" % slaveIfName,
                           "   v_sel             := %s_i.sel;\n" % slaveIfName]
                           
        self.wbs1_1     =  "   v_en              := %s_i.cyc and %s_i.stb and not (r_%s_out_stall or %s_regs_clk_%%s_i.STALL);\n" % (slaveIfName, slaveIfName, slaveIfName, slaveIfName)
                        
        self.wbs1_2     = ["   v_we              := %s_i.we;\n\n" % slaveIfName,
                           "   --interface outputs\n",
                           "   r_%s_out_stall   <= '0';\n" % slaveIfName,                            
                           "   r_%s_out_ack0    <= '0';\n" % slaveIfName,
                           "   r_%s_out_err0    <= '0';\n" % slaveIfName,
                           "   r_%s_out_dat0    <= (others => '0');\n\n" % slaveIfName,
                           "   r_%s_out_ack1    <= r_%s_out_ack0;\n" % (slaveIfName, slaveIfName),
                           "   r_%s_out_err1    <= r_%s_out_err0;\n" % (slaveIfName, slaveIfName),
                           "   r_%s_out_dat1    <= r_%s_out_dat0;\n\n" % (slaveIfName, slaveIfName)] 
      
        self.wbs2       = ["if(v_en = '1') then\n",
                           "   r_%s_out_ack0  <= '1';\n" % slaveIfName,
                           "   if(v_we = '1') then\n",
                           "      -- WISHBONE WRITE ACTIONS\n",
                           "      case v_adr is\n"]
    
        self.wbs3       = ["   end case;\n",
                           "else\n",
                           "   -- WISHBONE READ ACTIONS\n",
                           "   case v_adr is\n"]  

        self.wbs4       = ["               end case;\n",
                           "            end if; -- v_we\n",
                           "         end if; -- v_en\n",
                           "      end if; -- rst\n",
                           "   end if; -- clk edge\n",
                           "end process;\n\n"]
                           
        self.wbs5       = ["%s_regs_o <= r_%s;\n" % (slaveIfName, slaveIfName),
                           "s_%s <= %s_regs_i;\n" % (slaveIfName, slaveIfName),
                           "%s_o.stall <= r_%s_out_stall or %s_regs_i.STALL;\n" % (slaveIfName, slaveIfName, slaveIfName),                           
                           "%s_o.dat <= r_%s_out_dat1;\n" % (slaveIfName, slaveIfName),                           
                           "%s_o.ack <= r_%s_out_ack1 and not %s_regs_i.ERR;\n" % (slaveIfName, slaveIfName, slaveIfName),                           
                           "%s_o.err <= r_%s_out_err1 or      %s_regs_i.ERR;\n" % (slaveIfName, slaveIfName, slaveIfName)]
                           
        self.wbs5_0       = "%s_o.stall <= r_%s_out_stall or %s_regs_clk_%%s_i.STALL;\n" % (slaveIfName, slaveIfName, slaveIfName)                           
        self.wbs5_1       = "%s_o.dat <= r_%s_out_dat1;\n" % (slaveIfName, slaveIfName)                           
        self.wbs5_2       = "%s_o.ack <= r_%s_out_ack1 and not %s_regs_clk_%%s_i.ERR;\n" % (slaveIfName, slaveIfName, slaveIfName)                           
        self.wbs5_3       = "%s_o.err <= r_%s_out_err1 or      %s_regs_clk_%%s_i.ERR;\n" % (slaveIfName, slaveIfName, slaveIfName)                
                           
                           
                           
        self.syncProcStart0     = "sync_%s_clk_%%s_%%s : process(clk_%%s_i)\n   begin\n" % (slaveIfName)
        self.syncProcStart1     = "   if rising_edge(clk_%s_i) then\n         if(rst_n_i = '0') then\n"
        self.syncProcMid        = "      else\n"
        self.syncProcEnd        = ["      end if; -- rst\n",
                                  "   end if; -- clk edge\n",
                                  "end process;\n\n"]             
        
        self.syncProcReg        = "         r_%s_regs_clk_%%s_%%s_%%s <= r_%s_regs_clk_%%s_%%s_%%s;\n"  % (slaveIfName, slaveIfName)   
        self.syncAssignOutD     =  "%s_regs_clk_%%s_o.%%s <= r_%s.%%s;\n" % (slaveIfName, slaveIfName) #slaveIf clkdOut[i] recordsOut[i] slaveIf clkdOut[i] recordsOut[i]
        self.syncAssignOutI0    =  "%s_regs_clk_%%s_o.%%s <= r_%s_regs_clk_%%s_o_2.%%s;\n" % (slaveIfName, slaveIfName) #slaveIf clkdOut[i] recordsOut[i] slaveIf clkdOut[i] recordsOut[i]
        self.syncAssignOutI1    =  "r_%s_regs_clk_%%s_o_0.%%s <= r_%s.%%s;\n" % (slaveIfName, slaveIfName) #slave, clkd, slave
        
        self.syncAssignInD      =  "s_%s.%%s <= %s_regs_clk_%%s_i.%%s;\n" % (slaveIfName, slaveIfName) #slaveIf clkdOut[i] recordsOut[i] slaveIf clkdOut[i] recordsOut[i]
        self.syncAssignInI0     =  "r_%s_regs_clk_%%s_i_0.%%s <= %s_regs_clk_%%s_i.%%s;\n" % (slaveIfName, slaveIfName) #slaveIf clkdOut[i] recordsOut[i] slaveIf clkdOut[i] recordsOut[i]
        self.syncAssignInI1     =  "s_%s.%%s <= r_%s_regs_clk_%%s_i_2.%%s;\n" % (slaveIfName, slaveIfName) #slave, clkd, slave
        
      
        
        self.syncReg            = "signal r_%s_regs_clk_%%s_%%s_%%s : t_%s_regs_clk_%%s_%%s;\n" % (slaveIfName, slaveIfName)
        self.clkdomainComment   = "-- %s %%s domain %%s\n" % slaveIfName        
              
        self.slvSubType         = "subtype t_slv_%s_%%s is std_logic_vector(%%s-1 downto 0);\n" % slaveIfName #name, idxHi
        self.slvArrayType       = "type    t_slv_%s_%%s_array is array(natural range <>) of t_slv_%s_%%s;\n" % (slaveIfName, slaveIfName)  #name, #name
        self.signalSlvArray     = "%%s : t_slv_%s_%%s_array(%%s downto 0); -- %%s\n"  % slaveIfName #name, name, idxHi, desc
        self.wbsPageSelect      = "v_page := to_integer(unsigned(r_%s.%%s));\n\n"  % slaveIfName #pageSelect Register
        self.wbWrite            = "when c_%s_%%s => r_%s.%%s <= f_wb_wr(r_%s.%%s, v_dat_i, v_sel, \"%%s\"); -- %%s\n" % (slaveIfName, slaveIfName, slaveIfName) #registerName, registerName, (set/clr/owr), desc
        self.wbWriteWe          = "r_%s.%%s_WE <= '1'; --    %%s write enable\n" % (slaveIfName) 
        self.wbWriteWeZero      = "r_%s.%%s_WE <= '0'; -- %%s pulse\n" % (slaveIfName)
        self.wbStall            = "r_%s_out_stall  <= '1'; --    %%s auto stall\n" % (slaveIfName)
        self.wbWritePulseZero   = "r_%s.%%s <= (others => '0'); -- %%s pulse\n" % (slaveIfName) #registerName        
        self.wbWritePulseZeroArray = "r_%s.%%s <= (others => (others => '0')); -- %%s pulse\n" % (slaveIfName) #registerName        
                
        self.wbReadExt          = "when c_%s_%%s => r_%s_out_dat0(%%s) <= s_%s.%%s; -- %%s\n" % (slaveIfName, slaveIfName, slaveIfName) #registerName, registerName, desc
        self.wbReadInt          = "when c_%s_%%s => r_%s_out_dat0(%%s) <= r_%s.%%s; -- %%s\n" % (slaveIfName, slaveIfName, slaveIfName) #registerName, registerName, desc
                
        self.wbOthers           = "when others => r_%s_out_ack0 <= '0'; r_%s_out_err0 <= '1';\n" % (slaveIfName, slaveIfName) 
        self.wbs_ackerr         = ["signal r_%s_out_stall : std_logic;\n" % slaveIfName,
                                   "signal r_%s_out_ack0,\n" % slaveIfName,
                                   "       r_%s_out_ack1,\n" % slaveIfName,
                                   "       r_%s_out_err0,\n" % slaveIfName,
                                   "       r_%s_out_err1 : std_logic;\n" % slaveIfName,
                                   "signal r_%s_out_dat0,\n" % slaveIfName,
                                   "       r_%s_out_dat1 : std_logic_vector(31 downto 0);\n"  % slaveIfName]
                                
                                  
        self.wbs_reg_o          = "signal r_%s : t_%s_regs_o;\n" % (slaveIfName, slaveIfName)
        self.wbs_reg_i          = "signal s_%s : t_%s_regs_i;\n" % (slaveIfName, slaveIfName)
        
        self.resetOutput        = ["r_%s_out_stall   <= '0';\n" % slaveIfName,
                                   "r_%s_out_ack0    <= '0';\n" % slaveIfName,
                                   "r_%s_out_err0    <= '0';\n" % slaveIfName,
                                   "r_%s_out_dat0    <= (others => '0');\n" % slaveIfName,
                                   "r_%s_out_ack1    <= '0';\n" % slaveIfName,
                                   "r_%s_out_err1    <= '0';\n" % slaveIfName,
                                   "r_%s_out_dat1    <= (others => '0');\n" % slaveIfName]
        self.resetSignal        = "r_%s.%%s <= %%s;\n" % slaveIfName #registerName, resetvector
        self.others             = "(others => '%s')"
        self.int2slv            = "std_logic_vector(to_unsigned(16#%x#, %s))"
        self.resetSignalArray   = "r_%s.%%s <= (others =>%%s);\n" % slaveIfName #registerName, resetvector
        self.recordPortOut      = "%s_regs_%%s_o : out t_%s_regs_%%s_o;\n" % (slaveIfName, slaveIfName)
        self.recordPortIn       = "%s_regs_%%s_i : in  t_%s_regs_%%s_i;\n" % (slaveIfName, slaveIfName)
        self.recordRegStart     = "type t_%s_regs_%%s is record\n" % slaveIfName
        self.recordRegEnd       = "end record t_%s_regs_%%s;\n\n" % slaveIfName
        self.recordAdrStart     = "type t_%s_adr is record\n" % slaveIfName
        self.recordAdrEnd       = "end record t_%s_adr;\n\n" % slaveIfName
        self.recAdr             = "%s : natural;\n"
        self.constRegAdr        = "constant c_%s_%%s : natural := 16#%%s#; -- %%s 0x%%s, %%s\n" % slaveIfName #name, adrVal, adrVal, rw, msk, desc
        self.constRecAdrStart   = "constant c_%s_adr : t_%s_adr := (\n" % (slaveIfName, slaveIfName)
        self.constRecAdrLine    = "%s => 16#%x#%s -- 0x%02X, %s, _0x%08x %s\n" #name, adrVal, comma/noComma, adrVal, rw, msk, desc
        self.constRecAdrEnd     = ");\n"
        self.signalSlv          = "%s : std_logic_vector(%s-1 downto 0); -- %s\n" #name, idxHi, idxLo, desc
        self.signalSl           = "%s : std_logic; -- %s\n" #name, desc
        self.sdb                = ['constant c_%s_%s_sdb : t_sdb_device := (\n' % (unitname, slaveIfName),
                                   'abi_class     => x"%s", -- %s\n' % ("0000", "undocumented device"),
                                   'abi_ver_major => x"%s",\n' % "01",
                                   'abi_ver_minor => x"%s",\n' % "00",
                                   'wbd_endian    => c_sdb_endian_%s,\n' % "big",
                                   'wbd_width     => x"%s", -- 8/16/32-bit port granularity\n' % self.wbWidth[dataWidth],
                                   'sdb_component => (\n',
                                   'addr_first    => x"%s",\n',
                                   'addr_last     => x"%s",\n',
                                   'product => (\n',
                                   'vendor_id     => x"%016x",\n' % vendId,
                                   'device_id     => x"%08x",\n' % devId,
                                   'version       => x"%s",\n' % '{message:{fill}{align}{width}}'.format(message=version.replace('.', ''), fill='0', align='>', width=8),
                                   'date          => x"%04u%02u%02u",\n' % (now.year, now.month, now.day),
                                   'name          => "%s")));\n' % sdbname.ljust(19)]
        self.sdbReference       = "constant c_%s_%s_sdb : t_sdb_device := work.%s_pkg.c_%s_%s_sdb;\n" % (unitname, slaveIfName, (unitname + '_auto'), unitname, slaveIfName)                            
    
    wbWidth = {8   : '1',
               16  : '3',
               32  : '7', 
               64  : 'f'} 
     
                           
    wrModes = {'_GET'  : 'owr',
               '_SET'  : 'set',
               '_CLR'  : 'clr', 
               '_OWR'  : 'owr',
               '_RW '  : 'owr'} 

    nl          = "\n"
    snl         = ";\n"
    lnl         = "\n)\n" 
  
    def fsmPageSel(self, pageSel):
        if(pageSel == ""):
            return "\n"
        else:    
            return self.wbsPageSelect % pageSel
  

    def fsmRead(self, regList):
        s = []    
        for elem in regList:        
           (name, desc, rwmafs, width, opList, _, _) = elem
           if(rwmafs.find('m') > -1):
               ind = '(v_page)'
           else:
               ind = ""            
           
           for opLine in opList:
               (op, adrList) = opLine
               if((op == "_GET") or (op == "_RW ")):                    
                   if(len(adrList) > 1):
                       #this is sliced
                       adrIdx = 0            
                       for adrLine in adrList:
                           idx = '_%u' % adrIdx
                           (msk, adr) = adrLine
                           #Show comment only the first occurrance of a register name                    
                           if(adrIdx == 0):
                               comment  = desc
                           else:
                               comment  = '\"\"'
                           
                           #calculate register bitslice from adr idx    
                           (idxHi, idxLo)   = mskWidth(msk)
                           sliceWidth       = (idxHi-idxLo+1) 
                           curSlice         = "(%u downto %u)" % ( sliceWidth + adrIdx*self.dataWidth -1, adrIdx*self.dataWidth)
                           baseSlice        = "%u downto %u" % ( sliceWidth -1, 0)
                           adrIdx += 1
                               #append word idx and bitslice
                                
                           #We can't have two drivers for a register. Find out if the register driver is internal or external to the WB core
                           if(rwmafs.find('w') > -1):
                               #if the register can be written to by WB, it is internal. read from WB register 
                               s.append(self.wbReadInt % (name + op + idx, baseSlice, name + ind + curSlice, comment))
                           else:
                               #if the register cannot be written to by WB, it is external. read from input record 
                               s.append(self.wbReadExt % (name + op + idx, baseSlice, name + ind + curSlice, comment))
                   else:
                       (msk, adr) = adrList[0]
                       (idxHi, idxLo)   = mskWidth(msk)
                       sliceWidth       = (idxHi-idxLo+1) 
                       baseSlice        = "%u downto %u" % ( sliceWidth -1, 0)
                       if(rwmafs.find('w') > -1):
                           #if the register can be written to by WB, read from WB register
                           s.append(self.wbReadInt % (name + op, baseSlice, name+ind, desc))
                       else:
                           #if the register cannot be written to by WB, read from input record
                           s.append(self.wbReadExt % (name + op, baseSlice, name+ind, desc))
                   if((rwmafs.find('s') > -1)):             
                       s.append(self.wbStall % name)    
        return s

  

    def fsmWrite(self, regList):
        s = []    
        for elem in regList:        
            (name, desc, rwmafs, width, opList, _, _) = elem
           
            if(rwmafs.find('m') > -1):
                ind = '(v_page)'
            else:
                ind = ""
            opIdx = 0    
            for opLine in opList:
                (op, adrList) = opLine
                adrIdx = 0
                if(op != "_GET"):                    
                    if(len(adrList) > 1):
                        #this is sliced
                        adrIdx=0            
                        for adrLine in adrList:
                            idx = '_%u' % adrIdx
                            if((opIdx == 0) and (adrIdx == 0)):
                                comment = desc
                            else:
                                comment = '\"\"'
                            (msk, adr) = adrLine
                            (idxHi, idxLo) = mskWidth(msk)
                            sliceWidth   = (idxHi-idxLo+1) 
                            curSlice = "(%u downto %u)" % ( sliceWidth + adrIdx*self.dataWidth -1, adrIdx*self.dataWidth)
                            adrIdx += 1
                                                                
                            s.append(self.wbWrite % (name + op + idx, name + ind + curSlice, name + ind + curSlice, self.wrModes[op], comment))
                            
                    else:
                        (msk, adr) = adrList[0]
                        if(opIdx == 0):
                            comment = desc
                        else:
                            comment = '\"\"'
                        s.append(self.wbWrite % (name + op, name+ind, name+ind, self.wrModes[op], comment))
                    if(rwmafs.find('f') > -1):
                        s.append(self.wbWriteWe % (name, name))
                    if((rwmafs.find('s') > -1)):             
                        s.append(self.wbStall % name)     
                    opIdx += 1
        return s     




    def fsmWritePulse(self, regList):
        s = []    
        for elem in regList:        
            (name, _, rwmafs, _, _, _, _) = elem
            if(rwmafs.find('w') > -1):
                if((rwmafs.find('f') > -1)):
                    s.append(self.wbWriteWeZero % (name, name))
                if((rwmafs.find('p') > -1)):
                    if((rwmafs.find('m') > -1)):
                        s.append(self.wbWritePulseZeroArray % (name, name))
                    else:                
                        s.append(self.wbWritePulseZero % (name, name))
                                
        return s 
    
   
    def regs(self, regList):
       namesOut         = []
       namesIn          = []
       recordsOut       = []
       clkdOut          = []        
       recordsIn        = [] + [self.signalSl % ('STALL', 'Stall control for outside entity'),
                                self.signalSl % ('ERR', 'Error control for outside entity')]
       namesIn          = [] + ['STALL',
                                'ERR']                             
       
       clkdIn           = [] + [self.clocks[0], #clkdomain for STALL
                                self.clocks[0]] #clkdomain for ERR
                                
       types            = []
       for elem in regList:
           (name, desc, rwmafs, width, opList, clkd, _) = elem
           
           if(rwmafs.find('m') > -1):
               types += self.multitype(elem)
               if(rwmafs.find('w') > -1):
                   recordsOut += self.multielement(elem)
                   clkdOut.append(clkd)
                   namesOut.append(name)
                   if(rwmafs.find('f') > -1):
                       recordsOut.append(self.signalSl % (name + '_WE', 'WE flag'))
                       clkdOut.append(clkd)
                       namesOut.append(name + '_WE')
               elif(rwmafs.find('r') > -1):            
                   #We can't have two drivers. Only include register in the inputs list if it's not written to be WB IF                    
                   recordsIn += self.multielement(elem)
                   clkdIn.append(clkd)
                   namesIn.append(name)
           else:
               if(rwmafs.find('w') > -1):
                   recordsOut.append(self.reg(elem))
                   clkdOut.append(clkd)
                   namesOut.append(name)
                   if(rwmafs.find('f') > -1):
                       recordsOut.append(self.signalSl % (name + '_WE', 'WE flag'))
                       clkdOut.append(clkd)
                       namesOut.append(name + '_WE')
               elif(rwmafs.find('r') > -1):
                   #We can't have two drivers. Only include register in the inputs list if it's not written to be WB IF 
                   recordsIn.append(self.reg(elem))
                   clkdIn.append(clkd)
                   namesIn.append(name)
                   
       return [types, recordsOut, recordsIn, clkdOut, clkdIn, namesOut, namesIn]           

    
                   
    
    def reg(self, elem):
        (name, desc, _, width, _, _, _) = elem
        
        s = self.signalSlv % (name, width, desc)        
        return s
    


    

    def multitype(self, elem):
        (name, _, _, width, _, _, _) = elem        
        s = []        
        s.append('\n')
        s.append(self.slvSubType % (name, width)) #shift mask to LSB
        s.append(self.slvArrayType % (name, name))
        return s 
    
    def multielement(self, elem, qty=1):
        (name, desc, _, _, _, _, _) = elem        
        s = []        
        if(isinstance(self.pages, int)):
            prefix = ''
        else:
            prefix = 'c_g_'            
        s.append(self.signalSlvArray % (name, name, prefix + str(self.pages) + '-1', desc))
        
            
        return s    
              
    
    def cRegAdr(self, elem):
        (name, desc, rwmafs, _, opList, _, _) = elem
        rw = rwmafs.replace('m', '').replace('a', '')
        for opLine in opList:
            (op, adrList) = opLine
            for adrLine in adrList:
                (msk, adr) = adrLine
                s = self.recAdr % (name + op, adr, adr, rw, msk, desc)    
                    
        return s
    
    def resets(self, regList):
       s = []
       for elem in regList:
           (name, _, rwmafs, _, _, _, rstvec) = elem
           if(rwmafs.find('w') > -1):
               if(rwmafs.find('m') > -1):
                   s.append(self.resetSignalArray % (name, rstvec))                      
               else:
                   s.append(self.resetSignal % (name, rstvec))
               if(rwmafs.find('f') > -1):
                   s.append(self.wbWriteWeZero % (name, ""))    
       s += self.resetOutput           
       return s


class gVhdlStr(object):
   

    def __init__(self, unitname, filename="unknown", author="unknown", email="unknown", version="0.0", date=""):
        self.unitname   = unitname
        self.filename   = filename        
        self.author     = author
        self.version    = version
        
        self.header     = ["--! @file        %s\n" % filename,                 
                           "--  DesignUnit   %s\n" % unitname,                           
                           "--! @author      %s <%s>\n" % (author, email),
                           "--! @date        %s\n" % date,
                           "--! @version     %s\n" % version,                     
                           "--! @copyright   %s GSI Helmholtz Centre for Heavy Ion Research GmbH\n" % now.year,
                           "--!\n"]

        self.headerLPGL =    ["--------------------------------------------------------------------------------\n" 
                              "--! This library is free software; you can redistribute it and/or\n",
                              "--! modify it under the terms of the GNU Lesser General Public\n",
                              "--! License as published by the Free Software Foundation; either\n",
                              "--! version 3 of the License, or (at your option) any later version.\n",
                              "--!\n",
                              "--! This library is distributed in the hope that it will be useful,\n",
                              "--! but WITHOUT ANY WARRANTY; without even the implied warranty of\n",
                              "--! MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU\n",
                              "--! Lesser General Public License for more details.\n",
                              "--!\n",  
                              "--! You should have received a copy of the GNU Lesser General Public\n",
                              "--! License along with this library. If not, see <http://www.gnu.org/licenses/>.\n",
                              "--------------------------------------------------------------------------------\n\n"]                                

        self.headerDetails = []
       
        self.headerWarning =    ["-- ***********************************************************\n",
                                 "-- ** WARNING - THIS IS AUTO-GENERATED CODE! DO NOT MODIFY! **\n",
                                 "-- ***********************************************************\n",
                                 "--\n",
                                 "-- If you want to change the interface,\n"]
                            
        self.headerModify  =    "-- modify %s.xml and re-run 'python wbgenplus.py %s.xml' !\n\n"
                            
        self.libraries  = ["library ieee;\n",
                           "use ieee.std_logic_1164.all;\n",
                           "use ieee.numeric_std.all;\n",
                           "use work.wishbone_pkg.all;\n"]
        self.pkg        =  "use work.%s%%s_pkg.all;\n\n" % unitname                   
           
        self.packageStart       = "package %s_pkg is\n\n" % unitname
        self.componentStart     = "component %s is\n" % unitname
        self.componentMid       = "Port(\n"    
        self.componentEnd       = [");\n",
                                   "end component;\n\n"] 
        self.packageBodyStart   = "package body %s_pkg is\n" % unitname 
        self.packageEnd         = "end %s_pkg;\n" % unitname    
        
        self.entityStart        = "entity %s is\n" % unitname
        self.genStart           = "generic(\n"
        self.genEnd             = ");\n" 
         
        self.entityMid   = "Port(\n"
      
        self.entityEnd   = ");\nend %s;\n\n" % unitname
        
        self.archDecl    = "architecture rtl of %s is\n\n" % unitname
        self.archStart   = "\n\nbegin\n\n"
        self.archEnd     = "end rtl;\n"
        self.genport     = "g_%s : %s := %s%s -- %s\n" #name, type, default
        self.instGenPort    = "g_%s => g_%s%s\n" 
        self.instStart      = "INST_%s_auto : %s_auto\n" % (unitname, unitname)
        self.instGenStart   = "generic map (\n"
        self.instGenEnd     = ")\n"
        self.instPortStart  = "port map (\n"
        self.instPortEnd    = ");\n"
  


          
    nl          = "\n"
    snl         = ";\n"
    lnl         = "\n)\n"    

    masterIf    = ["%s_o : out t_wishbone_master_out;\n", # name
                   "%s_i : in  t_wishbone_master_in := ('0', '0', '0', '0', '0', x\"00000000\")"] # name
    

     

class wbsIf():
    
    def __init__(self, unitname, name, startAdr, pageSelect, pages, dataWidth, vendId, devId, sdbname, clocks):
        self.regs           = []        
        self.syncAssignList = []
        self.syncProcList   = []
        self.syncRegList    = []         
        self.portList       = []
        self.stubPortList   = []
        self.stubInstList   = []
        self.stubSigList    = []
        self.regList        = []   
        self.recordList     = []
        self.adrList        = []
        self.fsm            = []
        
        self.clocks     = clocks
        self.name       = name        
        self.startAdr   = startAdr
        self.pageSelect = pageSelect
        self.pages      = pages
        self.dataWidth  = dataWidth
        self.v = wbsVhdlStr(pages, unitname, name, dataWidth, vendId, devId, sdbname, clocks)        
        self.c = wbsCStr(pages, unitname, name, vendId, devId)
    
    def sliceMsk(self, aMsk):
                
        
        mskList = []
        msk     = 0 + aMsk
        (idxHi, idxLo) = mskWidth(msk)
        regWidth    = (idxHi-idxLo+1)
        words       = regWidth / self.dataWidth
        for i in range(0, words):
            mskList.append(2**self.dataWidth-1)                
            msk >>= self.dataWidth
        if(msk):
            mskList.append(msk)
        return (mskList)     
    
    def getLastAdr(self, elem):
        
        (_, _, _, _, opList, _, _) = elem
        #print opList
        (_, adrList) = opList[-1]
        #print adrList
        (_, adr)  = adrList[-1]
        #print adr
        return adr          
    
    def addOp(self, opList, startAdr, offs, bigMsk, op):
        adrList = []        
        
        if startAdr == None:
            if len(self.regs) == 0 and len(opList) ==  0:
                adr = self.startAdr
            else:
                if len(opList) >  0:
                    #print opList
                    (_, oldAdrList) = opList[-1]
                    (_, oldAdr)  = oldAdrList[-1]
                    adr = oldAdr + offs
                else:            
                    adr = self.getLastAdr(self.regs[-1]) + offs
        else:
            adr = (startAdr // offs) * offs          
        #print "OP <%s> adr is %x" % (op, adr)
        mskList = self.sliceMsk(bigMsk)
        for msk in mskList:
            adrList.append([msk, adr])
            adr += offs
       
        #print '*' * 10
        #print opList
        opList.append([op, adrList])
        #print '+' * 10        
        #print "OP: %s Msk: %u Oplsit: %u adrList %u" % (op, len(mskList), len(opList), len(adrList))
        
        
    
    def addReg(self, name, desc, bigMsk, rwmafs, startAdr=None, offs=4, clkdomain="sys", rstvec=None):
        opList  = []        
        newElem = []            
        adr = startAdr
              
        if(rwmafs.find('a') > -1): # atomic
            if rwmafs.find('r') > -1:
                self.addOp(opList, adr, offs, bigMsk, '_GET')
                adr = None
            if rwmafs.find('w') > -1:    
                if rwmafs.find('r') > -1:            
                    self.addOp(opList, adr, offs, bigMsk, '_SET')                
                    self.addOp(opList, None, offs, bigMsk, '_CLR')        
                else:    
                    self.addOp(opList, adr, offs, bigMsk, '_SET')
        else:
            op = str()        
            if rwmafs.find('rw') > -1:
                op = '_RW '
            elif rwmafs.find('r') > -1:    
                op = '_GET'
            elif rwmafs.find('w') > -1:
                op = '_OWR'
            self.addOp(opList, adr, offs, bigMsk, op)      

        
        (idxHi, idxLo) = mskWidth(bigMsk)
        width   = (idxHi-idxLo+1)
        newElem = [name, desc, rwmafs, width, opList, clkdomain, rstvec]
        
        self.regs.append(newElem)      
    
  
    def renderStubPorts(self):
        a = []
        a += self.v.slaveIf        
        self.stubPortList = a        
  
    def renderStubSigs(self):
        self.stubSigList += self.v.slaveSigs # no need to indent, we'll do it later with all IF lists together

        
    def renderStubInst(self):
        self.stubInstList += self.v.slaveInst # no need to indent, we'll do it later with all IF lists together    
  
    def renderPorts(self):
        self.portList += self.v.slaveIf # no need to indent, we'll do it later with all IF lists together
                
    

    def renderSdb(self):
        
        hiAdr = self.getLastAdr(self.regs[-1])
        (idxHi, idxLo) = mskWidth(hiAdr)
        adrRange = 2**(idxHi+1)-1
        self.v.sdb[7] = self.v.sdb[7] % ('0' * 16) 
        self.v.sdb[8] = self.v.sdb[8] % ("%016x" % adrRange)
        
    
    def renderFsm(self):
               
        
        hdr0 = iN(self.v.wbs0, 1) 
        
        rst = adj(self.v.resets(self.regs), ['<='], 4)       
        
        hiAdr = self.getLastAdr(self.regs[-1])
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
           
        
        print "Slave <%s>: Found %u register names, last Adr is %08x, Adr Range is %08x, = %u downto %u\n" % (self.name, len(self.regs), hiAdr, adrMsk, msbIdx-1, lsbIdx)
        print "\n%s" % ('*' * 80) 
        hdr1 = self.v.wbs1_0 
        hdr1.append(self.v.wbs1_1 % self.clocks[0]) 
        hdr1 += self.v.wbs1_2

        szero = adj(self.v.fsmWritePulse(self.regs), ['<=', '--'], 4)
        
        hdr1[3] = hdr1[3] % (('%u downto %u' % (msbIdx-1, lsbIdx)), padding)
        hdr1    = iN(hdr1, 3)
        
        psel    = iN([self.v.fsmPageSel(self.pageSelect)], 4)
        
        hdr2    = iN(self.v.wbs2, 4)  
        swr     = adj(self.v.fsmWrite(self.regs), ['=>', 'r_', '<=', 'v_dat_i', '--'], 7)    
              
        
        mid0    = iN([self.v.wbOthers], 7)
        mid1    = iN(self.v.wbs3, 5)
        
        srd     = adj(self.v.fsmRead(self.regs), ['=>', '<=', "--"], 7)
        ftr     = iN(self.v.wbs4, 1)
        wbs5    = []
        wbs5.append(self.v.wbs5_0 % self.clocks[0])
        wbs5.append(self.v.wbs5_1)
        wbs5.append(self.v.wbs5_2 % self.clocks[0])
        wbs5.append(self.v.wbs5_3 % self.clocks[0])
        con     = adj(wbs5, ['<=', "--"], 1)
        self.fsmList = hdr0 + rst + hdr1 + szero + psel +  hdr2 + swr + mid0 + mid1 + srd + mid0 + ftr + con
        
    def renderAdr(self):
        a = []
        b = []
        adrHi = self.getLastAdr(self.regs[-1])
        (idxHi, idxLo) = mskWidth(adrHi)
        
        adrx = ("%0" + str((idxHi+1+3)/4) + "x")
        mskx = ("%0" + str(self.dataWidth/4) + "x")
        #print adrx, mskx
        for elem in self.regs:        
            (name, desc, rwmafs, width, opList, clkdomain, _) = elem
            rw = rwmafs.replace('m', '').replace('a', '')
            opIdx = 0            
            for opLine in opList:
                
                (op, adrList) = opLine
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
                        comment = desc
                    else:
                        comment = '\"\"'
                    a.append(self.v.constRegAdr % (name + op + idx, adrx % adr, rw, mskx % msk, comment ))
                    b.append(self.c.constRegAdr % (name + op + idx, adrx % adr, rw, mskx % msk, comment ))
                    adrIdx += 1
                opIdx += 1            
        self.vAdrList = adj(a, [ ':', ':=', '--', '0x', ':'], 2)
        self.cAdrList = adj(b, [ '   0x', '//', '_0x', ','], 0)

    def renderSync(self):
                
        
        a = []        
        p = []
        (_, _, _, clkdO, clkdI, namesO, namesI) = self.v.regs(self.regs)
        
        for clkd in self.clocks:
            clkdOut     = []
            clkdIn      = []
            namesOut    = []
            namesIn     = []            
            a.append(self.v.clkdomainComment % (clkd,"out"))
            
            #rearrange
            for i in range(0, len(namesO)):             
                if(clkdO[i] == clkd):
                    namesOut.append(namesO[i])                    
                    clkdOut.append(clkdO[i])
            for i in range(0, len(namesI)):             
                if(clkdI[i] == clkd):
                    namesIn.append(namesI[i])                    
                    clkdIn.append(clkdI[i])
            
            for i in range(0, len(namesOut)):             
                name = namesOut[i]
                clkd = clkdOut[i]
                           
                if(clkdOut[i] == self.clocks[0]):
                    #direct assign
                    #slave_regs_clk_wb_o.X <= r_slave.X
                    a.append(self.v.syncAssignOutD % (clkd, name, name))
                else:
                    #synced assign
                    #slave_regs_clk_xyz_o.X      <= r_slave_regs_clk_xyz_o_2.X
                    a.append(self.v.syncAssignOutI0 % (clkd, name, clkd, name))
                    #r_slave_regs_clk_xyz_o_0.X  <= r_slave.X
                    a.append(self.v.syncAssignOutI1 % (clkd, name, name)) 
           #add process
                   
            
            if(len(namesOut)>0 and not clkd == self.clocks[0]):
                p.append(self.v.syncProcStart0 % (clkd, 'out', clkd))
                p.append(self.v.syncProcStart1 % clkd)
                p.append(self.v.syncProcMid)                
                p.append(self.v.syncProcReg % (clkd, 'o', '1', clkd, 'o', '0'))
                p.append(self.v.syncProcReg % (clkd, 'o', '2', clkd, 'o', '1'))
                p += self.v.syncProcEnd
                    
            a.append(self.v.clkdomainComment % (clkd,"in"))
            for i in range(0, len(namesIn)):
                if(clkdIn[i] == self.clocks[0]):
                    #direct assign
                    #s_slave.X <= slave_regs_clk_wb_i.X
                    a.append(self.v.syncAssignInD % (namesIn[i], clkdIn[i], namesIn[i]))
                else:
                    #synced assign
                    #r_slave_regs_clk_xyz_i_0.X <= slave_regs_clk_xyz_i.X
                    a.append(self.v.syncAssignInI0 % (clkdIn[i], namesIn[i], clkdIn[i], namesIn[i]))
                    #s_slave.X <= r_slave_regs_clk_xyz_i_2.X
                    a.append(self.v.syncAssignInI1 % (namesIn[i], clkdIn[i], namesIn[i])) 
                    #add process
                    #r_slave_regs_clk_xyz_o_1 <= r_slave_regs_clk_xyz_o_0;
                    
            
            if(len(namesIn)>0 and not clkd == self.clocks[0]):
                p.append(self.v.syncProcStart0 % (clkd, 'in', clkd))
                p.append(self.v.syncProcStart1 % clkd)
                p.append(self.v.syncProcMid)
                p.append(self.v.syncProcReg % (clkd, 'i', '1', clkd, 'i', '0'))
                p.append(self.v.syncProcReg % (clkd, 'i', '2', clkd, 'i', '1'))
                p += self.v.syncProcEnd
                
            a.append("\n")
        
        
        self.syncAssignList += a
        self.syncProcList   += p
        
    def renderRecords(self):
        a = []
        
        (types, recordsOut, recordsIn, clkdOut, clkdIn, _, _) = self.v.regs(self.regs)
        a += types
        a += self.v.nl
        #render whole out record
        if(len(recordsOut)>0):
            a.append(self.v.recordRegStart % 'o')
            a += iN(recordsOut, 1)        
            a.append(self.v.recordRegEnd % 'o')
    
            #render sub sets of out record
            for clkd in self.clocks:
                tmp = []
                for i in range(0, len(recordsOut)):             
                    if(clkdOut[i] == clkd):
                        tmp.append(recordsOut[i])
                if(len(tmp) > 0):
                    suffix = 'clk_'+clkd                
                    self.portList.append(self.v.recordPortOut % (suffix, suffix))
                    self.stubSigList.append(self.v.slaveSigsRegs % (clkd, 'o', clkd, 'o'))
                    self.stubInstList.append(self.v.slaveInstRegs % (clkd, 'o', clkd, 'o'))
                    if(clkd != self.clocks[0]):                
                        self.syncRegList.append(self.v.syncReg % (clkd, 'o', '0', clkd, 'o'))
                        self.syncRegList.append(self.v.syncReg % (clkd, 'o', '1', clkd, 'o'))
                        self.syncRegList.append(self.v.syncReg % (clkd, 'o', '2', clkd, 'o'))
                    a.append(self.v.recordRegStart % (suffix+'_o'))                
                    a += iN(tmp, 1) 
                    a.append(self.v.recordRegEnd   % (suffix+'_o'))
                else:
                    print "Info: no outgoing registers found for clk domain %s" % clkd 
        
        if(len(recordsIn)>0):                
            #render whole in record
            a.append(self.v.recordRegStart % 'i')
            a += iN(recordsIn, 1)        
            a.append(self.v.recordRegEnd % 'i')
            for clkd in self.clocks:
                tmp = []
                for i in range(0, len(recordsIn)):             
                    if(clkdIn[i] == clkd):
                        tmp.append(recordsIn[i])
                if(len(tmp) > 0):
                    suffix = 'clk_'+clkd               
                    self.portList.append(self.v.recordPortIn % (suffix, suffix))
                    self.stubSigList.append(self.v.slaveSigsRegs % (clkd, 'i', clkd, 'i'))
                    self.stubInstList.append(self.v.slaveInstRegs % (clkd, 'i', clkd, 'i'))
                    if(clkd != self.clocks[0]):
                        self.syncRegList.append(self.v.syncReg % (clkd, 'i', '0', clkd, 'i'))
                        self.syncRegList.append(self.v.syncReg % (clkd, 'i', '1', clkd, 'i'))
                        self.syncRegList.append(self.v.syncReg % (clkd, 'i', '2', clkd, 'i'))
                    a.append(self.v.recordRegStart % (suffix+'_i'))            
                    a += iN(tmp, 1) 
                    a.append(self.v.recordRegEnd   % (suffix+'_i'))
                else:
                    print "Info: no incoming registers found for clk domain %s" % clkd      
        
        #proper line endings for portlist
        #for i in range(0, len(self.portList)-1):
        #    self.portList[i] += ";\n"
                
        self.recordList = adj(a, [ ':', '--'], 0)
        

    
    
                        
    def renderRegs(self):
        a = []
        (_, recordsOut, recordsIn, _, _, _, _) = self.v.regs(self.regs)
        if(len(recordsOut)>0):
            a.append(self.v.wbs_reg_o)
        if(len(recordsIn)>0):        
            a.append(self.v.wbs_reg_i)
        a += (self.v.wbs_ackerr)        
        self.regList = a + self.syncRegList# no need to indent, we'll do it later with all IF lists together

    def renderAll(self):
        self.renderRecords()        
        self.renderStubPorts()
        self.renderStubSigs()
        self.renderStubInst()
        self.renderPorts()
        self.renderSync()
        self.renderAdr()        
        self.renderRegs()
        self.renderFsm()
        self.renderSdb()

    



    
codeGen = set(['vhdl', 'C', 'C++'])    

genTypes = {'u'        : 'unsigned',
            'uint'     : 'natural', 
            'int'      : 'integer', 
            'bool'     : 'boolean',
            'string'   : 'string',
            'sl'       : 'std_logic',
            'slv'      : 'std_logic_vector'}    


vendorIdD   = {'GSI'       : 0x0000000000000651,
               'CERN'      : 0x000000000000ce42}


                
  
    
def mergeIfLists(slaveList=[], masterList = []):
    uglyPortList = []
    uglyInstList = []
    syncList     = []    
    
    clocks = slaveList[0].clocks    
    for clock in clocks:
        uglyPortList += ["clk_%s_i   : in  std_logic;\n" % clock]
        uglyInstList += ["clk_%s_i => clk_%s_i,\n" % (clock, clock)]    
    
    uglyPortList    += ["rst_n_i   : in  std_logic;\n\n"]
    uglyInstList    += ["rst_n_i => rst_n_i,\n\n"]                   
    stubPortList    = [] + uglyPortList
    stubInstList    = [] + uglyInstList
    stubSigList     = []                   
    recordList      = []                   
    uglyRegList     = []
    uglyAdrList     = []
    cAdrList        = []     
    fsmList         = [] 
    genList         = []
    instGenList     = []
    sdbList         = []
    sdbRefList      = [] 
    
    v = gVhdlStr("")
    for slave in slaveList:
        uglyPortList += slave.portList
        stubPortList += slave.stubPortList
        stubInstList += slave.stubInstList
        #deal with vhdl not wanting a semicolon at the last port entry        
        if(slave != slaveList[-1]):
            uglyPortList[-1] += ";\n"
            stubPortList[-1] += ";\n"
            stubInstList[-1] += ",\n"
        else:
            uglyPortList[-1] += "\n"
            stubPortList[-1] += "\n"
            stubInstList[-1] += "\n"
        uglyPortList += ["\n"]    
        cAdrList     += slave.c.sdbVendorID
        cAdrList     += slave.c.sdbDeviceID
        cAdrList     += '\n'
        cAdrList     += commentLine("//","Address Map", slave.name)        
        cAdrList     += slave.cAdrList
        cAdrList     += "\n"
        uglyAdrList  += iN(commentLine("--","WBS Adr", slave.name), 1) 
        uglyAdrList  += slave.vAdrList
        uglyAdrList  += "\n"
        uglyRegList  += iN(commentLine("--","WBS Regs", slave.name),1) 
        uglyRegList  += adj(slave.regList, [' is ', ':', ':=', '--'], 1)
        uglyRegList  += "\n"
        fsmList      += iN(commentBox("--","WBS FSM", slave.name), 1)
        fsmList      += slave.fsmList   
        fsmList      += "\n\n"
        syncList     += iN(commentBox("--","Sync Signal Assignments", slave.name), 1)
        syncList     += adj(slave.syncAssignList, ['<='], 1)
        if(len(slave.syncProcList)>0):        
            syncList     += iN(commentBox("--","Sync Processes", slave.name), 1)        
            syncList     += adj(slave.syncProcList, ['<='], 1) 
            syncList     += "\n\n"
        recordList   += iN(commentLine("--","WBS Register Record", slave.name), 1) 
        recordList   += adj(slave.recordList, [ ':', '--'], 1)
             
        stubSigList  += slave.stubSigList
        sdbList      += slave.v.sdb + ['\n']
        sdbRefList   += [slave.v.sdbReference]
    
    for master in masterList:
        uglyPortList += master.portList
        uglyAdrList  += master.AdrList       
        uglyRegList  += master.regList    
    
        
    portList        = adj(uglyPortList, [':', ':=', '--'], 1)    
    stubPortList    = adj(stubPortList, [':', ':=', '--'], 1) 
    stubInstList    = adj(stubInstList, ['=>', '--'], 1) 
    stubSigList     = adj(stubSigList,  [':', ':=', '--'], 1)      

    
    recordList  = iN(commentBox("--","", "WB Slaves - Control Register Records"), 1) + ['\n']\
                + recordList    
    
    regList     = iN(commentBox("--","", "WB Registers"), 1) + ['\n']\
                + uglyRegList
                
                
    vAdrList     = iN(commentBox("--","", "WB Slaves - Adress Maps"), 1) + ['\n']\
                + uglyAdrList
                
    if( len(genMiscD) > 0):
        #last element is len(genMiscD) + len(genIntD) -1         
        lastIdx = len(genMiscD) + len(genIntD) -1  
    else:
        #last element is len(genIntD) -1
        lastIdx = len(genIntD) -1  
    
    idx = 0    
    for genName in genIntD.iterkeys():
        (genType, genVal, genDesc) = genIntD[genName]
        if(idx == lastIdx):
            lineEnd = ''
            instLineEnd = ''
        else:
            lineEnd = ';'
            instLineEnd = ','
        genList.append(v.genport % (genName, genType, genVal, lineEnd, genDesc))
        instGenList.append(v.instGenPort % (genName, genName, instLineEnd))
        idx += 1
    for genName in genMiscD.iterkeys():
        if(idx == lastIdx):
            lineEnd = ''
            instLineEnd = ''
        else:
            lineEnd = ';'
            instLineEnd = ','
        (genType, genVal, genDesc) = genMiscD[genName]
        genList.append(v.genport % (genName, genType, genVal, lineEnd, genDesc))
        instGenList.append(v.instGenPort % (genName, genName, instLineEnd))
        idx += 1
    genList = adj(genList, [':', ':=', '--'], 1)
    instGenList = adj(instGenList, ['=>', '--'], 1)              
    #Todo: missing generics 
    return [portList, recordList, regList, sdbList, sdbRefList, vAdrList, fsmList, syncList, genList, cAdrList, stubPortList, stubInstList, stubSigList, instGenList]        

def parseXML(xmlIn):
    xmldoc      = minidom.parse(xmlIn)   
    global unitname
    global author 
    global version
    global email    
    
    if (len(xmldoc.getElementsByTagName('wbdevice'))==0):
        print "No <wbdevice> tag found"
        sys.exit(2)
        
    author   = xmldoc.getElementsByTagName('wbdevice')[0].getAttribute('author')
    version  = xmldoc.getElementsByTagName('wbdevice')[0].getAttribute('version')
    email    = xmldoc.getElementsByTagName('wbdevice')[0].getAttribute('email')

    clockList = []    
    clocks = xmldoc.getElementsByTagName('clockdomain')
    if(len(clocks) > 0):    
        for clock in clocks:
            if(clock.hasAttribute("name")):
                clockList += [clock.getAttribute("name")]
            else:
                print "Clock must have a name!"
                sys.exit(2)
    else:
        clockList += ["sys"]        
            
    
    genericsParent = xmldoc.getElementsByTagName('generics')
    if len(genericsParent) > 1:
        print "There must be exactly 1 generics tag!"
        sys.exit(2)
    elif len(genericsParent) == 1:    
        genericsList = genericsParent[0].getElementsByTagName('item')
        print "Found %u generics\n" % len(genericsList)   
        for generic in genericsList:
            genName = generic.getAttribute('name')
            genType = generic.getAttribute('type')
            genVal  = generic.getAttribute('value')
            genDesc = generic.getAttribute('comment')
            if genTypes.has_key(genType):
                genType = genTypes[genType]               
                if(genType == 'natural'):
                    aux = str2int(genVal)
                    if(aux == None):            
                        print "Generic <%s>'s numeric value <%s> is invalid" % (genName, genVal)
                    else:        
                        genVal = aux
                        genIntD[genName] = [ genType , genVal, genDesc ]
                else:
                    genMiscD[genName] = [ genType , genVal, genDesc ]    
            else:
                print "%s is not a valid type" % generic.getAttribute('type')
                sys.exit(2)
 
        
    slaveIfList = xmldoc.getElementsByTagName('slaveinterface')
    print "Found %u slave interfaces\n" % len(slaveIfList)    
    for slaveIf in slaveIfList:
        
        genericPages = False 
        name    = slaveIf.getAttribute('name')
        ifWidth = str2int(slaveIf.getAttribute('data'))
        print "Slave <%s>: %u Bit wordsize" % (name, ifWidth)
        pages   = slaveIf.getAttribute('pages')
        #check integer generic list
        for genName in genIntD.iterkeys():
            if(pages.find(genName) > -1):
                genericPages = True                
        
        if(not genericPages):        
            aux = str2int(pages)
            if(aux == None):            
                print "Slave <%s>: Pages' numeric value <%s> is invalid. Defaulting to 0" % (name, pages)
                pages = 0
            else:        
                pages = aux
    
        
        #sdb record
        sdb = slaveIf.getElementsByTagName('sdb')
        vendId      = sdb[0].getAttribute('vendorID')
        prodId      = sdb[0].getAttribute('productID')
        #check vendors
        if vendorIdD.has_key(vendId):
            print "Slave <%s>: Known Vendor ID <%s> found" % (name, vendId)            
            vendId = vendorIdD[vendId]
             
        else:
            aux = str2int(vendId)
            if(aux == None):            
                print "Slave <%s>: Invalid Vendor ID <%s>!" % (name, vendId)
                sys.exit(2)
            else:
                vendId = aux                
                print "Slave <%s>: Unknown Vendor ID <%016x>" % (name, vendId)                
                
        
        aux = str2int(prodId)
        if(aux == None):            
                print "Slave <%s>: Invalid Product ID <%s>!" % (name, prodId)
        else:
            prodId = aux     
                
        sdbname     = sdb[0].getAttribute('name')
        if(len(sdbname) > 19):
            print "Slave <%s>: Sdb name <%s> is too long. It has %u chars, allowed are 19" % (name, sdbname, len(sdbname))
            sys.exit(2)
            
        tmpSlave    = wbsIf(unitname, name, 0, '', pages, ifWidth, vendId, prodId, sdbname, clockList) 
        
        selector = ""
        #name, adr, pages, selector
        #registers
        registerList = slaveIf.getElementsByTagName('reg')
        for reg in registerList:
            if reg.hasAttribute('name'):            
                regname = reg.getAttribute('name')
            else:
                print "Register must have a name!"
                sys.exit(2)
            
            if reg.hasAttribute('comment'):      
                regdesc = reg.getAttribute('comment')
            else:        
                print "Register must have a comment!"
                sys.exit(2)
            
            regadr = None       
            if reg.hasAttribute('address'):            
                regadr = reg.getAttribute('address')            
                aux = str2int(regadr)
                if(aux == None):            
                    print "Slave <%s>: Register <%s>'s supplied address <0x%x> is invalid, defaulting to auto" % (name, regname, regadr)
                regadr = aux            
                print "Slave <%s>: Register <%s> using supplied address <0x%x>, enumerating from there" % (name, regname, regadr)
                
            regrwmf    = str()
            if reg.hasAttribute('read'):
                if reg.getAttribute('read') == 'yes':            
                    regrwmf += 'r'    
            if reg.hasAttribute('write'):        
                if reg.getAttribute('write') == 'yes':
                    regrwmf += 'w'
            if reg.hasAttribute('paged'):
                if reg.getAttribute('paged') == 'yes':
                    regrwmf += 'm'
            if reg.hasAttribute('access'):
                if reg.getAttribute('access') == 'atomic':
                    regrwmf += 'a'
            if reg.hasAttribute('weflag'):
                if reg.getAttribute('weflag') == 'yes':            
                    regrwmf += 'f'
            if reg.hasAttribute('autostall'):
                if reg.getAttribute('autostall') == 'yes':            
                    regrwmf += 's'
            if reg.hasAttribute('pulse'):
                if reg.getAttribute('pulse') == 'yes':            
                    regrwmf += 'p'        
            if reg.hasAttribute('selector'):            
                if reg.getAttribute('selector') == 'yes':            
                    if(selector == ""):            
                        selector = regname
            regclk = clockList[0]                
            if reg.hasAttribute('clock'):
                regclk = reg.getAttribute('clock')
             
            if reg.hasAttribute('mask'):      
                regmsk    = reg.getAttribute('mask')
                genericMsk = False
                #check integer generic list
                for genName in genIntD.iterkeys():
                    if(regmsk.find(genName) > -1):
                        genericMsk = True          

                #check conversion function list
                if(not genericMsk):
                    aux = str2int(regmsk)
                    if(aux == None):
                        aux = 2^ int(ifWidth) -1
                        print "Slave <%s>: Register <%s>'s supplied mask <%s> is invalid, defaulting to %x" % (name, regname, regmsk, aux)
                    elif( (regmsk.find('0x') == 0) or (regmsk.find('0b') == 0) ):
                        #it's a mask. treat as such
                        regmsk = aux
                    else:
                        #it's decimal and therefore the bitwidth. make a bitmask                        
                        regmsk = 2**aux-1
                else:
                     #careful, using generics in register width probably causes more trouble than it's worth
                     print "Slave <%s>: Register <%s>'s using supplied generic width <%s>" % (name, regname, regmsk)
            else:        
                print "Slave <%s>: No mask for Register <%s> supplied, defaulting to 0x%x" % (name, regname, 2**ifWidth-1)
                regmsk = 2**ifWidth-1

            rstvec = tmpSlave.v.others % "0"    
            if reg.hasAttribute('reset'):
                print "Found Reset for %s" % regname
                aux = reg.getAttribute('reset')                 
                if(aux == "zeroes"):
                    rstvec = tmpSlave.v.others % "0"    
                elif(aux == "ones"):
                    rstvec = tmpSlave.v.others % "1"
                else:    
                    aux = str2int(aux)
                    if(aux != None):
                        [hi, lo] = mskWidth(regmsk)
                        rstvec = tmpSlave.v.int2slv % (aux, hi-lo+1)
                    else:
                        rstvec = tmpSlave.v.others % "0"
                     
            tmpSlave.addReg(regname, regdesc, regmsk, regrwmf,  regadr, ifWidth/8, regclk, rstvec)
            #x.addSimpleReg('NEXT2',     0xfff,  'rm',   "WTF")
        if(isinstance(pages, int)):
            if((selector != '') and (pages > 0)):    
                print "Slave <%s>: Interface has %u memory pages. Selector register is %s" % (name, pages, selector)    
                tmpSlave.pageSelect = selector    
                tmpSlave.pages      = pages
        elif(selector != ''):
                print "Slave <%s>: Interface has %s memory pages. Selector register is %s" % (name, pages, selector)                 
                tmpSlave.pageSelect = selector    
                tmpSlave.pages      = pages    
            
        tmpSlave.renderAll()    
        ifList.append(tmpSlave)
        


def writeStubVhd(filename):
    
    
    if os.path.isfile(mypath + filename):
        print "!!! Outer entity %s already exists !!!\n" % filename
        if not force:
            print "I don't want to accidentally trash your work. To force overwrite, use '-f' or '--force' option"
            return
        else:
            print "Overwrite forced"
            
    print "Generating stub entity           %s" % filename        
    fo = open(mypath + filename, "w")
    v = gVhdlStr(unitname, filename, author, email, version, date)

    header = adj(v.header + ['\n'], [':'], 0)
    
    for line in header:
        fo.write(line)
    fo.write("--TODO: This is a stub, finish/update it yourself\n")
    fo.write("--! @brief *** ADD BRIEF DESCRIPTION HERE ***\n")
    fo.write("--!\n")
                      
    for line in v.headerLPGL:
        fo.write(line)
    
    libraries = v.libraries + [v.pkg % '_auto']
    for line in libraries:
        fo.write(line)
        
    fo.write(v.entityStart)
    if(len(genIntD) + len(genMiscD) > 0):
        fo.write(v.genStart)
        for line in genList:   
            fo.write(line)
        fo.write(v.genEnd)
    
    fo.write(v.entityMid)
    for line in stubPortList:
        fo.write(line)
        
    fo.write(v.entityEnd)
    
    fo.write(v.archDecl)
    for line in stubSigList:
        fo.write(line)
    
    fo.write(v.archStart)
    

    a = []
    a.append(v.instStart)        
    
    #if(len(genIntD) + len(genMiscD) > 0):
    #   a.append(v.instGenStart)
    #   a += instGenList
    #   a.append(v.instGenEnd)    
    a.append(v.instPortStart)
    a += stubInstList
    a.append(v.instPortEnd)
    a = iN(a, 1) 
    for line in a:
        fo.write(line)
        
    fo.write(v.archEnd)
    
    fo.close

def writeMainVhd(filename):

    print "Generating WishBone core entity  %s" % filename 
    
    fo = open(mypath + filename, "w")
    v = gVhdlStr(autoUnitName, filename, author, email, version, date)

    header = adj(v.header + ['\n'], [':'], 0)
    for line in header:
        fo.write(line)
    fo.write("--! @brief AUTOGENERATED WISHBONE-SLAVE CORE FOR %s.vhd\n" % unitname)
    fo.write("--!\n")        
        
    for line in v.headerLPGL:
        fo.write(line)
    warning = [] + v.headerWarning
    warning.append(v.headerModify % (unitname, unitname))    
    for line in warning:
        fo.write(line)
    libraries = v.libraries + [v.pkg % '']
    for line in libraries:
        fo.write(line)
        
    fo.write(v.entityStart)
    if(len(genIntD) + len(genMiscD) > 0):
        fo.write(v.genStart)
        for line in genList:   
            fo.write(line)
        fo.write(v.genEnd)
    
    fo.write(v.entityMid)
    for line in portList:
        fo.write(line)
        
    fo.write(v.entityEnd)
    
    fo.write(v.archDecl)
    for line in regList:
        fo.write(line)
    
    fo.write(v.archStart)

    for line in syncList:
        fo.write(line)    
    
    for line in fsmList:
        fo.write(line)
    
    fo.write(v.archEnd)
    
    fo.close

def writePkgVhd(filename):

    print "Generating WishBone inner core package %s" % filename    
    
    fo = open(mypath + '/' + filename, "w")
    
    v = gVhdlStr(autoUnitName, filename, author, email, version, date)

    header = adj(v.header + ['\n'], [':'], 0)
    for line in header:
        fo.write(line)
    fo.write("--! @brief AUTOGENERATED WISHBONE-SLAVE PACKAGE FOR %s.vhd\n" % unitname)
    fo.write("--!\n")     
    for line in v.headerLPGL:
        fo.write(line)
    warning = [] + v.headerWarning
    warning.append(v.headerModify % (unitname, unitname))    
    for line in warning:
        fo.write(line)
    libraries = v.libraries
    for line in libraries:
        fo.write(line)    
    
    fo.write(v.packageStart)
    
    for line in vAdrList:
        fo.write(line)    
    
    decl = []
    for line in recordList:
        decl.append(line)
    decl += (iN(commentLine("--", "Component", autoUnitName), 1)) 
    
    for line in decl:
        fo.write(line)    
    
    decl = []
    decl.append(v.componentStart)
    if(len(genIntD) + len(genMiscD) > 0):
        decl.append(v.genStart)
        for line in genList:   
            decl.append(line)
        decl.append(v.genEnd)
    decl.append(v.entityMid)
    for line in portList:
        decl.append(line)
    decl += v.componentEnd
    
    for line in sdbList:
        decl.append(line)
   
    decl = iN(decl, 1)
    for line in decl:
        fo.write(line)
    
        
    
    fo.write(v.packageEnd)
    fo.write(v.packageBodyStart)
    fo.write(v.packageEnd)
    
    fo.close

def writeStubPkgVhd(filename):

    if os.path.isfile(mypath + filename):
        print "!!! Outer package stub %s already exists !!!\n" % filename
        if not force:
            return
        else:
            print "Overwrite forced"
            
    print "Generating stub outer package %s" % filename    
    
    fo = open(mypath + '/' + filename, "w")
    
    v = gVhdlStr(unitname, filename, author, email, version, date)

    header = adj(v.header + ['\n'], [':'], 0)
    for line in header:
        fo.write(line)
    fo.write("--TODO: This is a stub, finish/update it yourself\n")    
    fo.write("--! @brief Package for %s.vhd\n" % unitname)
    fo.write("--! If you modify the outer entity, don't forget to update this component! \n")
    fo.write("--!\n")     
    for line in v.headerLPGL:
        fo.write(line)
    
    libraries = v.libraries
    for line in libraries:
        fo.write(line)    
    
    fo.write(v.packageStart)
       
    decl = []
    decl += (iN(commentLine("--", "Component", unitname), 1)) 
    decl.append(v.componentStart)
    if(len(genIntD) + len(genMiscD) > 0):
        decl.append(v.genStart)
        for line in genList:   
            decl.append(line)
        decl.append(v.genEnd)
    decl.append(v.entityMid)
    for line in stubPortList:
        decl.append(line)
    decl += v.componentEnd
    decl += sdbRefList
    decl.append('\n')
    #constant c_eca_ac_wbm_slave_sdb : t_sdb_device := work.eca_ac_wbm_auto_pkg.c_eca_ac_wbm_slave_sdb;
    
    
    decl = iN(decl, 1)
    for line in decl:
        fo.write(line)
    
        
    
    fo.write(v.packageEnd)
    fo.write(v.packageBodyStart)
    fo.write(v.packageEnd)
    
    fo.close


def writeHdrC(filename):
    
    print "Generating C Header file         %s\n" % filename    
    
    fo = open(mypath + filename, "w")
    
    gc     = gCStr(filename, unitname, author, email, version, date)
    header = "" #gCStr.hdrfileStart
    
    for line in header:
        fo.write(line)
    
    for line in gc.hdrfileStart:
        fo.write(line)
   
    for line in cAdrList:
        fo.write(line)    
    fo.write(gc.hdrfileEnd)
    
    fo.close
#TODO: A lot ...

        
#masterIfList = xmldoc.getElementsByTagName('masterinterface')
#for masterIf in masterIfList:
#    if masterIf.getAttribute('name'):
#        print "Generating WBMF %s" % masterIf.getAttribute('name')
#        entityPortList.append(VhdlStr.masterIf % (masterIf.getAttribute('name'), masterIf.getAttribute('name'))) 
    

helpText = ["\nUsage: python %s <path-to-wishbone-descriptor.xml>\n" % sys.argv[0], 
            "-h    --help       Show detailed help. Lots of text, best redirect output to txt file",
            "-q    --quiet      No console output",
            "      --version    Shows version information",
            "-l    --log        Log build output\n"
            ]

#(" " * ((76-len(myCreator))/2))
#((76-len(myCreator)) % 2)
#(" " * ((76-len(myCreator))/2) + 0 )            
detailedHelpText = ['%s' % ("*" * 80),
                    '**                                                                            **',                    
                    '**                          wbgenplus Manual V%s                             **' % myVersion,                    
                    ('**' + '%s%s%s' + '**') % ((" " * ((76-len(myCreator))/2)), myCreator, (" " * ((76-len(myCreator))/2 + (76-len(myCreator))%2))),
                    '%s\n' % ("*" * 80),
                    'wbgenplus autogenerates wishbone devices for FPGAs in VHDL from a single XML file.',
                    'In VHDL, it builds the core logic, a package for register records and SDB entries',
                    'and provides a stub for the outer entity.',
                    'It also creates a C Header file with the address definitions and builds',
                    'documentation via doxygen (not yet implemented).\n',
                    'In order to keep things modular, wbgenplus creates a seperate core for the',
                    'wishbone interface to be instantiated for your design.\n',
                    'Because of this, there are a few design rules which must be obeyed:\n',                    
                    'All registers that are write/read-write on the wishbone side are read-only on the entity side.',
                    'All registers that are read only on the wishbone side will be driven by the entity side.\n',
                    'If you want to use generics, they will be defined as constants in an extra package,',
                    'so they can be imported into the core package. Although VHDL 2008 supports generic packages,',
                    'none of major Synthesizers fully supports VHDL 2008. So there is currently no alternative',
                    'to the workaround. Yes, this sucks.\n\n',
                    'wbgenplus currently supports the following features:\n',
                    '- completely modular wishbone interface core',
                    '- forces comments for all registers in order to produce self-explaining code',                    
                    '- multiple slave interfaces in one core',                       
                    '- auto-generated SDB records',
                    '- automatic clock crossing',
                    '- address offsets can be generated manually, automatically or by a mix of both',                    
                    '- optional autogeneration of get/set/clear adresses for registers (atomic bit manipulation)',                        
                    '- auto-splitting of registers wider than the bus data width',                    
                    '- option for multiple memory pages of registers, dependent on a selector register,',
                    '  quantity can be controlled via generic',
                    '- optional complete flow control by the outer (user generated) entity',
                    '- optional feedback control via ACK/ERR by the outer (user generated) entity',
                    '- auto feedback for successful or failed operations(accessing unmapped addresses or',
                    '  writing to read only / reading from write only registers)',
                    '- optional pulsed registers, reset to all 0 automatically after 1 cycle',
                    '- optional autogeneration of write enable (WE) flag for a register (e.g. easy fifo connection)',
                    '\n'
                    'Planned features / currently under development:\n'
                    '- named bit fields in registers',
                    '- automatic RAM block generation',                    
                    '\n',
                    '+%s+' % ("-" * 78),
                     '|                            Wishbone-Descriptor-XMLs                          |',
                    '+%s+\n' % ("-" * 78),                    
                    
                    'This sections covers the details of the XML syntax.\n',
                    'Supported tags:\n',
                    '<wbdevice             Supreme Tag introducing a new wishbone device with one ore more interfaces.',
                    '   <codegen>          Selects which outputs files should be built',
                    '   <generics>         Gives a list of generics to the device. Generic names can be used in interface',
                    '   <clockdomain>      Introduces a clockdomain. If no such tag is present, wbgenplus will automatically',
                    '                      generate the "sys" domain for the wb interface',                                       
                    '   <slaveinterface    Introduces a new Wishbone Slave interface to the device',
                    '       <sdb>          Parameters for Self Describing Bus (SDB) record of this slave interface',
                    '       <reg>          Introduces a new register to this slave interface interface',        
                    '       <ram>          Introduces a new memory block to this slave interface interface (not yet implemented)',
                    '   >',
                    '>',
                    
                    'Detailed Tag parameter descriptions. All parameters marked with an * are mandatory,',
                    'the rest is optional and does need to appear in the XML.',
                    'There are two exceptions, see below:',
                    '   1: Either read or write or both must be "yes"',
                    '   2: Only valid in a group: If pages is greater 0, exactly 1 register must have set selector="yes"',
                    '      and 1 or more registers must have set paged="yes"\n\n',
                    'Tag parameters:\n',
                    '<CLOCKDOMAIN>:\n',
                    '  *name:       Name of the clock domain. The first such tag is always treated as the Wishbone domain\n',
                    '   Example:',                      
                    '   <clockdomain name="wb"></clockdomain>\n',
                    '<WBDEVICE>:\n',                  
                    '  *unitname:   Name of the design unit of the wishbone top file.',
                    '               The inner core will be named "<unitname>_auto"\n',
                    '  *author:     Name of the author of this xml and all derived files\n',
                    '   email:      The email address of the author\n',
                    '   version:    version number of this device\n',
                    '   Example:',                      
                    '   <wbdevice unitname="my_cool_device" author="M. Kreider" email="m.kreider@gsi.de" version="0.0.1">\n',
                    '<SLAVEINTERFACE>:\n',                   
                    '  *name:       Name of the slave interface port\n',
                    '   data:       Bitwidth of the data lines. Default is 32\n',
                    '   type:       Type of flow control. Accepts "pipelined" or "classic", default is "pipelined"\n',
                    ' 2*pages:      Number <n> of memory pages to instantiate, default is 0.',
                    '               Accepts a generic (via const package, see above)',
                    '               All registers marked paged="yes" will be built as an array with n elements.',
                    '               If <n> is greater 0, one register must be marked as the page selector by issueing selector="yes"\n',
                    '   Example:',                      
                    '   <slaveinterface name="control" data="32" type="pipelined" pages="8">\n',
                    '<SDB>:\n',
                    '  *vendorID:   Vendor Identification code, 64 bit hex value. Also accepts known vendors like "GSI" or "CERN"\n',
                    '  *productID:  Product Identification code, 32 bit hex value\n',
                    '  *version:    Device version number, 1 to 3 digits\n',
                    '   date:       Date to be shown on sdb record. Default is "auto" (Today)\n',
                    '  *name:       Name to be shown on sdb record. 19 Characters max.\n', 
                    '   Example:',  
                    '   <sdb vendorID="GSI" productID="0x01234567" version="1" date="auto" name="my_ctrl_thingy"></sdb>\n',
              
                    '<REG>:\n',
                    '  *name:       Main name of the register. Actual address and record names might be extended by suffices\n',
                    '  *read:       indicates if this register is readable from Wishbone. Default is "no"\n',
                    '  *write:      indicates if this register is writeable from Wishbone. Default is "no"\n',
                    '  *comment:    A (hopefully) descriptive comment for this register\n',                        
                    '   access:     Access mode for this register, "simple" or "atomic", default is "simple"',
                    '               Simple mode allows direct overwriting of register content.',
                    '               Atomic mode provides seperate get, set, and clear addresses for this register,\n'
                    '               allowing atomic single bit manipulation\n',
                    '   mask:       Bitmask for this register (currently only functions as width), default is the',
                    '               data(bus width) parameter of the slave interface tag',
                    '               If "mask" is wider than "data", wbgenplus will automatically generate multiple addresses',
                    '               to allow word access of the register. Accepts either hex or binary values as',
                    '               masks (0x ... or 0b ...) or decimal values as the register bitwidth\n',
                    '   address:    Manually sets the offset for this register, default is auto addressing.',
                    '               All follwing Registers will be enumerated from this address onward\n',
                    '   reset:      Defines the reset value for this register. Accepts "ones", "zeroes", binary, hex or decimal value.',
                    '               Currently only works for registers that can be written to from WB. Default is "zeroes".\n',                      
                    '   weflag      Write enable flag, default is "no". If set to "yes", a additional flag register will be created,',
                    '               going HI for 1 clock cycle every time the parent register is written to.',
                    '               The flag register does not discriminate which page, word, or subword is accessed.\n',
                    '   autostall:  If set to "yes", raises the stall line for 1 cycle after each access. Default is "no"',
                    '               The outer entity can, only raise a stall request 2 cycles AFTER the bus operation.',
                    '               Autostall bridges this gap by keeping the bus stalled until the outer entity can do flow control\n',
                    '   pulse:      If set to "yes", the register will reset to all 0 after 1 cycle. Default is "no"\n', 
                    '   paged:      When set to "yes", this register will be instantiated as an array with the number of elements',
                    '               in the pages parameter of the slave interface tag\n',
                    '   selector:   Selects the active memory page of all paged registers. Value is auto range checked on access.\n',
                    '   clock:      Clock domain this register shall be synchronized to. Default is no sync (WB clock domain)',
                    '               Needs a corresponding <clockdomain> tag.\n',
                    '   Example:',                    
                    '   <reg name="ACT" read="yes" write="yes" access="atomic" mask="0xff" comment="Triggers on/off"></reg>\n',
                    '<RAM>:\n',
                    '  not yet implemented\n'
                    ]

versionText = ["\nwbgenplus - A Wishbone Slave Generator\n",
               "Version: %s" % myVersion,
               "Created %s by %s" % (myStart, myCreator),
               "Last updated %s\n" % myUpdate                 
               ]
                                          
def usage():
    for line in helpText:        
        print line

def manual():
    for line in detailedHelpText:        
        print line            

def version():
    for line in versionText:        
        print line 
                    
            
xmlIn = ""  
log = False
quiet = False



        
if(len(sys.argv) > 1):
    xmlIn = sys.argv[1]
else:
    usage()
    sys.exit(2)     

if(len(sys.argv) == 2):
    sIdx=1
else:
    sIdx=2
    
try:
    opts, args = getopt.getopt(sys.argv[sIdx:], "hlqf", ["help", "log", "quiet", "force", "version"])
except getopt.GetoptError, err:
    # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    sys.exit(2)    

needFile = True
force    = False
optFound = False
for option, argument in opts:
    if option in ("-h", "-?", "--help"):
        optFound = True        
        needFile = False
        manual()
    elif option in ("--version"):
        optFound = True        
        needFile = False        
        version()
    elif option in ("-f", "--force"):
        optFound = True            
        force = True    
    elif option in ("-q", "--quiet"):
        optFound = True            
        quiet = True
    elif option in ("-l", "--log"):
        optFound = True        
        log = True
    else:
        print "unhandled option %s" % option
        sys.exit(2) 


if(needFile):
    if(optFound and len(sys.argv) == 2):
        usage()
        sys.exit(0)
        
    if os.path.isfile(xmlIn):
        mypath, myfile = os.path.split(xmlIn)        
        if not mypath:
            mypath += './'
        
        
        
        genIntD     = dict()
        genMiscD    = dict()
        portList    = []
        recordList  = []
        regList     = []
        vAdrList    = []
        cAdrList    = []
        fsmList     = []
        syncList    = []
        genList     = []
        ifList      = []
        unitname    = "unknown unit"
        author      = "unknown author"
        email       = "unknown mail"
        version     = "unknown version"
        date    = "%02u/%02u/%04u" % (now.day, now.month, now.year)
        
        unitname = os.path.splitext(myfile)[0]        
        #path    = os.path.dirname(os.path.abspath(xmlIn)) + "/"
        
        print "input/output dir: %s" % mypath
        print "Trying to parse:  %s" % myfile
        print "Unit:             %s" % unitname
        print "\n%s" % ('*' * 80)
                    
        parseXML(xmlIn)
        
        autoUnitName = unitname + "_auto"
        
        #filenames for various output files
        fileMainVhd     = autoUnitName              + ".vhd"
        filePkgVhd      = autoUnitName  + "_pkg"    + ".vhd"
        
        fileStubVhd     = unitname                  + ".vhd"
        fileStubPkgVhd  = unitname      + "_pkg"    + ".vhd"
        fileTbVhd       = unitname      + "_tb"     + ".vhd"
        
        fileHdrC        = unitname                  + ".h"
        
        
        (portList, recordList, regList, sdbList, sdbRefList, vAdrList, fsmList, syncList, genList, cAdrList, stubPortList, stubInstList, stubSigList, instGenList) = mergeIfLists(ifList)
        
        
        writeMainVhd(fileMainVhd)
        writePkgVhd(filePkgVhd)
        writeHdrC(fileHdrC)
        writeStubVhd(fileStubVhd)
        writeStubPkgVhd(fileStubPkgVhd)
        #writeTbVhd(fileTbVhd)
        print "\n%s" % ('*' * 80) 
        print "\nDone!"
    else:
        print "\nFile not found: %s" % xmlIn
    
    






