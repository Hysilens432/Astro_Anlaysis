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


# Age - FeH plot for Vandenberg and Krause datasets
fig, ax = plt.subplots(figsize=(PLOT_WIDTH, PLOT_HEIGHT))
sns.scatterplot(
    data=DATASET,
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
    data=DATASET, x="FeH_Krause", y="Age_Krause", color="red", label="Krause", ax=ax
)
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
