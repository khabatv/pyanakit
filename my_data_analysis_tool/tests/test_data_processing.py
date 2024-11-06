# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:38:51 2024

@author: past
"""

import pandas as pd
import pytest 
from unittest.mock import patch, MagicMock
from data_processing import process_data, load_data 

# =============================================================================
#setzten des Dateipfade, da dieser eine globale variable aus process_data() ist
#file_path = 'C:/Users/past/Documents/DataAnalysisWorkflow/testTable.txt'

#test des einlesen der daten 
# @pytest.fixture
# def test_load_data():
#     data = pd.read_csv(file_path, sep="\t")
#     assert isinstance(data, pd.DataFrame), "geladenen Daten sind kein Dataframe" 
#     assert not data.empty, "Dataframe vorhanden, aber leer"
#     #return data, damit andere Funktionen darauf zugriff haben 
#     return data
# 
# # Clean data: drop rows with NaN values 
# #fixture, da auch hier ein wert an eine folgenden Funktion weitergegeben wird 
# @pytest.fixture  
# def test_drop_na(test_load_data): 
#     #teste ob na erkannt werden, original daten hat na drin 
#     #zweimal any() um für gesamten dataFrame eine infor über true/false zu bekommen
#     assert test_load_data.isna().any().any(), "DataFrame enthält keine NA"
#     
#     #testen der drop na 
#     clean_data = test_load_data.dropna()
#     assert not clean_data.isna().any().any(), "DataFrame enthält NA"
#     #Bedingung: weniger zeilen in cleanem Datensatz als im eingelesenen Datensatz
#     assert len(clean_data) < len(test_load_data), "Keine Zeilen wurden entfernt, obwohl NA-Werte vorhanden waren"
#     return clean_data
# 
# @pytest.fixture
# def test_table_first(test_drop_na): 
#     melted_data = test_drop_na.melt(id_vars="Accession", var_name="Treatment_Sample", value_name="Value")
#     #erwartete spaltenname aus funktion extra speichern und im assert abgleichen 
#     expected_columns = {"Accession", "Treatment_Sample", "Value"}
#     assert set(melted_data.columns) == expected_columns, "Spaltennamen stimmen nicht überein"
#     assert not melted_data.empty, "Der geschmolzene DataFrame ist leer"
#     return melted_data
# 
# def test_table_second(test_table_first): 
#    test_table_first[['Treatment1', 'Treatment2', 'Sample']] = test_table_first['Treatment_Sample'].str.split('_', expand=True, n=2)
#    test_table_first = test_table_first.drop(columns=['Treatment_Sample'])  # Drop the original column
#    expected_columns = {"Accession","Treatment1", "Treatment2", "Sample", "Value"}
#    assert set(test_table_first.columns) == expected_columns, "Spaltennamen stimmen nicht überein"
#    assert 'Treatment_Sample' not in test_table_first.columns, "'Treatment_Sample' wurde nicht entfernt"
# =============================================================================

#vorherige Einzeltests bestanden, nun end to end test um process_data() komplett zu testen 
@pytest.fixture
def test_load_data(): 
    test_file_path = 'C:/Users/past/Documents/DataAnalysisWorkflow/testTable.txt'
    data, file_path = load_data(test_file_path)
    
    assert data is not None, "Daten wurden nicht geladen"
    assert isinstance (data, pd.DataFrame), "Geladene Daten sind kein DataFrame"
    assert not data.empty, "DataFrame ist leer"
    assert file_path == test_file_path, "Der Dateipfad stimmt nicht überein"
    return data 

def test_process_data(test_load_data):
    processed_data = process_data(data=test_load_data, plot_type='Violin Plot', treatment_to_compare='Treatment1')
    
    assert processed_data is not None, "process data hat none zurück gegeben"
    
    expected_columns = {"Accession", "Treatment1", "Treatment2", "Sample", "Value"}
    assert set(processed_data.columns) == expected_columns, "Erwartete Spalten fehlen nach der Verarbeitung"
   
    # Sicherstellen, dass alle `NA`-Werte entfernt wurden
    assert not processed_data.isna().any().any(), "Der DataFrame enthält noch NA-Werte nach der Bereinigung"
   
    # Sicherstellen, dass der DataFrame nicht leer ist und eine erwartete Struktur hat
    assert not processed_data.empty, "Der DataFrame ist leer nach der Verarbeitung"
    assert len(processed_data) > 0, "Die Anzahl der Zeilen ist unerwartet niedrig"
    

    
    
    