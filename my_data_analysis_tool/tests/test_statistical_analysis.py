# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:44:37 2024

@author: past
"""

import pytest
import pandas as pd
from statistical_analysis import perform_t_test, perform_anova
from data_processing import process_data
from utils import load_clean  

@pytest.fixture
def import_data():
    # Lade die Daten und führe die Transformation durch
    test_file_path = 'C:/Users/past/Documents/DataAnalysisWorkflow/testTable1.txt'
    raw_data = load_clean(test_file_path)  # Originaldaten laden
    transformed_data = process_data(raw_data, treatment_to_compare="Treatment1", plot_type="Violin Plot")
    
    # Sicherstellen, dass die Daten korrekt geladen und transformiert wurden
    assert transformed_data is not None, "Daten wurden nicht transformiert"
    assert isinstance(transformed_data, pd.DataFrame), "Geladene Daten sind kein DataFrame"
    assert not transformed_data.empty, "DataFrame ist leer"
    
    return transformed_data

def test_perform_t_test(import_data):
    # Führe den t-Test aus, wenn nur zwei Gruppen in Treatment1 vorhanden sind
    if import_data['Treatment1'].nunique() == 2:
        t_stat, p_value = perform_t_test(import_data, 'Treatment1')
        
        # Sicherstellen, dass der Test erfolgreich lief und gültige Werte zurückgab
        assert t_stat is not None, "t-Test fehlgeschlagen"
        assert isinstance(t_stat, float), "t_stat sollte ein float sein"
        assert isinstance(p_value, float), "p_value sollte ein float sein"
        assert 0 <= p_value <= 1, "p_value sollte zwischen 0 und 1 liegen"
    else:
        pytest.skip("t-Test erfordert genau zwei Gruppen in 'Treatment1'.")

def test_perform_anova(import_data):
    # Führe den ANOVA-Test aus, wenn mehr als zwei Gruppen in Treatment2 vorhanden sind
    if import_data['Treatment2'].nunique() > 2:
        f_stat, p_value, tukey_summary = perform_anova(import_data, 'Treatment2')
        
        # Sicherstellen, dass der Test erfolgreich lief und gültige Werte zurückgab
        assert f_stat is not None, "ANOVA fehlgeschlagen"
        assert isinstance(f_stat, float), "f_stat sollte ein float sein"
        assert isinstance(p_value, float), "p_value sollte ein float sein"
        assert 0 <= p_value <= 1, "p_value sollte zwischen 0 und 1 liegen"
        
        # Überprüfen des Tukey-Tests bei signifikantem ANOVA-Ergebnis
        if p_value < 0.05:
            assert tukey_summary is not None, "Tukey summary sollte nicht None sein bei signifikantem ANOVA"
        else:
            assert tukey_summary is None, "Tukey summary sollte None sein, wenn ANOVA nicht signifikant ist"
    else:
        pytest.skip("ANOVA erfordert mehr als zwei Gruppen in 'Treatment2'.")
