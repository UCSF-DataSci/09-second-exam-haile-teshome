import pandas as pd
import numpy as np
import os

#Read processed data
data_path = os.path.join('.', 'ms_data.csv')
insurance_path = os.path.join('.', 'insurance.lst')
data = pd.read_csv(data_path)
insurance_types = pd.read_csv(insurance_path, header=None, names=['insurance_type'])

#Convert visit_date to datetime
data['visit_date'] = pd.to_datetime(data['visit_date'])

#Sort by patient_id and visit_date
data = data.sort_values(by=['patient_id', 'visit_date'])

#Assign insurance randomly to patients
unique_patients = data['patient_id'].unique()
np.random.seed(0)  # For reproducibility
patient_insurance = {pid: np.random.choice(insurance_types['insurance_type']) for pid in unique_patients}
data['insurance_type'] = data['patient_id'].map(patient_insurance)

#Define base costs for each insurance type
insurance_costs = {
    'PPO': 100,
    'HMO': 200,
    'Value': 300
}

#Apply base cost and add random variation to each visit
data['visit_cost'] = data['insurance_type'].apply(lambda x: insurance_costs[x] + np.random.normal(0, 20))

#Save the updated DataFrame back to the CSV file
data.to_csv(data_path, index=False)
print("Updated data saved with insurance_type and visit_cost columns.")

#Calculate summary statistics
mean_walking_speed_by_education = data.groupby('education_level')['walking_speed'].mean()
mean_cost_by_insurance = data.groupby('insurance_type')['visit_cost'].mean()
age_effect_on_walking_speed = data[['age', 'walking_speed']].corr().loc['age', 'walking_speed']

summary_statistics = {
    "Mean Walking Speed by Education Level": mean_walking_speed_by_education,
    "Mean Costs by Insurance Type": mean_cost_by_insurance,
    "Age Effect on Walking Speed": age_effect_on_walking_speed
}

print("\nSummary Statistics:")
for key, value in summary_statistics.items():
    print(f"{key}:\n{value}\n")


