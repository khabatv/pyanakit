# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:34:17 2024

@author: past
"""

#statistical analysis functions

from scipy.stats import ttest_ind, f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd

def perform_t_test(melted_data, treatment_to_compare):
    # Conduct a t-test between two treatments if applicable
    treatments = melted_data[treatment_to_compare].unique()
    if len(treatments) == 2:
        group1 = melted_data[melted_data[treatment_to_compare] == treatments[0]]['Value']
        group2 = melted_data[melted_data[treatment_to_compare] == treatments[1]]['Value']
        # Perform the t-test (independant?)
        t_stat, p_value = ttest_ind(group1, group2)
        print(f"t-statistic: {t_stat}, p-value: {p_value}")
        return t_stat, p_value
        
    else:
        print("No statistic! Current statistical analysis requires exactly two or more treatments.")
        return None, None
    
def perform_anova(melted_data, treatment_to_compare):
    # Perform ANOVA between multiple treatments
    treatments = melted_data[treatment_to_compare].unique()
    if len(treatments) > 2:
        groups = [melted_data[melted_data[treatment_to_compare] == t]['Value'] for t in treatments]
        f_stat, p_value = f_oneway(*groups)
        
        print(f"ANOVA F-statistic: {f_stat}, p-value: {p_value}")
        if p_value < 0.05: 
            tukey_result = pairwise_tukeyhsd(melted_data['Value'], melted_data[treatment_to_compare], alpha=0.05)
            #print(tukey_result)
            return f_stat, p_value, tukey_result.summary()
        else:
            print("No significant difference, therefore no post-hoc test required.")
            return f_stat, p_value, None
        
    else:
        print("ANOVA requires more than two treatments.")
        return None, None, None