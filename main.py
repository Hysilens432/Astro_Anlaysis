'''
Main file for implementing data analysis on given datasets.
Script only (So far)
'''


# Import necessary libraries
import pandas as pd
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
#print(HarrisPartI.head())
#print(HarrisPartI.info())


