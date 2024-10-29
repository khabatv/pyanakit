# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:33:52 2024

@author: past
"""

#plotting graphs 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

#funktioniert das mit dem dem treatment to compare und dem Value argumenten? 
def plot_violin(data, treatment_to_compare, y_column):
    sns.violinplot(x=treatment_to_compare, y='Value', data=data, inner=None)
    overlay_data_points_and_error_bars(data, treatment_to_compare)
    style_plot("Violin Plot", treatment_to_compare, y_column)
    
def plot_box(data, treatment_to_compare, y_column, ci=None):
    sns.boxplot(x=treatment_to_compare, y='Value', data=data)
    overlay_data_points_and_error_bars(data, treatment_to_compare)
    
def plot_bar(data, treatment_to_compare, y_column, ci=None):
    summary_stats = data.groupby(treatment_to_compare)['Value'].agg(['mean', 'std', 'count']).reset_index()
    summary_stats['error'] = summary_stats['std'] / summary_stats['count'] ** 0.5  # Standard error
        
    sns.barplot(x=treatment_to_compare, y='Value', data=data, estimator='mean', ci=None)
    plt.errorbar(summary_stats[treatment_to_compare], summary_stats['mean'], yerr=summary_stats['error'],
                     fmt='o', color='k', capsize=5, label='Mean ± SE')

def plot_scatter(data, treatment_to_compare, y_column):
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

def plot_swarm(data, treatment_to_compare, y_column):
        #durch overlay_data.. wird der plot schon kreiiert mit zwei Farben, -> sns. swarmplot unnötig
    sns.swarmplot(x=treatment_to_compare, y='Value', data=data)
    overlay_data_points_and_error_bars(data, treatment_to_compare)
  
    
def style_plot(plot_type, treatment_to_compare, y_column): 
    plt.figure(figsize=(12,6))
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


