'''
See more here: https://github.com/davidkastner/quick-csa/blob/main/README.md
DESCRIPTION
    Identify the ideal starting path for NEB from a TeraChem PES.
    Author: David Kastner
    Massachusetts Institute of Technology
    kastner (at) mit . edu
SEE ALSO
    collect_reaction_coordinate.py
'''
################################ DEPENDENCIES ##################################
from scipy.spatial import distance
import numpy as np

################################## FUNCTIONS ###################################
'''
Get the user's linear combination of restraints and preferred NEB path length.
Returns
-------
atoms : list
    list of atoms indices
Get the user's reaction coordinate definition.
Returns
-------
atoms : list
    list of atoms indices
'''
def user_input():
    # What atoms define the first reaction coordinate
    coord1_input = input('What atoms define your first reaction coordinate?')
    # Convert user input to a list even if it is hyphenated
    temp = [(lambda sub: range(sub[0], sub[-1] + 1))(list(map(int, ele.split('-')))) for ele in coord1_input.split(',')]
    coord1 = [b for a in temp for b in a]

    # What atoms define the second reaction coordinate
    coord2_input = input('What atoms define your second reaction coordinate?')
    # Convert user input to a list even if it is hyphenated
    temp = [(lambda sub: range(sub[0], sub[-1] + 1))(list(map(int, ele.split('-')))) for ele in coord2_input.split(',')]
    coord2 = [b for a in temp for b in a]

    # How many images should be in the NEB path
    image_count = int(input('What atoms define your second reaction coordinate?'))

    return coord1, coord2, image_count

'''
Get each one of the frames on store them.
Parameters
----------
dict : dictionary
    List of two atoms defining a reaction coordiante distance
Returns
-------
reaction_coordinates : list
    List of values mapping to the distance that two atoms have moved.
'''
def get_frames(coord1, coord2, master_list):
    # Variables that measure our progress in parsing the optim.xyz file
    frame_contents = []
    line_count = 0
    frame_count = 0
    section_length_flag = False
    # Loop through optim.xyz and collect distances, energies and frame contents 
    with open('./optim.xyz', 'r') as optim:
        for line in optim:
            # We need to know how long each section is but only count once
            if section_length_flag == False:
                section_length = int(line.strip()) + 1
                section_length_flag = True

            # The second line will have the energy
            if line_count == 1:
                energy = float(line.split(' ')[0])
                master_list[frame_count]['energy'] = energy
            
            # Get the distance between each atom for coordinate 1
            xyz_coord1_list = []
            current_atom = line_count - 1 
            if current_atom in coord1:
                line_elements = line.split()
                xyz_coords = line_elements[10:55]
                xyz_coord1_list.append(list(map(float, xyz_coords)))
                if len(xyz_coord1_list) and len(xyz_coord1_list) % 2 == 0:
                    atom_1 = tuple(xyz_coord1_list[-1])
                    atom_2 = tuple(xyz_coord1_list[-2])
                    coord1_dist = distance.euclidean(atom_1, atom_2)
                    master_list[frame_count]['coord1_dist'] = coord1_dist

            # Get the distance between each atom for coordinate 2
            xyz_coord2_list = []
            current_atom = line_count - 1 
            if current_atom in coord2:
                line_elements = line.split()
                xyz_coords = line_elements[10:55]
                xyz_coord2_list.append(list(map(float, xyz_coords)))
                if len(xyz_coord2_list) and len(xyz_coord2_list) % 2 == 0:
                    atom_1 = tuple(xyz_coord2_list[-1])
                    atom_2 = tuple(xyz_coord2_list[-2])
                    coord2_dist = distance.euclidean(atom_1, atom_2)
                    master_list[frame_count]['coord2_dist'] = coord2_dist

            # At the end of the frame's section reset the line_count
            if line_count == section_length + 1:
                line_count = 1
                master_list[frame_count]['frame_contents'] = frame_contents

            frame_contents.append(line)    
            line_count += 1

    return master_list

# General function handler
def reaction_coordinate_collector():
    print('\n.--------------------------------.')
    print('| WELCOME TO NEB IMAGE GENERATOR |')
    print('.--------------------------------.\n')
    print('Run this script in the same directory where you ran your TeraChem job.')
    print('Identifies the best set of images for an initial NEB path.\n')

    # This list will be populated with dictionaries for each frame
    master_list = [{}]
    # Get the two reaction coordinates and the preferred number of images
    #coord1,coord2,image_count = user_input()
    coord1 = [123,128]
    coord2 = [128,138]
    image_count = 20


    # Get the distances for the first reaction coordinate
    master_list = get_frames(coord1, coord2, master_list)
    print(master_list)


if __name__ == "__main__":
    reaction_coordinate_collector()
