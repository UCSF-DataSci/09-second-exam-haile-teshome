import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats
import matplotlib.pyplot as plt
import os

#Load the cleaned data
data_path = os.path.join('.', 'ms_data.csv')
data = pd.read_csv(data_path)
data['visit_date'] = pd.to_datetime(data['visit_date'])

#Walking Speed Analysis 
#Multiple regression of walking speed with education and age, controlling for patient_id
print("\n--- Walking Speed Regression Analysis ---")
mixed_model = smf.mixedlm("walking_speed ~ education_level + age", data, groups=data['patient_id'])
mixed_result = mixed_model.fit()
print(mixed_result.summary())

#Test for significant trends in walking speed by age and education level interaction
education_age_interaction_model = smf.ols("walking_speed ~ education_level * age", data).fit()
print("\n--- Interaction Model Analysis for Education Level and Age on Walking Speed ---")
print(education_age_interaction_model.summary())

#Cost Analysis 
print("\n--- Cost Analysis by Insurance Type ---")
#Box plot for insurance type effect on visit cost
plt.figure(figsize=(8, 6))
data.boxplot(column='visit_cost', by='insurance_type')
plt.title('Visit Cost by Insurance Type')
plt.suptitle('')  # Remove automatic title
plt.xlabel('Insurance Type')
plt.ylabel('Visit Cost')
plt.show()

#Calculate mean and median visit costs by insurance type
mean_cost_by_insurance = data.groupby('insurance_type')['visit_cost'].mean()
median_cost_by_insurance = data.groupby('insurance_type')['visit_cost'].median()

print("Mean Visit Cost by Insurance Type:\n", mean_cost_by_insurance)
print("\nMedian Visit Cost by Insurance Type:\n", median_cost_by_insurance)

#Calculate effect sizes Cohen's d between insurance types
def cohen_d(group1, group2):
    """Calculate Cohen's d for two groups"""
    return (np.mean(group1) - np.mean(group2)) / np.sqrt((np.var(group1) + np.var(group2)) / 2)

#Pairwise effect sizes between insurance types
value_costs = data[data['insurance_type'] == 'Value']['visit_cost']
hmo_costs = data[data['insurance_type'] == 'HMO']['visit_cost']
ppo_costs = data[data['insurance_type'] == 'PPO']['visit_cost']

cohen_d_value_hmo = cohen_d(value_costs, hmo_costs)
cohen_d_value_ppo = cohen_d(value_costs, ppo_costs)
cohen_d_hmo_ppo = cohen_d(hmo_costs, ppo_costs)

print("\n--- Effect Sizes (Cohen's d) Between Insurance Types ---")
print(f"Value vs HMO: {cohen_d_value_hmo:.2f}")
print(f"Value vs PPO: {cohen_d_value_ppo:.2f}")
print(f"HMO vs PPO: {cohen_d_hmo_ppo:.2f}")

#Advanced Analysis: Education and Age Interaction on Walking Speed
print("\n--- Advanced Analysis: Interaction Effects ---")
#ANOVA to examine interaction effect of education level and age on walking speed
anova_interaction_model = smf.ols("walking_speed ~ C(education_level) * age", data).fit()
anova_table = sm.stats.anova_lm(anova_interaction_model, typ=2)
print("\nANOVA for Interaction between Education Level and Age on Walking Speed")
print(anova_table)

#Control for additional confounders education level , age , insurance type
confounder_model = smf.ols("walking_speed ~ education_level + age + insurance_type", data).fit()
print("\n--- Confounder-Controlled Model ---")
print(confounder_model.summary())
