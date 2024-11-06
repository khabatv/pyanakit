# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 09:33:13 2024

@author: past
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 

def load_data(file_path = None): 
    if file_path is None: 
        from gui import file_path as global_file_path 
        file_path = global_file_path
    data = pd.read_csv(file_path, sep="\t") 
    data = data.dropna()
    return data, file_path

def plot_clustermap(
        data,
        method = 'average', #guessed default value, original: cluster_method_var.get()
        cmap = 'viridis', #guessed default value, original: color_map_var.get()
        width = 10, 
        height = 8, 
        font_size = 1, 
        line_thickness = 0.1, 
        dendro_line_thickness = 0.5
        ):
      
    
    plt.clf()  # Clear the current figure
    sns.set(font_scale=font_size)  # Set the font size

    # Clean data: drop rows with NaN values
    #drop na in load_data(), because we can not test if data is proper cleaned, cause output is only a plot!
    #data = data.dropna()

    # Generate clustermap
    g = sns.clustermap(data.set_index('Accession'), method=method, metric='euclidean', cmap=cmap, cbar=True, 
                       figsize=(width, height), linewidths=line_thickness)
    
    # Adjust the line thickness of the dendrogram
    for d in g.ax_row_dendrogram.collections:
        d.set_linewidth(dendro_line_thickness)
    for d in g.ax_col_dendrogram.collections:
        d.set_linewidth(dendro_line_thickness)

    plt.title(f'Heatmap with Dendrogram (Method: {method}, Color Map: {cmap})', fontsize=font_size * 10)  # Adjust title font size
    plt.xlabel('Samples', fontsize=font_size * 8)  # Adjust x-label font size
    plt.ylabel('Features', fontsize=font_size * 8)  # Adjust y-label font size
    plt.tight_layout()  # Ensure the layout is adjusted
    plt.show()