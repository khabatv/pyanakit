# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:35:12 2024

@author: past
"""

#what utility functions should be here? 
#general helper functions 
#file/directory paths which directly belong to data processing oder visualisation 
#Logging and errormanagement
#configuration management 
  
from tkinter import StringVar

# Global variables to store data and file path
data = None
file_path = ""
file_path_var = None

# Initialize any necessary global variables for the GUI or data processing
def initialize_globals():
    global file_path_var
    file_path_var = StringVar()
