# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:32:57 2024

@author: past
"""

from statistical_analysis import perform_t_test, perform_anova
from plotting import (
    plot_violin,
    plot_box,
    plot_bar,
    #plot_scatter,
    #plot_strip,
    plot_line,
    plot_hist,
    plot_heatmap,
    plot_swarm,
)
import pandas as pd
from tkinter import messagebox
import matplotlib.pyplot as plt

def process_data(data, plot_type=None, treatment_to_compare = None):  
    if plot_type is None or treatment_to_compare is None: 
       raise ValueError("Plot_type and treatment_to_compare are required.")
    
    try:
        # Extract treatments and biological replicates
        melted_data = data.melt(id_vars="Accession", var_name="Treatment_Sample", value_name="Value")
        # Extract treatment and sample information
        melted_data[['Treatment1', 'Treatment2', 'Sample']] = melted_data['Treatment_Sample'].str.split('_', expand=True, n=2)
        melted_data = melted_data.drop(columns=['Treatment_Sample'])  # Drop the original column
        
        if melted_data['Value'].dtype == 'object':
            melted_data['Value'] = pd.to_numeric(melted_data['Value'], errors='coerce')
        
        if melted_data['Value'].isnull().any():
            print("Warning: 'Value' enthält NaN-Werte nach Konvertierung zu numerisch.")
        
        # Add statistical analysis before plotting
        t_stat, t_p_value = None, None
        f_stat, f_p_value = None, None
       
        # Perform statistical analysis
        if treatment_to_compare == "Treatment1":
            print("Performing statistical analysis for Treatment1...")
            t_stat, t_p_value = perform_t_test(melted_data, treatment_to_compare)
        else:
            print(f"Performing ANOVA analysis for {treatment_to_compare}...")
            f_stat, f_p_value, tukey_summary = perform_anova(melted_data, treatment_to_compare)
            if tukey_summary is not None:
                print("Tukey Test Ergebnisse:")
                print(tukey_summary)

        # Generate selected plot type
        plt.figure(figsize=(12, 6))

        if plot_type == "Violin Plot":
            plot_violin(melted_data, treatment_to_compare, 'Value')
        
        elif plot_type == "Box Plot":
            plot_box(melted_data, treatment_to_compare, 'Value', ci=None)
        
        elif plot_type == "Bar Plot":
            plot_bar(melted_data, treatment_to_compare, 'Value', ci=None)

        # elif plot_type == "Scatter Plot":
        #     plot_scatter(melted_data, treatment_to_compare, 'Value')
        
        elif plot_type == "Line Plot":
            plot_line(melted_data, treatment_to_compare, 'Value')
        
        # elif plot_type == "Strip Plot":
        #     plot_strip(melted_data, treatment_to_compare, 'Value')

        elif plot_type == "Histogram":
            plot_hist(melted_data, treatment_to_compare, 'Value')

        elif plot_type == "Heatmap":
            plot_heatmap(melted_data, treatment_to_compare)
            
        elif plot_type == "Swarm Plot":
            plot_swarm(melted_data, treatment_to_compare,'Value')
         
        if t_stat is not None and t_p_value is not None:
            plt.title(f't-stat: {t_stat:.4f}, p-value: {t_p_value:.4f}', 
                     ha='center', va='top', x=0.47, y=1.02, color='blue')
        if f_stat is not None and f_p_value is not None:
            plt.title(f'F-stat: {f_stat:.4f}, p-value: {f_p_value:.4f}', fontsize = 10, 
                     ha='center', va='top', x=0.47, y=1.02, color='blue')
    
        #to prevent double plotting error 
        plt.show()
        
        return melted_data
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")