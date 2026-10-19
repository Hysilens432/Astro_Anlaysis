"""
This utility module provides essential tools for use at main.py.
"""

import os
import pandas as pd
import numpy as np
import seaborn as sns

"""
PLOT HELPER FUNCTIONS 
"""


"""
OTHER HELPER FUNCTIONS
"""


def csv_import(path):
    """
    Reads CSV files and returns them as pandas DataFrame objects.
    Input: path (str): The file path to the CSV file.
    Output: pandas.DataFrame: The DataFrame containing the CSV data.
    """
    if not path.endswith(".csv"):
        raise ValueError("The provided path does not point to a CSV file")
    elif not os.path.exists(path):
        raise ValueError("The file path does not exist")
    return pd.read_csv(path)
