# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:33:52 2024

@author: past
"""

#plotting graphs 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def plot_violin(data, treatment_to_compare, y_column):
    sns.violinplot(x=treatment_to_compare, y='Value', data=data, inner=None)
    overlay_data_points_and_error_bars(data, treatment_to_compare, "Violin Plot")
    style_plot("Violin Plot", treatment_to_compare, y_column)
    
def plot_box(data, treatment_to_compare, y_column, ci=None):
    sns.boxplot(x=treatment_to_compare, y='Value', data=data)
    overlay_data_points_and_error_bars(data, treatment_to_compare, "Box Plot")
    style_plot("Box Plot", treatment_to_compare, y_column)
    
def plot_bar(data, treatment_to_compare, y_column, ci=None):        
    sns.barplot(x=treatment_to_compare, y='Value', data=data, estimator='mean', ci=None)
    overlay_data_points_and_error_bars(data, treatment_to_compare, "Bar Plot")
    style_plot("Bar Plot", treatment_to_compare, y_column)

# def plot_scatter(data, treatment_to_compare, y_column):
#     sns.scatterplot(data=data, x=treatment_to_compare, y='Value', alpha=.6)
#     overlay_data_points_and_error_bars(data, treatment_to_compare, "Scatter Plot")
#     style_plot("Scatter Plot", treatment_to_compare, y_column)
    
def plot_line(data, treatment_to_compare, y_column):
    summary_stats = data.groupby(treatment_to_compare)['Value'].agg(['mean', 'std']).reset_index()
    sns.lineplot(data=data, x=treatment_to_compare, y='Value', estimator='mean', ci=None)
    plt.errorbar(summary_stats[treatment_to_compare], summary_stats['mean'], yerr=summary_stats['std'],
                     fmt='o', color='k', capsize=5, label='Mean ± SD')
    style_plot("Line Plot", treatment_to_compare, y_column)

# def plot_strip(data, treatment_to_compare, y_column):
#     sns.stripplot(x=treatment_to_compare, y='Value', data=data, alpha=0.6, jitter=True) 
#     overlay_data_points_and_error_bars(data, treatment_to_compare)
#     style_plot("Strip Plot", treatment_to_compare, y_column)

def plot_hist(data, treatment_to_compare, y_column):
    sns.histplot(data['Value'], bins=20)
    style_plot("Histogram", treatment_to_compare, y_column)

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
    style_plot("Heatmap", treatment_to_compare)

def plot_swarm(data, treatment_to_compare, y_column):
    sns.swarmplot(x=treatment_to_compare, y='Value', data=data)
    overlay_data_points_and_error_bars(data, treatment_to_compare, "Swarm Plot")
    style_plot("Swarm Plot", treatment_to_compare, y_column)
  
def style_plot(plot_type, treatment_to_compare, y_column=None): 
    plt.suptitle(f'{plot_type} for {treatment_to_compare}', fontsize = 18, ha='center', x=0.5)
    plt.xlabel(f'{treatment_to_compare}')
    if y_column: 
        plt.ylabel('Values')
    plt.xticks(rotation=45)
    plt.tight_layout() 
    plt.legend()
            
def overlay_data_points_and_error_bars(data, treatment_to_compare, plot_type):
    if plot_type != "Box Plot":
        summary_stats = data.groupby(treatment_to_compare)['Value'].agg(['mean', 'std', 'count']).reset_index()
        plt.errorbar(summary_stats[treatment_to_compare], summary_stats['mean'], yerr=summary_stats['std'],
                     fmt='o', color='k', capsize=5, label='Mean ± SD')
    
    if plot_type in ("Violin Plot", "Box Plot", "Box Plot"):
        sns.stripplot(x=treatment_to_compare, y='Value', data=data, color='red', alpha=0.6, jitter=True)
       
        
        
       

