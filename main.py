"""

Main file for implementing data analysis on given datasets.
Script only (So far)
"""

# Import necessary libraries
import pandas as pd
import numpy as np
from utils.tools import csv_import
import matplotlib.pyplot as plt
import seaborn as sns

# Constants
HARRIS_I = "./dataset/HarrisPartI.csv"
HARRIS_III = "./dataset/HarrisPartIII.csv"
KRAUSE_21 = "./dataset/Krause21.csv"
VANDENBERG_TABLE2 = "./dataset/vandenBerg_table2.csv"
PLOT_WIDTH = 10
PLOT_HEIGHT = 6

# Settings
sns.set_theme(context="paper", palette="pastel", style="whitegrid")

# Read the csv files into dataframes
HarrisPartI = csv_import(HARRIS_I)
HarrisPartIII = csv_import(HARRIS_III)
Krause21 = csv_import(KRAUSE_21)
vandenBerg_table2 = csv_import(VANDENBERG_TABLE2)

# These are the columns in the raw dataframes that contain the clusters identifiers.
# print(HarrisPartI["ID"])
# print(HarrisPartIII["ID"])
# print(Krause21["Object"])
# print(vandenBerg_table2["#NGC"])

# Create unified Cluster_ID column in each dataframe to easily compare which clusters
# exist across all datasets.
# HarrisPartI_test = HarrisPartI.copy()
HarrisPartI["Cluster_ID"] = HarrisPartI["ID"].str.replace(" ", "")
# print(HarrisPartI_test.head())

# HarrisPartIII_test = HarrisPartIII.copy()
HarrisPartIII["Cluster_ID"] = HarrisPartIII["ID"].str.replace(" ", "")
# print(HarrisPartIII_test.head())

# Krause21_test = Krause21.copy()
Krause21["Cluster_ID"] = Krause21["Object"].str.replace(" ", "")
# print(Krause21_test.head())

# vandenBerg_table2_test = vandenBerg_table2.copy()
vandenBerg_table2["Cluster_ID"] = "NGC" + vandenBerg_table2["#NGC"].astype(str)
# print(vandenBerg_table2_test.head())

# Check for duplucated Cluster_IDs in each dataframe.
print(
    "HarrisPartI_test duplicated Cluster_IDs: ",
    HarrisPartI["Cluster_ID"].duplicated().sum(),
)
print(
    "HarrisPartIII_test duplicated Cluster_IDs: ",
    HarrisPartIII["Cluster_ID"].duplicated().sum(),
)
print(
    "Krause21_test duplicated Cluster_IDs: ", Krause21["Cluster_ID"].duplicated().sum()
)
print(
    "vandenBerg_table2_test duplicated Cluster_IDs: ",
    vandenBerg_table2["Cluster_ID"].duplicated().sum(),
)

#### vandenBerg_table2 has three duplicate IDs. The bottom three entries have no numbers.
#### They are saved as NGCXXXX. They should be removed when we merge in the next step.

# Rename Age and FeH columns to include which dataset they came from.
vandenBerg_table2 = vandenBerg_table2.rename(
    columns={"Age": "Age_vandenBerg", "FeH": "FeH_vandenBerg"}
)
Krause21 = Krause21.rename(columns={"Age": "Age_Krause", "FeH": "FeH_Krause"})
print(vandenBerg_table2.head())
print(Krause21.head())

"""
# Merge into one combined dateframe keeping all the columns.
# merge uses inner by default. Only combines rows with matching Cluster_IDs.
combined = pd.merge(HarrisPartI, HarrisPartIII, on="Cluster_ID")
print(combined.shape)  # (157, 25)
combined = pd.merge(combined, Krause21, on="Cluster_ID")
print(combined.shape)  # (59, 33)
combined = pd.merge(combined, vandenBerg_table2, on="Cluster_ID")
print(combined.shape)  # (51, 46)

#### After merging, there are 51 clusters that appear in all four datasets.
print(combined.columns.duplicated().sum())
"""

# Note: I simplified merge here. DATASET should be constant unless wee wanna change it.
DATASET = (
    pd.merge(HarrisPartI, HarrisPartIII, on="Cluster_ID")
    .merge(Krause21, on="Cluster_ID")
    .merge(vandenBerg_table2, on="Cluster_ID")
)

# Age - FeH plot for Vandenberg and Krause datasets
fig, ax = plt.subplots(figsize=(PLOT_WIDTH, PLOT_HEIGHT))
sns.scatterplot(
    data=combined,
    x="FeH_vandenBerg",
    y="Age_vandenBerg",
    color="blue",
    label="Van den Bergh",
    ax=ax,
)
ax.set(
    xlabel="FeH",
    ylabel="Age (Gyr)",
    title="Age vs FeH for Van den Bergh and Krause Clusters",
)
sns.scatterplot(
    data=combined, x="FeH_Krause", y="Age_Krause", color="red", label="Krause", ax=ax
)
ax.legend()
plt.show()

# Plot systematic differences between the age measurements
fig, ax = plt.subplots(figsize=(PLOT_WIDTH, PLOT_HEIGHT))
sns.scatterplot(data=combined, x="Age_vandenBerg", y="Age_Krause", color="blue", ax=ax)
low_bound = min(combined["Age_vandenBerg"].min(), combined["Age_Krause"].min()) - 0.5
high_bound = max(combined["Age_vandenBerg"].max(), combined["Age_Krause"].max()) + 0.5
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
sns.scatterplot(data=combined, x="FeH_vandenBerg", y="FeH_Krause", color="blue", ax=ax)

low_bound = min(combined["FeH_vandenBerg"].min(), combined["FeH_Krause"].min()) - 0.1
high_bound = max(combined["FeH_vandenBerg"].max(), combined["FeH_Krause"].max()) + 0.1

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
