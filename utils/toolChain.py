"""
This utility module provides essential tools for use at main.py.
"""

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

"""
PLOT HELPER FUNCTIONS 
"""


def plot_scatter(
    dataset,
    *,
    x,
    y,
    color,
    colorbar_label,
    xlabel,
    ylabel,
    label=None,
    title,
    filename,
    xscale,
    PLOT_WIDTH,
    PLOT_HEIGHT
):
    fig, ax = plt.subplots(figsize=(PLOT_WIDTH, PLOT_HEIGHT))
    scatter = ax.scatter(
        data=dataset,
        x=x,
        y=y,
        c=color,
        cmap="flare",
        s=50,
        edgecolor="w",
        alpha=0.85,
    )
    colorbar = fig.colorbar(scatter, ax=ax)
    colorbar.set_label(colorbar_label, rotation=270, labelpad=15)
    ax.set(
        xlabel=xlabel,
        ylabel=ylabel,
        title=title,
        xscale=xscale,
    )

    output_path = Path("./output") / filename
    fig.savefig(output_path)
    plt.close(fig)


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
