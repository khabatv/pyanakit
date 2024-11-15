# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 11:19:14 2024

@author: past
"""

# Importiere die notwendigen Funktionen
from pca_analysis import load_data, perform_pca

# Definiere den Dateipfad zu deinem Testdatensatz
file_path = 'C:/Users/past/Documents/DataAnalysisWorkflow/testTable.txt'

# Lade die Daten
data, _ = load_data(file_path)

# Führe die PCA und das Plotten aus
perform_pca(data)
