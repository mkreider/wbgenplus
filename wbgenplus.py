# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/home/mkreider/.spyder2/.temp.py
"""
from xml.dom import minidom
from xml.parsers.expat import ExpatError
import datetime
from textformatting import parseNumeral as str2int
from textformatting import mskWidth as mskWidth 
import os.path
import sys
import getopt
from stringtemplates import sysIfStr as sysStr
from stringtemplates import wbsVhdlStrGeneral
from writeout import writeout
from wbslave import wbslave as wbs
from errors import WbgenError, fail

myVersion = "0.7"
myStart   = "10 Sep 2015"
myUpdate  = "25 Oct 2015"
myCreator = "M. Kreider <m.kreider@gsi.de>"

def parseXMLNew(xmlIn, now, unitname):
    xmldoc      = minidom.parse(xmlIn)   

    #defaults
    dictVendId  = {'GSI'       : 0x0000000000000651,
                   'CERN'      : 0x000000000000ce42}    
    
    author      = "unknown_author"
    email       = "unknown_mail"
    version     = "unknown_version"
        
    ifList      = []
    clockList   = []
    genIntD     = dict()
    genMiscD    = dict()
    
    if (len(xmldoc.getElementsByTagName('wbdevice'))==0):
        fail("No <wbdevice> tag found")
        
    author   = xmldoc.getElementsByTagName('wbdevice')[0].getAttribute('author')
    version  = xmldoc.getElementsByTagName('wbdevice')[0].getAttribute('version')
    email    = xmldoc.getElementsByTagName('wbdevice')[0].getAttribute('email')

       
    clocks = xmldoc.getElementsByTagName('clockdomain')
    if(len(clocks) > 0):    
        for clock in clocks:
            if(clock.hasAttribute("name")):
                clockList += [clock.getAttribute("name")]
            else:
                fail("<clockdomain> must have a name")
    else:
        clockList += ["sys"]        
            
    
    generics = xmldoc.getElementsByTagName('generic')
   
    print("Found %u generics\n" % len(generics))   
    for generic in generics:
        genName = generic.getAttribute('name')
        if not genName:
            fail("<generic> must have a name")
        if genName in genIntD or genName in genMiscD:
            fail("Generic <%s> is declared twice" % genName)
        genType = generic.getAttribute('type')
        genVal  = generic.getAttribute('default')
        genDesc = generic.getAttribute('comment')
        #if genTypes.has_key(genType):
        #    genType = genTypes[genType]               
        if(genType == 'natural'):
            aux = str2int(genVal)
            if(aux == None):            
                fail("Generic <%s>'s default <%s> is not a valid natural" % (genName, genVal))
            else:        
                genVal = aux
                genIntD[genName] = [ genType , genVal, genDesc ]
        else:
            genMiscD[genName] = [ genType , genVal, genDesc ]    
            #else:
            #    print "%s is not a valid type" % generic.getAttribute('type')
            #    sys.exit(2)
 
        
    slaveIfList = xmldoc.getElementsByTagName('slaveinterface')
    print("Found %u slave interfaces\n" % len(slaveIfList))    
    # All output file names derive from the XML name, so a second slave would
    # overwrite the first one's files (finding 1.8). No known XML has more than one.
    if len(slaveIfList) != 1:
        fail("Exactly one <slaveinterface> is supported, found %u" % len(slaveIfList))
    for slaveIf in slaveIfList:
        
        name    = slaveIf.getAttribute('name')
        if not name:
            fail("<slaveinterface> must have a name")
        data    = slaveIf.getAttribute('data')
        ifWidth = 32 if data == '' else str2int(data)
        if ifWidth is None or ifWidth <= 0 or ifWidth % 8:
            fail("Slave <%s>: data <%s> must be a positive multiple of 8" % (name, data))
        print("Slave <%s>: %u Bit wordsize" % (name, ifWidth))
        pages  = slaveIf.getAttribute('pages')
        #check integer generic list
        genericPages = (pages in genIntD)
        if pages == '':
            pages = 0
        elif(not genericPages):        
            aux = str2int(pages)
            if aux is None or aux < 0:
                fail("Slave <%s>: pages <%s> is neither a natural number nor a declared generic" % (name, pages))
            pages = aux
        else:
            print("Slave <%s>: Using supplied generic <%s> for memory pages " % (name, pages))
            
        #sdb record
        vendId = None
        prodId = None
        sdbname = None       
        
        sdb = slaveIf.getElementsByTagName('sdb')
        if len(sdb) == 1:
            print("Slave <%s>: Generating SDB record" % (name))              
            vendId      = sdb[0].getAttribute('vendorID')
            prodId      = sdb[0].getAttribute('productID')
            #check vendors
            if vendId in dictVendId:
                print("Slave <%s>: Known Vendor ID <%s> found" % (name, vendId))            
                vendId = dictVendId[vendId]
                 
            else:
                aux = str2int(vendId)
                if(aux == None):            
                    fail("Slave <%s>: Invalid Vendor ID <%s>" % (name, vendId))
                else:
                    vendId = aux                
                    print("Slave <%s>: Unknown Vendor ID <%016x>" % (name, vendId))                
                    
            
            aux = str2int(prodId)
            if(aux == None):            
                fail("Slave <%s>: Invalid Product ID <%s>" % (name, prodId))
            else:
                prodId = aux     
                    
            sdbname     = sdb[0].getAttribute('name')
            if(len(sdbname) > 19):
                fail("Slave <%s>: Sdb name <%s> is too long. It has %u chars, allowed are 19" % (name, sdbname, len(sdbname)))
        
        tmpSlave    = wbs(unitname, version, now, name, 0, '', pages, ifWidth, vendId, prodId, sdbname, clockList, genIntD, genMiscD, 'g_') 

        # word order of registers wider than the bus: must be explicit, see checks after the register loop
        wordorder = None
        if slaveIf.hasAttribute('wordorder'):
            wordorder = slaveIf.getAttribute('wordorder')
            if wordorder not in ('high', 'low'):
                fail("Slave <%s>: wordorder <%s> is invalid. Choose <high> (high word at the lowest address) or <low>" % (name, wordorder))
        tmpSlave.wordorder = wordorder
        
        selector = ""
        #name, adr, pages, selector
        #registers
        registerList = slaveIf.getElementsByTagName('reg')
        regnames = set()
        for reg in registerList:
            if reg.hasAttribute('name'):            
                regname = reg.getAttribute('name')
            else:
                fail("Slave <%s>: register must have a name" % name)
            if regname == name:
                fail("Slave <%s>: register <%s> has the same name as its slave interface; the generated ports would collide" % (name, regname))
            if regname in regnames:
                fail("Slave <%s>: register <%s> is declared twice" % (name, regname))
            regnames.add(regname)
            
            if reg.hasAttribute('comment'):      
                regdesc = reg.getAttribute('comment')
            else:        
                fail("Slave <%s>: register <%s> must have a comment" % (name, regname))
            
            regadr = None       
            if reg.hasAttribute('address'):            
                regadr = reg.getAttribute('address')            
                aux = str2int(regadr)
                if aux is None or aux < 0:
                    fail("Slave <%s>: Register <%s>'s address <%s> is invalid" % (name, regname, regadr))
                regadr = aux            
                print("Slave <%s>: Register <%s> using supplied address <0x%x>, enumerating from there" % (name, regname, regadr))
                
            regflags    = str()
            if reg.hasAttribute('read'):
                if reg.getAttribute('read') == 'yes':            
                    regflags += 'r'    
            if reg.hasAttribute('write'):        
                if reg.getAttribute('write') == 'yes':
                    regflags += 'w'
            if reg.hasAttribute('drive'):        
                if reg.getAttribute('drive') == 'yes':
                    regflags += 'd'        
            if reg.hasAttribute('paged'):
                if reg.getAttribute('paged') == 'yes':
                    regflags += 'm'
            if reg.hasAttribute('access'):
                if reg.getAttribute('access') == 'atomic':
                    regflags += 'a'
            if reg.hasAttribute('flags'):
                if reg.getAttribute('flags') == 'yes':            
                    regflags += 'f'
            if reg.hasAttribute('autostall'):
                if reg.getAttribute('autostall') == 'yes':            
                    regflags += 's'
            if reg.hasAttribute('pulse'):
                if reg.getAttribute('pulse') == 'yes':            
                    regflags += 'p'        
            if reg.hasAttribute('selector'):            
                if reg.getAttribute('selector') == 'yes':            
                    if(selector == ""):            
                        selector = regname
            regclk = clockList[0]                
            if reg.hasAttribute('clock'):
                regclk = reg.getAttribute('clock')
                print("Slave <%s>: Register <%s> is in clockdomain %s and will be synced" % (name, regname, regclk))
            
            if reg.hasAttribute('bits'):      
                regbits    = reg.getAttribute('bits')
                genericBits = (regbits in genIntD)
                if(not genericBits):
                    aux = str2int(regbits)
                    if aux is None or aux <= 0:
                        fail("Slave <%s>: Register <%s>'s bits <%s> is neither a positive number nor a declared generic" % (name, regname, regbits))
                    regbits = aux
                else:
                     print("Slave <%s>: Register <%s>'s using supplied generic width <%s>" % (name, regname, regbits))
         
            elif reg.hasAttribute('mask'):      
                regmsk  = reg.getAttribute('mask')
                aux     = str2int(regmsk)
                if aux is None or aux <= 0 or (aux & (aux + 1)) != 0:
                    fail("Slave <%s>: Register <%s>'s mask <%s> must be a contiguous bitmask starting at bit 0 (2^n-1, e.g. 0xff)" % (name, regname, regmsk))
                regbits = aux.bit_length()
            else:        
                print("Slave <%s>: No bitwidth or bitmask for Register <%s> supplied, defaulting to 0x%x" % (name, regname, ifWidth))
                regbits = ifWidth

            rstvec = None    
            if reg.hasAttribute('reset'):
                          
                    
                aux = reg.getAttribute('reset')

                if(aux in genIntD):
                    (_, val, _) = genIntD[aux]
                    print("Slave <%s>: Register <%s>'s Reset using supplied generic value <%s>" % (name, regname, val))
                    rstvec = aux
                #elif(aux in genMiscD):
                elif aux == 'zeroes':
                    rstvec = 0
                elif aux == 'ones':
                    rstvec = 'ones'
                else:    
                    tmp = str2int(aux)
                    if(tmp != None):
                        if aux.find("0x") > -1 or aux.find("0b") > -1:
                            rstvec = aux
                        else:
                            rstvec = tmp
                        print("Slave <%s>: Register <%s>'s Reset using supplied value <%s>" % (name, regname, aux))
                    
                    else:
                        fail("Slave <%s>: Register <%s>'s reset <%s> is invalid. Use a number, a declared generic, \"ones\" or \"zeroes\"" % (name, regname, aux))
                      
                      
            tmpSlave.addWbReg(regname, regdesc, regbits, regflags, regclk, rstvec, regadr)
      
            #x.addSimpleReg('NEXT2',     0xfff,  'rm',   "WTF")
            if(isinstance(pages, int)):
                if((selector != '') and (pages > 0)):    
                    print("Slave <%s>: Register <%s> has <%s> memory pages. Selector register is <%s>" % (name, regname, pages, selector))    
                    tmpSlave.selector = selector    
                    tmpSlave.pages      = pages
            elif(selector != ''):
                    print("Slave <%s>: Register <%s> has <%s> memory pages. Selector register is <%s>" % (name, regname, pages, selector))                   
                    tmpSlave.selector = selector    
                    tmpSlave.pages      = pages    
       
        multi = tmpSlave.getMultiWordRegNames()
        if multi and wordorder is None:
            fail("Slave <%s>: register(s) <%s> are wider than the %u bit bus. Add wordorder=\"high\" or wordorder=\"low\" to <slaveinterface>" % (name, ", ".join(multi), ifWidth))

        ifList.append(tmpSlave)
    return [author, version, email, ifList]


#TODO: A lot ...

        
#masterIfList = xmldoc.getElementsByTagName('masterinterface')
#for masterIf in masterIfList:
#    if masterIf.getAttribute('name'):
#        print "Generating WBMF %s" % masterIf.getAttribute('name')
#        entityPortList.append(VhdlStr.masterIf % (masterIf.getAttribute('name'), masterIf.getAttribute('name'))) 
    

        
def main():

    s = sysStr(sys.argv[0], myCreator, myVersion, myStart, myUpdate)             
             
    def usage():
        for line in s.helpText:        
            print(line)
    
    def manual():
        for line in s.detailedHelpText:        
            print(line)            
    
    def version():
        for line in s.versionText:        
            print(line) 
                    
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
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err)) # will print something like "option -a not recognized"
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
            print("unhandled option %s" % option)
            sys.exit(2) 
    
    
    if(needFile):
        if(optFound and len(sys.argv) == 2):
            usage()
            sys.exit(0)
            
        if os.path.isfile(xmlIn):
            mypath, myfile = os.path.split(xmlIn)        
            if not mypath:
                mypath += './'
                
            # Reproducible builds: honour SOURCE_DATE_EPOCH (https://reproducible-builds.org/specs/source-date-epoch/)
            sde = os.environ.get('SOURCE_DATE_EPOCH')
            if sde:
                now = datetime.datetime.fromtimestamp(int(sde), datetime.timezone.utc)
            else:
                now = datetime.datetime.now()
            print("f: %s p: %s" % (myfile, mypath))
            
            unitname = os.path.splitext(myfile)[0]        
            #path    = os.path.dirname(os.path.abspath(xmlIn)) + "/"
            
            print("input/output dir: %s" % mypath)
            print("Trying to parse:  %s" % myfile)
            print("Unit:             %s" % unitname)
            print("\n%s" % ('*' * 80))
                        
            try:
                [author, version, email, slaves] = parseXMLNew(xmlIn, now, unitname)
                wo = writeout(unitname, myfile, mypath, author, email, version, now)

                for slave in slaves:
                    wo.writeMainVhd(slave)
                    wo.writePkgVhd(slave)
                    wo.writeStubVhd(slave, force)
                    wo.writePythonDict(slave)
                    wo.writeHdrC(slave)
            except WbgenError as e:
                print("ERROR: %s" % e, file=sys.stderr)
                sys.exit(2)
            except ExpatError as e:
                print("ERROR: %s is not well-formed XML: %s" % (xmlIn, e), file=sys.stderr)
                sys.exit(2)
            
            #writeTbVhd(fileTbVhd)
            print("\n%s" % ('*' * 80)) 
            print("\nDone!")
        else:
            print("\nFile not found: %s" % xmlIn)
    
    


if __name__ == "__main__":
    main()



