'''
See more here: https://github.com/davidkastner/quick-csa/blob/main/README.md
DESCRIPTION
   By default, TeraChem scans only print the charge and spin of the final frame.
   We change this by using the ml_prop keyword. Now every optimization will print.
   However, we only need the charge and spin at the end of each optimization.
   This script will return the the charge and spin into a readable format.
   The coordinates are already piped nicely to scan_optim.xyz.

   Author: David Kastner
   Massachusetts Institute of Technology
   kastner (at) mit . edu
   
'''

################################## FUNCTIONS ###################################

'''
Reads through the qmscript.out and counts iterations per scan step.
Then returns then as a dictionary: {scan_number:iterations}.
Parameters
----------
pdb_name : str
    The name of the PDB that the user would like processed
    
Returns
-------
iteraction_pairs : dictionary
    The scan step number as the key and iterations as the value
'''


def get_iteration_pairs():
    # Read in the TeraChem output, the charge, and the spin
    opt_count = 0
    scan_count = 0
    scan_step_pairs = {}
    with open('./qmscript.out', 'r') as qmscript:
        for line in qmscript:
            if line[:14] == 'FINAL ENERGY: ':
                opt_count += 1
            if line[:24] == '-=#=- Optimized Energy: ':
                scan_count += 1
                scan_step_pairs[scan_count] = opt_count
                opt_count = 0

    # Convert dictionary to additive list
    final_scan_position = []
    running_count = 0
    for key, value in scan_step_pairs.items():
        running_count += value
        final_scan_position.append(running_count)

    return final_scan_position, scan_step_pairs


'''
Extracts spin sections from mullpop for each scan and stores them as a dict.
Parameters
----------
iter_pairs : dictionary
    The scan step number as the key and iterations as the value    
    
Returns
-------
spin_pairs : dictionary
    The scan step number as the key and the spin section as the key
'''


def get_scan_spins(final_scan_position):
    section_count = 0
    section_content = ''
    sections = []
    current_section = 0
    section_found = False
    with open('./scr/mullpop', 'r') as spins:
        for line in spins:
            if line[29:42] == 'Spin-Averaged':
                current_section += 1
                if current_section == final_scan_position[section_count]:
                    section_count += 1
                    section_found = True
                elif section_found:
                    sections.append(section_content)
                    section_found = False
                    section_content = ''

            # Combine all lines of a final section into a single string
            if section_found:
                section_content += line

    # Add the last section of the file to the list of sections
    if section_found:
        sections.append(section_content)

    # Write the spin data for the final step of each scan step to a file
    with open('./scr/scan_spin', 'w') as scan_spin_file:
        for index, section in enumerate(sections):
            scan_spin_file.write(section)
            scan_spin_file.write('End scan {}\n'.format(index + 1))

    return sections


'''
Extracts charges from charge_mull.xls for each scan and stores them as a dict.
Parameters
----------
iter_pairs : dictionary
    The scan step number as the key and iterations as the value    
    
Returns
-------
charge_pairs : dictionary
    The scan step number as the key and the charge section as the key
'''


def get_scan_charges(final_scan_position):
    section_count = 0
    section_content = ''
    sections = []
    current_section = 0
    section_found = False
    with open('./scr/charge_mull.xls', 'r') as charges:
        for line in charges:
            line_content = line.split()
            if line_content[0] == '1':
                current_section += 1
                if current_section == final_scan_position[section_count]:
                    section_count += 1
                    section_found = True
                elif section_found:
                    sections.append(section_content)
                    section_found = False
                    section_content = ''

            # Combine all lines of a final section into a single string
            if section_found:
                section_content += line

    # Add the last section of the file to the list of sections
    if section_found:
        sections.append(section_content)

    # Write the charge data for the final step of each scan step to a file
    with open('./scr/scan_charge', 'w') as scan_charge_file:
        for index, section in enumerate(sections):
            scan_charge_file.write(section)
            scan_charge_file.write('End scan {}\n'.format(index + 1))

    return sections


def scan_data_organizer():
    print('\n.---------------------------.')
    print('| ORGANIZE ENERGY SCAN DATA |')
    print('.---------------------------.\n')
    print('Use the ml_prop keyword when running your TeraChem scan.')
    print('Execute this script from the directory where this job was run.\n')

    final_scan_position, scan_step_pairs = get_iteration_pairs()
    get_scan_spins(final_scan_position)
    get_scan_charges(final_scan_position)


if __name__ == "__main__":
    scan_data_organizer()