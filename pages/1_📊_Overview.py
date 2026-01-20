"""
Overview Page - Executive Summary and Key Metrics
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import (
    load_data,
    apply_filters,
    apply_custom_css,
    page_header,
    create_metric_card,
    create_insight_box,
    COLOR_GRADIENTS,
    get_summary_stats
)

# Page config
st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")
apply_custom_css()

# Header
page_header("Executive Overview", "High-Level Metrics and Trends", "📊")

# Sidebar
st.sidebar.header("🔍 Filters")
df = load_data()
filtered_df = apply_filters(df)

# Get summary stats
stats = get_summary_stats(filtered_df)

# ============================================
# KEY METRICS CARDS
# ============================================
st.markdown("## Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(create_metric_card(
        title="Total Events",
        value=f"{stats['total_events']:,}",
        delta=f"📈 {stats['total_events']/len(df)*100:.1f}% of dataset",
        gradient_colors=COLOR_GRADIENTS['purple']
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_metric_card(
        title="People Affected",
        value=f"{stats['total_affected']/1e6:.2f}M",
        delta=f"👥 Avg: {stats['avg_affected']:,.0f}",
        gradient_colors=COLOR_GRADIENTS['pink']
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_metric_card(
        title="Economic Loss",
        value=f"${stats['total_economic_loss']/1e9:.2f}B",
        delta=f"💵 Avg: ${stats['avg_economic_loss']/1e6:.1f}M",
        gradient_colors=COLOR_GRADIENTS['blue']
    ), unsafe_allow_html=True)

with col4:
    st.markdown(create_metric_card(
        title="Avg Response Time",
        value=f"{stats['avg_response_time']:.1f}h",
        delta=f"⏱️ Median: {stats['median_response_time']:.1f}h",
        gradient_colors=COLOR_GRADIENTS['orange']
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================
# KEY INSIGHT
# ============================================
major_pct = stats['major_disasters']/stats['total_events']*100

st.markdown(create_insight_box(
    title="Executive Summary",
    content=f"""
    The analysis covers <strong>{stats['total_events']:,} disaster events</strong> over <strong>{stats['date_range_days']} days</strong> across <strong>{stats['unique_locations']} unique locations</strong>. 
    <strong>{stats['major_disasters']:,} events ({major_pct:.1f}%)</strong> are classified as major disasters,
    affecting <strong>{stats['total_affected']/1e6:.2f} million people</strong> with economic losses exceeding
    <strong>${stats['total_economic_loss']/1e9:.2f} billion</strong>. The most common disaster type is
    <strong>{filtered_df['disaster_type'].mode()[0]}</strong>.
    """,
    box_type="info"
), unsafe_allow_html=True)

# ============================================
# CHARTS SECTION
# ============================================
st.markdown("---")
st.markdown("## Trend Analysis")

col1, col2 = st.columns(2)

with col1:
    # Events trend over time
    st.markdown("##### Events Over Time")
    
    events_daily = filtered_df.groupby(filtered_df['date'].dt.to_period('D')).size().reset_index()
    events_daily.columns = ['Date', 'Events']
    events_daily['Date'] = events_daily['Date'].astype(str)
    events_daily['MA_7'] = events_daily['Events'].rolling(window=7, min_periods=1).mean()
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=events_daily['Date'],
        y=events_daily['Events'],
        name='Daily Events',
        mode='lines',
        line=dict(color='lightblue', width=1),
        opacity=0.5
    ))
    fig1.add_trace(go.Scatter(
        x=events_daily['Date'],
        y=events_daily['MA_7'],
        name='7-Day Moving Avg',
        mode='lines',
        line=dict(color='#667eea', width=3)
    ))
    fig1.update_layout(
        height=350,
        hovermode='x unified',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Cumulative affected population
    st.markdown("##### Cumulative Impact")
    
    cumulative_df = filtered_df.sort_values('date').copy()
    cumulative_df['Cumulative_Affected'] = cumulative_df['affected_population'].cumsum()
    cumulative_df['Cumulative_Loss'] = cumulative_df['estimated_economic_loss_usd'].cumsum()
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=cumulative_df['date'],
        y=cumulative_df['Cumulative_Affected'],
        name='Affected Population',
        fill='tozeroy',
        line=dict(color='#f5576c', width=2)
    ))
    fig2.update_layout(
        height=350,
        yaxis_title='Cumulative Affected Population',
        hovermode='x unified'
    )
    st.plotly_chart(fig2, use_container_width=True)

# ============================================
# DISTRIBUTION ANALYSIS
# ============================================
st.markdown("---")
st.markdown("## Distribution Analysis")

col1, col2 = st.columns(2)

with col1:
    # Disaster type distribution
    st.markdown("##### Disaster Type Distribution")
    
    type_dist = filtered_df['disaster_type'].value_counts().reset_index()
    type_dist.columns = ['Disaster Type', 'Count']
    
    fig3 = px.bar(
        type_dist,
        x='Count',
        y='Disaster Type',
        orientation='h',
        color='Count',
        color_continuous_scale='Viridis',
        text='Count'
    )
    fig3.update_traces(textposition='outside')
    fig3.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    # Severity distribution with economic impact
    st.markdown("##### Severity vs Economic Impact")
    
    severity_impact = filtered_df.groupby('severity_category').agg({
        'event_id': 'count',
        'estimated_economic_loss_usd': 'sum'
    }).reset_index()
    severity_impact.columns = ['Severity', 'Count', 'Total Loss']
    severity_impact['Severity'] = pd.Categorical(
        severity_impact['Severity'],
        categories=['Low', 'Medium', 'High', 'Critical'],
        ordered=True
    )
    severity_impact = severity_impact.sort_values('Severity')
    
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        x=severity_impact['Severity'],
        y=severity_impact['Count'],
        name='Event Count',
        marker_color='#667eea',
        yaxis='y'
    ))
    fig4.add_trace(go.Scatter(
        x=severity_impact['Severity'],
        y=severity_impact['Total Loss']/1e9,
        name='Total Loss ($B)',
        marker_color='#f5576c',
        yaxis='y2',
        mode='lines+markers',
        line=dict(width=3)
    ))
    fig4.update_layout(
        height=400,
        yaxis=dict(title='Event Count'),
        yaxis2=dict(title='Total Loss ($B)', overlaying='y', side='right'),
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig4, use_container_width=True)

# ============================================
# TOP PERFORMERS
# ============================================
st.markdown("---")
st.markdown("## Rankings and Comparisons")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("##### Most Frequent Disasters")
    top_disasters = filtered_df['disaster_type'].value_counts().head(5).reset_index()
    top_disasters.columns = ['Type', 'Count']
    top_disasters['Percentage'] = (top_disasters['Count'] / len(filtered_df) * 100).round(1)
    st.dataframe(
        top_disasters,
        column_config={
            "Type": "Disaster Type",
            "Count": st.column_config.NumberColumn("Events", format="%d"),
            "Percentage": st.column_config.NumberColumn("% of Total", format="%.1f%%")
        },
        hide_index=True,
        use_container_width=True
    )

with col2:
    st.markdown("##### Most Affected Locations")
    top_locations = filtered_df.groupby('location')['affected_population'].sum().sort_values(ascending=False).head(5).reset_index()
    top_locations.columns = ['Location', 'Total Affected']
    top_locations['Avg Per Event'] = (
        filtered_df.groupby('location')['affected_population'].mean().sort_values(ascending=False).head(5).values
    ).astype(int)
    st.dataframe(
        top_locations,
        column_config={
            "Location": "Location",
            "Total Affected": st.column_config.NumberColumn("Total Affected", format="%d"),
            "Avg Per Event": st.column_config.NumberColumn("Avg Per Event", format="%d")
        },
        hide_index=True,
        use_container_width=True
    )

with col3:
    st.markdown("##### Highest Economic Losses")
    top_losses = filtered_df.nlargest(5, 'estimated_economic_loss_usd')[['location', 'disaster_type', 'estimated_economic_loss_usd']].copy()
    top_losses.columns = ['Location', 'Type', 'Loss ($)']
    top_losses['Loss ($)'] = top_losses['Loss ($)'].apply(lambda x: f"${x/1e6:.1f}M")
    st.dataframe(
        top_losses,
        hide_index=True,
        use_container_width=True
    )

# ============================================
# COMPARISON CHART
# ============================================
st.markdown("---")
st.markdown("## Multi-Dimensional Comparison")

# Disaster type comparison
comparison_df = filtered_df.groupby('disaster_type').agg({
    'event_id': 'count',
    'affected_population': 'mean',
    'estimated_economic_loss_usd': 'mean',
    'response_time_hours': 'mean',
    'severity_level': 'mean',
    'infrastructure_damage_index': 'mean'
}).reset_index()

comparison_df.columns = ['Disaster Type', 'Count', 'Avg Affected', 'Avg Loss', 'Avg Response', 'Avg Severity', 'Avg Infrastructure Damage']

# Create radar chart for top 3 disaster types
top_3_disasters = comparison_df.nlargest(3, 'Count')

fig5 = go.Figure()

for idx, row in top_3_disasters.iterrows():
    fig5.add_trace(go.Scatterpolar(
        r=[
            row['Avg Severity']/10,  # Normalize to 0-1
            row['Avg Affected']/top_3_disasters['Avg Affected'].max(),
            row['Avg Loss']/top_3_disasters['Avg Loss'].max(),
            row['Avg Infrastructure Damage'],
            1 - (row['Avg Response']/top_3_disasters['Avg Response'].max())  # Invert: faster is better
        ],
        theta=['Severity', 'Population Impact', 'Economic Impact', 'Infrastructure Damage', 'Response Speed'],
        fill='toself',
        name=row['Disaster Type']
    ))

fig5.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
    showlegend=True,
    title="Multi-Dimensional Disaster Comparison (Top 3)",
    height=500
)
st.plotly_chart(fig5, use_container_width=True)

st.markdown("""
**Note**: All metrics are normalized to 0-1 scale. Higher values indicate greater impact/severity,
except for Response Speed where higher is better (faster response).
""")

# ============================================
# DATA EXPORT
# ============================================
st.markdown("---")
st.markdown("## Export Data")

col1, col2 = st.columns([3, 1])

with col1:
    st.info("Download the filtered dataset for further analysis in your preferred tools.")

with col2:
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data",
        data=csv,
        file_name='disaster_overview_data.csv',
        mime='text/csv'
    )
