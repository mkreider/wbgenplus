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




i1          = textformatting.setColIndent
iN          = textformatting.setColsIndent    
adj         = textformatting.adjBlockByMarks
mskWidth    = textformatting.mskWidth
str2int     = textformatting.parseNumeral
commentLine = textformatting.commentLine
commentBox  = textformatting.commentBox
now = datetime.datetime.now()

 

class wbsCStr(object):
   

    def __init__(self, pages, unitname, slaveIfName):
        self.unitname   = unitname
        self.slaveIfName  = slaveIfName        
        self.pages      = pages
        
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
   

    def __init__(self, pages, unitname, slaveIfName, dataWidth, vendId, devId, sdbname):
        self.unitname       = unitname
        self.slaveIfName    = slaveIfName        
        self.pages          = pages
        self.dataWidth      = dataWidth
        #################################################################################        
        #Strings galore        
        self.slaveIf    = ["%s_i : in  t_wishbone_slave_in := ('0', '0', x\"00000000\", x\"F\", '0', x\"00000000\");\n" % slaveIfName,
                           "%s_o : out t_wishbone_slave_out" % slaveIfName] #name
        self.slaveSigs = ["signal s_%s_i : t_wishbone_slave_in := ('0', '0', x\"00000000\", x\"F\", '0', x\"00000000\");\n" % slaveIfName,
                          "signal s_%s_o : t_wishbone_slave_out\n" % slaveIfName,
                          "signal s_%s_regs_o : t_%s_regs_o;\n" % (slaveIfName, slaveIfName),
                          "signal s_%s_regs_i : t_%s_regs_i;\n" % (slaveIfName, slaveIfName)]
        
        self.slaveInst = ["%s_regs_o => s_%s_regs_o,\n" % (slaveIfName, slaveIfName),
                          "%s_regs_i => s_%s_regs_i,\n" % (slaveIfName, slaveIfName), 
                          "%s_i => s_%s_i,\n" % (slaveIfName, slaveIfName),
                          "%s_o => s_%s_o" % (slaveIfName, slaveIfName)] #name     
           
        self.wbs0       = ["%s : process(clk_sys_i)\n" % slaveIfName,
                           "   variable v_dat_i  : t_wishbone_data;\n",
                           "   variable v_dat_o  : t_wishbone_data;\n",
                           "   variable v_adr    : natural;\n",
                           "   variable v_page   : natural;\n",
                           "   variable v_sel    : t_wishbone_byte_select;\n",
                           "   variable v_we     : std_logic;\n",
                           "   variable v_en     : std_logic;\n",
                           "begin\n",
                           "   if rising_edge(clk_sys_i) then\n",
                           "      if(rst_n_i = '0') then\n"]
       
        self.wbs1       = ["else\n",
                           "   -- short names\n",
                           "   v_dat_i           := %s_i.dat;\n" % slaveIfName,
                           "   v_adr             := to_integer(unsigned(%s_i.adr(%%s)) & \"00\");\n" % slaveIfName,
                           "   v_sel             := %s_i.sel;\n" % slaveIfName,
                           "   v_en              := %s_i.cyc and %s_i.stb and not (r_%s_out_stall or %s_regs_i.STALL);\n" % (slaveIfName, slaveIfName, slaveIfName, slaveIfName),
                           "   v_we              := %s_i.we;\n\n" % slaveIfName,
                           "   --interface outputs\n",
                           "   r_%s_out_stall   <= '0';\n" % slaveIfName,                            
                           "   r_%s_out_ack0    <= '0';\n" % slaveIfName,
                           "   r_%s_out_err0    <= '0';\n" % slaveIfName,
                           "   r_%s_out_dat0    <= (others => '0');\n\n" % slaveIfName,
                           "   r_%s_out_ack1    <= r_%s_out_ack0;\n" % (slaveIfName, slaveIfName),
                           "   r_%s_out_err1    <= r_%s_out_err0;\n" % (slaveIfName, slaveIfName),
                           "   r_%s_out_dat1    <= r_%s_out_dat0;\n\n" % (slaveIfName, slaveIfName),
] 
      
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
      
        self.slvSubType         = "subtype t_slv_%s_%%s is std_logic_vector(%%s downto 0);\n" % slaveIfName #name, idxHi
        self.slvArrayType       = "type    t_slv_%s_%%s_array is array(natural range <>) of t_slv_%s_%%s;\n" % (slaveIfName, slaveIfName)  #name, #name
        self.signalSlvArray     = "%%s : t_slv_%s_%%s_array(%%s downto 0); -- %%s\n"  % slaveIfName #name, name, idxHi, desc
        self.wbsPageSelect      = "v_page := to_integer(unsigned(r_%s.%%s));\n\n"  % slaveIfName #pageSelect Register
        self.wbWrite            = "when c_%s_%%s => r_%s.%%s <= f_wb_wr(r_%s.%%s, v_dat_i, v_sel, \"%%s\"); -- %%s\n" % (slaveIfName, slaveIfName, slaveIfName) #registerName, registerName, (set/clr/owr), desc
        self.wbWriteWe          = "r_%s.%%s_WE <= '1'; --    %%s write enable\n" % (slaveIfName) 
        self.wbWriteWeZero      = "r_%s.%%s_WE <= '0'; -- %%s pulse\n" % (slaveIfName)
        self.wbStall            = "r_%s_out_stall  <= '1'; --    %%s auto stall\n" % (slaveIfName)
        self.wbWritePulseZero   = "r_%s.%%s <= (others => '0'); -- %%s pulse\n" % (slaveIfName) #registerName        
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
        self.resetSignal        = "r_%s.%%s <= (others => '0');\n" % slaveIfName #registerName   
        self.resetSignalArray   = "r_%s.%%s <= (others =>(others => '0'));\n" % slaveIfName #registerName
        self.recordPortOut      = "%s_regs_o : out t_%s_regs_o;\n" % (slaveIfName, slaveIfName)
        self.recordPortIn       = "%s_regs_i : in  t_%s_regs_i;\n" % (slaveIfName, slaveIfName) 
        self.recordRegStart     = "type t_%s_regs_%%s is record\n" % slaveIfName
        self.recordRegEnd       = "end record t_%s_regs_%%s;\n\n" % slaveIfName
        self.recordAdrStart     = "type t_%s_adr is record\n" % slaveIfName
        self.recordAdrEnd       = "end record t_%s_adr;\n\n" % slaveIfName
        self.recAdr             = "%s : natural;\n"
        self.constRegAdr        = "constant c_%s_%%s : natural := 16#%%s#; -- %%s 0x%%s, %%s\n" % slaveIfName #name, adrVal, adrVal, rw, msk, desc
        self.constRecAdrStart   = "constant c_%s_adr : t_%s_adr := (\n" % (slaveIfName, slaveIfName)
        self.constRecAdrLine    = "%s => 16#%x#%s -- 0x%02X, %s, _0x%08x %s\n" #name, adrVal, comma/noComma, adrVal, rw, msk, desc
        self.constRecAdrEnd     = ");\n"
        self.signalSlv          = "%s : std_logic_vector(%s downto 0); -- %s\n" #name, idxHi, idxLo, desc
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
                                   'name          => "%s")));\n' % sdbname.upper().ljust(19)]
                                   
    
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
           (name, desc, rwmafs, width, opList) = elem
           if(rwmafs.find('m') > -1):
               ind = '(v_page)'
           else:
               ind = ""            
           
           for opLine in opList:
               (op, adrList) = opLine
               if(op == "_GET"):                    
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
            (name, desc, rwmafs, width, opList) = elem
           
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
            (name, desc, rwmafs, width, opList) = elem
           
            if(rwmafs.find('m') > -1):
                ind = '(v_page)'
            else:
                ind = ""
            
            if(rwmafs.find('w') > -1):
                if((rwmafs.find('f') > -1)):
                    s.append(self.wbWriteWeZero % (name, name))
                if((rwmafs.find('p') > -1)):             
                    s.append(self.wbWritePulseZero % (name, name))
                                
        return s 
    
   
    def regs(self, regList):
       recordsOut       = []
       recordsIn        = [] + [self.signalSl % ('STALL', 'Stall control for outside entity'),
                                self.signalSl % ('ERR', 'Error control for outside entity')]
       types            = []
       for elem in regList:        
           (name, desc, rwmafs, width, opList) = elem
           if(rwmafs.find('m') > -1):
               types += self.multitype(elem)
               if(rwmafs.find('w') > -1):
                   recordsOut += self.multielement(elem)
                   if(rwmafs.find('f') > -1):
                       recordsOut.append(self.signalSl % (name + '_WE', 'WE flag'))    
               elif(rwmafs.find('r') > -1):            
                   #We can't have two drivers. Only include register in the inputs list if it's not written to be WB IF                    
                   recordsIn += self.multielement(elem)      
           else:
               if(rwmafs.find('w') > -1):
                   recordsOut.append(self.reg(elem))
                   if(rwmafs.find('f') > -1):
                       recordsOut.append(self.signalSl % (name + '_WE', 'WE flag'))    
               elif(rwmafs.find('r') > -1):
                   #We can't have two drivers. Only include register in the inputs list if it's not written to be WB IF 
                   recordsIn.append(self.reg(elem))
                   
       return [types, recordsOut, recordsIn]           
    
    def reg(self, elem):
        (name, desc, rwmafs, width, opList) = elem       
        s = self.signalSlv % (name, width-1, desc)        
        return s
    

    def multitype(self, elem):
        (name, desc, rwmafs, width, opList) = elem        
        s = []        
        s.append('\n')        
        s.append(self.slvSubType % (name, width-1)) #shift mask to LSB
        s.append(self.slvArrayType % (name, name))
        return s 
    
    def multielement(self, elem, qty=1):
        (name, desc, rwmafs, width, opList) = elem        
        s = []        
      
        if(type(qty) == int):
            s.append(self.signalSlvArray % (name, name, (self.pages-1), desc))
        else:
            s.append(self.signalSlvArray % (name, name, self.pages + '-1', desc))
        return s    
              
    
    def cRegAdr(self, elem):
        (name, desc, rwmafs, width, opList) = elem
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
           (name, desc, rwmafs, width, opList) = elem
           if(rwmafs.find('w') > -1):
               if(rwmafs.find('m') > -1):
                   s.append(self.resetSignalArray % name)                      
               else:
                   s.append(self.resetSignal % name)
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
        self.pkg        =  "use work.%s_pkg.all;\n\n" % unitname                   
           
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
        
        self.instStart      = "INST_%s : %s\n" % (unitname, unitname)
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
    
    def __init__(self, unitname, name, startAdr, pageSelect, pages, dataWidth, vendId, devId, sdbname):
        self.regs       = []        
                
        self.portList   = []
        self.stubPortList = []
        self.stubInstList = []
        self.stubSigList = []
        self.regList    = []   
        self.recordList = []
        self.adrList    = []
        self.fsm        = []
        
        self.name       = name        
        self.startAdr   = startAdr
        self.pageSelect = pageSelect
        self.pages      = pages
        self.dataWidth  = dataWidth
        self.v = wbsVhdlStr(pages, unitname, name, dataWidth, vendId, devId, sdbname)        
        self.c = wbsCStr(pages, unitname, name)
    
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
        
        (_, _, _, _, opList) = elem
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
        
        
    
    def addReg(self, name, desc, bigMsk, rwmafs, startAdr=None, offs=4):
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
                op = '_OWR'
            elif rwmafs.find('r') > -1:    
                op = '_GET'
            elif rwmafs.find('w') > -1:
                op = '_OWR'
            self.addOp(opList, adr, offs, bigMsk, op)      
        (idxHi, idxLo) = mskWidth(bigMsk)
        width   = (idxHi-idxLo+1)
        newElem = [name, desc, rwmafs, width, opList]
        #print "lenElem %u" % len(newElem)
        print "Reg <%s>, Desc <%s>, <%s> w <%u>" % (name, desc, rwmafs, width)
        i = 0        
        for opLine in opList:
            #print opLine            
            (op, adrList) = opLine            
            #print "#%u <%s>" % (i, op)
            j=0            
            for adrLine in adrList:
               (msk, adr) = adrLine
               (idxHi, idxLo) = mskWidth(msk)
               sliceWidth   = (idxHi-idxLo+1) 
               curSlice = "%u downto %u" % ( sliceWidth + j*self.dataWidth -1, j*self.dataWidth)
               j += 1
               #print "msk <%x>, adr <%x> Slice %s" % (msk, adr, curSlice) 
        self.regs.append(newElem)      
    
  
    def renderStubPorts(self):
        a = []
        a += self.v.slaveIf        
        self.stubPortList = a        
  
    def renderStubSigs(self):
        a = []
        a += self.v.slaveSigs
        self.stubSigList = a # no need to indent, we'll do it later with all IF lists together

        
    def renderStubInst(self):
        a = []
        a += self.v.slaveInst
        self.stubInstList = a # no need to indent, we'll do it later with all IF lists together    
  
    def renderPorts(self):
        a = []        
        a.append(self.v.recordPortIn)        
        a.append(self.v.recordPortOut)
        a.append('\n')
        a += self.v.slaveIf
        self.portList = a # no need to indent, we'll do it later with all IF lists together
                
    

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
        #print hiAdr, type(hiAdr)
        (idxHi, idxLo) = mskWidth(hiAdr)
        adrRange = 2**(idxHi+1)-1
        
        print "Slave <%s>: Found %u register names, last Adr is %08x, Adr Range is %08x, = %u downto 0\n" % (self.name, len(self.regs), hiAdr, adrRange, idxHi)
        print "\n%s" % ('*' * 80) 
        hdr1 = self.v.wbs1

        szero = adj(self.v.fsmWritePulse(self.regs), ['<=', '--'], 4)
        
        hdr1[3] = hdr1[3] % ('%u downto %u' % (idxHi, 2))
        hdr1    = iN(hdr1, 3)
        
        psel    = iN([self.v.fsmPageSel(self.pageSelect)], 4)
        
        hdr2    = iN(self.v.wbs2, 4)  
        swr     = adj(self.v.fsmWrite(self.regs), ['=>', 'r_', '<=', 'v_dat_i', '--'], 7)    
              
        
        mid0    = iN([self.v.wbOthers], 7)
        mid1    = iN(self.v.wbs3, 5)
        
        srd     = adj(self.v.fsmRead(self.regs), ['=>', '<=', "--"], 7)
        ftr     = iN(self.v.wbs4, 1)
        con     = adj(self.v.wbs5, ['<=', "--"], 1)
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
            (name, desc, rwmafs, width, opList) = elem
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

    def renderRecords(self):
        a = []
        
        (types, recordsOut, recordsIn) = self.v.regs(self.regs)
        a += types
        a += self.v.nl
        a.append(self.v.recordRegStart % 'o')
        a += iN(recordsOut, 1)        
        a.append(self.v.recordRegEnd % 'o')
        a.append('\n')
        a.append(self.v.recordRegStart % 'i')
        a += iN(recordsIn, 1)        
        #a.append(i1(self.v.signalSl % ("stall", "Stall control for main entity"), 1))        
        # a += (iN(records, 1))
        a.append(self.v.recordRegEnd % 'i')
        self.recordList = adj(a, [ ':', '--'], 0)
    
    def renderRegs(self):
        a = []
        a.append(self.v.wbs_reg_o)
        a.append(self.v.wbs_reg_i)
        a += (self.v.wbs_ackerr)        
        self.regList = a # no need to indent, we'll do it later with all IF lists together

    def renderAll(self):
        self.renderStubPorts()
        self.renderStubSigs()
        self.renderStubInst()
        self.renderPorts()
        self.renderRecords()
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
    uglyPortList    = ["clk_sys_i : in  std_logic;\n",
                       "rst_n_i   : in  std_logic;\n\n"]
    uglyInstList    = ["clk_sys_i => clk_sys_i,\n",
                       "rst_n_i => rst_n_i,\n\n"]                   
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
        recordList   += iN(commentLine("--","WBS Register Record", slave.name), 1) 
        recordList   += adj(slave.recordList, [ ':', '--'], 1)
             
        stubSigList  += slave.stubSigList
        sdbList      += slave.v.sdb + ['\n']
        
    
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
        instGenList.append(v.instGenport % (genName, genVal, instLineEnd, genDesc))
        idx += 1
    for genName in genMiscD.iterkeys():
        if(idx == lastIdx):
            lineEnd = ''
        else:
            lineEnd = ';'
        (genType, genVal, genDesc) = genMiscD[genName]
        genList.append(v.genport % (genName, genType, genVal, lineEnd, genDesc))
        instGenList.append(v.instGenport % (genName, genVal, instLineEnd, genDesc))
        idx += 1
    genList = adj(genList, [':', ':=', '--'], 1)
    instGenList = adj(instGenList, ['=>', '--'], 1)              
    #Todo: missing generics 
    return [portList, recordList, regList, sdbList, vAdrList, fsmList, genList, cAdrList, stubPortList, stubInstList, stubSigList, instGenList]        

def parseXML(xmlIn):
    xmldoc      = minidom.parse(xmlIn)   
    global unitname
    global author 
    global version
    global email    
    
    unitname = xmldoc.getElementsByTagName('wbdevice')[0].getAttribute('unitname')
    author   = xmldoc.getElementsByTagName('wbdevice')[0].getAttribute('author')
    version  = xmldoc.getElementsByTagName('wbdevice')[0].getAttribute('version')
    email    = xmldoc.getElementsByTagName('wbdevice')[0].getAttribute('email')
    
    genericsParent = xmldoc.getElementsByTagName('generics')
    if len(genericsParent) != 1:
        print "There must be exactly 1 generics tag!"
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
    
    slaveIfList = xmldoc.getElementsByTagName('slaveinterface')
    print "Found %u slave interfaces\n" % len(slaveIfList)    
    for slaveIf in slaveIfList:
          
        name    = slaveIf.getAttribute('name')
        ifWidth = str2int(slaveIf.getAttribute('data'))
        print "Slave <%s>: %u Bit wordsize" % (name, ifWidth)
        pages   = slaveIf.getAttribute('pages')
        #check integer generic list
        for genName in genIntD.iterkeys():
            if(pages.find(genName) > -1):
                (genType, genVal, genDesc) = genIntD[genName]
                pages = pages.replace(genName, str(genVal))
        aux = str2int(pages)
        if(aux == None):            
            print "Slave <%s>: Pages' numeric value <%s> is invalid" % (name, pages)
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
            else:
                vendId = aux                
                print "Slave <%s>: Unknown Vendor ID <%016x>. Would you like to add to my list?" % (name, vendId)                
                
        
        aux = str2int(prodId)
        if(aux == None):            
                print "Slave <%s>: Invalid Product ID <%s>!" % (name, prodId)
        else:
            prodId = aux     
                
        sdbname     = sdb[0].getAttribute('name')
        if(len(sdbname) > 19):
            print "Slave <%s>: Sdb name <%s> is too long. It has %u chars, allowed are 19" % (name, sdbname, len(sdbname))
            
            
        tmpSlave    = wbsIf(unitname, name, 0, '', pages, ifWidth, vendId, prodId, sdbname) 
        
        selector = ""
        #name, adr, pages, selector
        #registers
        registerList = slaveIf.getElementsByTagName('reg')
        for reg in registerList:
            regname = reg.getAttribute('name')
            regdesc = reg.getAttribute('comment')
            regadr = None       
            if reg.hasAttribute('address'):            
                regadr = reg.getAttribute('address')            
                aux = str2int(regadr)
                if(aux == None):            
                    print "Slave <%s>: Register <%s>'s supplied address <%x> is invalid, defaulting to auto" % (name, regname, regadr)
                regadr = aux            
                
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
                        
                    #else:
                        #Error, we can't have more than one pageselector!
            if reg.hasAttribute('mask'):      
                regmsk    = reg.getAttribute('mask')
                
                #check integer generic list
                for genName in genIntD.iterkeys():
                    if(regmsk.find(genName) > -1):
                        (genType, genVal, genDesc) = genIntD[genName]
                        regmsk = regmsk.replace(genName, str(genVal))            

                #check conversion function list
                idxCmp = regmsk.find('f_makeMask(')            
                if(idxCmp > -1):
                    regmsk = regmsk.replace('f_makeMask(', '')
                    regmsk = regmsk.rstrip(')') #FIXME: this is extremely presumptious!
                            
                    #mask valid
                aux = str2int(regmsk)
                
                if(aux == None):
                    aux = 2^ int(ifWidth) -1
                    print "Slave <%s>: Register <%s>'s supplied mask <%s> is invalid, defaulting to %x" % (name, regname, regmsk, aux)
                if(idxCmp > -1):            
                    regmsk = 2**aux-1 
                else:
                    regmsk = aux                        
            else:        
                print "Slave <%s>: No mask for Register <%s> supplied, defaulting to 0x%x" % (name, regname, 2**ifWidth-1)
                regmsk = 2**ifWidth-1
            
            tmpSlave.addReg(regname, regdesc, regmsk, regrwmf,  regadr, ifWidth/8)
            #x.addSimpleReg('NEXT2',     0xfff,  'rm',   "WTF")
        if((selector != '') and (pages > 0)):    
            print "Slave <%s>: Interface has %u memory pages. Selector register is %s" % (name, pages, selector)    
        tmpSlave.pageSelect = selector    
        tmpSlave.pages      = pages    
        tmpSlave.renderAll()    
        ifList.append(tmpSlave)
        


def writeStubVhd(filename):
    
    
    if os.path.isfile(path + filename):
        print "!!! %s already exists !!!\n\nI don't want to accidentally trash your work.\nAre you sure you want to overwrite %s with a new stub entity? " % (filename, filename)
        inp = 'dunno'        
        
        while ((inp.lower() != 'y') and (inp.lower() != 'n') and (inp.lower() != '')):       
            inp = str(raw_input("(y/N) : "))
        if ((inp.lower() == 'n') or (inp == '')):
            print ""            
            return
        else:
            print ""
            
    print "Generating stub entity           %s" % filename        
    fo = open(path + filename, "w")
    v = gVhdlStr(unitname, filename, author, email, version, date)

    header = adj(v.header + ['\n'], [':'], 0)
    
    for line in header:
        fo.write(line)
    
    fo.write("--! @brief *** ADD BRIEF DESCRIPTION HERE ***\n")
    fo.write("--!\n")
                      
    for line in v.headerLPGL:
        fo.write(line)
    
    libraries = v.libraries + [v.pkg]
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
    if(len(genIntD) + len(genMiscD) > 0):
        a.append(v.instGenStart)
        a += instGenList
        a.append(v.instGenEnd)    
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
    
    fo = open(path + filename, "w")
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
    libraries = v.libraries + [v.pkg]
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
    for line in fsmList:
        fo.write(line)
    
    fo.write(v.archEnd)
    
    fo.close

def writePkgVhd(filename):

    print "Generating WishBone core package %s" % filename    
    
    fo = open(path + filename, "w")
    
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


def writeHdrC(filename):
    
    print "Generating C Header file         %s\n" % filename    
    
    fo = open(path + filename, "w")
    
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
    
  

xmlIn = sys.argv[1]
    

genIntD     = dict()
genMiscD    = dict()
portList    = []
recordList  = []
regList     = []
vAdrList    = []
cAdrList    = []
fsmList     = []
genList     = []
ifList      = []
unitname    = "unknown unit"
author      = "unknown author"
email       = "unknown mail"
version     = "unknown version"
date    = "%02u/%02u/%04u" % (now.day, now.month, now.year)
path    = os.path.dirname(os.path.abspath(xmlIn)) + "/"

print "input/output dir: %s" % path
print "Trying to parse %s..." % xmlIn
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


(portList, recordList, regList, sdbList, vAdrList, fsmList, genList, cAdrList, stubPortList, stubInstList, stubSigList, instGenList) = mergeIfLists(ifList)

writeStubVhd(fileStubVhd)
writeMainVhd(fileMainVhd)
writePkgVhd(filePkgVhd)
writeHdrC(fileHdrC)
#writeTbVhd(fileTbVhd)
print "\n%s" % ('*' * 80) 
print "\nDone!"







