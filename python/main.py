"""

For PHYS3116 Computational Assessment
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import utils.toolChain as tc
import utils.plots as plots
import matplotlib.pyplot as plt
import seaborn as sns

# Constants
HARRIS_I = "./dataset/HarrisPartI.csv"
HARRIS_III = "./dataset/HarrisPartIII.csv"
KRAUSE_21 = "./dataset/Krause21.csv"
VDB = "./dataset/vandenBerg_table2.csv"
PLOT_WIDTH = 10
PLOT_HEIGHT = 6

# Settings
sns.set_theme(context="paper", palette="pastel", style="whitegrid")

# Read the csv files into dataframes
harI = tc.csv_import(HARRIS_I)
harIII = tc.csv_import(HARRIS_III)
kr21 = tc.csv_import(KRAUSE_21)
vdb = tc.csv_import(VDB)


harI["Cluster_ID"] = harI["ID"].str.replace(" ", "")
harIII["Cluster_ID"] = harIII["ID"].str.replace(" ", "")
kr21["Cluster_ID"] = kr21["Object"].str.replace(" ", "")
vdb["Cluster_ID"] = "NGC" + vdb["#NGC"].astype(str)

# Rename Age and FeH columns to include which dataset they came from.
vdb = vdb.rename(columns={"Age": "Age_vandenBerg", "FeH": "FeH_vandenBerg"})
kr21 = kr21.rename(columns={"Age": "Age_Krause", "FeH": "FeH_Krause"})
#print(vdb.head())
#print(kr21.head())

# Note: I simplified merge here. dataset should be constant unless wee wanna change it.
dataset = (
    pd.merge(harI, harIII, on="Cluster_ID")
    .merge(kr21, on="Cluster_ID")
    .merge(vdb, on="Cluster_ID")
)

plots.run_plots(dataset, PLOT_WIDTH, PLOT_HEIGHT)

#### Identify potential acretted clusters ####

# Velocity  dispersion - Mass relation plot. Specifically, these have very high velocity dispersions for their mass,
diffuse_candidates = dataset[(dataset["sig_v"] > 10)]
print("Potentially accreted clusters based on velocity dispersion and mass:")
print(diffuse_candidates[["Cluster_ID", "sig_v", "Mstar"]])

# Metallicity - Galactocentric distance plot. Specifically, these are metal-rich clusters that are far from the galactic center.
metallicity_candidates = dataset[
    (dataset["FeH_Krause"] > -1.3) & (dataset["R_gc"] > 15)
]
print("Potentially accreted clusters based on metallicity and galactocentric distance:")
print(metallicity_candidates[["Cluster_ID", "FeH_Krause", "R_gc"]])

# Age - Metallicity plot for Krause data. These follow the lower track on the plot.
age_metallicity_candidates = dataset[(dataset["Age_Krause"] < 12)]
print("Potentially accreted clusters based on age and metallicity:")
print(age_metallicity_candidates[["Cluster_ID", "Age_Krause", "FeH_Krause"]])

# Radial velocity - Galactocentric distance plot. These are clusters with high radial velocities that are far from the galactic center.
radial_velocity_candidates = dataset[
    (dataset["v_LSR"] > 300) | (dataset["v_LSR"] < -300) | ((dataset["R_gc"] > 8) & (dataset["R_gc"] < 12) & (dataset["FeH_Krause"] < 1.6) & (dataset["v_LSR"] > -200) & (dataset["v_LSR"] < 0))
]
print("Potentially accreted clusters based on radial velocity and galactocentric distance:")
print(radial_velocity_candidates[["Cluster_ID", "v_LSR", "R_gc"]])

# Core relaxation time - galactocentric distance plot. These are clusters with long core relaxation times that are far from the galactic center.
relaxation_time_candidates = dataset[
    ((dataset["lg_tc"] < 6.7) & (dataset["R_gc"] > 5) & (dataset["R_gc"] < 7.5)) | ((dataset["lg_tc"] < 8) & (dataset["R_gc"] > 15))
]
print("Potentially accreted clusters based on core relaxation time and galactocentric distance:")
print(relaxation_time_candidates[["Cluster_ID", "lg_tc", "R_gc"]])

# Half light radius - Galactocentric distance plot. These are clusters with large half-light radii that are far from the galactic center.
half_light_radius_candidates = dataset[
    (dataset["r_h"] > 4) | ((dataset["R_gc"] > 8) & (dataset["R_gc"] < 11.5) & (dataset["FeH_Krause"] < -1.8))
]
print("Potentially accreted clusters based on half-light radius and galactocentric distance:")
print(half_light_radius_candidates[["Cluster_ID", "r_h", "R_gc"]])

# Concentration - velocity dispersion plot. These are clusters with low concentration and high velocity dispersions.
concentration_candidates = dataset[
    (dataset["c"] < 0.85) | (dataset["sig_v"] > 12) | (dataset["c"] == 2.5)
]
print("Potentially accreted clusters based on concentration and velocity dispersion:")
print(concentration_candidates[["Cluster_ID", "c", "sig_v"]])


# Identify clusters that appear at least twice in the above lists.
all_candidates = pd.concat(
    [
        diffuse_candidates[["Cluster_ID"]],
        metallicity_candidates[["Cluster_ID"]],
        age_metallicity_candidates[["Cluster_ID"]],
        radial_velocity_candidates[["Cluster_ID"]],
        relaxation_time_candidates[["Cluster_ID"]],
        half_light_radius_candidates[["Cluster_ID"]],
        concentration_candidates[["Cluster_ID"]],
    ]
)

id_counts = all_candidates["Cluster_ID"].value_counts()

# Filter the dataset to only include clusters that appear in at least two of the above criteria.
repeated_candidates = id_counts[id_counts > 1].index
shortlist = dataset[dataset["Cluster_ID"].isin(repeated_candidates)]

# Add a 'Count' column using the id_counts series
shortlist["Count"] = shortlist["Cluster_ID"].map(id_counts)

# Print the shortlist of clusters that appear in at least two of the above criteria.
print("Clusters that appear in at least two of the above criteria:")
print(
    shortlist[
        ["Cluster_ID", "Count", "sig_v", "Mstar", "FeH_Krause", "R_gc", "Age_Krause", "v_LSR"]
    ]
)

