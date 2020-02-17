# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 16:58:20 2015

@author: mkreider
"""
import datetime
from textformatting import setColIndent as i1


def il0(slist):
    return slist

def il1(slist):
    return i1(slist, 1)
    
def il2(slist):
    return i1(slist, 2)

def il3(slist):
    return i1(slist, 3)

def il4(slist):
    return i1(slist, 4)

def il5(slist):
    return i1(slist, 5)

    

class wbsCStr(object):
   

    def __init__(self, pages, unitname, slaveIfName, sdbVendorID, sdbDeviceID):
        self.unitname     = unitname
        self.slaveIfName  = slaveIfName        
        self.pages        = pages
        


class gCStr(object):
    def __init__(self, filename, unitname, author, email, version, date, sdbVendorID, sdbDeviceID):
        self.unitname   = unitname     
        self.author     = author
        self.email      = email
        self.version    = version
        self.date       = date
        self.dateStr    = "%02u/%02u/%04u" % (date.day, date.month, date.year)
        self.header     = ["/** @file        %s\n" % filename,                 
                           "  * DesignUnit   %s\n" % unitname,                           
                           "  * @author      %s <%s>\n" % (author, email),
                           "  * @date        %s\n" % self.dateStr,
                           "  * @version     %s\n" % version,                     
                           "  * @copyright   %04u GSI Helmholtz Centre for Heavy Ion Research GmbH\n" % (date.year),
                           "  *\n"
                           "  * @brief       Register map for Wishbone interface of VHDL entity <%s>\n" % (self.unitname + "_auto"),                     
                           "  */\n\n"]
        self.hdrfileStart   = ["#ifndef _%s_H_\n"   % unitname.upper(),
                               "#define _%s_H_\n\n" % unitname.upper()]
        self.sdbVendorId    =  ""
        self.sdbDeviceId    =  ""    
        if (sdbVendorID is not None) and (sdbDeviceID is not None):                           
            self.sdbVendorId    =  "#define %s_SDB_VENDOR_ID 0x%08x\n" % (unitname.upper(), sdbVendorID)
            self.sdbDeviceId    =  "#define %s_SDB_DEVICE_ID 0x%08x\n\n" % (unitname.upper(), sdbDeviceID)
        self.hdrfileEnd     =  "\n#endif\n"        


        





class syncVhdlStr(object):
    def __init__(self, name, depth, width, genWidthPrefix, pages, genPagePrefix, clkdomain, clkbase, direction):
        
        self.direction = direction        
        
        fifo   = "%s_fifo_%s_" % (name, direction)       
        decl   = "signal %s : std_logic;\n"
        port   = "%s : %s std_logic;\n"
        portI  = "%%s_%s_i" % clkdomain
        portSI = "s_%s_i"
        portSO = "s_%s_o"
        portO  = "%%s_%s_o" % clkdomain
        sig    = "s_%s"        
        reg    = "r_%s"        
        
        push   = fifo + "push"
        pop    = fifo + "pop"
        full   = fifo + "full"
        amfull = fifo + "almost_full"
        empty  = fifo + "empty"            
        
        self.push   = sig % push
        self.pop    = sig % pop
        self.full   = sig % full
        self.amfull = sig % amfull
        self.empty  = sig % empty
        
        matrixPageStr   = ""
        sigInWrapper    = "%s"
        sigOutWrapper   = "%s"
        if pages > 0:
            matrixPageStr   = "%s%s * " % (genPagePrefix, pages)
            sigInWrapper    = "mflat(%s)"
            sigOutWrapper   = "minfl(%s)"
        syncwidth = "%s%s%s" % (matrixPageStr, genWidthPrefix, width)
        
        self.syncSigsDeclaration = []        
        
        if direction == "out":
            self.syncSigsDeclaration  += [decl % (portSO % name)]
            sigin   = sigInWrapper  % (reg % name)
            sigout  = (portO % name)
            #sigout  = (portSO % name)
            clkin   = wbsVhdlStrGeneral.clkportname % (clkbase)
            clkout  = wbsVhdlStrGeneral.clkportname % (clkdomain)
            self.syncPortDeclaration    = [port % ((portI % pop), "in"), 
                                           port % ((portO % empty), direction) ]
            self.syncInstTemplate0      = ["\n",
                                           #"%s <= %s;\n" % ((portO % name), (portSO % name)),
                                           "%s <= %s;\n" % ((portO % empty), self.empty),
                                           "%s <= %s;\n\n" % (self.pop, (portI % pop)),
                                           ] 
        elif direction == "in":
            sigin   = sigInWrapper  % (portI % name)
            sigout  = (portSI % name)
            clkin   = wbsVhdlStrGeneral.clkportname % (clkdomain)
            clkout  = wbsVhdlStrGeneral.clkportname % (clkbase)
            self.syncPortDeclaration = [port % ((portI % push), direction) , 
                                        port % ((portO % full), "out") ]
            self.syncInstTemplate0   = ["\n",
                                       "%s <= not %s;\n"  % (self.pop, self.empty),
                                       "%s <= %s;\n"      % ((portO % full), self.full),
                                       "%s <= %s;\n\n"      % (self.push, (portI % push))]
        else:
            print "ERROR: Port direction <%s> of Register <%s> is unknown. Choose <in> or <out>" % (direction, self.name)
                
 
        self.syncSigsDeclaration  += [decl % (self.push), 
                                     decl % (self.pop), 
                                     decl % (self.full), 
                                     decl % (self.amfull),
                                     decl % (self.empty)
                                     ] 
         
        self.syncInstTemplate1      = ["%s_FIFO_%s : generic_async_fifo\n" % (name, direction),
                                       "generic map(\n",
                                       "  g_data_width          => %s,\n" % (syncwidth),
                                       "  g_size                => %s,\n" % (depth),
                                       "  g_show_ahead          => true,\n",
                                       "  g_with_rd_empty       => true,\n",
                                       "  g_with_wr_almost_full => true,\n",                                        
                                       "  g_with_wr_full        => true)\n",
                                       "port map(\n",
                                       "  rst_n_i  => %s,\n" % wbsVhdlStrGeneral.rstportname % (clkbase),
                                       "  we_i     => %s,\n" % (self.push), 
                                       "  rd_i     => %s,\n" % (self.pop), 
                                       "  rd_empty_o  => %s,\n" % (self.empty), 
                                       "  wr_full_o   => %s,\n" % (self.full), 
                                       "  clk_wr_i => %s,\n" % (clkin),                        
                                       "  clk_rd_i => %s,\n" % (clkout),
                                       "  d_i      => %s,\n" % (sigin),
                                       "  q_o      => %s);\n\n" % (sigout)]

           


class registerVhdlStr(object):
    others             = "(others => '%s')"
    wrModes = {'_GET'  : 'owr',
               '_SET'  : 'set',
               '_CLR'  : 'clr',
               '_OWR'  : 'owr',
               '_RW'   : 'owr'} 
    
    def __init__(self, wbsStr, name, description, reset, genResetPrefix, width, genWidthPrefix, pages, genPagePrefix, clockDomain, wbDomain):
        self.int2slv    = "std_logic_vector(to_unsigned(%%s, %s))" % (width)
        self.ghex2slv   = "std_logic_vector(to_unsigned(16#%%s#, %s))" % (width)
        self.hex2slv    = 'x"%s"'    
        self.bin2slv    = '"%s'
        if reset is None:
            self.resetvector = registerVhdlStr.others % 0
        else: 
           self.resetvector = self.int2slv % (str(genResetPrefix) + str(reset)) 
           if(str(reset).find('0x') > -1):
               tmpRst = (reset.replace('0x', '')).lower()
               if width == len(tmpRst)*4:
                   self.resetvector = self.hex2slv % tmpRst                    
               else:
                   if len(tmpRst)*4 > 32:
                       print "Register <%s>'s Resetvector <%s> length <%s> is not a multiple of four AND is longer than 32 bit. Sorry, can't convert that" % (name, reset, width)
                       exit(2)
                   else:    
                       print "Register <%s>'s Resetvector <%s> has the wrong bitlength (is %s, should be %s). Converting" % (name, reset, len(tmpRst)*4, width)                    
                       self.resetvector = self.ghex2slv % tmpRst 
                   
           elif(str(reset).find('0b') > -1):
             self.resetvector = self.bin2slv % reset.replace('0b', '')    
          
        self.pages          = pages
        self.genPagePrefix  = genPagePrefix
        self.width          = width
        self.genWidthPrefix = genWidthPrefix 
            
        self.clockDomain    = clockDomain
        self.wbDomain       = wbDomain
       
        self.name           = name
        self.regname        = "r_" + name
        self.signame        = "s_" + name
        
        #don't bother mentioning the clk domain in the portname if it is not foreign        
        clkdomainSuffix = ""
        if clockDomain != wbDomain:
            clkdomainSuffix = "_" + clockDomain
        #print "name <%s> Pre <%s> NotPre <%s> Pages>0 <%s> All <%s>" % (name, (genPagePrefix != ""), (genPagePrefix == ""), (pages > 0), (genPagePrefix != "") or ((genPagePrefix == "") and (pages > 0)))
        if (pages != 0):        
            self.dtype          = "matrix(%s%s-1 downto 0, %s%s-1 downto 0)" % (genPagePrefix, pages, genWidthPrefix, width)
            self.reset          = "%s <= mrst(%s);\n" % (self.regname, self.regname)
            self.wbOut          = wbsStr.wbOutMatrix % (self.regname, self.name, "") # Slice
            self.wbRead         = wbsStr.wbRead % (self.name)  #wbsStr.wbReadMatrix % (self.name, self.regname, "") # Slice
            self.wbWrite        = wbsStr.wbWriteMatrix % (self.name, self.regname, self.regname, "") # Slice, Slice
            self.wbPulseZero    = "%s <= mrst(%s);\n" % (self.regname, self.regname)
            self.setHigh        = "%s <= mrst(%s, %s);\n" % (self.regname, self.regname, (self.others % '1'))
        else:
            self.dtype = "std_logic_vector(%s%s-1 downto 0)" % (genWidthPrefix, width)
            self.reset                  = "%s <= %s;\n" % (self.regname, self.resetvector)
            self.wbOut                  = wbsStr.wbOut % (self.name, self.regname, "")  # Slice
            self.wbRead                 = wbsStr.wbRead % (self.name) 
            self.wbWrite                = wbsStr.wbWrite % (self.name, self.regname, self.regname, "") # Slice, Slice
            self.wbPulseZero            = "%s <= %s;\n" % (self.regname,  (self.others % '0'))
            self.setHigh                = "%s <= %s;\n" % (self.regname,  (self.others % '1'))
        
        
        self.portnamein     = name + clkdomainSuffix + "_i"
        self.portvalidin    = name + clkdomainSuffix + "_V_i"
        self.portsignamein  = 's_' + name + "_i"
        self.portsignameout = 's_' + name + "_i"
        self.portsigvalidin = 's_' + name + "_V_i"
        self.portnameout    = name + clkdomainSuffix + "_o"
        self.declaration    = "signal %%s : %s := %s; -- %s\n" % (self.dtype, self.resetvector, description)
        self.port           = "%%s : %%s %s; -- %s\n" % (self.dtype, description)
        
        
        self.sl           = "signal %%s : std_logic; -- %s\n" % (description)        
        # Create all Register Declarations, the reset command, FSM read & write command and pulse generation command  
        self.declarationReg         = self.declaration % (self.regname)
        self.declarationPortSigIn   = self.declaration % (self.portsignamein)
        self.declarationStubIn      = wbsStr.stub % (self.portnamein, self.dtype, description)
        self.declarationStubOut     = wbsStr.stub % (self.portnameout, self.dtype, description) 
        self.declarationPortIn      = self.port % (self.portnamein,  "in ")
        self.declarationPortOut     = self.port % (self.portnameout, "out")        
        
        
        

        #address constant
        self.vhdlConstRegAdr    = wbsStr.vhdlConstRegAdr % (self.name, description) #address, operation, address, mask
        self.cConstRegAdr       = "#define %%s_" + self.name.upper() + "%s 0x%s //%s, %s b, " + description + "\n" 
        self.pythonConstRegAdr  = "'%s%%s' : 0x%%s, # %%s, %%s b, %s\n" % (self.name.lower(), description) #name, adrVal, adrVal, rw, msk, desc
        self.pythonConstAdrReg  = "0x%%s : '%s%%s', # %%s, %%s b, %s\n" % (self.name.lower(), description) #name, adrVal, adrVal, rw, msk, desc              
        self.pythonVal          = "'%s' : %%s, # %s\n" % (self.name.lower(), description)             
        self.pythonFlag         = "'%s' : '%%s', # %s\n" % (self.name.lower(), description) 
        
        #Flow control
        self.wbStall            = wbsStr.wbStall
        self.wbValid            = wbsStr.wbValid % (self.portsigvalidin, self.name,  "")
        self.wbDrive            = wbsStr.wbDrive % (self.portsigvalidin, self.regname, self.portsignamein,  "")
        
        #port assignment, basic or with synchronisation
        
        self.assignStubOut      = wbsStr.assignStub % (self.portnameout, self.portnameout)
        self.assignStubIn       = wbsStr.assignStub % (self.portnamein, self.portnamein)
        
        #assigns the register input port to the register inside the FSM process. Write Arbitration with Wishbone write data, WB wins
        self.readUpdate         = wbsVhdlStrGeneral.assignTemplate % (self.regname, self.portsignamein)
        
        
    
class wbsVhdlStrRegister(object):
    

    def __init__(self, slaveIfName):
        self.slaveIfName    = slaveIfName        
        self.wbRead             = "when c_" + "%s%%s => null;\n" #regname, #op
        self.wbValid            = "%s(0) when c_" + "%s%%s, -- %s\n" #regname + op, #slice, registerName, #slice        
        self.wbDrive            = "if %s = \"1\" then %s <= %s; end if; -- %s\n" #validsignal, register, input
        self.wbOut              = "when c_" + "%s%%s => " + slaveIfName + "_o.dat <= std_logic_vector(resize(unsigned(%s%%s), " + slaveIfName + "_o.dat'length));  -- %s\n" #regname + op, #slice, registerName, #slice        
        self.wbWrite            = "when c_" + "%s%%s => %s%%s <= f_wb_wr(%s%%s, s_d, s_s, \"%%s\"); -- %s\n" #registerName, #op, #slice, registerName, #slice, #opmode, description
        
        self.wbReadMatrix       = "when c_" + "%s%%s => " + slaveIfName + "_o.dat(%%s) <= mget(%s, v_p)%%s; -- %s\n" #regname, #op, #slice, registerName, #slice, description
        self.wbOutMatrix        = "when c_" + "%s%%s => " + slaveIfName + "_o.dat <= std_logic_vector(resize(unsigned(mget(%s, v_p)%%s), " + slaveIfName + "_o.dat'length));  -- %s\n" #regname + op, #slice, registerName, #slice        
        self.wbWriteMatrix      = "when c_" + "%s%%s => mset(%s, f_wb_wr(mget(%s, r_p)%%s, s_d, s_s, \"%%s\"), r_p); -- %s\n" #registerName, registerName, (set/clr/owr), desc
        
        self.vhdlConstRegAdr    = "constant c_" + "%s%%s : natural := 16#%%s#; -- %%s, %%s b, %s\n" #name, adrVal, adrVal, rw, msk, desc
        self.stub               = "signal s_" + slaveIfName + "_%s : %s := (others => '0'); -- %s\n"
        self.assignStub         = "%s => s_" + slaveIfName + "_%s,\n"
        
        self.wbStall            = "r_%s_%%s <= \"1\"; --    %s auto stall\n" % (slaveIfName, slaveIfName)
 
        
     
class wbsVhdlStrGeneral(object):
    wbWidth = {8   : '1',
               16  : '3',
               32  : '7', 
               64  : 'f'}  

    hex2slv = "std_logic_vector(to_unsigned(16#%x#, %s))"
    int2slv = "std_logic_vector(to_unsigned(%s, %s))"
    generic = "%s : %s := %s%%s --%s\n"
    clkport = "clk_%s_i : std_logic; -- Clock input for %s domain\n"
    clkportname = "clk_%s_i"
    rstport     = "rst_%s_n_i : std_logic; -- Reset input (active low) for %s domain\n"
    rstportname = "rst_%s_n_i"
    assignStub  = "%s => %s,\n"
    assignTemplate = "%s <= %s;\n"    

    def __init__(self, unitname, slaveIfName, dataWidth, vendId, devId, sdbname, clocks, version, now):
        self.unitname       = unitname
        self.slaveIfName    = slaveIfName        
        self.dataWidth      = dataWidth
        self.clocks         = clocks

        #################################################################################        
        #Strings galore
        
        self.skidpad0    = [il0("sp : wb_skidpad\n"),
                           il0("generic map(\n")]
                           
        self.skidpadAdr0 = il1("g_adrbits   => %u\n")
        self.skidpad1    = [
                           il0(")\n"),
                           il0("Port map(\n"),
                           il1("clk_i        => %s,\n" % (wbsVhdlStrGeneral.clkportname % clocks[0])),
                           il1("rst_n_i      => %s,\n" % (wbsVhdlStrGeneral.rstportname % clocks[0])),             
                           il1("push_i       => s_push,\n"),
                           il1("pop_i        => s_pop,\n"),
                           il1("full_o       => s_full,\n"),
                           il1("empty_o      => s_empty,\n")]
        self.skidpadAdr1 = il1("adr_i        => %s_i.adr(%%u downto %%u),\n" % slaveIfName)
        self.skidpad2    = [                   
                           il1("dat_i        => %s_i.dat,\n" % slaveIfName),
                           il1("sel_i        => %s_i.sel,\n" % slaveIfName),  
                           il1("we_i         => %s_i.we,\n" % slaveIfName),
                           il1("adr_o        => s_a,\n"),
                           il1("dat_o        => s_d,\n"),
                           il1("sel_o        => s_s,\n"),
                           il1("we_o         => s_w\n"),
                           il0(");\n\n")]
        
        
        self.validmux0  = ["validmux: with to_integer(unsigned(s_a_ext)) select\n",
                           "s_valid <= \n"]
        self.validmux1  = ["'1' when others;\n",
                           "\n"]
        
        self.flowctrl = [#only check valid if entity saw flag without stall
                         "s_valid_ok <= r_valid_check and s_valid;\n",
                         #prolong enable
                         "s_e_p  <= r_e or r_e_wait;\n",
                         "s_a_ext <= s_a & \"00\";\n",
                         "s_stall <= s_full;\n",
                         "s_push  <= slave_i.cyc and slave_i.stb and not s_stall;\n",
                         #-- op enable when skidpad not empty and not waiting for op completion
                         "s_e     <= not (s_empty or s_e_p);\n",
                         #pop if operation went out, entity saw flag without stall and replied valid    
                         "s_pop   <= s_valid_ok;\n",
                         "%s_o.stall    <= s_stall;\n" % slaveIfName,
                         "\n"]     

        
        self.slaveIf    = ["\n",
                           "%s_i : in  t_wishbone_slave_in;\n" % slaveIfName,
                           "%s_o : out t_wishbone_slave_out\n\n" % slaveIfName]
                           
                           
 
                          
        self.slaveSigs = ["signal s_%s_i : t_wishbone_slave_in;\n" % slaveIfName,
                          "signal s_%s_o : t_wishbone_slave_out;\n" % slaveIfName]
                          
        self.IntSigs  =   ["signal s_pop, s_push   : std_logic;\n",
                           "signal s_empty, s_full : std_logic;\n",
                           "signal r_e_wait, s_e_p : std_logic;\n",
                           "signal s_stall : std_logic;\n",               
                           "signal s_valid,\n",
                           "       s_valid_ok,\n",
                           "       r_valid_check : std_logic;\n",
                           "signal r_ack : std_logic;\n", 
                           "signal r_err : std_logic;\n",                             
                           "signal s_e, r_e, s_w : std_logic;\n",
                           "signal s_d : std_logic_vector(%s-1 downto 0);\n" % self.dataWidth,
                           "signal s_s : std_logic_vector(%u-1 downto 0);\n" % ((int(self.dataWidth))/8),
                          ]
        self.IntSigsAdr = "signal s_a : std_logic_vector(%u-1 downto 0);\n"                  
        self.IntSigsAdrExt0 = ["signal s_a_ext,\n",
                               "       r_a_ext0,\n",
                              ]     
        self.IntSigsAdrExt1 =  "       r_a_ext1 : std_logic_vector(%u-1 downto 0);\n"
        self.slaveInst = ["%s_i => %s_i,\n" % (slaveIfName, slaveIfName),
                          "%s_o => %s_o" % (slaveIfName, slaveIfName)]         
        
        self.wbs0       = [il0("%s : process(%s)\n" % (slaveIfName, (wbsVhdlStrGeneral.clkportname % clocks[0]) )),
                           il0("begin\n"),
                           il1("if rising_edge(%s) then\n" % (wbsVhdlStrGeneral.clkportname % clocks[0])),
                           il2("if(%s = '0') then\n" % (wbsVhdlStrGeneral.rstportname % clocks[0])),
                           il3("r_e           <= '0';\n"),
                           il3("r_e_wait      <= '0';\n"),
                           il3("r_valid_check <= '0';\n")] 
       
        self.wbs1_0     = ["else\n"]
                           
        self.wbs1_1     = ["r_e <= s_e;\n",
                           "r_a_ext0 <= s_a_ext;\n",
                           "r_a_ext1 <= r_a_ext0;\n", #  -- need extra cycle for valid check, register 1x more
                           #-- enable is prolonged until 'check valid' and valid are both high
                           "r_e_wait <= s_e_p and not s_valid_ok;\n",
                           #-- 'check valid' goes high if the entity saw a flag without stall and goes low if valid is high                           
                           "r_valid_check <= (r_valid_check or (s_e_p and not stall_i(0))) and not s_valid_ok;\n",
                           "r_ack    <= s_pop and not (error_i(0) or r_error(0));\n",
                           "r_err    <= s_pop and     (error_i(0) or r_error(0));\n",
                           "%s_o.ack <= r_ack;\n" % slaveIfName,
                           "%s_o.err <= r_err;\n" % slaveIfName,         
                           "\n",
                           ]    
        #only clear flags if not stalled
        self.wbs1_2     = ["\n",
                           "if stall_i = \"0\" then\n"] 
        self.wbs1_3     = ["end if;\n",
                           "\n"] 
        
        self.wbs2       = [il0("\n"), 
                           il0("if(s_e = '1') then\n"),
                           il1("if(s_w = '1') then\n"),
                           il2("-- WISHBONE WRITE ACTIONS\n"),
                           il2("case to_integer(unsigned(s_a_ext)) is\n")]
    
        self.wbs3       = [il2("end case;\n"),
                           il1("else\n"),
                           il2("-- WISHBONE READ ACTIONS\n"),
                           il2("case to_integer(unsigned(s_a_ext)) is\n")]  

        self.wbs4       = [il2("end case;\n"),
                           il1("end if; -- s_w\n"),
                           il0("end if; -- s_e\n"),
                           "\n"
                           ]
                           
        self.out0       = ["case to_integer(unsigned(r_a_ext1)) is\n"]
                         
        self.outOthers  = "when others => %s_o.dat <= (others => 'X');\n" % slaveIfName                 
                         
        self.out1       = ["end case;\n\n",
                           "\n"]
                           
        self.wbs5       = [il2("end if; -- rst\n"),
                           il1("end if; -- clk edge\n"),
                           il0("end process;\n\n")]
                           
                           
        
                           
        self.wbsPageSelect      = "r_p <= to_integer(unsigned(r_%s));\n\n"  #pageSelect Register
                          
        self.fsmOthers          = "when others => r_error <= \"1\";\n"                   

                             
        self.wbs_reg_o          = "signal r_%s : t_%s_regs_o;\n" % (slaveIfName, slaveIfName)
        self.wbs_reg_i          = "signal s_%s : t_%s_regs_i;\n" % (slaveIfName, slaveIfName)
        
        if sdbname is not None:                       
            self.sdb0               = ['constant c_%s_%s_sdb : t_sdb_device := (\n' % (unitname, slaveIfName),
                                       'abi_class     => x"%s", -- %s\n' % ("0000", "undocumented device"),
                                       'abi_ver_major => x"%s",\n' % "01",
                                       'abi_ver_minor => x"%s",\n' % "00",
                                       'wbd_endian    => c_sdb_endian_%s,\n' % "big",
                                       'wbd_width     => x"%s", -- 8/16/32-bit port granularity\n' % self.wbWidth[dataWidth],
                                       'sdb_component => (\n']
            self.sdbAddrFirst        = 'addr_first    => x"%s",\n'
            self.sdbAddrLast         = 'addr_last     => x"%s",\n'
            self.sdb1                = ['product => (\n',
                                       'vendor_id     => x"%016x",\n' % vendId,
                                       'device_id     => x"%08x",\n' % devId,
                                       'version       => x"%s",\n' % '{message:{fill}{align}{width}}'.format(message=version.replace('.', ''), fill='0', align='>', width=8),
                                       'date          => x"%04u%02u%02u",\n' % (now.year, now.month, now.day),
                                       'name          => "%s")));\n' % sdbname.ljust(19)]
            self.sdbReference       = "constant c_%s_%s_sdb : t_sdb_device := work.%s_pkg.c_%s_%s_sdb;\n" % (unitname, slaveIfName, (unitname + '_auto'), unitname, slaveIfName)                            
    
                                 
                                  

  
    codeGen = set(['vhdl', 'C', 'C++'])    

    genTypes = {'u'        : 'unsigned',
            'uint'     : 'natural', 
            'int'      : 'integer', 
            'bool'     : 'boolean',
            'string'   : 'string',
            'sl'       : 'std_logic',
            'slv'      : 'std_logic_vector'}    

class gVhdlStr(object):
   

    def __init__(self, unitname, filename="unknown", author="unknown", email="unknown", version="0.0", date=""):
        self.unitname   = unitname
        self.filename   = filename        
        self.author     = author
        self.version    = version
        self.date       = date
        self.dateStr    = "%02u/%02u/%04u" % (date.day, date.month, date.year)
        
        self.header     = ["--! @file        %s\n" % filename,                 
                           "--  DesignUnit   %s\n" % unitname,                           
                           "--! @author      %s <%s>\n" % (author, email),
                           "--! @date        %s\n" % self.dateStr,
                           "--! @version     %s\n" % version,                     
                           "--! @copyright   %04u GSI Helmholtz Centre for Heavy Ion Research GmbH\n" % (date.year),
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
                           "use work.wishbone_pkg.all;\n",
                           "use work.wbgenplus_pkg.all;\n",
                           "use work.genram_pkg.all;\n"]
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
        self.generic     = "g_%s : %s := %s%s -- %s\n" #name, type, default
        self.instGenPort    = "%s => %s%s\n" 
        self.instStart      = "INST_%s_auto : %s_auto\n" % (unitname, unitname)
        self.instGenStart   = "generic map (\n"
        self.instGenEnd     = ")\n"
        self.instPortStart  = "port map (\n"
        self.instPortEnd    = ");\n"
  
                   
                   
class sysIfStr(object):                   
    def __init__(self, program, creator, version="0.0", start="", update=""):               
                   
        self.helpText = ["\nUsage: python %s <path-to-wishbone-descriptor.xml>\n" % program, 
                        "-h    --help       Show detailed help. Lots of text, best redirect output to txt file",
                        "-q    --quiet      No console output",
                        "      --version    Shows version information",
                        "-l    --log        Log build output\n"
                        ]
    
             
        self.detailedHelpText = ['%s' % ("*" * 80),
                        '**                                                                            **',                    
                        '**                          wbgenplus Manual V%s                             **' % version,                    
                        ('**' + '%s%s%s' + '**') % ((" " * ((76-len(creator))/2)), creator, (" " * ((76-len(creator))/2 + (76-len(creator))%2))),
                        '%s\n' % ("*" * 80),
                        'wbgenplus autogenerates wishbone devices for FPGAs in VHDL from a single XML file.',
                        'In VHDL, it builds the core logic, a package for register records and SDB entries',
                        'and provides a stub for the outer entity.',
                        'It also creates a C Header file with the address definitions and builds',
                        'documentation via doxygen (not yet implemented).\n',
                        'In order to keep things modular, wbgenplus creates a seperate core for the',
                        'wishbone interface to be instantiated for your design.\n',
                        'wbgenplus currently supports the following features:\n',
                        '- completely modular wishbone interface core',                  
                        '- auto-generated SDB records',
                        '- automatic clock crossing',
                        '- optional autogeneration of get/set/clear adresses for registers (atomic bit manipulation)',                        
                        '- auto-splitting of registers wider than the bus data width',                    
                        '- option for multiple memory pages of registers, dependent on a selector register,',
                        '  quantity can be controlled via generic',
                        '- optional complete flow control by the outer (user generated) entity',
                        '- auto feedback for successful or failed operations(accessing unmapped addresses or',
                        '  writing to read only / reading from write only registers)',
                        '- optional generation of read/write enable (WR/RD) flag output for a register',
                        '- ...',
                        '\n',
                        'Planned features / currently under development:\n',
                        '- clock crossing of paged registers',
                        '\n',
                        '+%s+' % ("-" * 78),
                         '|                            Wishbone-Descriptor-XMLs                          |',
                        '+%s+\n' % ("-" * 78),                    
                        
                        'This sections covers the details of the XML syntax.\n',
                        'Supported tags:\n',
                        '<wbdevice             Supreme Tag introducing a new wishbone device with one ore more interfaces.',
                        '   <codegen>          Selects which outputs files should be built',
                        '   <generic>          Introduces a generic. These can used as resetvector, a bitwidth or the number of memory pages',
                        '   <clockdomain>      Introduces a clockdomain. If no such tag is present, wbgenplus will automatically',
                        '                      generate the "sys" domain for the wb interface',                                       
                        '   <slaveinterface    Introduces a new Wishbone Slave interface to the device',
                        '       <sdb>          Parameters for Self Describing Bus (SDB) record of this slave interface',
                        '       <reg>          Introduces a new register to this slave interface interface',        
                        '   >',
                        '>',
                        
                        'Detailed Tag parameter descriptions. All parameters marked with an * are mandatory,',
                        'the rest is optional and does need to appear in the XML.',
                        'Tag parameters:\n',
                        '<GENERIC>:\n',
                        '  *name:       Name of the generic',
                        '  *type:       The data type of the generic. Only \'natural\' is supported now',
                        '  *default:    A default value for this generic',
                        '  *comment:    A (hopefully) descriptive comment for this generic',                        
                        '<CLOCKDOMAIN>:\n',
                        '  *name:       Name of the clock domain. The first such tag is always treated as the Wishbone domain\n',
                        '   Example:',                      
                        '   <clockdomain name="wb"></clockdomain>\n',
                        '<WBDEVICE>:\n',                  
                        '  *unitname:   Name of the design unit of the wishbone top file.',
                        '               The inner core will be named "<unitname>_auto"',
                        '  *author:     Name of the author of this xml and all derived files',
                        '   email:      The email address of the author',
                        '   version:    version number of this device\n',
                        '   Example:',                      
                        '   <wbdevice unitname="my_cool_device" author="M. Kreider" email="m.kreider@gsi.de" version="0.0.1">\n',
                        '<SLAVEINTERFACE>:\n',                   
                        '  *name:       Name of the slave interface port',
                        '   data:       Bitwidth of the data lines. Default is 32',
                        '   type:       Type of flow control. Accepts "pipelined" or "classic", default is "pipelined"',
                        '  pages:       Number <n> of memory pages to instantiate, default is 0.',
                        '               Accepts a generic (via const package, see above)',
                        '               All registers marked paged="yes" will be built as an array with n elements.',
                        '               If <n> is greater 0, one register must be marked as the page selector by issueing selector="yes"\n',
                        '   Example:',                      
                        '   <slaveinterface name="control" data="32" type="pipelined" pages="8">\n',
                        '<SDB>:\n',
                        '  *vendorID:   Vendor Identification code, 64 bit hex value. Also accepts known vendors like "GSI" or "CERN"',
                        '  *productID:  Product Identification code, 32 bit hex value',
                        '  *version:    Device version number, 1 to 3 digits',
                        '   date:       Date to be shown on sdb record. Default is "auto" (Today)',
                        '  *name:       Name to be shown on sdb record. 19 Characters max.\n', 
                        '   Example:',  
                        '   <sdb vendorID="GSI" productID="0x01234567" version="1" date="auto" name="my_ctrl_thingy"></sdb>\n',
                  
                        '<REG>:\n',
                        '  *name:       Main name of the register. Actual address and record names might be extended by suffices',
                        '  *read:       Indicates if this register is readable from Wishbone. Default is "no"',
                        '  *write:      Indicates if this register is driven from Wishbone. Default is "no"',
                        '  *drive:      Indicates if this register is driven from the outer entity. Default is "no"',
                        '  *comment:    A (hopefully) descriptive comment for this register',                        
                        '   access:     Access mode for this register, "simple" or "atomic", default is "simple"',
                        '               Simple mode allows direct overwriting of register content.',
                        '               Atomic mode provides seperate get, set, and clear addresses for this register,',
                        '               allowing atomic single bit manipulation',
                        '   mask:       Binary or hexadecimal Bitmask for this register, must not have gaps. Default is the',
                        '               data(bus width) parameter of the slave interface tag',
                        '               If "mask" is wider than "data", wbgenplus will automatically generate multiple addresses',
                        '               to allow word access of the register.',
                        '   bits:       Bitwidth for this register, default is the',
                        '               data(bus width) parameter of the slave interface tag',
                        '               If "bits" is wider than "data", wbgenplus will automatically generate multiple addresses',
                        '               to allow word access of the register.',
                        '   address:    Manually sets the offset for this register, default is auto addressing.',
                        '               All follwing Registers will be enumerated from this address onward',
                        '   reset:      Defines the reset value for this register. Accepts "ones", "zeroes", binary, hex or decimal value.',
                        '               Currently only works for registers that can be written to from WB. Default is "zeroes".',                      
                        '   flags       Write/Read enable flag, default is "no". If set to "yes", two additional flag registers will be created,',
                        '               going HI for 1 clock cycle every time the parent register is written to/read from.',
                        '               The flag register does not discriminate which page, word, or subword is accessed.',
                        '   autostall:  If set to "yes", raises the stall line for 1 cycle after each access. Default is "no"',
                        '               The outer entity can, only raise a stall request 2 cycles AFTER the bus operation.',
                        '               Autostall bridges this gap by keeping the bus stalled until the outer entity can do flow control',
                        '   pulse:      If set to "yes", the register will reset to all 0 after 1 cycle. Default is "no"', 
                        '   paged:      When set to "yes", this register will be instantiated as an array with the number of elements',
                        '               in the pages parameter of the slave interface tag',
                        '   selector:   Selects the active memory page of all paged registers. Value is auto range checked on access.',
                        '   clock:      Clock domain this register shall be synchronized to. Default is no sync (WB clock domain)',
                        '               Needs a corresponding <clockdomain> tag.\n',
                        '   Example:',                    
                        '   <reg name="ACT" read="yes" write="yes" access="atomic" mask="0xff" comment="Triggers on/off"></reg>\n',
                        '\n',
                        ]
    
        self.versionText = ["\nwbgenplus - A Wishbone Slave Generator\n",
                   "Version: %s" % version,
                   "Created %s by %s" % (start, creator),
                   "Last updated %s\n" % update                 
                   ]                   
                   