# Takes a PDB accession when prompted and generates a sequence file
from modeller import *
code = input("Enter a PDB accession: ") 

e = Environ()
m = Model(e, file=code)
aln = Alignment(e)
aln.append_model(m, align_codes=code)
aln.write(file=code+'.seq')

print('A sequence file for {} was generated.'.format(code))