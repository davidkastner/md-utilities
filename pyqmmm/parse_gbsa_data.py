'''
See more here: https://github.com/davidkastner/quick-csa/blob/main/README.md
DESCRIPTION
    Generates GBSA data and processes and plots the output.

    Author: David Kastner
    Massachusetts Institute of Technology
    kastner (at) mit . edu

'''
################################ DEPENDENCIES ##################################
import pandas as pd
import numpy as np
import time
from os import defpath
import glob

################################## VARIABLES ###################################
top_res_count = 10   # How many of the top residues are you interested in?

################################## FUNCTIONS ###################################

'''
Extract the total decomposition energy from the DELTA section.
Returns
-------
df : pandas dataframe
    A Pandas dataframe containing only the delta G of binding energies
'''


def clean_raw_data():
    # List of file keywords from the GBSA output
    file_extenstion = '*24.dat'
    total_energy_keyword = 'T,o,t,a,l, ,E,n,e,r,g,y'
    sidechain_keyword = 'S,i,d,e,c,h,a,i,n'
    backbone_keyword = 'B,a,c,k,b,o,n,e'
    csv_file_name = 'deltas.csv'

    # MMGBSA.py generates four files and we want the one that ends in 24.dat
    raw_file = glob.glob(file_extenstion, recursive=True)[0]
    delta_section = False
    # The raw file contains data we don't need; we only want the DELTA section
    with open(raw_file, 'r') as raw_data:
        with open(csv_file_name, 'w') as csv_file:
            for line in raw_data:
                # If we reach the DELTA section write the current line to a new file
                if delta_section == True:
                    # Stop at the end of the section
                    if sidechain_keyword in line or backbone_keyword in line:
                        break
                    # Save the data to a csv file for to open in pandas later
                    else:
                        csv_file.write(line)
                # Set a flag when we find the poorly named section generated by GBSA
                if line[:len(total_energy_keyword)] == total_energy_keyword:
                    delta_section = True

    # Save the data to a Pandas dataframe and return the data
    df = pd.read_csv(csv_file_name)
    # Fix the default headers
    df.columns = ['Resid 1', 'Resid 2', 'Internal Avg', 'Internal SD', 'Internal SDM', 'VDW Avg', 'VDW SD', 'VDW SDM', 'Electrostatic Avg', 'Electrostatic SD', 'Electrostatic SDM',
                  'Polar Solvation Avg', 'Polar Solvation SD', 'Polar Solvation SDM', 'Non-polar Solvation Avg', 'Non-polar Solvation SD', 'Non-polar Solvation SDM', 'Total Avg', 'Total SD', 'Total SDM']
    df.drop(index=df.index[0], axis=0, inplace=True)
    df = df[df['Resid 1'].str.contains('LY1')]

    return df


'''
Get the data for resdues interacting with substrate.
Parameters
-------
df : pandas dataframe
    A Pandas dataframe containing only the delta G of binding energies
'''


def get_total_energy(df):
    total_energy_dict = {}
    for index, row in df.iterrows():
        # Create a dictionary with every residue and its total G
        total_energy_dict[row[1]] = row[17]

    return total_energy_dict


'''
Generates a plot of the total energies.
Parameters
-------
df : pandas dataframe
    A Pandas dataframe containing only the delta G of binding energies
'''


def plot_totals(df):
    return


'''
Generates a plot of the energies broken down.
Parameters
-------
df : pandas dataframe
    A Pandas dataframe containing only the delta G of binding energies
'''


def plot_individuals(df):
    return

# General function handler


def parse_gbsa_data():
    print('\n.-----------------.')
    print('| PARSE GBSA DATA |')
    print('.-----------------.\n')
    print('Run this in the same directory as your GBSA output')
    print('Remember to update variables section for your system')
    # Give the user time to read description
    # time.sleep(5)

    # Clean the GBSA output and convert it to a dataframe
    print('\nParsing GBSA output file...')
    df = clean_raw_data()

    # Obtain only the interactions involving the substrate
    print('\nGetting total energies...')
    total_energy_dict = get_total_energy(df)
    print(total_energy_dict)


if __name__ == "__main__":
    parse_gbsa_data()