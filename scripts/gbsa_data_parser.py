import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def update_res_names(df):
    # Dict containing MCPB residue names and their more convnetional pairs
    res_names = {'AG2':'ARG', 'AN1':'ASN', 'HIE':'HIS', 'TR1':'TYR', 'HD1':'HIS', 'HD2':'HIS', 'AP1':'ASP', 'CL1':'CL'}
    df.reset_index(inplace=True)
    df = df.replace({'Resname 1':res_names})
    df = df.replace({'Resname 2':res_names})
    df['Resname 2'].replace(res_names)

    df.insert(4, 'Residue', df['Resname 2'] + df['Resid 2'].astype(str))
    return df

def get_gbsa_df(raw):
    # List of file keywords from the GBSA output
    total_energy_keyword = 'D,E,L,T,A,S,:'
    sidechain_keyword = 'S,i,d,e,c,h,a,i,n, ,E,n,e,r,g,y, ,D,e,c,o,m,p,o,s,i,t,i,o,n,:'
    columns = ['Resname 1', 'Resid 1','Resname 2', 'Resid 2','Internal', 'Internal SD', 'Internal SDM', 'VDW', 'VDW SD', 'VDW SDM', 'Electrostatic', 'Electrostatic SD', 'Electrostatic SDM',
                  'Polar', 'Polar SD', 'Polar SDM', 'Non-polar', 'Non-polar SD', 'Non-polar SDM', 'Total', 'Total SD', 'Total SDM']
    csv_file_name = 'deltas.csv'

    # MMGBSA.py generates four files and we want the one that ends in 24.dat
    delta_section = False
    # The raw file contains data we don't need; we only want the DELTA section
    with open(raw, 'r') as raw_data:
        with open(csv_file_name, 'w') as csv_file:
            for line in raw_data:
                # If we reach the DELTA section write the current line to a new file
                if delta_section == True:
                    if 'T,o,t,a,l' in line:
                        continue
                    if "Std" in line:
                        continue
                    if "Resid" in line:
                        csv_file.write(",".join(columns)) 
                        continue
                    # Stop at the end of the section
                    if sidechain_keyword in line:
                        break
                    # Save the data to a csv file for to open in pandas later
                    else:
                        line = '\n' + ','.join(line.split())
                        csv_file.write(line)

                # Set a flag when we find the poorly named section generated by GBSA
                if line[:len(total_energy_keyword)] == total_energy_keyword:
                    delta_section = True

    # Save the data to a Pandas dataframe and return the data
    df = pd.read_csv(csv_file_name)
    # Remove all rows where Resid 1 and Resid 2 are the same number
    df = df[df['Resid 1'] != df['Resid 2']]

    # Rewrite the csv file
    df.to_csv('deltas.csv')

    return df

def get_top_hits_df(df):
    # Ask the user how many of the top hits they would like to see
    hit_num = int(input('Show me the top n residues: '))
    # Get the top largest contributors to ligand interaction energies
    df_hits = df[df['Resid 1'] == 247].nsmallest(hit_num, 'Total', keep='all')

    return  df_hits

def figure_formatting():
    font = {'family': 'sans-serif', 'weight': 'bold', 'size': 18}
    plt.rc('font', **font)
    plt.rcParams['axes.linewidth'] = 2.5
    plt.rcParams['xtick.major.size'] = 10
    plt.rcParams['xtick.major.width'] = 2.5
    plt.rcParams['ytick.major.size'] = 10
    plt.rcParams['ytick.major.width'] = 2.5
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['mathtext.default'] = 'regular'
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')

def plot_single_total_gbsa(df, file_name):
    colors = ['#8ecae6', '#219ebc', '#023047', '#ffb703', '#fb8500']
    ax = df.plot.bar(x='Residue', y='Total', color = colors)
    figure_formatting()
    ax.set_ylabel("GBSA energy score", weight='bold')
    ax.set_xlabel("Residue", weight='bold')
    plt.savefig(file_name, bbox_inches='tight')

def plot_single_all_gbsa(df, file_name):
    colors = ['#8ecae6', '#219ebc', '#023047', '#ffb703', '#fb8500']
    ax = df.plot.bar(x='Residue', y=['VDW','Electrostatic','Polar','Non-polar','Total'], color = colors)
    figure_formatting()
    ax.set_ylabel("GBSA energy score", weight='bold')
    ax.set_xlabel("Residue", weight='bold')
    plt.savefig(file_name, bbox_inches='tight')

# def plot_multi_total_gbsa(df_hits, df):
#     # Use df_hits as a mask to select the top hits from df
#     df.to_csv('test_unfiltered.csv')
#     df = df[df['index'].isin(df_hits['index'])]
#     df_extracted = df[['Residue']]

    
    # # Convert dataframe data to lists
    # x1 = df_hits['Residue'].tolist()
    # y1 = df_hits['Total'].tolist()
    # x2 = df['Residue'].tolist()
    # y2 = df['Total'].tolist()

    # # generate plots
    # labels = 
    # width = 0.35 # The width of each bar
    # x = np.arange(len(x1)) # The label locations
    # fig, ax = plt.subplots()
    # rects1 = ax.bar(x - width/2, y1, width, label='Acute BesD')
    # rects2 = ax.bar(x + width/2, y2, width, label='Obtuse BesD')

    # ax.set_ylabel('GBSA energy score')
    # ax.set_xticks(x, labels)


def gbsa():
    file_extension = '*24.dat'
    acute_plot_names = ['acute_total.pdf','acute_all.pdf']
    obtuse_plot_names = ['obtuse_total.pdf','obtuse_all.pdf']
    plot_file_names = [acute_plot_names, obtuse_plot_names]
    df_list = []
    df_hits_list = []
    # Collect all the GBSA data located in the current directory
    raw_files = glob.glob(file_extension, recursive=True)
    sorted(raw_files)
    # Loop through each GBSA file and analyze the results
    for raw, file_name_list in zip(raw_files, plot_file_names):
        df = get_gbsa_df(raw)
        df = update_res_names(df)
        df_hits = get_top_hits_df(df)
        df_list.append(df)
        df_hits_list.append(df_hits)

        # Generate a plots
        plot_single_total_gbsa(df_hits, file_name_list[0])
        plot_single_all_gbsa(df_hits, file_name_list[1])
    
    # plot_multi_total_gbsa(df_hits)
    # plot_multi_total_gbsa(df_hits_list[0], df_list[1])
    # plot_multi_total_gbsa(df_hits_list[1], df_list[0])

if __name__ == "__main__":
    gbsa()
