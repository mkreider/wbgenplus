# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 17:09:35 2015

@author: mkreider
"""
import textformatting
import os.path
from stringtemplates import gVhdlStr
from stringtemplates import gCStr

is_seq      = textformatting.is_sequence
i1          = textformatting.setColIndent
iN          = textformatting.setColsIndent    
adj         = textformatting.beautify
mskWidth    = textformatting.mskWidth
str2int     = textformatting.parseNumeral
commentLine = textformatting.commentLine
commentBox  = textformatting.commentBox



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
        
        
        

    def writeStubVhd(self, slave, force=False):
        filename        = self.unitname                  + ".vhd"       
        
        if os.path.isfile(self.mypath + filename):
            print("!!! Outer entity %s already exists !!!\n" % filename)
            if not force:
                print("I don't want to accidentally trash your work. To force overwrite, use '-f' or '--force' option")
                return
            else:
                print("Overwrite forced")
                
        print("Generating stub entity           %s" % filename)        
        fo = open(self.mypath + filename, "w")
        v = gVhdlStr(self.unitname, self.filename, self.author, self.email, self.version, self.date)
    
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
        for line in slave.getStubSignalList():
            fo.write(line)
        
        fo.write(v.archStart)
        
    
        a = []
        a.append(v.instStart)        
        
        #if(len(genIntD) + len(genMiscD) > 0):
        #   a.append(v.instGenStart)
        #   a += instGenList
        #   a.append(v.instGenEnd)    
        a.append(v.instPortStart)
        a += slave.getStubInstanceList()
        a.append(v.instPortEnd)
        a = iN(a, 1) 
        for line in a:
            fo.write(line)
            
        fo.write(v.archEnd)
        
        fo.close

    def writeMainVhd(self, slave):
    
        #filenames for various output files
        filename     = self.autoUnitName              + ".vhd"
    
        print("Generating WishBone core entity  %s" % filename) 
        
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
    
        for line in slave.getSkidPad():
            fo.write(line)    
    
        for line in slave.getValidMux():
            fo.write(line)
            
  
        
        for line in slave.getFlowControl():
            fo.write(line)            
        
        for line in slave.getAssignmentList():
            fo.write(line)    
        
        for line in slave.getFsmList():
            fo.write(line)
        
        fo.write(v.archEnd)
        
        fo.close
        
    def writePythonDict(self, slave):
    
        #filenames for various output files
        filename     = self.autoUnitName              + ".py"
    
        print("Generating Pyhton WB address dictionary for use in testbenches  %s" % filename) 
        
        fo = open(self.mypath + filename, "w")
        
        s = []
        tmp = []        
        
        s.append("class %s (object):\n" % self.unitname)
        tmp.append("ifname = '%s'\n\n" % slave.name)    
        tmp.append("adrDict = {\n")
        tmp += slave.getAddressListPython()
        tmp.append("}\n\n")
        tmp.append("adrDict_reverse = {\n")
        tmp += slave.getAddressListPythonReverse()
        tmp.append("}\n\n")            
        tmp.append("flagDict = {\n")
        tmp += slave.getFlagListPython()
        tmp.append("}\n\n")
        tmp.append("valDict = {\n")
        tmp += slave.getValueListPython()
        tmp.append("}\n")             
        tmp = iN(tmp, 1)
        s += tmp
        
        
        
        for line in s:
            fo.write(line)
        
        fo.close        

    def writePkgVhd(self, slave):
    
    
        filename      = self.autoUnitName  + "_pkg"    + ".vhd"

        print("Generating WishBone inner core package %s" % filename)    
        
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
        decl.append("\n")
        decl += (iN(commentLine("--", "Component", self.autoUnitName), 1)) 
        
        for line in decl:
            fo.write(line)    
        
        decl = []
        decl.append(v.componentStart)
        if len(slave.getGenericList()):
            decl.append(v.genStart)
            for line in slave.getGenericList():   
                decl.append(line)
            decl.append(v.genEnd)
        decl.append(v.entityMid)
        for line in slave.getPortList():
            decl.append(line)
        decl += v.componentEnd
        
        for line in slave.getStrSDB():
            decl.append(line)
       
        decl = iN(decl, 1)
        decl.append("\n")
        for line in decl:
            fo.write(line)
        
            
        
        fo.write(v.packageEnd)
        fo.write(v.packageBodyStart)
        fo.write(v.packageEnd)
        
        fo.close

    


    def writeHdrC(self, slave):
 
        
        filename        = self.unitname      + "_regs"   + ".h"      
    
        print("Generating C Header file         %s\n" % filename)    
        
        fo = open(self.mypath + filename, "w")
        
        gc     = gCStr(filename, self.unitname, self.author, self.email, self.version, self.date, slave.sdbVendorID, slave.sdbDeviceID)
        for line in gc.header:
            fo.write(line)        
        
        for line in gc.hdrfileStart:
            fo.write(line)

        tmp = []
        tmp.append(str(gc.sdbVendorId))
        tmp.append(str(gc.sdbDeviceId))            
        tmp = iN(tmp, 1)
        
        for line in tmp:
            fo.write(line)
        
       
        for line in slave.getAddressListC():
            fo.write(line % self.unitname.upper())    
        fo.write(gc.hdrfileEnd)
        
        fo.close
    
    
       