import pandas as pd

# Load the dataset
df = pd.read_csv('credit_card_fraud.csv')

# Filter rows where is_fraud is not equal to 0
filtered_df = df[df['is_fraud'] != 0]

# Group by 'category', calculate the sum of 'amt', and round to 2 decimal places
category_summary = (
    filtered_df.groupby('category')['amt']
    .sum()
    .round(2)
    .reset_index()
    .rename(columns={'amt': 'total_transaction'})
)

# Filter out rows where total_transaction is zero (equivalent to HAVING clause in SQL)
category_summary = category_summary[category_summary['total_transaction'] > 0]

# Sort by total_transaction in descending order
category_summary = category_summary.sort_values(by='total_transaction', ascending=False)

# Display the result
print(category_summary)

import pandas as pd

# Load your data
df = pd.read_csv('credit_card_fraud.csv')

# Group by state and calculate fraud rate
state_fraud = (
    df.groupby("state")
    .agg(
        total_transactions=("trans_num", "count"),
        fraud_count=("is_fraud", "sum"),
    )
    .assign(fraud_rate_percentage=lambda x: (x["fraud_count"] / x["total_transactions"]) * 100)
    .reset_index()
)

import plotly.express as px

# Create the choropleth map
fig = px.choropleth(
    state_fraud,
    locations="state",               # Column containing state abbreviations
    locationmode="USA-states",       # Use US state codes (e.g., CA, TX)
    color="fraud_rate_percentage",   # Value to plot
    color_continuous_scale="Viridis", # Color scale
    scope="usa",                     # Focus on USA
    title="Fraud Rates Across States",
    labels={"fraud_rate_percentage": "Fraud Rate (%)"}
)

# Display the map
fig.show()

# Data Prep

import pandas as pd
from datetime import datetime

# Load dataset
df = pd.read_csv('credit_card_fraud.csv')

# Calculate current year
current_year = datetime.now().year

# Convert 'dob' to datetime and calculate age
df['dob'] = pd.to_datetime(df['dob'], errors='coerce')
df['age'] = current_year - df['dob'].dt.year

# Remove rows with missing or invalid age
df = df.dropna(subset=['age'])

# Create age group column
df['age_group'] = pd.cut(
    df['age'],
    bins=[0, 30, 50, 100],
    labels=['Under 30', '30-50', 'Above 50'],
    right=False
)

# Group by age group and calculate fraud rates
age_fraud = (
    df.groupby('age_group')
    .agg(
        total_customers=('age', 'count'),
        fraud_cases=('is_fraud', 'sum')
    )
    .assign(fraud_rate=lambda x: (x['fraud_cases'] / x['total_customers']) * 100)
    .reset_index()
)

print(age_fraud)

import seaborn as sns
import matplotlib.pyplot as plt

# Plot fraud rates
sns.barplot(data=age_fraud, x='age_group', y='fraud_rate', palette='coolwarm')
plt.title('Fraud Rates by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Fraud Rate (%)')
plt.show()

from scipy.stats import chi2_contingency

# Create a contingency table for fraud cases and age groups
contingency_table = pd.crosstab(df['age_group'], df['is_fraud'])

# Perform Chi-Square Test
chi2, p, dof, expected = chi2_contingency(contingency_table)

print(f"Chi-Square Statistic: {chi2}")
print(f"P-value: {p}")

# Interpret results
if p < 0.05:
    print("There is a statistically significant association between age group and fraud likelihood.")
else:
    print("There is no statistically significant association between age group and fraud likelihood.")

import pandas as pd
from datetime import datetime

# Load dataset
df = pd.read_csv('credit_card_fraud.csv')

# Calculate current year and customer age
current_year = datetime.now().year
df['dob'] = pd.to_datetime(df['dob'], errors='coerce')
df['age'] = current_year - df['dob'].dt.year

# Remove rows with missing or invalid age
df = df.dropna(subset=['age'])

# Create specific age ranges
df['age_range'] = pd.cut(
    df['age'],
    bins=[0, 30, 40, 50, 60, 100],
    labels=['Under 30', '30-40', '41-50', '51-60', 'Above 60'],
    right=False
)

# Group by age range and calculate fraud rates
age_range_fraud = (
    df.groupby('age_range')
    .agg(
        total_customers=('age', 'count'),
        fraud_cases=('is_fraud', 'sum')
    )
    .assign(fraud_rate=lambda x: (x['fraud_cases'] / x['total_customers']) * 100)
    .reset_index()
)

print(age_range_fraud)

import seaborn as sns
import matplotlib.pyplot as plt

# Bar plot for fraud rates by age range
sns.barplot(data=age_range_fraud, x='age_range', y='fraud_rate', palette='coolwarm')
plt.title('Fraud Rates by Age Range')
plt.xlabel('Age Range')
plt.ylabel('Fraud Rate (%)')
plt.show()

from scipy.stats import chi2_contingency

# Create a contingency table for age range and fraud cases
contingency_table = pd.crosstab(df['age_range'], df['is_fraud'])

# Perform Chi-Square Test
chi2, p, dof, expected = chi2_contingency(contingency_table)

print(f"Chi-Square Statistic: {chi2}")
print(f"P-value: {p}")

# Interpretation
if p < 0.05:
    print("Fraud rates differ significantly across age ranges.")
else:
    print("No significant difference in fraud rates across age ranges.")

# Filter for fraud cases
fraud_cases = df[df['is_fraud'] == 1]

# Box plot for fraud transaction amounts by age range
sns.boxplot(data=fraud_cases, x='age_range', y='amt', palette='coolwarm')
plt.title('Transaction Amounts for Fraud Cases by Age Range')
plt.xlabel('Age Range')
plt.ylabel('Transaction Amount ($)')
plt.show()
