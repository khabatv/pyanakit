# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:33:52 2024

@author: past
"""

#plotting graphs 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

    #Info aus dem process_data modul
    #plot_type = plot_type_var.get()
    # Select treatment to compare (Treatment1 or Treatment2)
    #treatment_to_compare = treatment_var.get()
    # Generate selected plot type
    #plt.figure(figsize=(12, 6))
plt.figure(figsize=(12,6))

#funktioniert das mit dem dem treatment to compare und dem Value argumenten? 
def plot_violin(data, treatment_to_compare, y_column):
    sns.violinplot(x=treatment_to_compare, y='Value', data=data, inner=None)
    overlay_data_points_and_error_bars(data, treatment_to_compare)
    
def plot_bar(data, treatment_to_compare, y_column, ci=None):
    sns.boxplot(x=treatment_to_compare, y='Value', data=data)
    overlay_data_points_and_error_bars(data, treatment_to_compare)
    
def plot_bar(data, treatment_to_compare, y_column, ci=None):
    summary_stats = data.groupby(treatment_to_compare)['Value'].agg(['mean', 'std', 'count']).reset_index()
    summary_stats['error'] = summary_stats['std'] / summary_stats['count'] ** 0.5  # Standard error
        
    sns.barplot(x=treatment_to_compare, y='Value', data=data, estimator='mean', ci=None)
    plt.errorbar(summary_stats[treatment_to_compare], summary_stats['mean'], yerr=summary_stats['error'],
                     fmt='o', color='k', capsize=5, label='Mean ± SE')

def plot_scatter(data, treatment_to_compare, y_column,):
    #orange an blue data point on the plot, the same datapoint-information? 
    sns.scatterplot(data=data, x=treatment_to_compare, y='Value', color="red", alpha=.6, jitter=True)
    overlay_data_points_and_error_bars(data, treatment_to_compare)
    
def plot_line(data, treatment_to_compare, y_column):
    summary_stats = data.groupby(treatment_to_compare)['Value'].agg(['mean', 'std']).reset_index()
    sns.lineplot(data=data, x=treatment_to_compare, y='Value', estimator='mean', ci=None)
    plt.errorbar(summary_stats[treatment_to_compare], summary_stats['mean'], yerr=summary_stats['std'],
                     fmt='o', color='k', capsize=5, label='Mean ± SD')

def plot_strip(data, treatment_to_compare, y_column):
    sns.stripplot(x=treatment_to_compare, y='Value', data=data, color='red', alpha=0.6, jitter=False)
    overlay_data_points_and_error_bars(data, treatment_to_compare)

def plot_hist(data, treatment_to_compare, y_column):
    sns.histplot(data['Value'], bins=20)

def plot_heatmap(data, treatment_to_compare):
    if treatment_to_compare not in ["Treatment1", "Treatment2"]:
        raise ValueError("Unsupported treatment specified.")

    if treatment_to_compare == "Treatment1":
        unique_treatment = data['Treatment1']
    elif treatment_to_compare == "Treatment2":
        unique_treatment = data['Treatment1'] + "_" + data['Treatment2']
    else:
        unique_treatment = data['Treatment1'] + "_" + data['Treatment2'] + "_" + data['Sample']

    data['Unique_Treatment'] = unique_treatment

    heatmap_data = pd.pivot_table(data, index="Accession", columns="Unique_Treatment", values="Value", aggfunc="mean")
    sns.heatmap(heatmap_data, cmap="YlGnBu", annot=False)

def plot_swam(data, treatment_to_compare, y_column):
        #durch overlay_data.. wird der plot schon kreiiert mit zwei Farben, -> sns. swarmplot unnötig
    sns.swarmplot(x=treatment_to_compare, y='Value', data=data)
    overlay_data_points_and_error_bars(data, treatment_to_compare)
  
    
#wie hiermit umgegangen werden muss, weiß ich auch noch nicht 
if t_stat is not None and t_p_value is not None:
    plt.title(f't-stat: {t_stat:.4f}, p-value: {t_p_value:.4f}', 
    ha='center')#, va='center', transform=plt.gca().transAxes, color='blue')
if f_stat is not None and f_p_value is not None:
    plt.title(f'F-stat: {f_stat:.4f}, p-value: {f_p_value:.4f}', fontsize = 10, ha='center', va='top', x=0.47, y=1.02, color='blue')
        
plt.suptitle(f'{plot_type} for {treatment_to_compare}', fontsize = 18, ha='center', x=0.5)
plt.xlabel(f'{treatment_to_compare}')
plt.ylabel('Values')
plt.xticks(rotation=45)
plt.tight_layout()  # Ensure the layout is adjusted
plt.legend()
plt.show()
        
def overlay_data_points_and_error_bars(data, treatment_to_compare):
    summary_stats = data.groupby(treatment_to_compare)['Value'].agg(['mean', 'std', 'count']).reset_index()
    # Standard error of the mean? What is the message of this plot?
    summary_stats['error'] = summary_stats['std'] / summary_stats['count'] ** 0.5  

    # Overlay individual data points
    sns.stripplot(x=treatment_to_compare, y='Value', data=data, color='red', alpha=0.6, jitter=True)#, label='Data Points'),no valuable information cause one color 

    # Overlay error bars
    plt.errorbar(summary_stats[treatment_to_compare], summary_stats['mean'], yerr=summary_stats['error'],
                 fmt='o', color='k', capsize=5, label='Mean ± SE')

# Step 3: Plot Clustermap Function
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
