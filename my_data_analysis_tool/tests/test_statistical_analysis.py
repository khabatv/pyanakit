# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:44:37 2024

@author: past
"""

#generieren von testdaten für statistik, aufrufen der Statistiksfunktion 
# test_statistical_analysis.py


#import pytest
from statistical_analysis import perform_t_test, perform_anova
#import sys
#import os
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

#print(sys.path)


def test_perform_t_test():
    # Define sample data for testing
    data1 = [1, 2, 3, 4, 5]
    data2 = [2, 3, 4, 5, 6]
    
    # Run the t-test
    result = perform_t_test(data1, data2)
    
    # Check if the returned dictionary contains expected keys
    assert 'test' in result, "Result should contain 'test' key"
    assert 'stat' in result, "Result should contain 'stat' key"
    assert 'p_value' in result, "Result should contain 'p_value' key"
    
    # Check the values
    assert result['test'] == 't-test', "Test name should be 't-test'"
    assert isinstance(result['stat'], float), "Stat should be a float"
    assert isinstance(result['p_value'], float), "p_value should be a float"
    assert 0 <= result['p_value'] <= 1, "p_value should be between 0 and 1"

def test_perform_anova():
       
    
    # Define sample data for testing
    group1 = [1, 2, 3, 4, 5]
    group2 = [2, 3, 4, 5, 6]
    #group3 = [3, 4, 5, 6, 7]
    
    # Run the ANOVA
    result = perform_anova(group1, group2)
    
    # Check if the returned dictionary contains expected keys
    assert 'test' in result, "Result should contain 'test' key"
    assert 'stat' in result, "Result should contain 'stat' key"
    assert 'p_value' in result, "Result should contain 'p_value' key"
    
    # Check the values
    assert result['test'] == 'anova', "Test name should be 'anova'"
    assert isinstance(result['stat'], float), "Stat should be a float"
    assert isinstance(result['p_value'], float), "p_value should be a float"
    assert 0 <= result['p_value'] <= 1, "p_value should be between 0 and 1"