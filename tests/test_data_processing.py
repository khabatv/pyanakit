# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:38:51 2024

@author: past
"""

import pandas as pd
import pytest 
from unittest.mock import patch
from data_processing import process_data
from utils import load_data
import matplotlib.pyplot as plt


@pytest.fixture
def test_load_data(): 
    test_file_path = 'C:/Users/past/Documents/DataAnalysisWorkflow/testTable.txt'
    data = load_data(test_file_path)
    
    assert data is not None, "Daten wurden nicht geladen"
    assert isinstance (data, pd.DataFrame), "Geladene Daten sind kein DataFrame"
    assert not data.empty, "DataFrame ist leer"
    return data 

def test_process_data(test_load_data):
# Mock plt.show to check if it gets called
    with patch.object(plt, 'show') as mock_show:
        processed_data = process_data(data=test_load_data, plot_type='Violin Plot', treatment_to_compare='Treatment1')
        
        # Verifiziere, dass die Daten zurückgegeben wurden
        assert processed_data is not None, "process_data hat None zurückgegeben"
        
        # Verifiziere, dass bestimmte erwartete Spalten existieren
        expected_columns = {"Accession", "Treatment1", "Treatment2", "Sample", "Value"}
        assert expected_columns.issubset(processed_data.columns), "Erforderliche Spalten fehlen im DataFrame"
        
        # Überprüfe, ob plt.show() aufgerufen wurde
        mock_show.assert_called_once()
    

    
    
    