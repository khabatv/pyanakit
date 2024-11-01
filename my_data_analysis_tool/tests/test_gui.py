# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 10:16:12 2024

@author: past
"""

#import sys
#import os
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from gui import get_plot_type, get_treatment, plot_type_var, treatment_var

def test_get_plot_type():
    plot_type_var.set("Box Plot")
    assert get_plot_type() == "Box Plot"

def test_get_treatment():
    treatment_var.set("Treatment1")
    assert get_treatment() == "Treatment1"
