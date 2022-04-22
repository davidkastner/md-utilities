"""
Docs: https://github.com/davidkastner/pyQMMM/blob/main/pyqmmm/README.md
DESCRIPTION
    Reads in DCCM data and formats it into the Kulik Lab standard format.

    Author: David Kastner
    Massachusetts Institute of Technology
    kastner (at) mit . edu

"""

################################ DEPENDENCIES ##################################
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

################################## FUNCTIONS ###################################

"""
Read in the DCCA CSV and format the dataframe
Parameters
----------
Returns
-------
"""


def get_dccm():
    df = pd.read_csv("cij.csv", index_col=None)
    df = df.iloc[:, 1:]
    df.columns = (x for x in range(1, len(df) + 1))
    df.index = (x for x in range(1, len(df) + 1))
    return df


"""
Takes the final dataframe and plots it according the the Kulik Group style
Parameters
----------
Returns
-------
"""


def get_plot(df):
    font = {"family": "sans-serif", "weight": "bold", "size": 18}
    plt.rc("font", **font)
    plt.rc("axes", linewidth=2.5)
    plt.rcParams["lines.linewidth"] = 2.5
    plt.rcParams["xtick.major.size"] = 10
    plt.rcParams["xtick.major.width"] = 2.5
    plt.rcParams["ytick.major.size"] = 10
    plt.rcParams["ytick.major.width"] = 2.5
    plt.rcParams["xtick.direction"] = "in"
    plt.rcParams["ytick.direction"] = "in"
    plt.rcParams["mathtext.default"] = "regular"
    plt.figure(figsize=(7, 7), linewidth=10)

    plt.imshow(df, cmap="seismic", vmax=1, vmin=-1)
    plt.colorbar(shrink=0.55)
    plt.ylabel("Residue Number", fontweight="bold")
    plt.xlabel("Residue Number", fontweight="bold")
    plt.xticks([1, 100, 200, 300, 400, 500, 600, 700])
    plt.yticks([1, 100, 200, 300, 400, 500, 600, 700])
    plt.savefig("dccm.pdf", bbox_inches="tight", dpi=300)
    plt.show()


"""
Takes the final dataframe and plots it according the the Kulik Group style
Parameters
----------
Returns
-------
"""


def dccm_plot_formattor():
    df = get_dccm()
    get_plot(df)


# Execute the DCCM Mapper function when run as a script
if __name__ == "__main__":
    dccm_plot_formattor()