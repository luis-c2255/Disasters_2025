import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Load cleaned data
df = pd.read_csv('disaster_events_cleaned.csv')
df['date'] = pd.to_datetime(df['date'])

print("=" * 60)
print("DISASTER EVENTS ANALYSIS & VISUALIZATIONS")
print("=" * 60)

# ============================================
# 1. TEMPORAL ANALYSIS
# ============================================
print("\n1. TEMPORAL PATTERNS")
print("-" * 60)

# Events over time
events_by_month = df.groupby(df['date'].dt.to_period('M')).size()
print(f"Average events per month: {events_by_month.mean():.1f}")

# Seasonal analysis
seasonal = df.groupby('month_name').size().reindex([
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
])
print(f"Peak month: {seasonal.idxmax()} ({seasonal.max()} events)")

# ============================================
# 2. DISASTER TYPE ANALYSIS
# ============================================
print("\n2. DISASTER TYPE ANALYSIS")
print("-" * 60)

disaster_summary = df.groupby('disaster_type').agg({
    'event_id': 'count',
    'affected_population': 'sum',
    'estimated_economic_loss_usd': 'sum',
    'severity_level': 'mean',
    'response_time_hours': 'mean'
}).round(2)
disaster_summary.columns = ['Count', 'Total Affected', 'Total Loss ($)', 'Avg Severity', 'Avg Response (hrs)']
disaster_summary = disaster_summary.sort_values('Count', ascending=False)
print(disaster_summary)

# ============================================
# 3. SEVERITY ANALYSIS
# ============================================
print("\n3. SEVERITY ANALYSIS")
print("-" * 60)

severity_dist = df['severity_category'].value_counts()
print(severity_dist)

# Major disasters analysis
major_disasters = df[df['is_major_disaster'] == 1]
print(f"\nMajor Disasters: {len(major_disasters):,}")
print(f"Total affected by major disasters: {major_disasters['affected_population'].sum():,}")
print(f"Total economic loss from major disasters: ${major_disasters['estimated_economic_loss_usd'].sum():,.0f}")

# ============================================
# 4. GEOGRAPHIC ANALYSIS
# ============================================
print("\n4. GEOGRAPHIC ANALYSIS")
print("-" * 60)

top_locations = df['location'].value_counts().head(10)
print("Top 10 Most Affected Locations:")
print(top_locations)

# ============================================
# 5. RESPONSE TIME ANALYSIS
# ============================================
print("\n5. RESPONSE TIME ANALYSIS")
print("-" * 60)

response_stats = df.groupby('disaster_type')['response_time_hours'].agg(['mean', 'median', 'min', 'max']).round(2)
print(response_stats)

# ============================================
# 6. ECONOMIC IMPACT ANALYSIS
# ============================================
print("\n6. ECONOMIC IMPACT ANALYSIS")
print("-" * 60)

total_loss = df['estimated_economic_loss_usd'].sum()
avg_loss = df['estimated_economic_loss_usd'].mean()
print(f"Total Economic Loss: ${total_loss:,.0f}")
print(f"Average Loss per Event: ${avg_loss:,.0f}")

economic_by_type = df.groupby('disaster_type')['estimated_economic_loss_usd'].sum().sort_values(ascending=False)
print(f"\nMost Economically Damaging Disaster Type: {economic_by_type.idxmax()} (${economic_by_type.max():,.0f})")

# ============================================
# 7. CORRELATION ANALYSIS
# ============================================
print("\n7. CORRELATION ANALYSIS")
print("-" * 60)

correlations = df[['severity_level', 'affected_population', 'estimated_economic_loss_usd', 
                   'response_time_hours', 'infrastructure_damage_index']].corr()
print(correlations)

# ============================================
# 8. KEY INSIGHTS
# ============================================
print("\n" + "=" * 60)
print("KEY INSIGHTS")
print("=" * 60)

print(f"1. Dataset contains {len(df):,} disaster events")
print(f"2. {len(major_disasters):,} ({len(major_disasters)/len(df)*100:.1f}%) are classified as major disasters")
print(f"3. Total population affected: {df['affected_population'].sum():,}")
print(f"4. Total economic loss: ${df['estimated_economic_loss_usd'].sum():,.0f}")
print(f"5. Average response time: {df['response_time_hours'].mean():.1f} hours")
print(f"6. Most common disaster type: {df['disaster_type'].mode()[0]}")
print(f"7. Highest severity events: {len(df[df['severity_level'] >= 9]):,}")
print(f"8. Average infrastructure damage: {df['infrastructure_damage_index'].mean():.2%}")

print("\n✓ Analysis complete! Ready for dashboard creation.")
print("=" * 60)
