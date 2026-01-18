import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Step 1: Load and Explore the Data
print("=" * 60)
print("DISASTER EVENTS DATASET - INITIAL EXPLORATION")
print("=" * 60)

# Load the dataset
df = pd.read_csv('synthetic_disaster_events_2025.csv')

# Basic information
print("\n1. DATASET OVERVIEW")
print("-" * 60)
print(f"Total Records: {len(df):,}")
print(f"Total Columns: {len(df.columns)}")
print(f"\nColumn Names and Types:")
print(df.dtypes)

# First few rows
print("\n2. SAMPLE DATA (First 5 rows)")
print("-" * 60)
print(df.head())

# Check for missing values
print("\n3. MISSING VALUES CHECK")
print("-" * 60)
missing = df.isnull().sum()
missing_pct = (missing / len(df)) * 100
missing_df = pd.DataFrame({
    'Missing Count': missing,
    'Percentage': missing_pct
})
print(missing_df[missing_df['Missing Count'] > 0])

# Statistical summary
print("\n4. STATISTICAL SUMMARY")
print("-" * 60)
print(df.describe())

# Unique values in categorical columns
print("\n5. CATEGORICAL COLUMNS ANALYSIS")
print("-" * 60)
print(f"Disaster Types: {df['disaster_type'].nunique()}")
print(df['disaster_type'].value_counts())
print(f"\nLocations: {df['location'].nunique()}")
print(f"\nAid Types: {df['aid_provided'].nunique()}")
print(df['aid_provided'].value_counts())

# Date range
print("\n6. DATE RANGE")
print("-" * 60)
df['date'] = pd.to_datetime(df['date'])
print(f"From: {df['date'].min()}")
print(f"To: {df['date'].max()}")

# Severity levels
print("\n7. SEVERITY DISTRIBUTION")
print("-" * 60)
print(df['severity_level'].value_counts().sort_index())

# Major disasters
print("\n8. MAJOR DISASTERS")
print("-" * 60)
major_count = df['is_major_disaster'].sum()
print(f"Major Disasters: {major_count:,} ({(major_count/len(df)*100):.2f}%)")
print(f"Regular Events: {len(df) - major_count:,} ({((len(df)-major_count)/len(df)*100):.2f}%)")

print("\n" + "=" * 60)
print("DATA EXPLORATION COMPLETE")
print("=" * 60)
