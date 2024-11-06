# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:34:54 2024

@author: past
"""

#pca_analysis.py

from tkinter import messagebox
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#aber woher kommen jetzt die Daten? perform pca muss irgendow die Daten herbekommen?? 
#hier wird wie bei process_data() eine load_data gebraucht? 
# gehört load data deswegen in utils? 
#erstmal nur pro forma eingefügt:

def load_data(file_path = None): 
    if file_path is None: 
        from gui import file_path as global_file_path 
        file_path = global_file_path
    data = pd.read_csv(file_path, sep="\t") 
    #dropna schritt auch hier? 
    data = data.dropna()
    return data

def perform_pca(data):
    if data is None:
        messagebox.showerror("Error", "Please select a file and load data first.")

    try:
        # Drop non-numeric columns and handle NaNs
        numeric_data = data.select_dtypes(include=['number']).dropna()
        print(f"Bereinigter Datensatz:\n{numeric_data}\n")
        
        # Überprüfen, ob Daten nach Bereinigung existieren
        if numeric_data.empty:
           print("Bereinigter Datensatz ist leer, keine Daten für PCA verfügbar.")
           messagebox.showerror("Error", "No numeric data available for PCA after cleaning.")
           return None
        
        # Standardize the data
        standardized_data = StandardScaler().fit_transform(numeric_data)
        print(f"Standardized Data Shape: {standardized_data.shape}")  # Debugging-Ausgabe
        
        # Perform PCA
        pca = PCA(n_components=2)
        pca_result = pca.fit_transform(standardized_data)
        print(f"PCA Ergebnis:\n{pca_result}\n")  # Debugging-Ausgabe

        # Create a DataFrame for PCA results
        pca_df = pd.DataFrame(data=pca_result, columns=['Principal Component 1', 'Principal Component 2'])
        pca_df['Accession'] = data['Accession']  # Add Accession back for labeling

        # Plot PCA results
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x='Principal Component 1', y='Principal Component 2', data=pca_df)
        #plt.scatter(pca_df['Principal Component 1'], pca_df['Principal Component 2'])
        plt.title('PCA of Data')
        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        
        # Manuelle Anpassung der Achsenlimits nötig für test?
        plt.xlim(pca_df['Principal Component 1'].min() - 1, pca_df['Principal Component 1'].max() + 1)
        plt.ylim(pca_df['Principal Component 2'].min() - 1, pca_df['Principal Component 2'].max() + 1)
        
        plt.tight_layout()
        plt.show()
    
    except Exception as e:
        print(f"Exception during PCA: {e}")  # Debugging-Ausgabe
        messagebox.showerror("Error", f"An error occurred during PCA: {str(e)}")
        