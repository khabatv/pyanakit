# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:35:12 2024

@author: past
"""

#general helper functions 
#file/directory paths which directly belong to data processing or visualisation 
#Logging and errormanagement
#configuration management 

import pandas as pd
from tkinter import filedialog

def load_clean(file_path):
    if not file_path:
        raise ValueError("File path is required.")

    # checking 
    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    elif file_path.endswith('.txt'):
        data = pd.read_table(file_path)
    else:
        raise ValueError("Unsupported file format")

    #clean data 
    data = data.dropna()
    return data

def select_file_path():
    return filedialog.askopenfilename(
        title="Select the input table",
        filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")]
    )

