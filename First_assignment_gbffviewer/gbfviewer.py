import sys
import os
import re 
#Erase the newline in dnaseq and proteinlist

## Location functions 
def location(k):
    if k[1].split("=")[0] == "data":
        data=k[1].split("=")[1]
    else:
        raise Exception('You should specify the data option')
    return data

#print(location(sys.argv))#Validation of the last function


def verificarPath():
    path = location(sys.argv)
    if path != "":##verify that is not empty
        pass
    else:
        raise Exception('location is null')
    

#verificarPath()#Validation of the last function

###ID functions

def listaArchivos(path):####ask for extension, specifically gbff
    filelist=[]
    with os.scandir(path) as entries:
        for i in entries:
            if i.name[len(i.name)-4:len(i.name)]=="gbff":
                filelist.append(i.name)
    return filelist

#print(listaArchivos(location(sys.argv)))#Validation of the last function

def ID():# Validator that a path is given
    verificarPath()
    if sys.argv[2].split("=")[0] == "id":
        path = sys.argv[2].split("=")[1]
        if path != "":##verify that is not empty
            return path
        else:
            return ''
    else:
        return ''

def findaccesion(files,accesion): 
    lines = []
    accfiles=[]
    for i in files:
        with open(i) as file:
            lines = file.readlines()
            for line in lines:
                if re.search(r'\bACCESSION\b', line):
                    acc=line.split("   ")[1]
                    if re.search(r'\b \b', acc):
                        acc = acc.split(" ")[0]
                    #print(acc,accesion)
                    if acc[0:len(accesion)] == accesion:
                        accfiles.append(file.name)
                        break
    return accfiles
#'AY721616'
#print(findaccesion(listaArchivos(location(sys.argv)),"AY585228")) #Validation of the last function

def findname(files,name): ## This is when a name of the organism is given only
    namefiles=[]
    for i in files:
        lines = []
        with open(i) as file:
            lines = file.readlines()
            for line in lines:
                if re.search(r'\bORGANISM\b', line):
                    acc=line.split("  ")[2]
                    #print(acc,name)
                    if acc[0:len(name)] == name:
                        namefiles.append(file.name)
    return namefiles

#print(findname(listaArchivos(location(sys.argv)),"Human coronavirus OC43")) #Validation of the last function

def findprot(files,prot):##This function is when a prot is given and not an accesion
    protfiles=[]
    for i in files:
        lines = []
        with open(i) as file:
            lines = file.readlines()
            for line in lines:
                if re.search(r'\b/protein_id\b', line):
                    acc=line.split("=")[1]
                    #print(acc,accesion)
                    if acc[0:len(prot)] == prot:
                        protfiles.append(file.name)
    return protfiles


def queryfiles():##loop through the files to get the match you want to search according to waht to look for
    filestot=[]
    if ID() != '': ##Search for a file with the specific id
        files=listaArchivos(location(sys.argv))## files in wich we are going loop
        type=ID().split(':')[0]#Getting the type of search we are looking for
        accesion=ID().split(':')[1]
        if type== "prot":
            filestot = findprot(files,accesion)
        elif type == "acc":   
            filestot = findaccesion(files,str(accesion))# accesion should be here
        elif type == "name":
            filestot = findname(files, accesion)
        else:
            raise Exception('ID is not given according to instructions')
    else: ##SEARCH IN ALL FILES
        filestot=listaArchivos(location(sys.argv))
    return filestot

#print(queryfiles())##files in which to search #Validation of the last function



####options of query functions

def filesopt(specificfiles):# get only the files and locus
    for i in specificfiles:
        lines = []
        with open(i) as file:
            lines = file.readlines()
            m=str(file.name)+':'
            print(m+"\n"+lines[0])

def totalopt(specificfiles):##Form Data-START to Data-END
    lines = []
    lines2print=[]
    for i in specificfiles:
        enter=0
        with open(i) as file:
            lines = file.readlines()
            linelocus=lines[0]
            for line in lines:
                if re.search(r'\bGenome-Assembly-Data-END\b', line):
                    enter = 0
                    break## this break the last loop if im doing it right
                if enter==1:
                    lines2print.append(line)
                if re.search(r'\bGenome-Assembly-Data-START\b', line):
                    #lines2print.append('\n') maybe to atrt in newline after each file
                    u=str(file.name)+':'
                    lines2print.append(u)
                    lines2print.append(linelocus)
                    enter=1
    print('\n'.join(map(str,lines2print)))

def headeropt(specificfiles):##LOCUS throgh ORGANISM
    lines = []
    lines2print=[]
    for i in specificfiles:
        with open(i) as file:
            lines = file.readlines()
            enter= 0
            for line in lines:
                if re.search(r'\bREFERENCE\b', line):
                    enter = 0
                    break## This is done only once per file
                if enter==1:
                    lines2print.append(line)
                if re.search(r'\bLOCUS\b', line):
                    #lines2print.append('\n') maybe to atrt in newline after each file
                    u=str(file.name)+":"
                    lines2print.append(u)
                    lines2print.append(line)
                    enter=1
    print('\n'.join(map(str,lines2print)))

def locusheader(filename):#Print the locus header of a file
    with open(filename) as file:
        line = file.readline()
        print(line)

def dnaseqopt(specificfiles):## Origin to //
    lines = []
    lines2print=[]
    for i in specificfiles:
        enter=0
        with open(i) as file:
            lines = file.readlines()
            for line in lines:
                if line[0:2]=="//":
                    enter = 0
                if enter==1:
                    lines2print.append(line[:-2])
                if re.search(r'\bORIGIN\b', line):
                    u=str(file.name)+':'
                    print(locusheader(file.name))
                    lines2print.append(u)
                    enter=1
    print('\n'.join(map(str,lines2print)))


def protseqopt(specificfiles,protseq):#/protein_id\ and after it /translation ending in CDS 
    for i in specificfiles:
        lines = []
        p=0
        space='                     '
        with open(i) as file:
            print(file.name+",")
            print(locusheader(file.name))
            lines = file.readlines()
            for line in lines:
                if p==1 and not (line[0:21] == space):
                    p=0
                if re.search(r'\bprotein_id\b', line):
                    id=line.split("=")[1]
                    if id[1:len(id)-2] == protseq:
                        p=1
                if p==1 and re.search(r'\btranslation\b', line):
                    seq=line.split("=")[1]
                    print(seq[1:len(seq)-2])
                if p==1 and not (re.search(r'\btranslation\b', line)):
                    sequence1=line.split(space)[1]
                    print(sequence1[:-2])

                #

def protlistopt(specificfiles):#protein id list and product
    for i in specificfiles:
        lines = []
        p=0
        with open(i) as file:
            print(file.name+",")
            print(locusheader(file.name))
            lines = file.readlines()
            for line in lines:
                if re.search(r'\bproduct\b', line):
                    product=line.split("=")[1]
                    p=1
                if p==1 and (re.search(r'\bprotein_id\b', line)):
                    id=line.split("=")[1].split("\n")[0]
                    print(id[1:len(id)-1]+' '+product[1:len(product)-2])
        


def Principalfunction(): # function that does something depending on the option arg
    specificfiles=queryfiles()
    if len(sys.argv) != 4:
        raise Exception('Enter valid options')
    else:
        queryoption=sys.argv[3]#available files, totals, header, dnaseq, proteinlist, proteinseq
        if queryoption=="files":
            filesopt(specificfiles)
        elif queryoption=="totals":## Genome annoation or Genome Assembly
            totalopt(specificfiles)
        elif queryoption=="header":##LOCUS throgh ORGANISM
            headeropt(specificfiles)
        elif queryoption=="dnaseq": ##ORIGIN
            dnaseqopt(specificfiles)
        elif queryoption=="proteinlist":#/protein_id\ and after it /product
            protlistopt(specificfiles)
        elif queryoption[0:10]=="proteinseq":#/protein_id\ and after it /translation
            protseq = queryoption.split('=')[1]
            protseqopt(specificfiles,protseq)

Principalfunction()

#Example commands:

#command python gbfviewer.py data=. id=acc:NW_008703570 totals  
###Command to try python gbfviewer.py data=. id=acc:AY585228 files
###Command to try python gbfviewer.py data=. id=acc:AY585228 header
##python gbfviewer.py data=. id=acc:AY585228 proteinseq=AAT84351.1  
##python gbfviewer.py data=. id=acc:AY585228 dnaseq
##python gbfviewer.py data=. id=acc:AY585228 proteinlist
