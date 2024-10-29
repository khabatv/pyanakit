# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:34:54 2024

@author: past
"""

#pca function

from tkinter import messagebox
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def perform_pca():
    global data
    if data is None:
        messagebox.showerror("Error", "Please select a file and load data first.")
        return

    try:
        # Drop non-numeric columns and handle NaNs
        numeric_data = data.select_dtypes(include=['number']).dropna()
        
        # Standardize the data
        standardized_data = StandardScaler().fit_transform(numeric_data)

        # Perform PCA
        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(standardized_data)

        # Create a DataFrame for PCA results
        pca_df = pd.DataFrame(data=pca_result, columns=['Principal Component 1', 'Principal Component 2'])
        pca_df['Accession'] = data['Accession']  # Add Accession back for labeling

        # Plot PCA results
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='Principal Component 1', y='Principal Component 2', data=pca_df)
        plt.title('PCA of Data')
        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during PCA: {str(e)}")
