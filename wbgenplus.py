# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/mkreider/.spyder2/.temp.py
"""
from xml.dom import minidom
import string
import datetime

now = datetime.datetime.now()

def setColIndent(sLine, level, tabsize=3):
    if(sLine == ""):
        s = ""
    else:    
        ind = ' ' * (tabsize * level)        
        s = ind + sLine#s = sLine.lstrip(' ')    
    return s      

def i1(sLine, level, tabsize=3):
    return setColIndent(sLine, level, tabsize)
    
def setColsIndent(sLines, level, tabsize=3):
    l = []    
    for i in range(0, len(sLines)):    
        l.append(setColIndent(sLines[i], level, tabsize))    
    return l

def iN(sLines, level, tabsize=3):
    return setColsIndent(sLines, level, tabsize)

def getMaxBlockColByMark(sLines, cMark, tabsize):
    offs = 0
    for line in sLines:
        if(line.find(cMark) > offs):
            offs = line.find(cMark)
            
    alignedOffs = ((offs + tabsize - 1) // tabsize) * tabsize;        
    #print "Mark: <%s> Offs: %u Aoffs: %u\n" % (cMark, offs, alignedOffs)
    return alignedOffs 

def adjColByMark(sLine, cMark, offs):
    pos = sLine.find(cMark)
    ins = ' ' * (offs - pos)
    s = sLine[:pos] + ins + sLine[pos:]    
    return s

def adjBlockByMarks(sLines, cMarks, indentLvl, tabsize=3):
    l  = setColsIndent(sLines, indentLvl, tabsize)
        
    for mark in cMarks:
        offs    = getMaxBlockColByMark(l, mark, tabsize)
        
        for i in range(0, len(l)):    
            sLine = l[i]
            sLine = adjColByMark(sLine, mark, offs)   
            l[i] = sLine    
    
    return l

def mskWidth(msk):
    result  = 0
    if(msk != 0): 
        aux     = bin(msk).split('b')
        tmpmsk  = aux[-1];
        hiIdx   = len(tmpmsk)-1 - tmpmsk.find('1')        
        tmpmsk  = tmpmsk[::-1]
        loIdx   = tmpmsk.find('1')
        result  = [hiIdx, loIdx]
    return result   

class VhdlStr(object):
   

    def __init__(self, pages):
        self.filename   = ""       
        self.pages      = pages
       
  
  
      
  
    def fsmPageSel(self, name, pageSel):
        if(pageSel == ""):
            return "\n"
        else:    
            return self.wbsPageSelect % (name, pageSel)
  
    def fsmRead(self, regList, name):
        s = []    
        #print "r ------------------------------ "        
        for elem, nextElem in zip(regList, regList[1:]+[regList[0]]):
            #print "a %s b %s %u" % (elem[0], nextElem[0], elem[3].find('r'))         
            if(elem[3].find('r') > -1):
                if(elem[3].find('m') > -1):
                    ind = '(v_page)'
                else:
                    ind = ""
                #  wbRead      = "when c_%s => r_%s_out.dat(r_%s.%s'range) <= r_%s.%s; %s\n"          
                s.append(self.wbRead % (elem[0] + elem[1], name, name, elem[0]+ind, name, elem[0]+ind, elem[4]))
        return s

    def fsmWrite(self, regList, name):
        s = []    
        #print "W ------------------------------ " 
        for elem, nextElem in zip(regList, regList[1:]+[regList[0]]):
            if(elem[3].find('w') > -1):
                if(elem[3].find('m') > -1):
                    ind = '(v_page)'
                else:
                    ind = ""
                        
                #wbWrite     = "when c_%s => r_%s.%s <= f_wb_wr(r_%s.%s, v_dat_i, v_sel, \"%s\"); %s\n"
                s.append(self.wbWrite % (elem[0] + elem[1], name, elem[0]+ind, name, elem[0]+ind, self.wrModes[elem[1]], elem[4]))
        return s     
    
    def regs(self, regList, qty = 0):
       recordelements   = []
       types            = []
       m                = []
       for elem, nextElem in zip(regList, regList[1:]+[regList[0]]):
           if(elem[0] != nextElem[0]):
               if(elem[3].find('m') > -1):
                   types            += self.multitype(elem, self.pages)
                   recordelements   += self.multielement(elem, self.pages)                    
               else:    
                   recordelements.append(self.reg(elem))
       return [types, recordelements]           
    
    def reg(self, (name, suf, msk, rw, desc, adr)):
        (idxHi, idxLo) = mskWidth(msk);        
        s = self.signalSlv % (name, idxHi-idxLo, 0, desc)        
        return s
    

    def multitype(self, (name, suf, msk, rw, desc, adr), qty = 1):
        s = []        
        (idxHi, idxLo) = mskWidth(msk);
        s.append('\n')        
        s.append(self.slvSubType % (name, idxHi-idxLo, 0)) #shift mask to LSB
        s.append(self.slvArrayType % (name, name))
        return s 
    
    def multielement(self, (name, suf, msk, rw, desc, adr), qty = 1):
        s = []        
        (idxHi, idxLo) = mskWidth(msk);
        s.append('\n')        
        if(type(qty) == int):
            s.append(self.signalSlvArray % (name, name, (qty-1), desc))
        else:
            s.append(self.signalSlvArray % (name, name, qty + '-1', desc))
        return s    
              
    
    def cRegAdr(self, (name, suf, msk, rw, desc, adr)):
        s = self.constRegAdr % (name + suf, adr, adr, rw, msk, desc)        
        return s
    
    def resets(self, regList, name):
       s = []
       for elem, nextElem in zip(regList, regList[1:]+[regList[0]]):
           if(elem[0] != nextElem[0]):
               if(elem[3].find('m') > -1):
                   s.append("r_" + name + '.' + elem[0] + " <= (others =>(others => '0'));\n")                  
               else:    
                   s.append("r_" + name + '.' + elem[0] + " <= (others => '0');\n")
       return s
    
    wrModes = {'_GET'   : 'owr',
               '_SET'   : 'set',
               '_CLR'   : 'clr', 
               '_OWR'   : 'owr',
               '_RW '   : 'owr'}    
    
    header      = ["-- File Name : %s\n",       # fileName
                   "-- Design Unit Name : %s\n",    # autoUnitName
                   "-- Revision : %s\n",            # Revision
                   "-- Author : %s\n",              # Author
                   "-- Created: %s\n"]              # Date        
    
    libraries   = ["library ieee;\n",
                   "use ieee.std_logic_1164.all;\n",
                   "use ieee.numeric_std.all;\n",
                   "use work.wishbone_pkg.all;\n"]
                   
    
    nl          = "\n"
    snl          = ";\n"
    lnl         = "\n)\n"    


    packageStart = "package %s_pkg is\n\n" # autoUnitName
    componentStart = "component %s is\n" # autoUnitName
    componentMid   = "Port(\n"    
    componentEnd   = [");\n",
                      "end component;\n\n"] 
    packageBodyStart = "package body %s_pkg is\n" # autoUnitName 
    packageEnd = "end %s_pkg;\n" # autoUnitName    
    
    entityStart = "entity %s is\n" # autoUnitName
    genStart = "generic(\n"
    genEnd = ");\n" 
     
    entityMid   = "Port(\n"
    entityEnd   = ");\nend %s;\n\n"
    
    archDecl    = "architecture rtl of %s is\n\n" # autoUnitName
    archStart   = "\n\nbegin\n\n"
    archEnd     = "end rtl;\n" # autoUnitName
    
    genport     = "g_%s : %s := %s%s -- %s\n" #name, type, default
    signalSlv   = "%s : std_logic_vector(%u downto %u); %s\n" #name, idxHi, idxLo, desc
    signalSl    = "signal %s : std_logic; %s\n" #name, desc
    constRegAdr = "constant c_%s : natural := 16#%x#; -- 0x%02X, %s, _0x%08x %s\n" #name, adrVal, adrVal, rw, msk, desc
  
    
    masterIf    = ["%s_o : out t_wishbone_master_out;\n", # name
                   "%s_i : in  t_wishbone_master_in := ('0', '0', '0', '0', '0', x\"00000000\")"] # name
    
    slaveIf     = ["%s_i : in  t_wishbone_slave_in := ('0', '0', x\"00000000\", x\"F\", '0', x\"00000000\");\n", #name
                   "%s_o : out t_wishbone_slave_out"] #name
    
   
    commBoxLine     = "--+" + '*' * 90 + "+\n"
    commBoxCont0    = "--| %s" #topic
    commBoxCont1    = "|\n" #topic
        
       
    wbs0         = ["%s : process(clk_sys_i)\n", 
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
      
    wbs1         = ["else\n",
                    "   -- short names\n",
                    "   v_dat_i           := %s_i.dat;\n",
                    "   v_adr             := to_integer(unsigned(%s_i.adr(%s)) & \"00\");\n",
                    "   v_sel             := %s_i.sel;\n",
                    "   v_en              := %s_i.cyc and %s_i.stb and not r_%s_out.stall;\n",
                    "   v_we              := %s_i.we;\n\n",
                    "   --interface outputs\n",
                    "   r_%s_out.stall  <= '0';\n",
                    "   r_%s_out.ack    <= '0';\n",
                    "   r_%s_out.err    <= '0';\n",
                    "   r_%s_out.dat    <= (others => '0');\n" ] 
    
    wbsPageSelect   = "v_page := to_integer(unsigned(r_%s.%s));\n\n"    
    
    slvSubType      = "subtype t_slv_%s is std_logic_vector(%u downto %u);\n"
    slvArrayType    = "type    t_slv_%s_array is array(natural range <>) of t_slv_%s;\n"
    signalSlvArray  = "%s : t_slv_%s_array(%s downto 0); %s\n"
      

    wbs2 = ["if(v_en = '1') then\n",
            "   r_%s_out.ack  <= '1';\n",
            "   if(v_we = '1') then\n",
            "      -- WISHBONE WRITE ACTIONS\n",
            "      case v_adr is\n"]
    
    wbs3 = ["   end case;\n",
            "else\n",
            "   -- WISHBONE READ ACTIONS\n",
            "   case v_adr is\n"]  

    wbs4 = ["               end case;\n",
            "            end if; -- v_we\n",
            "         end if; -- v_en\n",
            "      end if; -- rst\n",
            "   end if; -- clk edge\n",
            "end process;\n\n"]

    wbWrite     = "when c_%s => r_%s.%s <= f_wb_wr(r_%s.%s, v_dat_i, v_sel, \"%s\"); %s\n"
    
    wbRead      = "when c_%s => r_%s_out.dat(r_%s.%s'range) <= r_%s.%s; %s\n"
    
    wbOthers    = "when others => r_%s_out.ack <= '0'; r_%s_out.err <= '1';\n"

    sdbtemplate = ['constant c_%s_sdb : t_sdb_device := (',
                   'abi_class => x"%s", -- %s',
                   'abi_ver_major => x"%s",\n',
                   'abi_ver_minor => x"%s",\n',
                   'wbd_endian    => c_sdb_%s,\n',
                   'wbd_width     => x"%s", -- 8/16/32-bit port granularity\n',
                   'sdb_component => (\n',
                   'addr_first    => x"%s",\n',
                   'addr_last     => x"%s",\n',
                   'product => (\n',
                   'vendor_id     => x"%s", -- %s\n',
                   'device_id     => x"%s",\n',
                   'version       => x"%s",\n',
                   'date          => x"%s",\n',
                   'name          => "%s")));\n']
    #def addGen(self, name, gtype, value, desc):
        #self.genList.append([name, gtype, value, desc])

class wbsIf():

    #startAdr    = 0
    #name        = ""
    
    #regs        = []
    
    #portList    = []
    #adrList     = []
    #regList     = []     
    #fsmList     = []
    #v = None
        
    
    def __init__(self, name, startAdr, adrBits, pageSelect, pages):
        self.regs       = []        
        self.portList   = []
        self.regList    = []
        self.recordList = []
        self.adrList    = []
        self.fsm        = []
        self.name       = name        
        self.startAdr   = startAdr
        self.adrBits    = adrBits
        self.pageSelect = pageSelect
        self.pages      = pages
        self.v = VhdlStr(self.pages)        
        
        

    
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
        a = []        
        a.append(self.v.slaveIf[0] % self.name)
        a.append(self.v.slaveIf[1] % self.name)
        self.portList = a # no need to indent, we'll do it later with all IF lists together  
  
    def renderPorts(self):
        a = []        
        a.append("%s_regs_o : out t_%s_regs;\n" % (self.name, self.name))        
        a.append(self.v.slaveIf[0] % self.name)
        a.append(self.v.slaveIf[1] % self.name)
        self.portList = a # no need to indent, we'll do it later with all IF lists together      
        
        
    def renderFsm(self):
        hdr0 = []
        hdr0.append(self.v.wbs0[0] % self.name)
        for i in range(1, len(self.v.wbs0)):        
            hdr0.append(self.v.wbs0[i])
        hdr0 = iN(hdr0, 1)
        rstaux = "r_%s_out <= ('0', '0', '0', '0', '0', x\"00000000\");\n" % self.name
        rst = adjBlockByMarks(self.v.resets(self.regs, self.name) + [rstaux], ['<='], 4)       
        
        hdr1 = []        
        hdr1.append(self.v.wbs1[0])
        hdr1.append(self.v.wbs1[1]) 
        hdr1.append(self.v.wbs1[2] % self.name)
        hdr1.append(self.v.wbs1[3] % (self.name, '%u downto %u' % (self.adrBits-1, 2)))
        hdr1.append(self.v.wbs1[4] % self.name)
        hdr1.append(self.v.wbs1[5] % (self.name, self.name, self.name))
        hdr1.append(self.v.wbs1[6] % self.name)
        hdr1.append(self.v.wbs1[7])
        for i in range(8, len(self.v.wbs1)):        
            hdr1.append(self.v.wbs1[i] % self.name)
        
        hdr1    = iN(hdr1, 3)
        psel    = iN([self.v.fsmPageSel(self.name, self.pageSelect)], 4)
        
        hdr2    = []   
        hdr2.append(self.v.wbs2[0])
        hdr2.append(self.v.wbs2[1] % self.name)
        hdr2.append(self.v.wbs2[2])
        hdr2.append(self.v.wbs2[3])
        hdr2.append(self.v.wbs2[4])
        hdr2 = iN(hdr2, 4)
        
        wr      = self.v.fsmWrite(self.regs, self.name)        
        swr     = adjBlockByMarks(wr, ['=>', '<=', 'v_dat_i'], 7)    
        mid0    = iN([self.v.wbOthers % (self.name, self.name)], 7)
        mid1    = iN(self.v.wbs3, 5)
        rd      = self.v.fsmRead(self.regs, self.name)       
        srd     = adjBlockByMarks(rd, ['=>', '<=', "--"], 7)
        ftr     = iN(self.v.wbs4, 1)
        
        self.fsmList = hdr0 + rst + hdr1 + psel +  hdr2 + swr + mid0 + mid1 + srd + mid0 + ftr
    
    def renderRecords(self):
        a = []
        (types, records) = self.v.regs(self.regs)
        a += types     
        a.append("type t_%s_regs is record\n" % self.name)
        a += (iN(records, 1))
        a.append("end record t_%s_regs;\n\n" % self.name)    
        self.recordList = a
    
    def renderRegs(self):
        a = []        
        a.append("signal r_%s_out : t_wishbone_slave_out; --> WB output buffer register\n" % self.name)
        a.append("signal r_%s : t_%s_regs;\n" % (self.name, self.name))
        self.regList = a # no need to indent, we'll do it later with all IF lists together

        
    def renderAdr(self):
        a = []        
        for line in self.regs:
            a.append(self.v.cRegAdr(line))
        self.adrList = a # no need to indent, we'll do it later with all IF lists together
        #adjBlockByMarks(a, [':', ':=', '-- 0x', '-->'], 1)
        
    
    def renderAll(self):
               
        self.renderPorts()
        self.renderAdr()
        print "%s regs: %u" % (self.name, len(self.regs))
        self.renderRecords()        
        self.renderRegs()
        self.renderFsm()
        print "%s regs: %u" % (self.name, len(self.regList))   

    



    
codeGen = set(['vhdl', 'C', 'C++'])    

genTypes = {'u'        : 'unsigned',
            'uint'     : 'natural', 
            'int'      : 'integer', 
            'bool'     : 'boolean',
            'string'   : 'string',
            'sl'       : 'std_logic',
            'slv'      : 'std_logic_vector'}    




def parseNumeral(num, default = None):
    result = default 
    if(num.find('0x') == 0):       
        base = 16
    elif(num.find('0b') == 0):
        base = 2  
    else:
        base = 10
    
    try:
        result = int(num, base)
    except ValueError:
        result = default
    return result    
                
def commentLine(ifType, ifName):
    l = []
    tmp = VhdlStr.commBoxCont0 % ifType
    a = len(VhdlStr.commBoxLine)
    b = len(tmp)
    c = len(ifName)
    d = a - (b + c + 3 + 2)
    pad0 = d // 2 - len(ifType)
    pad1 = d - pad0
    cont = tmp + ' ' + ('-' * pad0) + ' ' + ifName + ' ' + ('-' * pad1) + VhdlStr.commBoxCont1   
    l.append(cont)
    return l 

def commentBox(ifType, ifName):
    l = []
    l.append(VhdlStr.commBoxLine)
    tmp = VhdlStr.commBoxCont0 % ifType
    a = len(VhdlStr.commBoxLine)
    b = len(tmp)
    c = len(ifName)
    d = a - (b + c + 3 + 2)
    print "line %u start %u name %u sum %u" % (a, b, c, d)
    pad0 = d // 2 - len(ifType)
    pad1 = d - pad0
    
    cont = tmp + ' ' + (' ' * pad0) + ' ' + ifName + ' ' + (' ' * pad1) + VhdlStr.commBoxCont1   
    l.append(cont)
    l.append(VhdlStr.commBoxLine)
 
    return l    
    
def mergeIfLists(slaveList=[], masterList = []):
    uglyPortList    = ["clk_sys_i : in  std_logic;\n",
                       "rst_n_i   : in  std_logic;\n\n"]    
    recordList      = []                   
    uglyRegList     = []
    uglyAdrList     = []     
    fsmList         = [] 
    genList         = []
    
    print len(slaveList)
    for slave in slaveList:
        uglyPortList += slave.portList
        #deal with vhdl not wanting a semicolon at the last port entry        
        if(slave != slaveList[-1]):
            uglyPortList[-1] += ";\n"
        else:
            uglyPortList[-1] += "\n"
        uglyPortList  += "\n"    
        uglyAdrList  += iN(commentLine("WBS Adr", slave.name), 1) 
        uglyAdrList  += adjBlockByMarks(slave.adrList, [ ':', ':=', '-- 0x', '_0x', '--> '], 1)
        uglyAdrList  += "\n"
        uglyRegList  += iN(commentLine("WBS Regs", slave.name),1) 
        uglyRegList  += adjBlockByMarks(slave.regList, [' is ', ':', ':=', '-->'], 1)
        uglyRegList  += "\n"
        fsmList      += iN(commentBox("WBS FSM", slave.name), 1)
        fsmList      += slave.fsmList   
        fsmList      += "\n\n"
        recordList   += iN(commentLine("WBS Register Records", slave.name), 1) 
        recordList   += adjBlockByMarks(slave.recordList, [ ':', '--> '], 1)
        
    for master in masterList:
        uglyPortList += master.portList
        uglyAdrList  += master.AdrList       
        uglyRegList  += master.regList    
    
    portList    = adjBlockByMarks(uglyPortList, [':', ':=', '--'], 1)    
    regList     = iN(commentBox("", "WB Registers"), 1) + ['\n']\
                + uglyRegList
                
                
    adrList     = iN(commentBox("", "WB Adress Map"), 1) + ['\n']\
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
        genList.append(VhdlStr.genport % (genName, genType, genVal, lineEnd, genDesc))
        idx += 1
    for genName in genMiscD.iterkeys():
        if(idx == lastIdx):
            lineEnd = ''
        else:
            lineEnd = ';'
        (genType, genVal, genDesc) = genMiscD[genName]
        genList.append(VhdlStr.genport % (genName, genType, genVal, lineEnd, genDesc))
        idx += 1
    genList = adjBlockByMarks(genList, [':', ':=', '--'], 1)             
    #Todo: missing generics 
    return [portList, recordList, regList, adrList, fsmList, genList]           

def parseXML(xmlIn):
    xmldoc      = minidom.parse(xmlIn)   
    global unitName
    global author 
    global version
    
    unitName = xmldoc.getElementsByTagName('wbdevice')[0].getAttribute('unitname')
    author   = xmldoc.getElementsByTagName('wbdevice')[0].getAttribute('author')
    version  = xmldoc.getElementsByTagName('wbdevice')[0].getAttribute('version')

    
    genericsParent = xmldoc.getElementsByTagName('generics')
    if len(genericsParent) != 1:
        print "There must be exactly 1 generics tag!"
    else:
        print "Found generics" 
    genericsList = genericsParent[0].getElementsByTagName('item')
    for generic in genericsList:
        genName = generic.getAttribute('name')
        genType = generic.getAttribute('type')
        genVal  = generic.getAttribute('value')
        genDesc = generic.getAttribute('comment')
        if genTypes.has_key(genType):
            genType = genTypes[genType]               
            if(genType == 'natural'):
                aux = parseNumeral(genVal)
                if(not aux):            
                    print "Generic <%s>'s numeric value <%s> is invalid" % (genName, genVal)
                else:        
                    genVal = aux
                    genIntD[genName] = [ genType , genVal, genDesc ]
            else:
                genMiscD[genName] = [ genType , genVal, genDesc ]    
        else:
            print "%s is not a valid type" % generic.getAttribute('type')
    
    slaveIfList = xmldoc.getElementsByTagName('slaveinterface')
    for slaveIf in slaveIfList:
          
        name    = slaveIf.getAttribute('name')
        ifWidth = parseNumeral(slaveIf.getAttribute('data'))
        pages   = slaveIf.getAttribute('pages')
        #check integer generic list
        print "PAGES0: %s\n" % pages
        for genName in genIntD.iterkeys():
            if(pages.find(genName) > -1):
                (genType, genVal, genDesc) = genIntD[genName]
                print "Val: %s\n" % genVal                
                pages = pages.replace(genName, str(genVal))
                
        print "PAGES: %s\n" % pages 
        aux = parseNumeral(pages)
        if(not aux):            
            print "Pages' numeric value <%s> is invalid" % (pages)
            pages = 0
        else:        
            pages = aux
    
        tmpSlave = wbsIf(name, 0, 32, '', pages)  
                
                
        #get child nodes
        slaveIfChildren = slaveIf.childNodes
        #sdb record
        sdb = slaveIf.getElementsByTagName('sdb')
        vendId  = sdb[0].getAttribute('vendorID')
        prodId  = sdb[0].getAttribute('productID')
    
        
        selector = ""
        #name, adr, pages, selector
        #registers
        registerList = slaveIf.getElementsByTagName('reg')
        for reg in registerList:
            regname = reg.getAttribute('name')
            regdesc = reg.getAttribute('comment')
                   
                    
            
            if reg.hasAttribute('address'):            
                regadr = reg.getAttribute('address')            
                aux = parseNumeral(regadr)
                if(not aux):            
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
                aux = parseNumeral(regmsk)
                
                if(not aux):
                    aux = 2^ int(ifWidth) -1
                    print "Slave <%s>: Register <%s>'s supplied mask <%s> is invalid, defaulting to %x" % (name, regname, regmsk, aux)
                if(idxCmp > -1):            
                    regmsk = 2**aux-1 
                else:
                    regmsk = aux                        
            else:        
                print "Slave <%s>: No mask for Register <%s> supplied, defaulting to %x" % (name, regname, 2**ifWidth-1)
                regmsk = 2**ifWidth-1
            
         
            if (reg.getAttribute('atomic')):
                tmpSlave.addAtomicReg(regname, regmsk, regrwmf, regdesc)
            else:        
                tmpSlave.addSimpleReg(regname, regmsk, regrwmf, regdesc)
            #x.addSimpleReg('NEXT2',     0xfff,  'rm',   "WTF")    
        print "changing slave sel to %s and pages to %s" % (selector, pages)    
        tmpSlave.pageSelect = selector    
        tmpSlave.pages      = pages    
        tmpSlave.renderAll()    
        ifList.append(tmpSlave)
        

def writeMainVhd(filename):
    
    fo = open(filename, "w")
    
    header = []
    header.append(VhdlStr.header[0] % filename)
    header.append(VhdlStr.header[1] % autoUnitName)
    header.append(VhdlStr.header[2] % version)
    header.append(VhdlStr.header[3] % author)
    header.append(VhdlStr.header[4] % date)
    header.append('\n')
    header = adjBlockByMarks(header, [':'], 0)
    
    for line in header:
        fo.write(line)
    
    libraries = []
    libraries += VhdlStr.libraries
    libraries += "use work.%s_pkg.all;\n\n" % autoUnitName
    for line in libraries:
        fo.write(line)
        
    fo.write(VhdlStr.entityStart % autoUnitName)
    
    if(len(genIntD) + len(genMiscD) > 0):
        fo.write(VhdlStr.genStart)
        for line in genList:   
            fo.write(line)
        fo.write(VhdlStr.genEnd)
    
    fo.write(VhdlStr.entityMid)
    
    for line in portList:
        fo.write(line)
        
    fo.write(VhdlStr.entityEnd % autoUnitName)
    
    fo.write(VhdlStr.archDecl % autoUnitName)
    
    for line in adrList:
        fo.write(line)
    
    for line in regList:
        fo.write(line)
    
    fo.write(VhdlStr.archStart)
    
    for line in fsmList:
        fo.write(line)
    
    fo.write(VhdlStr.archEnd)
    
    fo.close

def writePkgVhd(filename):
    fo = open(filename, "w")
    
    header = []
    header.append(VhdlStr.header[0] % filename)
    header.append(VhdlStr.header[1] % autoUnitName)
    header.append(VhdlStr.header[2] % version)
    header.append(VhdlStr.header[3] % author)
    header.append(VhdlStr.header[4] % date)
    header.append('\n')
    header = adjBlockByMarks(header, [':'], 0)
    
    for line in header:
        fo.write(line)
    
    libraries = []
    libraries += VhdlStr.libraries
    libraries += '\n'
    for line in libraries:
        fo.write(line)
    
    
    fo.write(VhdlStr.packageStart % autoUnitName)
    
    decl = []
    for line in recordList:
        decl.append(line)
    decl += (iN(commentLine("Component", autoUnitName), 1)) 
    
    for line in decl:
        fo.write(line)    
    
    decl = []
    decl.append(VhdlStr.componentStart % autoUnitName)
    if(len(genIntD) + len(genMiscD) > 0):
        decl.append(VhdlStr.genStart)
        for line in genList:   
            decl.append(line)
        decl.append(VhdlStr.genEnd)
    decl.append(VhdlStr.entityMid)
    for line in portList:
        decl.append(line)
    decl += VhdlStr.componentEnd
    decl = iN(decl, 1)
    for line in decl:
        fo.write(line)
        
    fo.write(VhdlStr.packageEnd % autoUnitName)
    fo.write(VhdlStr.packageBodyStart % autoUnitName)
    fo.write(VhdlStr.packageEnd % autoUnitName)
    
    fo.close

#TODO: A lot ...
            
#        codegenParent = self.xmldoc.getElementsByTagName('codegen')
#        if len(codegenParent) != 1:
#            print "There must be exactly 1 codegen tag!"
#        else:
#            print "Found codegen"    
#            codegenList = codegenParent[0].getElementsByTagName('generate')
#            for generator in codegenList:
#                s = generator.getAttribute('language')
                #if(set([s]).issubset(codeGen)):
                    #valid language
#                else:
                    #nothing
        
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
adrList     = []
fsmList     = []
genList     = []
ifList      = []
unitName    = "unknown unit"
author      = "unknown author"
version     = "unknown version"
date    = "%02u/%02u/%04u" % (now.day, now.month, now.year)

parseXML(xmlIn)
autoUnitName = unitName + "_auto"

fileMainVhd = autoUnitName              + ".vhd"
filePkgVhd  = autoUnitName  + "_pkg"    + ".vhd"
fileTbVhd   = unitName      + "_tb"     + ".vhd"
fileHdrC    = unitName                  + ".h"


(portList, recordList, regList, adrList, fsmList, genList) = mergeIfLists(ifList)
writeMainVhd(fileMainVhd)
writePkgVhd(filePkgVhd)









