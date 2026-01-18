import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Global Disaster Events Dashboard 2025",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .insight-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    df = pd.read_csv('disaster_events.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# ============================================
# HEADER SECTION
# ============================================
st.markdown('<h1 class="main-header">🌍 Global Disaster Events Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Understanding Patterns, Impact, and Response in Natural Disasters</p>', unsafe_allow_html=True)

# ============================================
# SIDEBAR FILTERS
# ============================================
st.sidebar.header("🔍 Filters")

# Date range filter
date_range = st.sidebar.date_input(
    "Date Range",
    value=(df['date'].min(), df['date'].max()),
    min_value=df['date'].min(),
    max_value=df['date'].max()
)

# Disaster type filter
disaster_types = st.sidebar.multiselect(
    "Disaster Type",
    options=df['disaster_type'].unique(),
    default=df['disaster_type'].unique()
)

# Severity filter
severity_filter = st.sidebar.multiselect(
    "Severity Level",
    options=df['severity_category'].unique(),
    default=df['severity_category'].unique()
)

# Major disaster filter
major_only = st.sidebar.checkbox("Show Major Disasters Only", value=False)

# Apply filters
filtered_df = df[
    (df['date'] >= pd.to_datetime(date_range[0])) &
    (df['date'] <= pd.to_datetime(date_range[1])) &
    (df['disaster_type'].isin(disaster_types)) &
    (df['severity_category'].isin(severity_filter))
]

if major_only:
    filtered_df = filtered_df[filtered_df['is_major_disaster'] == 1]

# ============================================
# STORYTELLING: EXECUTIVE SUMMARY
# ============================================
st.header("📊 Executive Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Events",
        value=f"{len(filtered_df):,}",
        delta=f"{len(filtered_df)/len(df)*100:.1f}% of dataset"
    )

with col2:
    st.metric(
        label="People Affected",
        value=f"{filtered_df['affected_population'].sum()/1e6:.2f}M",
        delta=f"Avg: {filtered_df['affected_population'].mean():,.0f}"
    )

with col3:
    st.metric(
        label="Economic Loss",
        value=f"${filtered_df['estimated_economic_loss_usd'].sum()/1e9:.2f}B",
        delta=f"Avg: ${filtered_df['estimated_economic_loss_usd'].mean()/1e6:.1f}M"
    )

with col4:
    st.metric(
        label="Avg Response Time",
        value=f"{filtered_df['response_time_hours'].mean():.1f}h",
        delta=f"Median: {filtered_df['response_time_hours'].median():.1f}h"
    )

# Key Insight Box
st.markdown(f"""
<div class="insight-box">
    <h3>💡 Key Insight</h3>
    <p>The data shows <strong>{len(filtered_df[filtered_df['is_major_disaster']==1]):,}</strong> major disasters 
    affecting <strong>{filtered_df[filtered_df['is_major_disaster']==1]['affected_population'].sum()/1e6:.2f} million people</strong> 
    with total economic losses exceeding <strong>${filtered_df['estimated_economic_loss_usd'].sum()/1e9:.2f} billion</strong>. 
    The most frequent disaster type is <strong>{filtered_df['disaster_type'].mode()[0]}</strong>.</p>
</div>
""", unsafe_allow_html=True)

# ============================================
# SECTION 1: TEMPORAL PATTERNS
# ============================================
st.header("📅 Temporal Patterns: When Do Disasters Strike?")

col1, col2 = st.columns(2)

with col1:
    # Events over time
    events_timeline = filtered_df.groupby(filtered_df['date'].dt.to_period('M')).size().reset_index()
    events_timeline.columns = ['Month', 'Events']
    events_timeline['Month'] = events_timeline['Month'].astype(str)
    
    fig_timeline = px.line(
        events_timeline,
        x='Month',
        y='Events',
        title='Disaster Events Over Time',
        markers=True
    )
    fig_timeline.update_layout(height=400)
    st.plotly_chart(fig_timeline, use_container_width=True)

with col2:
    # Monthly distribution
    monthly_dist = filtered_df.groupby('month_name').size().reindex([
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]).reset_index()
    monthly_dist.columns = ['Month', 'Events']
    
    fig_monthly = px.bar(
        monthly_dist,
        x='Month',
        y='Events',
        title='Seasonal Distribution of Disasters',
        color='Events',
        color_continuous_scale='Reds'
    )
    fig_monthly.update_layout(height=400)
    st.plotly_chart(fig_monthly, use_container_width=True)

st.markdown(f"""
**Analysis**: Peak disaster activity occurs in **{monthly_dist.loc[monthly_dist['Events'].idxmax(), 'Month']}** 
with {monthly_dist['Events'].max()} events, suggesting potential seasonal patterns in disaster occurrence.
""")

# ============================================
# SECTION 2: DISASTER TYPES
# ============================================
st.header("🌪️ Disaster Types: Understanding the Threats")

col1, col2 = st.columns(2)

with col1:
    # Disaster type distribution
    disaster_dist = filtered_df['disaster_type'].value_counts().reset_index()
    disaster_dist.columns = ['Disaster Type', 'Count']
    
    fig_disaster_pie = px.pie(
        disaster_dist,
        values='Count',
        names='Disaster Type',
        title='Distribution by Disaster Type',
        hole=0.4
    )
    fig_disaster_pie.update_layout(height=400)
    st.plotly_chart(fig_disaster_pie, use_container_width=True)

with col2:
    # Impact by disaster type
    impact_by_type = filtered_df.groupby('disaster_type').agg({
        'affected_population': 'sum',
        'estimated_economic_loss_usd': 'sum'
    }).reset_index()
    
    fig_impact = go.Figure()
    fig_impact.add_trace(go.Bar(
        x=impact_by_type['disaster_type'],
        y=impact_by_type['affected_population'],
        name='Affected Population',
        marker_color='indianred'
    ))
    fig_impact.update_layout(
        title='Total Impact by Disaster Type',
        yaxis_title='Affected Population',
        height=400
    )
    st.plotly_chart(fig_impact, use_container_width=True)

# ============================================
# SECTION 3: SEVERITY AND IMPACT
# ============================================
st.header("⚠️ Severity and Impact: Measuring the Damage")

col1, col2, col3 = st.columns(3)

with col1:
    # Severity distribution
    severity_dist = filtered_df['severity_category'].value_counts().reset_index()
    severity_dist.columns = ['Severity', 'Count']
    
    fig_severity = px.bar(
        severity_dist,
        x='Severity',
        y='Count',
        title='Severity Distribution',
        color='Severity',
        color_discrete_map={
            'Low': '#90EE90',
            'Medium': '#FFD700',
            'High': '#FFA500',
            'Critical': '#FF4500'
        }
    )
    fig_severity.update_layout(height=350)
    st.plotly_chart(fig_severity, use_container_width=True)

with col2:
    # Economic impact categories
    econ_dist = filtered_df['economic_impact_category'].value_counts().reset_index()
    econ_dist.columns = ['Category', 'Count']
    
    fig_econ = px.bar(
        econ_dist,
        x='Category',
        y='Count',
        title='Economic Impact Distribution',
        color='Count',
        color_continuous_scale='Oranges'
    )
    fig_econ.update_layout(height=350, xaxis_tickangle=-45)
    st.plotly_chart(fig_econ, use_container_width=True)

with col3:
    # Population impact
    pop_dist = filtered_df['population_impact_category'].value_counts().reset_index()
    pop_dist.columns = ['Category', 'Count']
    
    fig_pop = px.bar(
        pop_dist,
        x='Category',
        y='Count',
        title='Population Impact Distribution',
        color='Count',
        color_continuous_scale='Blues'
    )
    fig_pop.update_layout(height=350, xaxis_tickangle=-45)
    st.plotly_chart(fig_pop, use_container_width=True)

# ============================================
# SECTION 4: GEOGRAPHIC ANALYSIS
# ============================================
st.header("🗺️ Geographic Patterns: Where Disasters Occur")

col1, col2 = st.columns([2, 1])

with col1:
    # Map visualization
    fig_map = px.scatter_geo(
        filtered_df,
        lat='latitude',
        lon='longitude',
        color='severity_level',
        size='affected_population',
        hover_data=['location', 'disaster_type', 'date'],
        title='Global Distribution of Disaster Events',
        color_continuous_scale='Reds',
        size_max=20
    )
    fig_map.update_layout(height=500)
    st.plotly_chart(fig_map, use_container_width=True)

with col2:
    # Top affected locations
    top_locations = filtered_df['location'].value_counts().head(10).reset_index()
    top_locations.columns = ['Location', 'Events']
    
    st.subheader("Top 10 Affected Locations")
    st.dataframe(top_locations, use_container_width=True, height=400)

# ============================================
# SECTION 5: RESPONSE ANALYSIS
# ============================================
st.header("🚨 Response Analysis: Speed and Effectiveness")

col1, col2 = st.columns(2)

with col1:
    # Response time by disaster type
    response_by_type = filtered_df.groupby('disaster_type')['response_time_hours'].mean().reset_index()
    response_by_type = response_by_type.sort_values('response_time_hours', ascending=False)
    
    fig_response = px.bar(
        response_by_type,
        x='response_time_hours',
        y='disaster_type',
        orientation='h',
        title='Average Response Time by Disaster Type',
        color='response_time_hours',
        color_continuous_scale='RdYlGn_r'
    )
    fig_response.update_layout(height=400)
    st.plotly_chart(fig_response, use_container_width=True)

with col2:
    # Aid distribution
    aid_dist = filtered_df['aid_provided'].value_counts().reset_index()
    aid_dist.columns = ['Aid Type', 'Count']
    
    fig_aid = px.pie(
        aid_dist,
        values='Count',
        names='Aid Type',
        title='Aid Distribution by Type',
        hole=0.3
    )
    fig_aid.update_layout(height=400)
    st.plotly_chart(fig_aid, use_container_width=True)

# Response time analysis
avg_response = filtered_df['response_time_hours'].mean()
best_disaster = response_by_type.iloc[-1]
worst_disaster = response_by_type.iloc[0]

st.markdown(f"""
**Response Insights**: Average response time is **{avg_response:.1f} hours**. 
**{best_disaster['disaster_type']}** events receive the fastest response ({best_disaster['response_time_hours']:.1f}h), 
while **{worst_disaster['disaster_type']}** events take longer ({worst_disaster['response_time_hours']:.1f}h).
""")

# ============================================
# SECTION 6: CORRELATIONS
# ============================================
st.header("🔗 Relationships: Understanding Connections")

# Correlation heatmap
corr_cols = ['severity_level', 'affected_population', 'estimated_economic_loss_usd', 
             'response_time_hours', 'infrastructure_damage_index']
corr_matrix = filtered_df[corr_cols].corr()

fig_corr = px.imshow(
    corr_matrix,
    text_auto='.2f',
    aspect='auto',
    title='Correlation Matrix of Key Variables',
    color_continuous_scale='RdBu_r'
)
fig_corr.update_layout(height=500)
st.plotly_chart(fig_corr, use_container_width=True)

# Scatter plots
col1, col2 = st.columns(2)

with col1:
    fig_scatter1 = px.scatter(
        filtered_df,
        x='severity_level',
        y='affected_population',
        color='disaster_type',
        title='Severity vs Affected Population',
        trendline='ols'
    )
    st.plotly_chart(fig_scatter1, use_container_width=True)

with col2:
    fig_scatter2 = px.scatter(
        filtered_df,
        x='response_time_hours',
        y='estimated_economic_loss_usd',
        color='severity_category',
        title='Response Time vs Economic Loss',
        trendline='ols'
    )
    st.plotly_chart(fig_scatter2, use_container_width=True)

# ============================================
# SECTION 7: DATA TABLE
# ============================================
st.header("📋 Detailed Data Explorer")

# Show detailed table
st.dataframe(
    filtered_df[[
        'date', 'disaster_type', 'location', 'severity_category',
        'affected_population', 'estimated_economic_loss_usd',
        'response_time_hours', 'aid_provided'
    ]].head(100),
    use_container_width=True
)

# Download button
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name='filtered_disaster_data.csv',
    mime='text/csv'
)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🌍 Global Disaster Events Dashboard 2025 | Data-Driven Insights for Disaster Management</p>
    <p>Created with Streamlit • Data processed with Python & Pandas</p>
</div>
""", unsafe_allow_html=True)
