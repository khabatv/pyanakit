# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:43:57 2024

@author: past
"""

#generieren von Plotdaten und testen der Plotfunktion (positiv/negativ - Test)

import pytest
import pandas as pd
import matplotlib.pyplot as plt
from plotting import (
    plot_violin,
    plot_box,
    plot_bar,
    #plot_scatter,
    plot_line,
    #plot_strip,
    plot_hist,
    plot_swarm,
    plot_heatmap,
    overlay_data_points_and_error_bars,
    style_plot
)

# Beispiel-Testdaten
@pytest.fixture
def example_data():
    return pd.DataFrame({
        'Treatment1': ['A', 'A', 'B', 'B'],
        'Treatment2': ['X', 'Y', 'X', 'Y'],
        'Value': [1.0, 2.5, 3.0, 4.5],
        'Sample': ['S1', 'S2', 'S3', 'S4'],
        'Accession': ['ID1', 'ID2', 'ID3', 'ID4']
    })

def test_plot_violin(example_data):
    plt.figure()
    plot_violin(example_data, 'Treatment1', 'Value')
    assert plt.gca().get_title() != "" or (plt.gcf()._suptitle and plt.gcf()._suptitle.get_text()) != ""
    assert plt.gca().get_xlabel() == "Treatment1"
    assert plt.gca().get_ylabel() == "Values"
    plt.close()

def test_plot_box(example_data):
    plt.figure()
    plot_box(example_data, 'Treatment1', 'Value')
    assert plt.gca().get_title() != ""  or (plt.gcf()._suptitle and plt.gcf()._suptitle.get_text()) != ""
    assert plt.gca().get_xlabel() == "Treatment1"
    assert plt.gca().get_ylabel() == "Values"
    plt.close()

def test_plot_bar(example_data):
    plt.figure()
    plot_bar(example_data, 'Treatment1', 'Value')
    assert plt.gca().get_title() != ""  or (plt.gcf()._suptitle and plt.gcf()._suptitle.get_text()) != ""
    assert plt.gca().get_xlabel() == "Treatment1" 
    assert plt.gca().get_ylabel() == "Values"
    plt.close()

# def test_plot_scatter(example_data):
#     plt.figure()
#     plot_scatter(example_data, 'Treatment1', 'Value')
#     assert plt.gca().get_title() != "" or (plt.gcf()._suptitle and plt.gcf()._suptitle.get_text()) != ""
#     assert plt.gca().get_xlabel() == "Treatment1" 
#     assert plt.gca().get_ylabel() == "Values"
#     plt.close()

def test_plot_line(example_data):
    plt.figure()
    plot_line(example_data, 'Treatment1', 'Value')
    assert plt.gca().get_title() != "" or (plt.gcf()._suptitle and plt.gcf()._suptitle.get_text()) != ""
    assert plt.gca().get_xlabel() == "Treatment1"
    assert plt.gca().get_ylabel() == "Values"
    plt.close()
    
# def test_plot_strip(example_data):
#     plt.figure()
#     plot_strip(example_data, 'Treatment1', 'Value')
#     assert plt.gca().get_title() != "" or (plt.gcf()._suptitle and plt.gcf()._suptitle.get_text()) != ""
#     assert plt.gca().get_xlabel() == "Treatment1"
#     assert plt.gca().get_ylabel() == "Values"
#     plt.close()

def test_plot_hist(example_data):
    plt.figure()
    plot_hist(example_data, 'Treatment1', 'Value')
    assert plt.gca().get_title() != "" or (plt.gcf()._suptitle and plt.gcf()._suptitle.get_text()) != ""
    assert plt.gca().get_xlabel() == "Treatment1"
    plt.close()
    
def test_plot_swarm(example_data):
    plt.figure()
    plot_swarm(example_data, 'Treatment1', 'Value')
    assert plt.gca().get_title() != "" or (plt.gcf()._suptitle and plt.gcf()._suptitle.get_text()) != ""
    assert plt.gca().get_xlabel() == "Treatment1"
    assert plt.gca().get_ylabel() == "Values"
    plt.close()


# Test für plot_heatmap, da spezielle Spalten benötigt werden
def test_plot_heatmap(example_data):
    plt.figure()
    plot_heatmap(example_data, 'Treatment1')
    # Überprüfen, ob der Plot erstellt wurde
    assert plt.gca().get_title() == "Heatmap for Treatment1" or (plt.gcf()._suptitle and plt.gcf()._suptitle.get_text()) == "Heatmap for Treatment1"
    plt.close()

# Test für overlay_data_points_and_error_bars
def test_overlay_data_points_and_error_bars(example_data):
    plt.figure()
    overlay_data_points_and_error_bars(example_data, 'Treatment1', "Swarm Plot")
    # Überprüfen, ob Fehlerbalken und Punkte gezeichnet wurden
    assert len(plt.gca().lines) > 0  # Linien für Fehlerbalken
    plt.close()

# Test für style_plot
def test_style_plot():
    plt.figure()
    style_plot("Test Plot", "Test Treatment", "Test Y")
    # Überprüfen, ob Titel und Achsenbeschriftungen gesetzt sind
    assert plt.gca().get_title() == "Test Plot for Test Treatment" or (plt.gcf()._suptitle and plt.gcf()._suptitle.get_text()) == "Test Plot for Test Treatment"
    assert plt.gca().get_xlabel() == "Test Treatment"
    assert plt.gca().get_ylabel() == "Values"
    plt.close()
