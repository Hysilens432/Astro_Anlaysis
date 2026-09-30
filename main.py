'''

Main file for implementing data analysis on given datasets.
Script only (So far)
'''

# Import necessary libraries
import pandas as pd
import numpy as np
from utils.csv_import import csv_import
import matplotlib.pyplot as plt
import seaborn as sns

# Constants 
HARRIS_I = "./dataset/HarrisPartI.csv"
HARRIS_III = "./dataset/HarrisPartIII.csv"
KRAUSE_21 = "./dataset/Krause21.csv"
VANDENBERG_TABLE2 = "./dataset/vandenBerg_table2.csv"

# Read the csv files into dataframes
HarrisPartI = csv_import(HARRIS_I)
HarrisPartIII = csv_import(HARRIS_III)
Krause21 = csv_import(KRAUSE_21)
vandenBerg_table2 = csv_import(VANDENBERG_TABLE2)

# These are the columns in the raw dataframes that contain the clusters identifiers. 
#print(HarrisPartI["ID"])
#print(HarrisPartIII["ID"])
#print(Krause21["Object"])
#print(vandenBerg_table2["#NGC"])

# Create unified Cluster_ID column in each dataframe to easily compare which clusters
# exist across all datasets. 
#HarrisPartI_test = HarrisPartI.copy()
HarrisPartI["Cluster_ID"] = HarrisPartI["ID"].str.replace(" ", "")
#print(HarrisPartI_test.head())

#HarrisPartIII_test = HarrisPartIII.copy()
HarrisPartIII["Cluster_ID"] = HarrisPartIII["ID"].str.replace(" ", "")
#print(HarrisPartIII_test.head())

#Krause21_test = Krause21.copy()
Krause21["Cluster_ID"] = Krause21["Object"].str.replace(" ", "")
#print(Krause21_test.head())

#vandenBerg_table2_test = vandenBerg_table2.copy()
vandenBerg_table2["Cluster_ID"] = "NGC" + vandenBerg_table2["#NGC"].astype(str)
#print(vandenBerg_table2_test.head())

# Check for duplucated Cluster_IDs in each dataframe.
print("HarrisPartI_test duplicated Cluster_IDs: ", HarrisPartI["Cluster_ID"].duplicated().sum())
print("HarrisPartIII_test duplicated Cluster_IDs: ", HarrisPartIII["Cluster_ID"].duplicated().sum())
print("Krause21_test duplicated Cluster_IDs: ", Krause21["Cluster_ID"].duplicated().sum())
print("vandenBerg_table2_test duplicated Cluster_IDs: ", vandenBerg_table2["Cluster_ID"].duplicated().sum())

#### vandenBerg_table2 has three duplicate IDs. The bottom three entries have no numbers.
#### They are saved as NGCXXXX. They should be removed when we merge in the next step. 

# Rename Age and FeH columns to include which dataset they came from. 
vandenBerg_table2 = vandenBerg_table2.rename(columns={"Age": "Age_vandenBerg", "FeH": "FeH_vandenBerg"})
Krause21 = Krause21.rename(columns={"Age": "Age_Krause", "FeH": "FeH_Krause"})
print(vandenBerg_table2.head())
print(Krause21.head())

# Merge into one combined dateframe keeping all the columns. 
# merge uses inner by default. Only combines rows with matching Cluster_IDs. 
combined = pd.merge(HarrisPartI, HarrisPartIII, on="Cluster_ID")
print(combined.shape) #(157, 25)
combined = pd.merge(combined, Krause21, on="Cluster_ID")
print(combined.shape) #(59, 33)
combined = pd.merge(combined, vandenBerg_table2, on="Cluster_ID")
print(combined.shape) #(51, 46)

#### After merging, there are 51 clusters that appear in all four datasets. 
print(combined.columns)

# Plot of Age vs FeH on the combined dataset for the both the vandenBerg and Krausedata
plt.figure(1, figsize=(10, 6))
plt.scatter(combined["FeH_vandenBerg"], combined["Age_vandenBerg"], color='blue', label='vandenBerg')
plt.scatter(combined["FeH_Krause"], combined["Age_Krause"], color='red', label='Krause')
plt.xlabel("FeH")
plt.ylabel("Age (Gyr)")
plt.title("Age vs FeH for van den Berg and Krause Clusters")
plt.legend()
plt.show()


# Look at systematic differences between the age measurements in the Krause and vandenBerg datasets. 
plt.figure(2, figsize=(10, 6))
plt.scatter(combined["Age_vandenBerg"], combined["Age_Krause"], color='blue')
# Add line y=x to see if the points are systematically above or below the line.
low_bound = min(combined["Age_vandenBerg"].min(), combined["Age_Krause"].min()) - 0.5
high_bound = max(combined["Age_vandenBerg"].max(), combined["Age_Krause"].max()) + 0.5
plt.axline((0, 0), slope=1, color='red', linestyle='--', label='y=x')
plt.xlim(low_bound, high_bound)
plt.ylim(low_bound, high_bound)
plt.xlabel("Age van den Berg (Gyr)")
plt.ylabel("Age Krause (Gyr)")
plt.title("Age Comparison between van den Berg and Krause Clusters")
plt.legend()
plt.show()

# Look at systematic differences between the FeH measurements in the Krause and vandenBerg datasets. 
plt.figure(3, figsize=(10, 6))
plt.scatter(combined["FeH_vandenBerg"], combined["FeH_Krause"], color='blue')
# Add line y=x to see if the points are systematically above or below the line.
low_bound = min(combined["FeH_vandenBerg"].min(), combined["FeH_Krause"].min()) - 0.1
high_bound = max(combined["FeH_vandenBerg"].max(), combined["FeH_Krause"].max()) + 0.1
plt.axline((0, 0), slope=1, color='red', linestyle='--', label='y=x')
plt.xlim(low_bound, high_bound)
plt.ylim(low_bound, high_bound)
plt.xlabel("FeH van den Berg")
plt.ylabel("FeH Krause")
plt.title("FeH Comparison between van den Berg and Krause Clusters")
plt.legend()
plt.show()