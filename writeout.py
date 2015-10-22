# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 17:09:35 2015

@author: mkreider
"""
import textformatting
import os.path
from stringtemplates import gVhdlStr

is_seq      = textformatting.is_sequence
i1          = textformatting.setColIndent
iN          = textformatting.setColsIndent    
adj         = textformatting.beautify
mskWidth    = textformatting.mskWidth
str2int     = textformatting.parseNumeral
commentLine = textformatting.commentLine
commentBox  = textformatting.commentBox

def mergeIfLists(slaveList=[], masterList = []):
    uglyPortList = []
    uglyTypeList = []
    instList = []
    stubInstList = []
    syncList     = []    
    docList      = []    
    
    clocks = slaveList[0].clocks    
    for clock in clocks:
        uglyPortList += ["clk_%s_i   : in  std_logic;\n" % clock]   
    uglyPortList    += ["rst_n_i   : in  std_logic;\n\n"]
    stubPortList    = [] + uglyPortList
    stubSigList     = []                   
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
        
        uglyPortList += slave.getRegisterPortList()
        stubPortList += slave.getRegisterPortList()
        #deal with vhdl not wanting a semicolon at the last port entry        
        if(slave != slaveList[-1]):
            uglyPortList[-1] += ";\n"
            stubPortList[-1] += ";\n"
            stubInstList[-1] += ",\n"
        else:
            uglyPortList[-1] += "\n"
            stubPortList[-1] += "\n"
        uglyPortList += ["\n"]    
        #cAdrList     += slave.c.sdbVendorID
        #cAdrList     += slave.c.sdbDeviceID
        #cAdrList     += '\n'
        #cAdrList     += commentLine("//","Address Map", slave.name)        
        #cAdrList     += slave.cAdrList
        #cAdrList     += "\n"
        #uglyTypeList += slave.getRegisterTypeList()
         
        uglyAdrList  += iN(commentLine("--","WBS Adr", slave.name), 1) 
        uglyAdrList  += slave.getAddressListVHDL()
        
        uglyAdrList  += ["\n"]
        uglyRegList  += iN(commentLine("--","WBS Regs", slave.name),1)
        uglyRegList  += adj(slave.getRegisterDefinitionList(), [' is ', ':', ':=', '--'], 1)
        uglyRegList  += ["\n"]
        
        instList     += adj(slave.getInstanceList(), ['=>', '<='], 1) 
        fsmList      += iN(commentBox("--","WBS FSM", slave.name), 1)
        fsmList      += slave.getFsmList()
        docList      += slave.getDocList("VHDL") 
        #fsmList      += "\n\n"
        #syncList     += iN(commentBox("--","Sync Signal Assignments", slave.name), 1)
        #syncList     += adj(slave.syncAssignList, ['<='], 1)
        #if(len(slave.syncProcList)>0):        
        #    syncList     += iN(commentBox("--","Sync Processes", slave.name), 1)        
        #    syncList     += adj(slave.syncProcList, ['<='], 1) 
        #    syncList     += "\n\n"
           
        #stubSigList  += slave.stubSigList
        #sdbList      += slave.v.sdb + ['\n']
        #sdbRefList   += [slave.v.sdbReference]
    
   # for master in masterList:
   #     uglyPortList += master.portList
   #     uglyAdrList  += master.AdrList       
   #     uglyRegList  += master.regList    
    
    portList        = adj(uglyPortList, [':', ':=', '--'], 1)
       
    typeList        = [] #adj(uglyTypeList, [' is ', ':', ':=', '--'], 1)    
    stubPortList    = adj(stubPortList, [':', ':=', '--'], 1) 
    stubSigList     = adj(stubSigList,  [':', ':=', '--'], 1)      
    docList         = adj(docList,  [' : ', ' -> '], 0)   
    #exit(1)
    regList     = iN(commentBox("--","", "WB Registers"), 1) + ['\n']\
                + uglyRegList
                
                
    vAdrList     = iN(commentBox("--","", "WB Slaves - Adress Maps"), 1) + ['\n']\
                + adj(uglyAdrList, [':', ':=', '--'], 1)
                
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
        genList.append(v.generic % (genName, genType, genVal, lineEnd, genDesc))
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
    return [portList, typeList, regList, sdbList, sdbRefList, vAdrList, fsmList, instList, genList, cAdrList, stubPortList, stubInstList, stubSigList, instGenList, docList]        



class writeout(object):
    def __init__(self, unitname, filename, mypath, author, email, version, date):   
        self.unitname = unitname
        self.filename = filename
        self.mypath = mypath
        self.author = author
        self.email = email
        self.version = version
        self.date = date
        self.autoUnitName = unitname + "_auto"
        
        
        

    def writeStubVhd(self):
        fileStubVhd     = self.unitname                  + ".vhd"
        
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

    def writeMainVhd(self, slave):
    
        #filenames for various output files
        filename     = self.autoUnitName              + ".vhd"
    
        print "Generating WishBone core entity  %s" % filename 
        
        fo = open(self.mypath + filename, "w")
        v = gVhdlStr(self.autoUnitName, filename, self.author, self.email, self.version, self.date)
    
        header = adj(v.header + ['\n'], [':'], 0)
        for line in header:
            fo.write(line)
        fo.write("--! @brief AUTOGENERATED WISHBONE-SLAVE CORE FOR %s.vhd\n" % self.unitname)
        fo.write("--!\n")        
            
        for line in v.headerLPGL:
            fo.write(line)
        warning = [] + v.headerWarning
        warning.append(v.headerModify % (self.unitname, self.unitname))
        for line in warning:
            fo.write(line)
        
        #for line in docList:
        #    fo.write(line)   
            
        libraries = v.libraries + [v.pkg % '']
        for line in libraries:
            fo.write(line)
            
        fo.write(v.entityStart)
        if len(slave.getGenericList()):
            fo.write(v.genStart)
            for line in slave.getGenericList():   
                fo.write(line)
            fo.write(v.genEnd)
        
        fo.write(v.entityMid)
        
        for line in slave.getPortList():
            fo.write(line)
            
        fo.write(v.entityEnd)
        
        fo.write(v.archDecl)
        
    
        for line in slave.getDeclarationList():
            fo.write(line)
        
        fo.write(v.archStart)
    
        for line in slave.getAssignmentList():
            fo.write(line)    
        
        for line in slave.getFsmList():
            fo.write(line)
        
        fo.write(v.archEnd)
        
        fo.close
        
        

    def writePkgVhd(self, slave):
    
    
        filename      = self.autoUnitName  + "_pkg"    + ".vhd"

        print "Generating WishBone inner core package %s" % filename    
        
        fo = open(self.mypath + '/' + filename, "w")
        
        v = gVhdlStr(self.autoUnitName, filename, self.author, self.email, self.version, self.date)
    
        header = adj(v.header + ['\n'], [':'], 0)
        for line in header:
            fo.write(line)
        fo.write("--! @brief AUTOGENERATED WISHBONE-SLAVE PACKAGE FOR %s.vhd\n" % self.unitname)
        fo.write("--!\n")     
        for line in v.headerLPGL:
            fo.write(line)
        warning = [] + v.headerWarning
        warning.append(v.headerModify % (self.unitname, self.unitname))    
        for line in warning:
            fo.write(line)
        libraries = v.libraries
        for line in libraries:
            fo.write(line)    
        
        fo.write(v.packageStart)
        
        for line in slave.getAddressListVHDL():
            fo.write(line)    
        
        decl = []
       
        decl += (iN(commentLine("--", "Component", self.autoUnitName), 1)) 
        
        for line in decl:
            fo.write(line)    
        
        decl = []
        decl.append(v.componentStart)
        if len(slave.getGenericList()):
            fo.write(v.genStart)
            for line in slave.getGenericList():   
                fo.write(line)
            fo.write(v.genEnd)
        decl.append(v.entityMid)
        for line in slave.getPortList():
            fo.write(line)
        decl += v.componentEnd
        
        for line in slave.getStrSDB():
            decl.append(line)
       
        decl = iN(decl, 1)
        for line in decl:
            fo.write(line)
        
            
        
        fo.write(v.packageEnd)
        fo.write(v.packageBodyStart)
        fo.write(v.packageEnd)
        
        fo.close

    def writeStubPkgVhd(self):

    
        
        filename  = self.unitname      + "_pkg"    + ".vhd"  
    
        if os.path.isfile(self.mypath + filename):
            print "!!! Outer package stub %s already exists !!!\n" % filename
            if not force:
                return
            else:
                print "Overwrite forced"
                
        print "Generating stub outer package %s" % filename    
        
        fo = open(self.mypath + '/' + filename, "w")
        
        v = gVhdlStr(self.unitname, filename, self.author, self.email, self.version, self.date)
    
        header = adj(v.header + ['\n'], [':'], 0)
        for line in header:
            fo.write(line)
        fo.write("--TODO: This is a stub, finish/update it yourself\n")    
        fo.write("--! @brief Package for %s.vhd\n" % self.unitname)
        fo.write("--! If you modify the outer entity, don't forget to update this component! \n")
        fo.write("--!\n")     
        for line in v.headerLPGL:
            fo.write(line)
        
        libraries = v.libraries
        for line in libraries:
            fo.write(line)    
        
        fo.write(v.packageStart)
           
        decl = []
        decl += (iN(commentLine("--", "Component", self.unitname), 1)) 
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
        
        
        decl = iN(decl, 1)
        for line in decl:
            fo.write(line)
        
            
        
        fo.write(v.packageEnd)
        fo.write(v.packageBodyStart)
        fo.write(v.packageEnd)
        
        fo.close


    def writeHdrC(filename):
 
        
        filename        = self.unitname      + "_regs"   + ".h"      
    
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
    
    
       
    
        fileTbVhd       = self.unitname      + "_tb"     + ".vhd"