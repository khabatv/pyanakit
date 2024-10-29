# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 09:33:13 2024

@author: past
"""
import matplotlib_inline.pyplot as plt
import seaborn as sns


def plot_clustermap(data, method, cmap, width, height, font_size, line_thickness, dendro_line_thickness):
    plt.clf()  # Clear the current figure
    sns.set(font_scale=font_size)  # Set the font size

    # Clean data: drop rows with NaN values
    data = data.dropna()

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