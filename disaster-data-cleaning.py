import pandas as pd
import numpy as np
from datetime import datetime

# Load the data
df = pd.read_csv('synthetic_disaster_events_2025.csv')

print("=" * 60)
print("DATA CLEANING & PREPROCESSING")
print("=" * 60)

# 1. Convert date to datetime
print("\n1. Converting date column to datetime...")
df['date'] = pd.to_datetime(df['date'])

# 2. Create temporal features for analysis
print("2. Creating temporal features...")
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['month_name'] = df['date'].dt.month_name()
df['quarter'] = df['date'].dt.quarter
df['day_of_week'] = df['date'].dt.day_name()
df['week_of_year'] = df['date'].dt.isocalendar().week

# 3. Handle any missing values
print("3. Handling missing values...")
initial_rows = len(df)
df = df.dropna()  # Remove rows with any missing values
print(f"   Rows removed: {initial_rows - len(df)}")

# 4. Remove duplicates if any
print("4. Checking for duplicates...")
duplicates = df.duplicated().sum()
if duplicates > 0:
    df = df.drop_duplicates()
    print(f"   Duplicates removed: {duplicates}")
else:
    print("   No duplicates found")

# 5. Validate data ranges
print("5. Validating data ranges...")
# Severity should be between reasonable bounds
df = df[(df['severity_level'] >= 1) & (df['severity_level'] <= 10)]
# Response time should be positive
df = df[df['response_time_hours'] >= 0]
# Affected population should be positive
df = df[df['affected_population'] >= 0]
# Economic loss should be non-negative
df = df[df['estimated_economic_loss_usd'] >= 0]
# Infrastructure damage index should be between 0 and 1
df = df[(df['infrastructure_damage_index'] >= 0) & (df['infrastructure_damage_index'] <= 1)]

# 6. Create categorical severity labels
print("6. Creating severity categories...")
def categorize_severity(severity):
    if severity <= 3:
        return 'Low'
    elif severity <= 6:
        return 'Medium'
    elif severity <= 8:
        return 'High'
    else:
        return 'Critical'

df['severity_category'] = df['severity_level'].apply(categorize_severity)

# 7. Create economic loss categories
print("7. Creating economic impact categories...")
def categorize_economic_loss(loss):
    if loss < 1_000_000:
        return 'Minor (<$1M)'
    elif loss < 10_000_000:
        return 'Moderate ($1M-$10M)'
    elif loss < 100_000_000:
        return 'Severe ($10M-$100M)'
    else:
        return 'Catastrophic (>$100M)'

df['economic_impact_category'] = df['estimated_economic_loss_usd'].apply(categorize_economic_loss)

# 8. Create response time categories
print("8. Creating response time categories...")
def categorize_response(hours):
    if hours < 6:
        return 'Immediate (<6h)'
    elif hours < 24:
        return 'Fast (6-24h)'
    elif hours < 72:
        return 'Moderate (24-72h)'
    else:
        return 'Slow (>72h)'

df['response_category'] = df['response_time_hours'].apply(categorize_response)

# 9. Create affected population categories
print("9. Creating population impact categories...")
def categorize_population(pop):
    if pop < 1000:
        return 'Small (<1K)'
    elif pop < 10000:
        return 'Medium (1K-10K)'
    elif pop < 100000:
        return 'Large (10K-100K)'
    else:
        return 'Very Large (>100K)'

df['population_impact_category'] = df['affected_population'].apply(categorize_population)

# 10. Save cleaned data
print("10. Saving cleaned dataset...")
df.to_csv('disaster_events_cleaned.csv', index=False)

print("\n" + "=" * 60)
print("CLEANING SUMMARY")
print("=" * 60)
print(f"Final dataset shape: {df.shape}")
print(f"Total events: {len(df):,}")
print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
print(f"Disaster types: {df['disaster_type'].nunique()}")
print(f"Locations: {df['location'].nunique()}")
print(f"\nNew columns created:")
print("- Temporal: year, month, month_name, quarter, day_of_week, week_of_year")
print("- Categories: severity_category, economic_impact_category")
print("- Categories: response_category, population_impact_category")

print("\n✓ Cleaned data saved to 'disaster_events_cleaned.csv'")
print("=" * 60)
