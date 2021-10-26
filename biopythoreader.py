import Bio 
from Bio import Entrez , SeqIO
from Bio.Seq import Seq
import pandas as pd
import sys

### Get the ids that match the query
def query(queri,maximum):
  Querie=str(queri)
  Entrez.email = "evelas13@eafit.edu.co"
  handleSearch = Entrez.esearch(db="Nucleotide", retmax=maximum, term=Querie)
  rec = Entrez.read(handleSearch)
  idlist = rec["IdList"]
  return idlist



def UniqueIDS(idlist):
    taxa={}
    for i in idlist:
      handleFetch = Entrez.efetch(db="nucleotide", retype="gb" ,id=i, retmode="xml")
      record = Entrez.parse(handleFetch).__next__()
      taxonomy=record['GBSeq_taxonomy'].split(';')
      #Creating a  dictionary for each ID as value and  the taxa as a key and verifying that there is only 1 taxa for each ID and the term COI in the 
      if taxonomy[len(taxonomy)-2] in taxa.keys() or not (record['GBSeq_feature-table'][2]['GBFeature_quals'][0]['GBQualifier_value']== 'COI'):
        pass
      else:
        taxa[taxonomy[len(taxonomy)-2]]= i  # this command gets the taxon one step above the genera, in this case is the family
    handleFetch.close()
    return list(taxa.values())




def get_csv(IDlist):
  myDataDictionary={}
  record=[]#Done
  moleculetype=[]# Done
  locus=[]#Done
  length=[]#Done
  strandedness=[]#Done
  topology=[]# Done
  division=[]#done
  source=[]#done
  organism=[]#done
  taxonomy=[]#done
  sequence=[]#done
  totalA=[]
  totalC=[]
  totalG=[]
  totalT=[]
  for i in IDlist:
    with Entrez.efetch(db="nucleotide", rettype="gb", retmode="text", id=i) as handle:
      seq_record = SeqIO.read(handle, "genbank")#Locus, length, strandedness, moltype, topology, division, source, organism,taxonomy, sequence
      name = seq_record.description.split(' ')[0]+' '+seq_record.description.split(' ')[1]
      record.append(i)
      moleculetype.append(seq_record.annotations['molecule_type'])
      topology.append(seq_record.annotations['topology'])
      division.append(seq_record.annotations['data_file_division'])
      source.append(seq_record.annotations['source'])
      taxonomy.append(seq_record.annotations['taxonomy'])
      sequence.append(seq_record.seq)
      organism.append(name)
      totalA.append(seq_record.seq.count("A"))
      totalC.append(seq_record.seq.count("C"))
      totalG.append(seq_record.seq.count("G"))
      totalT.append(seq_record.seq.count("T"))
      if seq_record.features[1].type=='gene':
        locus.append(str(seq_record.features[1].location).split('(')[0])
        strandedness.append(str(seq_record.features[1].location).split('(')[1][:-1])
        minus=int(str(seq_record.features[1].location).split('<')[1].split(':')[0])
        plus=int(str(seq_record.features[1].location).split('>')[1].split(']')[0])
        length.append(plus-minus)
      else:# fill missing values to have everything  in the same index
        locus.append('')
        strandedness.append('')
        length.append('')
  #Filling the dictionary
  myDataDictionary['Record']=record
  myDataDictionary['Moleculetype']=moleculetype
  myDataDictionary['Locus']=locus
  myDataDictionary['Length']=length
  myDataDictionary['Strandedness']=strandedness
  myDataDictionary['Topology']=topology
  myDataDictionary['Division'] = division
  myDataDictionary['Source']=source
  myDataDictionary['Organism']=organism
  myDataDictionary['Taxonomy']=taxonomy
  myDataDictionary['Sequence']=sequence
  myDataDictionary['TotalA']=totalA
  myDataDictionary['TotalG']=totalG
  myDataDictionary['TotalC']=totalC
  myDataDictionary['TotalT']=totalT

  dfObj = pd.DataFrame(myDataDictionary)
  return dfObj
  #dfObj.to_csv("afilenameyoupreffer.csv",sep='\t')

def Getfasta(IDlist):
  for i in IDlist:
    with Entrez.efetch(db="nucleotide", rettype="gb", retmode="text", id=i) as handle:
      seq_record = SeqIO.read(handle, "genbank")
      name = seq_record.description.split(' ')[0]+'_'+seq_record.description.split(' ')[1]+'.fasta'
      count = SeqIO.write(seq_record, name, "fasta")

def main():
    queri=sys.argv[1]
    option=sys.argv[2]
    n=int(sys.argv[3])
    idlist=query(queri,n)
    IDlist=UniqueIDS(idlist)
    if option=='a':
        dfObj=get_csv(IDlist)
        dfObj.to_csv("NCBIquery.csv",sep='\t')
    if option=='b':
        Getfasta(IDlist)


main()

#python biopythoreader.py "(\"Sedentaria\"[Organism] OR Sedentaria[All Fields]) AND COI[All Fields]" a 100
#  
