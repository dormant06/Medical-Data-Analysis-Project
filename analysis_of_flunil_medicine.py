# -*- coding: utf-8 -*-
"""Analysis of Flunil medicine.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11dmHQEHzCAsqpBLxKLc22RFYrMqzq8BU
"""

import numpy as np
import pandas as pd
from scipy import stats

data = pd.read_csv("/content/med data grouped.csv")
data.head()

"""     Here f == those patients who took medicine flunil
    
     n== those patients who did not take any medicine
    
     1 == first checkup
    
     2== checkup after 30 days

     And all the scores are PHQ values
"""

type(data["group_f_1"].values)

"""A test to check if data is approximately normal to allow application of following statistical methods"""

from scipy import stats

# Group 1: Patients who took the medicine
group1_day1_scores = data["group_f_1"].values
group1_day30_scores = data["group_f_2"].values

# Group 2: Patients who did not take the medicine
group2_day1_scores = data["group_n_1"].values
group2_day30_scores = data["group_n_2"].values

# Perform Shapiro-Wilk test for normality
_, p_value_group1_day1 = stats.shapiro(group1_day1_scores)
_, p_value_group1_day30 = stats.shapiro(group1_day30_scores)
_, p_value_group2_day1 = stats.shapiro(group2_day1_scores)
_, p_value_group2_day30 = stats.shapiro(group2_day30_scores)

# Print the results
print("Group 1 (Medicine) - Day 1 Scores:")
print("  - Shapiro-Wilk p-value:", p_value_group1_day1)
print()
print("Group 1 (Medicine) - Day 30 Scores:")
print("  - Shapiro-Wilk p-value:", p_value_group1_day30)
print()
print("Group 2 (No Medicine) - Day 1 Scores:")
print("  - Shapiro-Wilk p-value:", p_value_group2_day1)
print()
print("Group 2 (No Medicine) - Day 30 Scores:")
print("  - Shapiro-Wilk p-value:", p_value_group2_day30)

"""Since p values > 0.05  -> Yes the data can be approximately considered normal

Applying t test to check if the groups with and without medicine have behave differently after 30 days
"""

# Group 1: Patients who took the medicine
group1_day1_scores = data["group_f_1"].values
group1_day30_scores = data["group_f_2"].values

# Group 2: Patients who did not take the medicine
group2_day1_scores = data["group_n_1"].values
group2_day30_scores = data["group_n_2"].values

# Perform paired t-test for each group
_, p_value_group1 = stats.ttest_rel(group1_day1_scores, group1_day30_scores)
_, p_value_group2 = stats.ttest_rel(group2_day1_scores, group2_day30_scores)

# Print the results
print("Group 1 (Medicine):")
print("  - Mean Day 1 Score:", np.mean(group1_day1_scores))
print("  - Mean Day 30 Score:", np.mean(group1_day30_scores))
print("  - p-value:", p_value_group1)
print()
print("Group 2 (No Medicine):")
print("  - Mean Day 1 Score:", np.mean(group2_day1_scores))
print("  - Mean Day 30 Score:", np.mean(group2_day30_scores))
print("  - p-value:", p_value_group2)

"""Since p value of Group 1 < 0.05 and group 2 > 0.05 it can be concluded that the medicine has a significant effect on the scores in Group 1 (Medicine), but there is no significant change in scores in Group 2 (No Medicine).

Applying Cohen's d test to measure effect size.
"""

# Calculate Cohen's d
mean_diff_group1 = np.mean(group1_day1_scores - group1_day30_scores)
mean_diff_group2 = np.mean(group2_day1_scores - group2_day30_scores)
std_dev_group1 = np.std(group1_day1_scores - group1_day30_scores, ddof=1)
std_dev_group2 = np.std(group2_day1_scores - group2_day30_scores, ddof=1)

cohens_d = (mean_diff_group1 - mean_diff_group2) / np.sqrt((std_dev_group1**2 + std_dev_group2**2) / 2)

# Print Cohen's d
print("Cohen's d:", cohens_d)

"""Conclusion: Presence of medicine had a substancial impact given large Cohen's d value

However, till now I have ignored the age gender and other factors of patients while performing above analysis. Using these informations also and doing anaysis
"""

import statsmodels.api as sm

# Group 1: Patients who took the medicine
group1_day1_scores = data["group_f_1"].values
group1_day30_scores = data["group_f_2"].values
group1_age = data["age_group_f"].values
group1_gender = data["Gender_group_f"].values

# Create the design matrix for Group 1 with covariates
group1_covariates = sm.add_constant(np.column_stack((group1_age, group1_gender)))

# Fit the ANCOVA model for Group 1
model_group1 = sm.OLS(group1_day30_scores, sm.add_constant(group1_day1_scores)).fit()

# Print the ANCOVA results for Group 1
print("Group 1 (Medicine) - Day 30 Scores:")
print(model_group1.summary())
print()

# Group 2: Patients who did not take the medicine
group2_day1_scores = data["group_n_1"].values
group2_day30_scores = data["group_n_2"].values
group2_age = data["age_group_n"].values
group2_gender = data["Gender_group_n"].values

# Create the design matrix for Group 2 with covariates
group2_covariates = sm.add_constant(np.column_stack((group2_age, group2_gender)))

# Fit the ANCOVA model for Group 2
model_group2 = sm.OLS(group2_day30_scores, sm.add_constant(group2_day1_scores)).fit()

# Print the ANCOVA results for Group 2
print("Group 2 (No Medicine) - Day 30 Scores:")
print(model_group2.summary())
print()

"""The above results give the following:

There is a statistical significance between the day 1 and day 30 scores in group 2.
However, their doesn't exist any statistical significance in day 1 and day 30 scores of group 1 (medicine).

Interpretaion:  in group 2 we see a clear pattern in change of health score; however, their isn't a clear pattern (like linear) in group 1 impliing the medicine had some effect which isn't clear yet due to presence of a lot of other factors

# Overall Conclusion: The medicine has significant affect on patients. However, it doesn't affect all patients uniformly and has varied effect depending on other factors.
"""