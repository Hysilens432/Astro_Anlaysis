"""

For PHYS3116 Computational Assessment
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import utils.toolChain as tc
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
print(vdb.head())
print(kr21.head())

# Note: I simplified merge here. DATASET should be constant unless wee wanna change it.
DATASET = (
    pd.merge(harI, harIII, on="Cluster_ID")
    .merge(kr21, on="Cluster_ID")
    .merge(vdb, on="Cluster_ID")
)


### To investigate potential outliers, create a residuals plot for the Age vs FeH relationship.
### The code here creates a small dataset and a linear regression model.
### This code here only does it for the van den Berg data.
vdb_fit = DATASET[["FeH_vandenBerg", "Age_vandenBerg"]].dropna().copy()
# Generate a linear regression model - polynomial of degree 1
slope_vdb, intercept_vdb = np.polyfit(
    vdb_fit["FeH_vandenBerg"], vdb_fit["Age_vandenBerg"], 1
)
print("Slope:", slope_vdb)
print("Intercept:", intercept_vdb)
# Create a new column for predicted age of each cluster based on the regression
vdb_fit["Age_predicted"] = intercept_vdb + slope_vdb * vdb_fit["FeH_vandenBerg"]
# Calculate the residuals, which is actual age minus predicted age
vdb_fit["Residual"] = vdb_fit["Age_vandenBerg"] - vdb_fit["Age_predicted"]

### This code here only does it for the Krause data.
kr21_fit = DATASET[["FeH_Krause", "Age_Krause"]].dropna().copy()
# Generate a linear regression model - polynomial of degree 1
slope_kr21, intercept_kr21 = np.polyfit(
    kr21_fit["FeH_Krause"], kr21_fit["Age_Krause"], 1
)
print("Slope:", slope_kr21)
print("Intercept:", intercept_kr21)
# Create a new column for predicted age of each cluster based on the regression
kr21_fit["Age_predicted"] = intercept_kr21 + slope_kr21 * kr21_fit["FeH_Krause"]
# Calculate the residuals, which is actual age minus predicted age
kr21_fit["Residual"] = kr21_fit["Age_Krause"] - kr21_fit["Age_predicted"]


# Normalised residuals for van den Berg data
n = len(vdb_fit)
# Divide by n - 2 as there are two estimated parameters. This is a standard statistical method.
residual_sd = np.sqrt(np.sum(vdb_fit["Residual"] ** 2) / (n - 2))
vdb_fit["Standardised_Residual"] = vdb_fit["Residual"] / residual_sd
# Normalised residuals for Krause data
n = len(kr21_fit)
# Divide by n - 2 as there are two estimated parameters. This is a standard statistical method.
residual_sd = np.sqrt(np.sum(kr21_fit["Residual"] ** 2) / (n - 2))
kr21_fit["Standardised_Residual"] = kr21_fit["Residual"] / residual_sd

# Velocity dispersion - Mass. Added colour coding with half light radius.
tc.plot_scatter(
    dataset=DATASET,
    x="Mstar",
    y="sig_v",
    color="r_h",
    colorbar_label="Half light radius (pc)",
    xlabel="log(Mass) (log(M_sun))",
    ylabel="Velocity Dispersion (km/s)",
    title="Velocity Dispersion-Mass Relation with Half Light Radius",
    filename="mstar_v_sigv.png",
    xscale="log",
    PLOT_WIDTH=PLOT_WIDTH,
    PLOT_HEIGHT=PLOT_HEIGHT,
)

# FeH - Galactocentric distance, coloured by age.
tc.plot_scatter(
    dataset=DATASET,
    x="R_gc",
    y="FeH_Krause",
    color="Age_Krause",
    colorbar_label="Age (Gyr)",
    xlabel="Galactocentric Distance (kpc)",
    ylabel="Metallicity [Fe/H]",
    title="Metallicity-Galactocentric Distance with Age for Krause Clusters",
    filename="feh_rgc_age.png",
    xscale="linear",
    PLOT_WIDTH=PLOT_WIDTH,
    PLOT_HEIGHT=PLOT_HEIGHT,
)

# Plot of Age vs FeH for only Krause to identify two branches. Coloured by Galactocentric distance.
# Plot with color representing Galactocentric distance as a nice way to visualize the data.
tc.plot_scatter(
    dataset=DATASET,
    x="FeH_Krause",
    y="Age_Krause",
    color="R_gc",
    colorbar_label="Galactocentric Distance $R_{gc}$ (kpc)",
    label="Krause Clusters",
    filename="krause_age_feh.png",
    xscale="linear",
    PLOT_WIDTH=PLOT_WIDTH,
    PLOT_HEIGHT=PLOT_HEIGHT,
)


# Plot of Age vs FeH for only van den Berg to identify two branches. Coloured by Galactocentric distance.rg Clusters",
tc.plot_scatter(
    dataset=DATASET,
    x="FeH_vandenBerg",
    y="Age_vandenBerg",
    color="R_gc",
    colorbar_label="Galactocentric Distance $R_{gc}$ (kpc)",
    xlabel="Metallicity [Fe/H]",
    ylabel="Age (Gyr)",
    title="van den Berg Age-Metallicity Relation with Galactocentric Distance",
    filename="vandenberg_age_feh.png",
    xscale="linear",
    PLOT_WIDTH=PLOT_WIDTH,
    PLOT_HEIGHT=PLOT_HEIGHT,
)


#### Identify potential acretted clusters ####
# These are rough criteria for now. We will need to adjust them as we go. This was just a first pass to potentially identify some clusters.

# Velocity  dispersion - Mass relation plot. Specifically, these have very high velocity dispersions for their mass,
diffuse_candidates = DATASET[(DATASET["sig_v"] > 10)]
print("Potentially accreted clusters based on velocity dispersion and mass:")
print(diffuse_candidates[["Cluster_ID", "sig_v", "Mstar"]])

# Metallicity - Galactocentric distance plot. Specifically, these are metal-rich clusters that are far from the galactic center.
metallicity_candidates = DATASET[
    (DATASET["FeH_Krause"] > -1.3) & (DATASET["R_gc"] > 15)
]
print("Potentially accreted clusters based on metallicity and galactocentric distance:")
print(metallicity_candidates[["Cluster_ID", "FeH_Krause", "R_gc"]])

# Age - Metallicity plot for Krause data. These follow the lower track on the plot.
age_metallicity_candidates = DATASET[(DATASET["Age_Krause"] < 12)]
print("Potentially accreted clusters based on age and metallicity:")
print(age_metallicity_candidates[["Cluster_ID", "Age_Krause", "FeH_Krause"]])

# Radial velocity - Galactocentric distance plot. These are clusters with high radial velocities that are far from the galactic center.
radial_velocity_candidates = DATASET[
    (DATASET["v_LSR"] > 300) | (DATASET["v_LSR"] < -300)
]
print(
    "Potentially accreted clusters based on radial velocity and galactocentric distance:"
)
print(radial_velocity_candidates[["Cluster_ID", "v_LSR", "R_gc"]])

# Identify clusters that appear at least twice in the above lists.
all_candidates = pd.concat(
    [
        diffuse_candidates[["Cluster_ID"]],
        metallicity_candidates[["Cluster_ID"]],
        age_metallicity_candidates[["Cluster_ID"]],
        radial_velocity_candidates[["Cluster_ID"]],
    ]
)

id_counts = all_candidates["Cluster_ID"].value_counts()
repeated_candidates = id_counts[id_counts > 1].index
shortlist = DATASET[DATASET["Cluster_ID"].isin(repeated_candidates)]
print("Clusters that appear in at least two of the above criteria:")
print(
    shortlist[
        ["Cluster_ID", "sig_v", "Mstar", "FeH_Krause", "R_gc", "Age_Krause", "v_LSR"]
    ]
)
