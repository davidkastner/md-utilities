'''
See more here: https://github.com/davidkastner/pdb-utilities/blob/main/README.md
DESCRIPTION
   Creates a "mask" from a PDB file only containing user-specified residues.
   Author: David Kastner
   Massachusetts Institute of Technology
   kastner (at) mit . edu
SEE ALSO
   renumerate.py, renumber_waters.py
'''

#Introduce user to the function
print('WELCOME TO MASK MAKER')
print('--------------------------\n')
print('You want to select a specific selection of residues from your PDB?')
pdb_name = input('Which PDB in this directory are we selecting from?: ')
raw_mask = input('Enter the residues as a list (1,2,3,etc.)?: ')
print('--------------------------\n')

#Create a list from the users input
mask = raw_mask.split(',')

#The code for Mask Maker begins here
res_type_array = []
new_pdb = '{}_mask.pdb'.format(pdb_name[:-4])
with open(new_pdb, 'w') as new_mask:
  with open(pdb_name, 'r') as original:
    for line in original:

      #Start checking once we reach the ATOM section
      res_index = line[22:28].strip()
      res_type = line[:4]
      if res_type == 'ATOM' and res_index in mask:
        new_mask.write(line)
        res_type_array.append(res_index)
        continue
      #We don't won't to count chain breaks as a discarded residue
      if line[:3] == 'TER':
        continue
      #We don't want to include the last line so we will watch for END
      if line[:3] == 'END':
        new_mask.write(line)
        break

#Print important statistics for the user
print('We extracted {} residues for the mask'.format(len(set(res_type_array))))
print('Your new file is named {}'.format(new_pdb))
print('Done.')