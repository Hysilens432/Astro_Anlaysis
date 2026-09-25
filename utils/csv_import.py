'''
This utility module reads CSV files and returns
them as pandas DataFrame objects.
    Input: path (str): The file path to the CSV file.
    Output: pandas.DataFrame: The DataFrame containing the CSV data.
'''

import os 
import pandas as pd

def csv_import(path):
    '''
    Perform Path Validation,
    Import CSV file as dataframes, return the
    data frame object corresponding to the CSV file at the given path.
    '''
    if not path.endswith('.csv'):
        raise ValueError("The provided path does not point to a CSV dataset")
    elif not os.path.exists(path):
        raise ValueError("The file path does not exist")
    return pd.read_csv(path)
 