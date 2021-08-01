import sys
import os
import re 

## Location functions 
def location(k):
    if k[1].split("=")[0] == "data":
        data=k[1].split("=")[1]
    else:
        print(k[1].split("=")[1])
        raise Exception('You should specify the data option')
    return data
print(sys.argv)
#print(location(sys.argv))


def verificarPath():
    path = location(sys.argv)
    if path != "":##verify that is not empty
        pass
    else:
        raise Exception('location is null')
    

#verificarPath()
#id=acc:NC_0144
###ID functions

def listaArchivos(path):
    filelist=[]
    with os.scandir(path) as entries:
        for i in entries:
            filelist.append(i.name)
    return filelist

#print(listaArchivos(location(sys.argv)))

def ID():
    if sys.argv[2].split("=")[0] == "id":
        path = sys.argv[2].split("=")[1]
        if path != "":##verify that is not empty
            return path
        else:
            return ''
    else:
        return ''

def findaccesion(files,accesion):
    for i in files:
        lines = []
        accfiles=[]
        with open(i) as file:
            lines = file.readlines()
            for line in lines:
                if re.search(r'\bACCESSION\b', line):
                    acc=line.split("   ")[1]
                    if re.search(r'\b \b', acc):
                        acc = acc.split(' ')[0]
                    #print(acc,accesion)
                    if acc[0:len(accesion)] == accesion:
                        accfiles.append(file.name)
    return accfiles
#'AY721616'
#print(findaccesion(listaArchivos(location(sys.argv)),"AY585228"))

def findname(files,name):
    for i in files:
        lines = []
        namefiles=[]
        with open(i) as file:
            lines = file.readlines()
            for line in lines:
                if re.search(r'\bORGANISM\b', line):
                    acc=line.split("  ")[2]
                    #print(acc,name)
                    if acc[0:len(name)] == name:
                        namefiles.append(file.name)
    return namefiles

#print(findname(listaArchivos(location(sys.argv)),"Human coronavirus OC43"))

def findprot(files,prot):
    for i in files:
        lines = []
        protfiles=[]
        with open(i) as file:
            lines = file.readlines()
            for line in lines:
                if re.search(r'\b/protein_id\b', line):
                    acc=line.split("=")[1]
                    #print(acc,accesion)
                    if acc[0:len(prot)] == prot:
                        protfiles.append(file.name)
    return protfiles


def queryfiles():##loop through the files to get the math you want
    filestot=[]
    if ID() != '': ##Search for a file with the specific id
        files=listaArchivos(location(sys.argv))## files in wich we are going loop
        type=ID().split(':')[0]#Getting the type of search we are looking for
        accesion=ID().split(':')[1]
        if type== "prot":
            filestot = findprot(files,accesion)
        elif type == "acc":
            print(str(accesion))
            filestot = findaccesion(files,str(accesion))# accesion should be here
        elif type == "name":
            filestot = findname(files, accesion)
        else:
            raise Exception('ID is not given according to instructions')
    else: ##SEARCH IN ALL FILES
        filestot=listaArchivos(location(sys.argv))
    return filestot

#print(queryfiles())##files in which to search

#maybe define each action of each if as aa function

specificfiles=queryfiles()
if len(sys.argv != 4):
     raise Exception('Enter valid options')
else:
    queryoption=sys.argv[3]#available files, totals, header, dnaseq, proteinlist, proteinseq
    if queryoption=="files":
        for i in specificfiles:
            lines = []
            namefiles=[]
            with open(i) as file:
                lines = file.readlines()
                m=str(file.name)+':'
                print(m+"\n"+lines[0])
    elif queryoption=="totals":
        for i in specificfiles:
            lines = []
            lines2print=[]
            enter=0
            with open(i) as file:
                lines = file.readlines()
                for line in lines:
                    if re.search(r'\b##Genome-Annotation-Data-END##\b', line):
                        enter = 0
                        break
                    if enter==1:
                        lines2print.append(line)
                    if re.search(r'\b##Genome-Annotation-Data-START##\b', line):
                        #lines2print.append('\n') maybe to atrt in newline after each file
                        u=str(file.name)+':'
                        lines2print.append(u)
                        enter=1
        print('\n'.join(map(str,lines2print)))
    elif queryoption=="header":
        pass
    elif queryoption=="dnaseq":
        pass
    elif queryoption=="proteinlist":
        pass
    elif queryoption[0:10]=="proteinseq":
        protseq = queryoption.split('=')[1]

print()
for i in specificfiles:
    lines = []
    namefiles=[]
    with open(i) as file:
        lines = file.readlines()
        for line in lines:
            if re.search(r'\bORGANISM\b', line):
                acc=line.split("  ")[2]
                #print(acc,name)
                if acc[0:len(name)] == name:
                    namefiles.append(file.name)


###Command to try python gbfviewer.py data=. id=acc:AY585228 files