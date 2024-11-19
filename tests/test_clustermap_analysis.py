# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 13:39:35 2024

@author: past
"""

#test abläufe: 
# =============================================================================
#     1. laden der daten prüfen
#     2. drop na prüfen 
#     3. clustermap erstellen und prüfen    
# =============================================================================

import pandas as pd 
import pytest
from clustermap_analysis import load_data, plot_clustermap
from unittest.mock import patch


#load data tested and after passing, fixture put in place
@pytest.fixture
def test_load_data(): 
    test_file_path = 'C:/Users/past/Documents/DataAnalysisWorkflow/testTable.txt'
    data, file_path = load_data(test_file_path)
    
    assert data is not None, "Daten wurden nicht geladen"
    assert isinstance (data, pd.DataFrame), "Geladene Daten sind kein DataFrame"
    assert not data.empty, "DataFrame ist leer"
    assert file_path == test_file_path, "Der Dateipfad stimmt nicht überein"
    assert not data.isna().any().any()
    return data

def test_plot_clustermap(test_load_data):
    with patch("matplotlib.pyplot.show") as mock_show, \
         patch("matplotlib.pyplot.title") as mock_title, \
         patch("matplotlib.pyplot.xlabel") as mock_xlabel, \
         patch("matplotlib.pyplot.ylabel") as mock_ylabel:
        
        
        # Rufe plot_clustermap auf
        plot_clustermap(
            data=test_load_data,
            method='single',  # Überschreibt den Standardwert 'average'
            cmap='plasma',  # Überschreibt den Standardwert 'viridis'
            width=12,
            height=10,
            font_size=2,
            line_thickness=0.2,
            dendro_line_thickness=0.8
        )

        assert 'Accession' in test_load_data.columns, "Spalte 'Accession' fehlt im DataFrame"

        # wenn diese zeile keinen fehler wirft, wird der plot erfolgreich angezeigt 
        mock_show.assert_called_once()

        # Diese Assertions überprüfen nur die Default-Werte, die an plot_clustermap übergeben wurden
        assert plot_clustermap.__defaults__[0] == 'average', "Default-Wert für 'method' ist nicht korrekt"
        assert plot_clustermap.__defaults__[1] == 'viridis', "Default-Wert für 'cmap' ist nicht korrekt"

        #testen ob titel usw. übereinstimmen        
        expected_title = "Heatmap with Dendrogram (Method: single, Color Map: plasma)"
        mock_title.assert_called_once_with(expected_title, fontsize=2 * 10)  # fontsize=2 * 10 ergibt 20

        # Überprüfen, dass die x- und y-Achsenbeschriftungen korrekt gesetzt wurden
        mock_xlabel.assert_called_once_with("Samples", fontsize=2 * 8)  # fontsize=2 * 8 ergibt 16
        mock_ylabel.assert_called_once_with("Features", fontsize=2 * 8)  # fontsize=2 * 8 ergibt 16



# visuelle Prüfung funktioniert nicht so wie ich es mir denke =============================================================================
# def test_plot_clustermap_visual(test_load_data):
#     # Dies ist der visuelle Test, der den Plot tatsächlich anzeigt
#     plot_clustermap(
#         data=test_load_data,
#         method='single',
#         cmap='plasma',
#         width=12,
#         height=10,
#         font_size=2,
#         line_thickness=0.2,
#         dendro_line_thickness=0.8
#     )
# =============================================================================

    
    
    