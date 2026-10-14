"""

Main file for implementing data analysis on given datasets.
Script only (So far)
"""

# Import necessary libraries
import pandas as pd
import numpy as np
import utils.tools as tc
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
slope_vdb, intercept_vdb = np.polyfit(vdb_fit["FeH_vandenBerg"], vdb_fit["Age_vandenBerg"], 1)
print("Slope:", slope_vdb)
print("Intercept:", intercept_vdb)
# Create a new column for predicted age of each cluster based on the regression
vdb_fit["Age_predicted"] = (intercept_vdb + slope_vdb * vdb_fit["FeH_vandenBerg"])
# Calculate the residuals, which is actual age minus predicted age
vdb_fit["Residual"] = (vdb_fit["Age_vandenBerg"] - vdb_fit["Age_predicted"])

### This code here only does it for the Krause data. 
kr21_fit = DATASET[["FeH_Krause", "Age_Krause"]].dropna().copy()
# Generate a linear regression model - polynomial of degree 1
slope_kr21, intercept_kr21 = np.polyfit(kr21_fit["FeH_Krause"], kr21_fit["Age_Krause"], 1)
print("Slope:", slope_kr21)
print("Intercept:", intercept_kr21)
# Create a new column for predicted age of each cluster based on the regression
kr21_fit["Age_predicted"] = (intercept_kr21 + slope_kr21 * kr21_fit["FeH_Krause"])
# Calculate the residuals, which is actual age minus predicted age
kr21_fit["Residual"] = (kr21_fit["Age_Krause"] - kr21_fit["Age_predicted"])



# Age - FeH plot for Vandenberg and Krause datasets
fig, ax = plt.subplots(figsize=(PLOT_WIDTH, PLOT_HEIGHT))
sns.scatterplot(
    data=DATASET,
    x="FeH_vandenBerg",
    y="Age_vandenBerg",
    color="blue",
    label="Van den Berg",
    ax=ax,
)
ax.set(
    xlabel="FeH",
    ylabel="Age (Gyr)",
    title="Age vs FeH for Van den Berg and Krause Clusters",
)
sns.scatterplot(
    data=DATASET, x="FeH_Krause", y="Age_Krause", color="red", label="Krause", ax=ax
)

# Plot the linear regression fit for van den Berg data
x_line = np.sort(vdb_fit["FeH_vandenBerg"])
y_line = intercept_vdb + slope_vdb * x_line
ax.plot(x_line, y_line, color="blue", linestyle="--", label="van den Berg Linear Regression")

# Plot the linear regression fit for Krause data
x_line = np.sort(kr21_fit["FeH_Krause"])
y_line = intercept_kr21 + slope_kr21 * x_line
ax.plot(x_line, y_line, color="red", linestyle="--", label="Krause Linear Regression")

ax.legend()
plt.show()

# Plot systematic differences between the age measurements
fig, ax = plt.subplots(figsize=(PLOT_WIDTH, PLOT_HEIGHT))
sns.scatterplot(data=DATASET, x="Age_vandenBerg", y="Age_Krause", color="blue", ax=ax)
low_bound = min(DATASET["Age_vandenBerg"].min(), DATASET["Age_Krause"].min()) - 0.5
high_bound = max(DATASET["Age_vandenBerg"].max(), DATASET["Age_Krause"].max()) + 0.5
ax.axline(
    (0, 0), slope=1, color="red", linestyle="--", label="y=x"
)  # regression reference
ax.set(
    xlim=(low_bound, high_bound),
    ylim=(low_bound, high_bound),
    xlabel="Age van den Berg (Gyr)",
    ylabel="Age Krause (Gyr)",
    title="Age Comparison between van den Berg and Krause Clusters",
)
ax.legend()
plt.show()

# Plot systematic differences between the FeH measurements
fig, ax = plt.subplots(figsize=(PLOT_WIDTH, PLOT_HEIGHT))
sns.scatterplot(data=DATASET, x="FeH_vandenBerg", y="FeH_Krause", color="blue", ax=ax)

low_bound = min(DATASET["FeH_vandenBerg"].min(), DATASET["FeH_Krause"].min()) - 0.1
high_bound = max(DATASET["FeH_vandenBerg"].max(), DATASET["FeH_Krause"].max()) + 0.1

ax.axline((0, 0), slope=1, color="red", linestyle="--", label="y=x")
ax.set(
    xlim=(low_bound, high_bound),
    ylim=(low_bound, high_bound),
    xlabel="FeH van den Berg",
    ylabel="FeH Krause",
    title="FeH Comparison between van den Berg and Krause Clusters",
)
ax.legend()
plt.show()

# Normalised residuals for van den Berg data
n = len(vdb_fit)
# Divide by n - 2 as there are two estimated parameters. This is a standard statistical method. 
residual_sd = np.sqrt(np.sum(vdb_fit["Residual"] ** 2) / (n - 2))
vdb_fit["Standardised_Residual"] = (vdb_fit["Residual"] / residual_sd)
# Normalised residuals for Krause data
n = len(kr21_fit)
# Divide by n - 2 as there are two estimated parameters. This is a standard statistical method. 
residual_sd = np.sqrt(np.sum(kr21_fit["Residual"] ** 2) / (n - 2))
kr21_fit["Standardised_Residual"] = (kr21_fit["Residual"] / residual_sd)

### Plot standardised residuals with threshold lines. 
### Data points outside the orange lines are potential outliers. Points inside are unlikely to be outliers. 
fig, ax = plt.subplots(figsize=(PLOT_WIDTH, PLOT_HEIGHT))

sns.scatterplot(
    data=vdb_fit,
    x="Age_predicted",
    y="Standardised_Residual",
    color="blue",
    label="van den Berg",
    ax=ax
)

sns.scatterplot(
    data=kr21_fit,
    x="Age_predicted",
    y="Standardised_Residual",
    color="red",
    label="Krause",
    ax=ax
)

ax.axhline(0, color="black", linestyle="--")
ax.axhline(2, color="orange", linestyle=":")
ax.axhline(-2, color="orange", linestyle=":")
ax.axhline(3, color="red", linestyle=":")
ax.axhline(-3, color="red", linestyle=":")

ax.set(
    xlabel="Predicted age (Gyr)",
    ylabel="Standardised residual",
    title="Standardised Residuals: van den Berg and Krause"
)

ax.legend()
plt.show()

# Radial velocity (v_LSR and v_r) - Galactic longitude
fig, ax = plt.subplots(figsize=(PLOT_WIDTH, PLOT_HEIGHT))
sns.scatterplot(
    data=DATASET,
    x="L",
    y="v_LSR",
    color="blue",
    label="v_LSR",
    ax=ax,
)

sns.scatterplot(
    data=DATASET,
    x="L",
    y="v_r",
    color="red",
    label="v_r",
    ax=ax,
)

ax.set(
    xlabel="Galactic Longitude (deg)",
    ylabel="Radial Velocity (km/s)",
    title="Radial Velocity vs Galactic Longitude",
)

ax.legend()
plt.show()

# Radial velocity (v_LSR and v_r) - Galactocentric distance
fig, ax = plt.subplots(figsize=(PLOT_WIDTH, PLOT_HEIGHT))
sns.scatterplot(
    data=DATASET,
    x="R_gc",
    y="v_LSR",
    color="blue",
    label="v_LSR",
    ax=ax,
)

sns.scatterplot(
    data=DATASET,
    x="R_gc",
    y="v_r",
    color="red",
    label="v_r",
    ax=ax,
)

ax.set(
    xlabel="Galactocentric Distance (kpc)",
    ylabel="Radial Velocity (km/s)",
    title="Radial Velocity vs Galactocentric Distance",
)

ax.legend()
plt.show()

# Velocity dispersion - Mass
fig, ax = plt.subplots(figsize=(PLOT_WIDTH, PLOT_HEIGHT))
sns.scatterplot(
    data=DATASET,
    x="Mstar",
    y="sig_v",
    color="blue",
    #label="Velocity Dispersion",
    ax=ax,
)

ax.set(
    xlabel="Mass (M_sun)",
    ylabel="Velocity Dispersion (km/s)",
    title="Velocity Dispersion vs Mass",
)

#ax.legend()
plt.show()

# FeH - Galactocentric distance
fig, ax = plt.subplots(figsize=(PLOT_WIDTH, PLOT_HEIGHT))
sns.scatterplot(
    data=DATASET,
    x="R_gc",
    y="FeH_vandenBerg",
    color="blue",
    label="van den Berg",
    ax=ax,
)

sns.scatterplot(
    data=DATASET,
    x="R_gc",
    y="FeH_Krause",
    color="red",
    label="Krause",
    ax=ax,
)

ax.set(
    xlabel="Galactocentric Distance (kpc)",
    ylabel="[Fe/H]",
    title="[Fe/H] vs Galactocentric Distance",
)

ax.legend()
plt.show()


### TEST ###
# Plot of Age vs FeH for only Krause to identify two branches
fig, ax = plt.subplots(figsize=(PLOT_WIDTH, PLOT_HEIGHT))
# Plot with color representing Galactocentric distance as a nice way to visualize the data.
scatter = ax.scatter(
    data=DATASET,
    x="FeH_Krause",
    y="Age_Krause",
    c="R_gc",             # Color by distance
    cmap="flare",         # A nice sequential palette (darker/warmer = further out)
    s=50,                 # Size of points
    edgecolor="w",
    alpha=0.85,
    label="Krause Clusters"
)
# Add a colourbar to guide the reader on what the point colors mean
cbar = fig.colorbar(scatter, ax=ax)
cbar.set_label("Galactocentric Distance $R_{gc}$ (kpc)", rotation=270, labelpad=15)

ax.set(
    xlabel="Metallicity [Fe/H]",
    ylabel="Age (Gyr)",
    title="Krause Age-Metallicity Relation with Galactocentric Distance",
    #ylim=(7, 15)  # Constrain Y-axis to focus tightly on the clusters
)

ax.legend()
plt.show()

# Plot of Age vs FeH for only van den Berg to identify two branches
fig, ax = plt.subplots(figsize=(PLOT_WIDTH, PLOT_HEIGHT))
# Plot with color representing Galactocentric distance as a nice way to visualize the data.
scatter = ax.scatter(
    data=DATASET,
    x="FeH_vandenBerg",
    y="Age_vandenBerg",
    c="R_gc",             # Color by distance
    cmap="flare",         # A nice sequential palette (darker/warmer = further out)
    s=50,                 # Size of points
    edgecolor="w",
    alpha=0.85,
    label="van den Berg Clusters"
)
# Add a colourbar to guide the reader on what the point colors mean
cbar = fig.colorbar(scatter, ax=ax)
cbar.set_label("Galactocentric Distance $R_{gc}$ (kpc)", rotation=270, labelpad=15)

ax.set(
    xlabel="Metallicity [Fe/H]",
    ylabel="Age (Gyr)",
    title="van den Berg Age-Metallicity Relation with Galactocentric Distance",
    #ylim=(7, 15)  # Constrain Y-axis to focus tightly on the clusters
)

ax.legend()
plt.show()