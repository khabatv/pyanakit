# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:34:17 2024

@author: past
"""

#statistical analysis functions

from scipy.stats import ttest_ind, f_oneway

def perform_t_test (data1, data2): 
    t_stat, t_p_value = ttest_ind(data1, data2)
    return {'test': 't-test', 'stat': t_stat, 'p_value': t_p_value}

def preform_anova(*groups):
    f_stat, p_value = f_oneway(*groups)
    return {'test': 'anova', 'stat': f_stat, 'p_value': p_value}