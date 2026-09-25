# Constants 
HARRIS_I = "./dataset/HarrisPartI.csv"
HARRIS_III = "./dataset/HarrisPartIII.csv"
KRAUSE_21 = "./dataset/Krause21.csv"
VANDENBERG_TABLE2 = "./dataset/vandenBerg_table2.csv"

import pandas as pd

# Read the csv files into dataframes
HarrisPartI = pd.read_csv(HARRIS_I)
HarrisPartIII = pd.read_csv(HARRIS_III)
Krause21 = pd.read_csv(KRAUSE_21)
vandenBerg_table2 = pd.read_csv(VANDENBERG_TABLE2)
#print(HarrisPartI.head())
#print(HarrisPartI.info())


