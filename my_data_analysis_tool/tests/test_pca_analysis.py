# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:45:22 2024

@author: past
"""
import pytest
import pandas as pd
from pca_analysis import load_data, perform_pca
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from unittest.mock import patch

# Beispiel-Pfad für die Testdaten
data_file_path = 'C:/Users/past/Documents/DataAnalysisWorkflow/testTable.txt'

@pytest.fixture
def loaded_data():
    """Fixture zum Laden der Testdaten."""
    return load_data(data_file_path)

def test_load_data(loaded_data):
    """Testet die load_data Funktion."""
    data, file_path = loaded_data
    assert data is not None, "Daten wurden nicht geladen."
    assert isinstance(data, pd.DataFrame), "Die geladenen Daten sind kein DataFrame."
    assert not data.empty, "Der DataFrame ist leer."
    assert file_path == data_file_path, "Der Dateipfad stimmt nicht überein."

    # Überprüfen, dass der DataFrame die erwarteten Spalten enthält
    expected_columns = ['Accession']  # und ggf. weitere erwartete Spaltennamen
    assert all(col in data.columns for col in expected_columns), "Die erwarteten Spalten fehlen."

def test_perform_pca_data_cleaning(loaded_data):
    """Testet die Bereinigung der Daten in perform_pca."""
    data, _ = loaded_data

    # Nur numerische Spalten auswählen und `NaN`-Werte entfernen
    numeric_data = data.select_dtypes(include=['number']).dropna()
    assert not numeric_data.isna().any().any(), "Der DataFrame enthält nach der Bereinigung noch `NaN`-Werte."
    assert not numeric_data.empty, "Der bereinigte DataFrame ist leer."

def test_perform_pca_standardization(loaded_data):
    """Testet die Standardisierung der Daten in perform_pca."""
    data, _ = loaded_data

    # Bereinigung und Standardisierung der Daten
    numeric_data = data.select_dtypes(include=['number']).dropna()
    standardized_data = StandardScaler().fit_transform(numeric_data)
    
    # Überprüfen der Standardisierung: Mittelwert nahe 0, Standardabweichung nahe 1
    assert standardized_data.mean() < 1e-6, "Standardisierte Daten sollten Mittelwert nahe 0 haben."
    assert abs(standardized_data.std() - 1) < 1e-6, "Standardisierte Daten sollten Standardabweichung nahe 1 haben."

def test_perform_pca_computation(loaded_data):
    """Testet die Durchführung der PCA in perform_pca."""
    data, _ = loaded_data

    # Datenbereinigung und Standardisierung
    numeric_data = data.select_dtypes(include=['number']).dropna()
    standardized_data = StandardScaler().fit_transform(numeric_data)

    # PCA durchführen
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(standardized_data)
    
    # Überprüfen der Form des PCA-Ergebnisses
    assert pca_result.shape[1] == 2, "PCA-Ergebnis sollte 2 Komponenten enthalten."
    assert pca_result.shape[0] == standardized_data.shape[0], "PCA-Ergebnis sollte gleiche Anzahl Zeilen wie Eingabedaten haben."

def test_perform_pca_plot(loaded_data, monkeypatch):
    """Testet die Erstellung des PCA-Plots in perform_pca."""
    data, _ = loaded_data

    # Mock `messagebox.showerror`, um Fehler abzufangen
    monkeypatch.setattr("tkinter.messagebox.showerror", lambda title, message: (title, message))
    
    with patch("matplotlib.pyplot.show"):
        perform_pca(data)
    
        # Überprüfe die Achsenbeschriftungen und den Scatterplot
        ax = plt.gca()
        assert ax.get_xlabel() == "Principal Component 1", "Die X-Achse sollte PCA1 darstellen."
        assert ax.get_ylabel() == "Principal Component 2", "Die Y-Achse sollte PCA2 darstellen."
        assert len(ax.collections) > 0, "Der Scatterplot sollte Datenpunkte enthalten."




