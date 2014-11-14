# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/mkreider/.spyder2/.temp.py
"""
from xml.dom import minidom
import datetime
import textformatting

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
        self.constRegAdr    = "#define %s_%%s   0x%%08x // _0x%%08x %%s, %%s\n" % slaveIfName.upper() #name, adrVal,  msk, rw, desc

class gCStr(object):
    def __init__(self, filename, unitname, author, version, date):
        self.unitname   = unitname     
        self.author     = author
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
        #################################################################################        
        #Strings galore        
        self.slaveIf    = ["%s_i : in  t_wishbone_slave_in := ('0', '0', x\"00000000\", x\"F\", '0', x\"00000000\");\n" % slaveIfName,
                           "%s_o : out t_wishbone_slave_out" % slaveIfName] #name
  
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
                           "   v_en              := %s_i.cyc and %s_i.stb and not r_%s_out.stall;\n" % (slaveIfName, slaveIfName, slaveIfName),
                           "   v_we              := %s_i.we;\n\n" % slaveIfName,
                           "   --interface outputs\n",
                           "   r_%s_out.stall  <= '0';\n" % slaveIfName,
                           "   r_%s_out.ack    <= '0';\n" % slaveIfName,
                           "   r_%s_out.err    <= '0';\n" % slaveIfName,
                           "   r_%s_out.dat    <= (others => '0');\n" % slaveIfName] 
      
        self.wbs2       = ["if(v_en = '1') then\n",
                           "   r_%s_out.ack  <= '1';\n" % slaveIfName,
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
      
        self.slvSubType         = "subtype t_slv_%s_%%s is std_logic_vector(%%s downto 0);\n" % slaveIfName #name, idxHi
        self.slvArrayType       = "type    t_slv_%s_%%s_array is array(natural range <>) of t_slv_%s_%%s;\n" % (slaveIfName, slaveIfName)  #name, #name
        self.signalSlvArray     = "%%s : t_slv_%s_%%s_array(%%s downto 0); %%s\n"  % slaveIfName #name, name, idxHi, desc
        self.wbsPageSelect      = "v_page := to_integer(unsigned(r_%s.%%s));\n\n"  % slaveIfName #pageSelect Register
        self.wbWrite            = "when c_%s_%%s => r_%s.%%s <= f_wb_wr(r_%s.%%s, v_dat_i, v_sel, \"%%s\"); %%s\n" % (slaveIfName, slaveIfName, slaveIfName) #registerName, registerName, (set/clr/owr), desc
        self.wbRead             = "when c_%s_%%s => r_%s_out.dat(r_%s.%%s'range) <= r_%s.%%s; %%s\n" % (slaveIfName, slaveIfName, slaveIfName, slaveIfName) #registerName, registerName, desc
        self.wbOthers           = "when others => r_%s_out.ack <= '0'; r_%s_out.err <= '1';\n" % (slaveIfName, slaveIfName) 
        self.wbs_output_reg     = "signal r_%s_out : t_wishbone_slave_out; --> WB output buffer register\n" % slaveIfName
        self.wbs_reg_rec        = "signal r_%s : t_%s_regs;\n" % (slaveIfName, slaveIfName)
        self.resetOutput        = "r_%s_out <= ('0', '0', '0', '0', '0', x\"00000000\");\n" % slaveIfName 
        self.resetSignal        = "r_%s.%%s <= (others => '0');\n" % slaveIfName #registerName   
        self.resetSignalArray   = "r_%s.%%s <= (others =>(others => '0'));\n" % slaveIfName #registerName
        self.recordPortOut      = "%s_regs_o : out t_%s_regs;\n" % (slaveIfName, slaveIfName) 
        self.recordRegStart     = "type t_%s_regs is record\n" % slaveIfName
        self.recordRegEnd       = "end record t_%s_regs;\n\n" % slaveIfName
        self.recordAdrStart     = "type t_%s_adr is record\n" % slaveIfName
        self.recordAdrEnd       = "end record t_%s_adr;\n\n" % slaveIfName
        self.recAdr             = "%s : natural;\n"
        self.constRegAdr        = "constant c_%s_%%s : natural := 16#%%x#; -- 0x%%02X, _0x%%08x %%s, %%s\n" % slaveIfName #name, adrVal, adrVal, rw, msk, desc
        self.constRecAdrStart   = "constant c_%s_adr : t_%s_adr := (\n" % (slaveIfName, slaveIfName)
        self.constRecAdrLine    = "%s => 16#%x#%s -- 0x%02X, %s, _0x%08x %s\n" #name, adrVal, comma/noComma, adrVal, rw, msk, desc
        self.constRecAdrEnd     = ");\n"
        self.signalSlv          = "%s : std_logic_vector(%s downto 0); %s\n" #name, idxHi, idxLo, desc
        self.signalSl           = "signal %s : std_logic; %s\n" #name, desc
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
        for elem, nextElem in zip(regList, regList[1:]+[regList[0]]):
            (name, suf, _, rw, desc, _) = elem            
            if(rw.find('r') > -1):
                if(rw.find('m') > -1):
                    ind = '(v_page)'
                else:
                    ind = ""
                s.append(self.wbRead % (name + suf, name+ind, name+ind, desc))
        return s

    def fsmWrite(self, regList):
        s = []    
        for elem, nextElem in zip(regList, regList[1:]+[regList[0]]):
            (name, suf, _, rw, desc, _) = elem            
            if(rw.find('w') > -1):
                if(rw.find('m') > -1):
                    ind = '(v_page)'
                else:
                    ind = ""
                s.append(self.wbWrite % (name + suf, name+ind, name+ind, self.wrModes[suf], desc))
        return s     
    
   
    def regs(self, regList):
       recordelements   = []
       types            = []
       for elem, nextElem in zip(regList, regList[1:]+[regList[0]]):
           if(elem[0] != nextElem[0]):
               if(elem[3].find('m') > -1):
                   types            += self.multitype(elem)
                   recordelements   += self.multielement(elem)                    
               else:    
                   recordelements.append(self.reg(elem))
       return [types, recordelements]           
    
    def reg(self, (name, suf, msk, rw, desc, adr)):
        (idxHi, idxLo) = mskWidth(msk);        
        s = self.signalSlv % (name, idxHi-idxLo, desc)        
        return s
    

    def multitype(self, (name, suf, msk, rw, desc, adr), qty = 1):
        s = []        
        (idxHi, idxLo) = mskWidth(msk);
        s.append('\n')        
        s.append(self.slvSubType % (name, idxHi-idxLo)) #shift mask to LSB
        s.append(self.slvArrayType % (name, name))
        return s 
    
    def multielement(self, (name, suf, msk, rw, desc, adr), qty = 1):
        s = []        
        (idxHi, idxLo) = mskWidth(msk);
        s.append('\n')        
        if(type(qty) == int):
            s.append(self.signalSlvArray % (name, name, (self.pages-1), desc))
        else:
            s.append(self.signalSlvArray % (name, name, self.pages + '-1', desc))
        return s    
              
    
    def cRegAdr(self, (name, suf, msk, rw, desc, adr)):
        s = self.recAdr % (name + suf, adr, adr, rw, msk, desc)        
        return s
    
    def resets(self, regList):
       s = []
       for elem, nextElem in zip(regList, regList[1:]+[regList[0]]):
           if(elem[0] != nextElem[0]):
               if(elem[3].find('m') > -1):
                   s.append(self.resetSignalArray % elem[0])                      
               else:
                   s.append(self.resetSignal % elem[0])
       s.append(self.resetOutput)           
       return s


class gVhdlStr(object):
   

    def __init__(self, unitname, filename="unknown", author="unknown", version="0.0", date=""):
        self.unitname   = unitname
        self.filename   = filename        
        self.author     = author
        self.version    = version
        
        self.header     = ["-- File Name : %s\n"        % filename,                 
                           "-- Design Unit Name : %s\n" % unitname,    
                           "-- Revision : %s\n"         % version,                     
                           "-- Author : %s\n"           % author,                          
                           "-- Created: %s\n"           % date]                                
    
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
        self.regList    = []
        self.stubRegList = []    
        self.recordList = []
        self.adrList    = []
        self.fsm        = []
        self.stubInstanceList = []
        self.name       = name        
        self.startAdr   = startAdr
        self.pageSelect = pageSelect
        self.pages      = pages
        self.v = wbsVhdlStr(pages, unitname, name, dataWidth, vendId, devId, sdbname)        
        self.c = wbsCStr(pages, unitname, name)
    
    def addReg(self, name, suf, msk, rw, desc, adr = None, offs = 4):
        if adr == None:
            if len(self.regs) == 0:
                adr = self.startAdr
                self.regs.append([name, suf, msk, rw, desc, adr])
            else:            
                self.regs.append([name, suf, msk, rw, desc, self.regs[-1][5] +offs])
        else:
            if len(self.regList) > 1:            
                if adr > self.regList[-1][5]:
                    self.regs.append([name, suf, msk, rw, desc, adr])
                else:
                    print "Error, double address detected"
            else:
                self.regs.append([name, suf, msk, rw, desc, adr])
                
    
    def addSimpleReg(self, name, msk, rw, desc, adr = None, offs = 4):
        s = str()        
        if rw.find('rw') > -1:
            s = '_RW '
        elif rw.find('r') > -1:    
            s = '_GET'
        elif rw.find('w') > -1:
            s = '_OWR'            
        self.addReg(name, s, msk, rw, "--> " + desc, adr, offs)
        
    def addAtomicReg(self, name, msk, rw, desc, adr = None, offs = 4):
        if rw.find('r') > -1:
            self.addReg(name, '_GET', msk, rw.translate(None, 'w'), "--> " + desc, adr, offs)
            adr = None
        if rw.find('w') > -1:    
            if rw.find('r') > -1:            
                self.addReg(name, '_SET', msk, rw.translate(None, 'r'), "--> " + desc, adr, offs)                
                self.addReg(name, '_CLR', msk, rw.translate(None, 'r'), "--> " + desc, None, offs)        
            else:
                self.addReg(name, '_SET', msk, rw.translate(None, 'r'), "--> " + desc, adr, offs) 

  
    def renderPortStub(self):
        return self.v.slaveIf  
  
    def renderPorts(self):
        a = []        
        a.append(self.v.recordPortOut)
        a += self.renderPortStub()
        self.portList = a # no need to indent, we'll do it later with all IF lists together
                
    

    def renderSdb(self):
        
        (_, _, _, _, _, hiAdr) = self.regs[-1]
        (idxHi, idxLo) = mskWidth(hiAdr)
        adrRange = 2**(idxHi+1)-1
        self.v.sdb[7] = self.v.sdb[7] % ('0' * 16) 
        self.v.sdb[8] = self.v.sdb[8] % ("%016x" % adrRange)
        
    
    def renderFsm(self):
               
        
        hdr0 = iN(self.v.wbs0, 1) 
        
        rst = adj(self.v.resets(self.regs), ['<='], 4)       
        
        (_, _, _, _, _, hiAdr) = self.regs[-1]
        (idxHi, idxLo) = mskWidth(hiAdr)
        adrRange = 2**(idxHi+1)-1
        print "Slave <%s>: Found %u register names, last Adr is %08x, Adr Range is %08x, = %u downto 0\n" % (self.name, len(self.regs), hiAdr, adrRange, idxHi)
        
        hdr1 = self.v.wbs1        
        hdr1[3] = hdr1[3] % ('%u downto %u' % (idxHi, 2))
        hdr1    = iN(hdr1, 3)
        
        psel    = iN([self.v.fsmPageSel(self.pageSelect)], 4)
        
        hdr2    = iN(self.v.wbs2, 4)  
        
        swr     = adj(self.v.fsmWrite(self.regs), ['=>', '<=', 'v_dat_i'], 7)    
        
        mid0    = iN([self.v.wbOthers], 7)
        mid1    = iN(self.v.wbs3, 5)
        
        srd     = adj(self.v.fsmRead(self.regs), ['=>', '<=', "--"], 7)
        ftr     = iN(self.v.wbs4, 1)
        
        self.fsmList = hdr0 + rst + hdr1 + psel +  hdr2 + swr + mid0 + mid1 + srd + mid0 + ftr
        
    def renderAdr(self):
        a = []
        b = []
        for elem in self.regs:
            (name, suf, msk, rw, desc, adr) = elem
            a.append(self.v.constRegAdr % (name + suf, adr, adr, msk, rw, desc ))
            b.append(self.c.constRegAdr % (name + suf, adr, msk, rw, desc ))
        self.vAdrList = adj(a, [ ':', ':=', '-- 0x', '_0x', '--> '], 2)
        self.cAdrList = adj(b, [ '   0x', '//', ','], 0)

    def renderRecords(self):
        a = []
        (types, records) = self.v.regs(self.regs)
        a += types
        a += self.v.nl
        a.append(self.v.recordRegStart)
        a += (iN(records, 1))
        a.append(self.v.recordRegEnd)   
        self.recordList = a
    
    def renderRegs(self):
        a = []
        a.append(self.v.wbs_output_reg)
        a.append(self.v.wbs_reg_rec)
        self.regList = a # no need to indent, we'll do it later with all IF lists together

    def renderAll(self):
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
    stubPortList    = [] + uglyPortList                   
    recordList      = []                   
    uglyRegList     = []
    uglyAdrList     = []
    cAdrList        = []     
    fsmList         = [] 
    genList         = []
    sdbList         = []
    
    v = gVhdlStr("")
    
    for slave in slaveList:
        uglyPortList += slave.portList
        stubPortList += slave.stubPortList
        #deal with vhdl not wanting a semicolon at the last port entry        
        if(slave != slaveList[-1]):
            uglyPortList[-1] += ";\n"
            stubPortList[-1] += ";\n"
        else:
            uglyPortList[-1] += "\n"
            stubPortList[-1] += "\n"
        uglyPortList += ["\n"]    
        cAdrList     += commentLine("//","Address Map", slave.name)
        cAdrList     += slave.cAdrList
        cAdrList     += "\n"
        uglyAdrList  += iN(commentLine("--","WBS Adr", slave.name), 1) 
        uglyAdrList  += slave.vAdrList
        uglyAdrList  += "\n"
        uglyRegList  += iN(commentLine("--","WBS Regs", slave.name),1) 
        uglyRegList  += adj(slave.regList, [' is ', ':', ':=', '-->'], 1)
        uglyRegList  += "\n"
        fsmList      += iN(commentBox("--","WBS FSM", slave.name), 1)
        fsmList      += slave.fsmList   
        fsmList      += "\n\n"
        recordList   += iN(commentLine("--","WBS Register Record", slave.name), 1) 
        recordList   += adj(slave.recordList, [ ':', '--> '], 1)
        sdbList      += slave.v.sdb + ['\n']
        
    
    for master in masterList:
        uglyPortList += master.portList
        uglyAdrList  += master.AdrList       
        uglyRegList  += master.regList    
    
    portList    = adj(uglyPortList, [':', ':=', '--'], 1)    
    
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
        else:
            lineEnd = ';'
        genList.append(v.genport % (genName, genType, genVal, lineEnd, genDesc))
        idx += 1
    for genName in genMiscD.iterkeys():
        if(idx == lastIdx):
            lineEnd = ''
        else:
            lineEnd = ';'
        (genType, genVal, genDesc) = genMiscD[genName]
        genList.append(v.genport % (genName, genType, genVal, lineEnd, genDesc))
        idx += 1
    genList = adj(genList, [':', ':=', '--'], 1)             
    #Todo: missing generics 
    return [portList, recordList, regList, sdbList, vAdrList, fsmList, genList, cAdrList]        

def parseXML(xmlIn):
    xmldoc      = minidom.parse(xmlIn)   
    global unitname
    global author 
    global version
    
    unitname = xmldoc.getElementsByTagName('wbdevice')[0].getAttribute('unitname')
    author   = xmldoc.getElementsByTagName('wbdevice')[0].getAttribute('author')
    version  = xmldoc.getElementsByTagName('wbdevice')[0].getAttribute('version')

    
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
                   
            if reg.hasAttribute('address'):            
                regadr = reg.getAttribute('address')            
                aux = str2int(regadr)
                if(aux == None):            
                    print "Slave <%s>: Register <%s>'s supplied address <%x> is invalid, defaulting to auto" % (name, regname, regadr)
                        
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
            
         
            if (reg.getAttribute('access') == "atomic"):
                tmpSlave.addAtomicReg(regname, regmsk, regrwmf, regdesc)
            else:        
                tmpSlave.addSimpleReg(regname, regmsk, regrwmf, regdesc)
            #x.addSimpleReg('NEXT2',     0xfff,  'rm',   "WTF")
        if((selector != '') and (pages > 0)):    
            print "Slave <%s>: Interface has %u memory pages. Selector register is %s" % (name, pages, selector)    
        tmpSlave.pageSelect = selector    
        tmpSlave.pages      = pages    
        tmpSlave.renderAll()    
        ifList.append(tmpSlave)
        

def writeMainVhd(filename):
    
    fo = open(filename, "w")
    v = gVhdlStr(autoUnitName, filename, author, version, date)

    header = adj(v.header + ['\n'], [':'], 0)
    
    for line in header:
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
    fo = open(filename, "w")
    
    v = gVhdlStr(autoUnitName, filename, author, version, date)

    header = adj(v.header + ['\n'], [':'], 0)
    
    for line in header:
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
    fo = open(filename, "w")
    
    gc     = gCStr(filename, unitname, author, version, date)
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
    
  

xmlIn = "testme.xml"

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
version     = "unknown version"
date    = "%02u/%02u/%04u" % (now.day, now.month, now.year)

parseXML(xmlIn)

autoUnitName = unitname + "_auto"

#filenames for various output files
fileMainVhd     = autoUnitName              + ".vhd"
filePkgVhd      = autoUnitName  + "_pkg"    + ".vhd"

fileStubVhd     = unitname                  + ".vhd"
fileStubPkgVhd  = unitname      + "_pkg"    + ".vhd"
fileTbVhd       = unitname      + "_tb"     + ".vhd"

fileHdrC        = unitname                  + ".h"


(portList, recordList, regList, sdbList, vAdrList, fsmList, genList, cAdrList) = mergeIfLists(ifList)

writeMainVhd(fileMainVhd)
writePkgVhd(filePkgVhd)
#writeStubVhd(fileStubVhd)
#writeTbVhd(fileTbVhd)
writeHdrC(fileHdrC)







