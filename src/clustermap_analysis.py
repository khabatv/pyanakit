# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 09:33:13 2024

@author: past
"""
import matplotlib.pyplot as plt
import seaborn as sns

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
    sns.set(font_scale=font_size)

    # Generate clustermap
    g = sns.clustermap(data.set_index('Accession'), method=method, metric='euclidean', cmap=cmap, cbar=True, 
                       figsize=(width, height), linewidths=line_thickness)
    
    # Adjust the line thickness of the dendrogram
    for d in g.ax_row_dendrogram.collections:
        d.set_linewidth(dendro_line_thickness)
    for d in g.ax_col_dendrogram.collections:
        d.set_linewidth(dendro_line_thickness)
    
    #plotting 
    plt.title(f'Heatmap with Dendrogram (Method: {method}, Color Map: {cmap})', fontsize=font_size * 10)
    plt.xlabel('Samples', fontsize=font_size * 8)  
    plt.ylabel('Features', fontsize=font_size * 8) 
    plt.tight_layout()
    plt.show()