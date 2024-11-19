# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:32:21 2024

@author: past
"""

from tkinter import Tk, Label, Button, StringVar, OptionMenu, LabelFrame, messagebox
from data_processing import process_data
from pca_analysis import perform_pca
from clustermap_analysis import plot_clustermap
from utils import select_file_path, load_clean

def select_file():
    global file_path, loaded_data
    file_path = select_file_path() 
    
    if file_path:
        file_path_var.set(file_path)  # Update displayed file path
        loaded_data = load_clean(file_path)
        if loaded_data is None: 
            print("Failed to load data.")

#create window 
root = Tk()
root.title("Data Analysis Tool")
root.geometry("600x300")
#set default values
file_path_var = StringVar()
plot_type_var = StringVar(value="Violin Plot")  # Default plot type
treatment_var = StringVar(value="Treatment2")  # Default treatment to compare
cluster_method_var = StringVar(value="average")  # Default clustering method
color_map_var = StringVar(value="viridis")  # Default color map

def process_data_from_gui():
    global loaded_data
    # Überprüfen, ob die Datei geladen wurde
    if 'loaded_data' not in globals() or loaded_data is None:
        messagebox.showerror("Error", "Please select a file before processing data.")
        return  # Funktion abbrechen, falls keine Datei geladen ist
    else: 
        process_data(data=loaded_data, plot_type=plot_type_var.get(), treatment_to_compare=treatment_var.get())
    
def pca_analysis_from_gui(): 
    global loaded_data
    # Überprüfen, ob die Datei geladen wurde
    if 'loaded_data' not in globals() or loaded_data is None:
        messagebox.showerror("Error", "Please select a file before processing data.")
        return  # Funktion abbrechen, falls keine Datei geladen ist
    else:
        perform_pca(data=loaded_data)
        
def plot_clustermap_from_gui():
    global loaded_data
    # Überprüfen, ob die Datei geladen wurde
    if 'loaded_data' not in globals() or loaded_data is None:
        messagebox.showerror("Error", "Please select a file before processing data.")
        return  # Funktion abbrechen, falls keine Datei geladen ist
    else:
        plot_clustermap(data=loaded_data)
    
#ensure realtiv window and elementsize 
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)
root.grid_columnconfigure(2, weight=1)

# Create UI elements
label = Label(root, text="Selected file:")
label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

file_path_entry = Label(root, textvariable=file_path_var, wraplength=400, bg ="ghostwhite")
file_path_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='ew')

select_file_button = Button(root, text="Select File", command=select_file)
select_file_button.grid(row=1, column=2, padx=5, pady=5, sticky='e')

# Label and dropdown menu for plot types
plot_type_label = Label(root, text="Select Plot Type:")
plot_type_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')

plot_type_menu = OptionMenu(root, plot_type_var, 
                             "Violin Plot", 
                             "Box Plot", 
                             "Bar Plot", 
                             #"Scatter Plot", 
                             "Line Plot", 
                             #"Strip Plot", 
                             "Histogram", 
                             "Swarm Plot", 
                             "Heatmap")  
plot_type_menu.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='ew')

# Label and dropdown menu for selecting treatment to compare
treatment_label = Label(root, text="Select Treatment to Compare:")
treatment_label.grid(row=3, column=0, padx=5, pady=5, sticky='w') 

treatment_menu = OptionMenu(root, treatment_var, "Treatment1", "Treatment2")
treatment_menu.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky='ew')

# Button to process data and generate plots
process_button = Button(root, text="Process Data and Generate Plots", command=process_data_from_gui)
process_button.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky='ew')  

#Labelframe for visual seperation of PCA and Clustermap 
label_frame = LabelFrame(root, text = "Advanced insights:", labelanchor = "nw")
label_frame.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky='ew') 
label_frame.columnconfigure(0, weight=1)  
label_frame.columnconfigure(1, weight=1)  

# Button to plot Clustermap
clustermap_button = Button(label_frame, text="Plot Clustermap", command=plot_clustermap_from_gui)
clustermap_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew') 

# Button to perform PCA
pca_button = Button(label_frame, text="Perform PCA", command=pca_analysis_from_gui)
pca_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew') 

# Start the GUI
root.mainloop()