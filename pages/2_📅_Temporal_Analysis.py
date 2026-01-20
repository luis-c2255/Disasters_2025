"""
Temporal Analysis Page - Time-based patterns and trends
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import (
    load_data,
    apply_filters,
    apply_custom_css,
    page_header,
    create_metric_card,
    create_insight_box,
    COLOR_GRADIENTS
)

# Page config
st.set_page_config(page_title="Temporal Analysis", page_icon="📅", layout="wide")
apply_custom_css()

# Header
page_header("Temporal Analysis", "Understanding When Disasters Strike", "📅")

# Sidebar
st.sidebar.header("🔍 Filters")
df = load_data()
filtered_df = apply_filters(df)

# ============================================
# TIME-BASED METRICS
# ============================================
st.markdown("## Time-Based Metrics")

col1, col2, col3, col4 = st.columns(4)

# Calculate metrics
events_per_day = len(filtered_df) / ((filtered_df['date'].max() - filtered_df['date'].min()).days + 1)
events_per_month = filtered_df.groupby(filtered_df['date'].dt.to_period('M')).size().mean()
peak_month = filtered_df.groupby('month_name').size().idxmax()
peak_quarter = filtered_df.groupby('quarter').size().idxmax()

with col1:
    st.markdown(create_metric_card(
        title="Daily Average",
        value=f"{events_per_day:.1f}",
        delta="Events per day",
        gradient_colors=COLOR_GRADIENTS['blue']
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_metric_card(
        title="Monthly Average",
        value=f"{events_per_month:.1f}",
        delta="Events per month",
        gradient_colors=COLOR_GRADIENTS['purple']
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_metric_card(
        title="Peak Month",
        value=peak_month[:3],
        delta=f"{filtered_df.groupby('month_name').size().max()} events",
        gradient_colors=COLOR_GRADIENTS['orange']
    ), unsafe_allow_html=True)

with col4:
    st.markdown(create_metric_card(
        title="Peak Quarter",
        value=f"Q{peak_quarter}",
        delta=f"{filtered_df.groupby('quarter').size().max()} events",
        gradient_colors=COLOR_GRADIENTS['pink']
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Insight
st.markdown(create_insight_box(
    title="Temporal Pattern Insight",
    content=f"""
    Disaster events show clear temporal patterns with an average of <strong>{events_per_day:.1f} events per day</strong>. 
    <strong>{peak_month}</strong> experiences the highest frequency with <strong>{filtered_df.groupby('month_name').size().max()} events</strong>,
    suggesting seasonal factors influence disaster occurrence.
    """,
    box_type="info"
), unsafe_allow_html=True)

# ============================================
# TIMELINE VISUALIZATIONS
# ============================================
st.markdown("---")
st.markdown("## Event Timeline")

col1, col2 = st.columns(2)

with col1:
    # Monthly events timeline
    st.markdown("##### Monthly Event Count")
    monthly_events = filtered_df.groupby(filtered_df['date'].dt.to_period('M')).size().reset_index()
    monthly_events.columns = ['Month', 'Events']
    monthly_events['Month'] = monthly_events['Month'].astype(str)
    
    fig1 = px.area(
        monthly_events,
        x='Month',
        y='Events',
        title='Events per Month',
        color_discrete_sequence=['#667eea']
    )
    fig1.update_layout(height=400)
    fig1.update_traces(line=dict(width=2))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Weekly pattern
    st.markdown("##### Weekly Pattern")
    weekly_pattern = filtered_df.groupby('day_of_week').size().reindex([
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ]).reset_index()
    weekly_pattern.columns = ['Day', 'Events']
    
    fig2 = px.bar(
        weekly_pattern,
        x='Day',
        y='Events',
        title='Events by Day of Week',
        color='Events',
        color_continuous_scale='Blues'
    )
    fig2.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# ============================================
# SEASONAL ANALYSIS
# ============================================
st.markdown("---")
st.markdown("## Seasonal Analysis")

col1, col2 = st.columns(2)

with col1:
    # Monthly distribution
    st.markdown("##### Monthly Distribution")
    monthly_dist = filtered_df.groupby('month_name').size().reindex([
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]).reset_index()
    monthly_dist.columns = ['Month', 'Events']
    monthly_dist['Month_Short'] = monthly_dist['Month'].str[:3]
    
    fig3 = px.bar(
        monthly_dist,
        x='Month_Short',
        y='Events',
        title='Seasonal Distribution of Disasters',
        color='Events',
        color_continuous_scale='Reds',
        text='Events'
    )
    fig3.update_traces(textposition='outside')
    fig3.update_layout(height=400, showlegend=False)
    fig3.update_xaxes(title='Month')
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    # Quarterly comparison
    st.markdown("##### Quarterly Breakdown")
    quarterly = filtered_df.groupby('quarter').agg({
        'event_id': 'count',
        'affected_population': 'sum',
        'estimated_economic_loss_usd': 'sum'
    }).reset_index()
    quarterly.columns = ['Quarter', 'Events', 'Total Affected', 'Total Loss']
    quarterly['Quarter'] = 'Q' + quarterly['Quarter'].astype(str)
    
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(
        x=quarterly['Quarter'],
        y=quarterly['Events'],
        name='Events',
        marker_color='#667eea'
    ))
    fig4.add_trace(go.Scatter(
        x=quarterly['Quarter'],
        y=quarterly['Total Affected']/1000,
        name='Affected (thousands)',
        yaxis='y2',
        mode='lines+markers',
        marker=dict(size=10, color='#f5576c'),
        line=dict(width=3)
    ))
    fig4.update_layout(
        title='Quarterly Events and Impact',
        yaxis=dict(title='Number of Events'),
        yaxis2=dict(title='Affected Population', overlaying='y', side='right'),
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig4, use_container_width=True)

# ============================================
# DISASTER TYPE OVER TIME
# ============================================
st.markdown("---")
st.markdown("## Disaster Types Over Time")

# Disaster type evolution
disaster_timeline = filtered_df.groupby([filtered_df['date'].dt.to_period('M'), 'disaster_type']).size().reset_index()
disaster_timeline.columns = ['Month', 'Disaster Type', 'Count']
disaster_timeline['Month'] = disaster_timeline['Month'].astype(str)

# Get top 5 disaster types
top_5_types = filtered_df['disaster_type'].value_counts().head(5).index.tolist()
disaster_timeline_top5 = disaster_timeline[disaster_timeline['Disaster Type'].isin(top_5_types)]

fig5 = px.line(
    disaster_timeline_top5,
    x='Month',
    y='Count',
    color='Disaster Type',
    title='Top 5 Disaster Types Evolution Over Time',
    markers=True
)
fig5.update_layout(height=450, hovermode='x unified')
st.plotly_chart(fig5, use_container_width=True)

# ============================================
# HEATMAP
# ============================================
st.markdown("---")
st.markdown("## Temporal Heatmap")

col1, col2 = st.columns(2)

with col1:
    # Month vs Day of Week heatmap
    st.markdown("###### Month vs Day of Week")
    
    heatmap_data = filtered_df.groupby(['month_name', 'day_of_week']).size().reset_index()
    heatmap_data.columns = ['Month', 'Day', 'Count']
    
    # Create pivot table
    heatmap_pivot = heatmap_data.pivot(index='Month', columns='Day', values='Count')
    heatmap_pivot = heatmap_pivot.reindex([
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ])
    heatmap_pivot = heatmap_pivot[[
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
    ]]
    
    fig6 = px.imshow(
        heatmap_pivot,
        labels=dict(x="Day of Week", y="Month", color="Events"),
        color_continuous_scale='YlOrRd',
        aspect='auto'
    )
    fig6.update_layout(height=500)
    st.plotly_chart(fig6, use_container_width=True)

with col2:
    # Quarter vs Severity heatmap
    st.markdown("###### Quarter vs Severity")
    
    severity_temporal = filtered_df.groupby(['quarter', 'severity_category']).size().reset_index()
    severity_temporal.columns = ['Quarter', 'Severity', 'Count']
    severity_temporal['Quarter'] = 'Q' + severity_temporal['Quarter'].astype(str)
    
    severity_pivot = severity_temporal.pivot(index='Severity', columns='Quarter', values='Count')
    severity_pivot = severity_pivot.reindex(['Low', 'Medium', 'High', 'Critical'])
    
    fig7 = px.imshow(
        severity_pivot,
        labels=dict(x="Quarter", y="Severity", color="Events"),
        color_continuous_scale='Reds',
        aspect='auto',
        text_auto=True
    )
    fig7.update_layout(height=500)
    st.plotly_chart(fig7, use_container_width=True)

# ============================================
# YEAR-OVER-YEAR (if applicable)
# ============================================
if filtered_df['year'].nunique() > 1:
    st.markdown("---")
    st.markdown("## Year-over-Year Comparison")
    
    yearly_comparison = filtered_df.groupby(['year', 'disaster_type']).size().reset_index()
    yearly_comparison.columns = ['Year', 'Disaster Type', 'Count']
    
    fig8 = px.bar(
        yearly_comparison,
        x='Year',
        y='Count',
        color='Disaster Type',
        title='Year-over-Year Disaster Distribution',
        barmode='stack'
    )
    fig8.update_layout(height=400)
    st.plotly_chart(fig8, use_container_width=True)

# ============================================
# SUMMARY TABLE
# ============================================
st.markdown("---")
st.markdown("## Temporal Summary Table")

# Create comprehensive summary
temporal_summary = filtered_df.groupby('month_name').agg({
    'event_id': 'count',
    'affected_population': ['sum', 'mean'],
    'estimated_economic_loss_usd': ['sum', 'mean'],
    'response_time_hours': 'mean',
    'severity_level': 'mean'
}).round(2)

temporal_summary.columns = ['Events', 'Total Affected', 'Avg Affected', 'Total Loss ($)', 'Avg Loss ($)', 'Avg Response (h)', 'Avg Severity']
temporal_summary = temporal_summary.reindex([
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
])

st.dataframe(temporal_summary, use_container_width=True)

# Download button
csv = temporal_summary.to_csv()
st.download_button(
    label="📥 Download Data",
    data=csv,
    file_name='temporal_analysis.csv',
    mime='text/csv'
)
