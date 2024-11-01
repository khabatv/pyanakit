# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:34:17 2024

@author: past
"""

#statistical analysis functions

from scipy.stats import ttest_ind, f_oneway

def perform_t_test (melted_data, treatment_to_compare): 
    t_stat, t_p_value = ttest_ind(melted_data, treatment_to_compare)
    return {'test': 't-test', 'stat': t_stat, 'p_value': t_p_value}

def perform_anova(melted_data, treatment_to_compare):
    f_stat, p_value = f_oneway(melted_data, treatment_to_compare)
    return {'test': 'anova', 'stat': f_stat, 'p_value': p_value}