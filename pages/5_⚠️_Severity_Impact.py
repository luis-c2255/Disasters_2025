"""
Severity & Impact Page - Understanding damage levels and consequences
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
    CHART_COLORS
)

# Page config
st.set_page_config(page_title="Severity & Impact", page_icon="⚠️", layout="wide")
apply_custom_css()

# Header
page_header("Severity & Impact Analysis", "Understanding Damage Levels and Consequences", "⚠️")

# Sidebar
st.sidebar.header("🔍 Filters")
df = load_data()
filtered_df = apply_filters(df)

# ============================================
# SEVERITY METRICS
# ============================================
st.markdown("## Severity Metrics")

# Calculate metrics
avg_severity = filtered_df['severity_level'].mean()
critical_events = len(filtered_df[filtered_df['severity_level'] >= 9])
high_severity_pct = len(filtered_df[filtered_df['severity_category'].isin(['High', 'Critical'])]) / len(filtered_df) * 100
avg_infra_damage = filtered_df['infrastructure_damage_index'].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(create_metric_card(
        title="Average Severity",
        value=f"{avg_severity:.2f}",
        delta="Out of 10",
        gradient_colors=COLOR_GRADIENTS['purple']
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_metric_card(
        title="Critical Events",
        value=f"{critical_events:,}",
        delta=f"Severity ≥ 9",
        gradient_colors=COLOR_GRADIENTS['fire']
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_metric_card(
        title="High Severity",
        value=f"{high_severity_pct:.1f}%",
        delta="High + Critical",
        gradient_colors=COLOR_GRADIENTS['orange']
    ), unsafe_allow_html=True)

with col4:
    st.markdown(create_metric_card(
        title="Avg Infrastructure",
        value=f"{avg_infra_damage:.2%}",
        delta="Damage index",
        gradient_colors=COLOR_GRADIENTS['blue']
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Insight
st.markdown(create_insight_box(
    title="Severity Overview",
    content=f"""
    The average severity level is <strong>{avg_severity:.2f}/10</strong>, with <strong>{critical_events:,} critical events</strong> (severity ≥9). 
    <strong>{high_severity_pct:.1f}% of all events</strong> are classified as high or critical severity. 
    On average, disasters damage <strong>{avg_infra_damage:.1%} of infrastructure</strong> in affected areas.
    """,
    box_type="warning"
), unsafe_allow_html=True)

# ============================================
# SEVERITY DISTRIBUTION
# ============================================
st.markdown("---")
st.markdown("## Severity Distribution")

col1, col2 = st.columns(2)

with col1:
    # Histogram of severity levels
    st.markdown("##### Severity Level Distribution")
    
    fig1 = px.histogram(
        filtered_df,
        x='severity_level',
        nbins=10,
        color_discrete_sequence=['#4cc2a6'],
        title='Distribution of Severity Levels (1-10)',
        labels={'count': 'Count', 'severity_level': 'Severity Level'}
    )
    fig1.update_traces(marker=dict(line=dict(color='white', width=1)))
    fig1.update_layout(height=400, bargap=0.1)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Severity categories pie chart
    st.markdown("##### Severity Categories")
    
    severity_counts = filtered_df['severity_category'].value_counts().reindex(['Low', 'Medium', 'High', 'Critical']).reset_index()
    severity_counts.columns = ['Category', 'Count']
    
    fig2 = px.pie(
        severity_counts,
        values='Count',
        names='Category',
        title='Proportion by Severity Category',
        color='Category',
        color_discrete_map=CHART_COLORS['severity'],
        hole=0.4
    )
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

# ============================================
# SEVERITY VS IMPACT
# ============================================
st.markdown("---")
st.markdown("## Severity vs Impact Analysis")

col1, col2 = st.columns(2)

with col1:
    # Scatter: Severity vs Affected Population
    st.markdown("##### Severity vs Affected Population")
    
    fig3 = px.scatter(
        filtered_df,
        x='severity_level',
        y='affected_population',
        color='disaster_type',
        size='estimated_economic_loss_usd',
        hover_data=['location', 'date'],
        title='Severity Level vs Affected Population',
        trendline='ols',
        labels={
            'severity_level': 'Severity Level',
            'affected_population': 'Affected Population',
            'disaster_type': 'Disaster Type'
        }
    )
    fig3.update_layout(height=450)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    # Scatter: Severity vs Economic Loss
    st.markdown("##### Severity vs Economic Loss")
    
    fig4 = px.scatter(
        filtered_df,
        x='severity_level',
        y='estimated_economic_loss_usd',
        color='severity_category',
        size='affected_population',
        hover_data=['location', 'disaster_type', 'date'],
        title='Severity Level vs Economic Loss',
        trendline='ols',
        color_discrete_map=CHART_COLORS['severity'],
        labels={
            'severity_level': 'Severity Level',
            'estimated_economic_loss_usd': 'Economic Loss ($)',
            'severity_category': 'Severity Category'
        }
    )
    fig4.update_yaxes(type='log')
    fig4.update_layout(height=450)
    st.plotly_chart(fig4, use_container_width=True)

# ============================================
# INFRASTRUCTURE DAMAGE
# ============================================
st.markdown("---")
st.markdown("## Infrastructure Damage Analysis")

col1, col2 = st.columns(2)

with col1:
    # Box plot: Infrastructure damage by severity
    st.markdown("##### Damage by Severity Category")
    
    fig5 = px.box(
        filtered_df,
        x='severity_category',
        y='infrastructure_damage_index',
        color='severity_category',
        color_discrete_map=CHART_COLORS['severity'],
        title='Infrastructure Damage Distribution by Severity',
        category_orders={'severity_category': ['Low', 'Medium', 'High', 'Critical']},
        labels={'infrastructure_damage_index': 'Infrastructure Damage Index', 
                'severity_category': 'Severity Category'}
    )
    fig5.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    # Violin plot: Infrastructure damage by disaster type
    st.markdown("##### Damage by Disaster Type")
    
    fig6 = px.violin(
        filtered_df,
        x='disaster_type',
        y='infrastructure_damage_index',
        color='disaster_type',
        box=True,
        title='Infrastructure Damage Distribution by Disaster Type',
        labels={'infrastructure_damage_index': 'Infrastructure Damage Index', 
                'disaster_type': 'Disaster Type'}
    )
    fig6.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
    st.plotly_chart(fig6, use_container_width=True)

# ============================================
# SEVERITY PROGRESSION
# ============================================
st.markdown("---")
st.markdown("## Severity Progression & Funnel Analysis")

col1, col2 = st.columns(2)

with col1:
    # Funnel chart showing event count by severity
    st.markdown("##### Event Volume by Severity")
    
    funnel_data = filtered_df['severity_category'].value_counts().reindex(['Low', 'Medium', 'High', 'Critical']).reset_index()
    funnel_data.columns = ['Severity', 'Count']
    
    fig7 = go.Figure(go.Funnel(
        y=funnel_data['Severity'],
        x=funnel_data['Count'],
        textposition='inside',
        textinfo='value+percent initial',
        marker=dict(
            color=['#90EE90', '#FFD700', '#FFA500', '#FF4500']
        )
    ))
    fig7.update_layout(
        title='Event Funnel by Severity Level',
        height=450
    )
    st.plotly_chart(fig7, use_container_width=True)

with col2:
    # Stacked area: Cumulative impact by severity
    st.markdown("##### Cumulative Impact Over Time")
    
    severity_timeline = filtered_df.groupby([
        filtered_df['date'].dt.to_period('M'),
        'severity_category'
    ])['affected_population'].sum().reset_index()
    severity_timeline.columns = ['Month', 'Severity', 'Affected']
    severity_timeline['Month'] = severity_timeline['Month'].astype(str)
    
    fig8 = px.area(
        severity_timeline,
        x='Month',
        y='Affected',
        color='Severity',
        title='Affected Population Over Time by Severity',
        color_discrete_map=CHART_COLORS['severity'],
        category_orders={'Severity': ['Low', 'Medium', 'High', 'Critical']}
    )
    fig8.update_layout(height=450, hovermode='x unified')
    st.plotly_chart(fig8, use_container_width=True)

# ============================================
# RESPONSE TIME BY SEVERITY
# ============================================
st.markdown("---")
st.markdown("## Response Time vs Severity")

col1, col2 = st.columns(2)

with col1:
    # Box plot: Response time by severity
    st.markdown("##### Response Time Distribution")
    
    fig9 = px.box(
        filtered_df,
        x='severity_category',
        y='response_time_hours',
        color='severity_category',
        color_discrete_map=CHART_COLORS['severity'],
        title='Response Time by Severity Category',
        category_orders={'severity_category': ['Low', 'Medium', 'High', 'Critical']},
        labels={'response_time_hours': 'Response Time (hours)', 'severity_category': 'Severity Category'}
    )
    fig9.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig9, use_container_width=True)

with col2:
    # Scatter: Response time vs Severity with size
    st.markdown("##### Response Efficiency")
    
    response_severity = filtered_df.sample(min(1000, len(filtered_df)))  # Sample for performance
    
    fig10 = px.scatter(
        response_severity,
        x='severity_level',
        y='response_time_hours',
        color='severity_category',
        size='affected_population',
        hover_data=['location', 'disaster_type'],
        title='Response Time vs Severity (sample)',
        color_discrete_map=CHART_COLORS['severity'],
        labels={
            'severity_level': 'Severity Level',
            'response_time_hours': 'Response Time (hours)',
            'severity_category': 'Severity Category'
        }
    )
    fig10.update_layout(height=400)
    st.plotly_chart(fig10, use_container_width=True)

# ============================================
# MAJOR DISASTERS ANALYSIS
# ============================================
st.markdown("---")
st.markdown("## Major Disasters Deep Dive")

major_disasters = filtered_df[filtered_df['is_major_disaster'] == 1]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Major Disasters", f"{len(major_disasters):,}", 
              f"{len(major_disasters)/len(filtered_df)*100:.1f}% of total")

with col2:
    st.metric("Avg Severity", f"{major_disasters['severity_level'].mean():.2f}",
              f"+{major_disasters['severity_level'].mean() - filtered_df['severity_level'].mean():.2f} vs overall")

with col3:
    st.metric("Total Affected", f"{major_disasters['affected_population'].sum()/1e6:.1f}M",
              f"{major_disasters['affected_population'].sum()/filtered_df['affected_population'].sum()*100:.1f}% of total")

with col4:
    st.metric("Total Loss", f"${major_disasters['estimated_economic_loss_usd'].sum()/1e9:.1f}B",
              f"{major_disasters['estimated_economic_loss_usd'].sum()/filtered_df['estimated_economic_loss_usd'].sum()*100:.1f}% of total")

st.markdown("<br>", unsafe_allow_html=True)

# Comparison: Major vs Regular
col1, col2 = st.columns(2)

with col1:
    st.markdown("##### Major vs Regular Disasters")
    
    comparison_df = pd.DataFrame({
        'Category': ['Major Disasters', 'Regular Events'] * 3,
        'Metric': ['Avg Severity']*2 + ['Avg Affected']*2 + ['Avg Loss ($M)']*2,
        'Value': [
            major_disasters['severity_level'].mean(),
            filtered_df[filtered_df['is_major_disaster'] == 0]['severity_level'].mean(),
            major_disasters['affected_population'].mean(),
            filtered_df[filtered_df['is_major_disaster'] == 0]['affected_population'].mean(),
            major_disasters['estimated_economic_loss_usd'].mean() / 1e6,
            filtered_df[filtered_df['is_major_disaster'] == 0]['estimated_economic_loss_usd'].mean() / 1e6
        ]
    })
    
    fig11 = px.bar(
        comparison_df,
        x='Metric',
        y='Value',
        color='Category',
        barmode='group',
        title='Major vs Regular Disasters Comparison',
        color_discrete_map={'Major Disasters': '#FF4500', 'Regular Events': '#90EE90'}
    )
    fig11.update_layout(height=400)
    st.plotly_chart(fig11, use_container_width=True)

with col2:
    st.markdown("##### Major Disasters by Type")
    
    major_by_type = major_disasters['disaster_type'].value_counts().reset_index()
    major_by_type.columns = ['Disaster Type', 'Count']
    
    fig12 = px.pie(
        major_by_type,
        values='Count',
        names='Disaster Type',
        title='Distribution of Major Disasters by Type',
        hole=0.3
    )
    fig12.update_layout(height=400)
    st.plotly_chart(fig12, use_container_width=True)

# ============================================
# HEATMAP: SEVERITY VS DISASTER TYPE
# ============================================
st.markdown("---")
st.markdown("## Severity Heatmap: Type vs Time")

# Create pivot table
heatmap_data = filtered_df.groupby([
    filtered_df['date'].dt.to_period('M'),
    'disaster_type'
])['severity_level'].mean().reset_index()
heatmap_data.columns = ['Month', 'Disaster Type', 'Avg Severity']
heatmap_data['Month'] = heatmap_data['Month'].astype(str)

# Pivot for heatmap
heatmap_pivot = heatmap_data.pivot(index='Disaster Type', columns='Month', values='Avg Severity')

fig13 = px.imshow(
    heatmap_pivot,
    labels=dict(x="Month", y="Disaster Type", color="Avg Severity"),
    color_continuous_scale='YlOrRd',
    aspect='auto',
    title='Average Severity by Disaster Type Over Time'
)
fig13.update_layout(height=500)
st.plotly_chart(fig13, use_container_width=True)

# ============================================
# DETAILED STATISTICS TABLE
# ============================================
st.markdown("---")
st.markdown("## Detailed Severity Statistics")

severity_stats = filtered_df.groupby('severity_category').agg({
    'event_id': 'count',
    'affected_population': ['sum', 'mean', 'max'],
    'estimated_economic_loss_usd': ['sum', 'mean', 'max'],
    'response_time_hours': ['mean', 'min', 'max'],
    'infrastructure_damage_index': ['mean', 'max'],
    'is_major_disaster': 'sum'
}).round(2)

severity_stats.columns = [
    'Events', 
    'Total Affected', 'Avg Affected', 'Max Affected',
    'Total Loss ($)', 'Avg Loss ($)', 'Max Loss ($)',
    'Avg Response (h)', 'Min Response (h)', 'Max Response (h)',
    'Avg Infra Damage', 'Max Infra Damage',
    'Major Disasters'
]

severity_stats = severity_stats.reindex(['Low', 'Medium', 'High', 'Critical'])

st.dataframe(
    severity_stats,
    use_container_width=True,
    column_config={
        "Events": st.column_config.NumberColumn(format="%d"),
        "Total Affected": st.column_config.NumberColumn(format="%d"),
        "Avg Affected": st.column_config.NumberColumn(format="%.0f"),
        "Max Affected": st.column_config.NumberColumn(format="%d"),
        "Total Loss ($)": st.column_config.NumberColumn(format="$%.0f"),
        "Avg Loss ($)": st.column_config.NumberColumn(format="$%.0f"),
        "Max Loss ($)": st.column_config.NumberColumn(format="$%.0f"),
        "Avg Response (h)": st.column_config.NumberColumn(format="%.1f"),
        "Min Response (h)": st.column_config.NumberColumn(format="%.1f"),
        "Max Response (h)": st.column_config.NumberColumn(format="%.1f"),
        "Avg Infra Damage": st.column_config.NumberColumn(format="%.2%"),
        "Max Infra Damage": st.column_config.NumberColumn(format="%.2%"),
        "Major Disasters": st.column_config.NumberColumn(format="%d")
    }
)

# ============================================
# EXTREME EVENTS
# ============================================
st.markdown("---")
st.markdown("## Extreme Events Analysis")

col1, col2 = st.columns(2)

with col1:
    st.markdown("##### Most Severe Events")
    extreme_events = filtered_df.nlargest(10, 'severity_level')[
        ['date', 'location', 'disaster_type', 'severity_level', 'affected_population', 'estimated_economic_loss_usd']
    ].copy()
    extreme_events['date'] = extreme_events['date'].dt.strftime('%Y-%m-%d')
    extreme_events['Loss ($M)'] = (extreme_events['estimated_economic_loss_usd'] / 1e6).round(1)
    extreme_events = extreme_events[['date', 'location', 'disaster_type', 'severity_level', 'affected_population', 'Loss ($M)']]
    extreme_events.columns = ['Date', 'Location', 'Type', 'Severity', 'Affected', 'Loss ($M)']
    
    st.dataframe(extreme_events, hide_index=True, use_container_width=True)

with col2:
    st.markdown("##### Highest Infrastructure Damage")
    infra_events = filtered_df.nlargest(10, 'infrastructure_damage_index')[
        ['date', 'location', 'disaster_type', 'infrastructure_damage_index', 'severity_level']
    ].copy()
    infra_events['date'] = infra_events['date'].dt.strftime('%Y-%m-%d')
    infra_events['Damage %'] = (infra_events['infrastructure_damage_index'] * 100).round(1)
    infra_events = infra_events[['date', 'location', 'disaster_type', 'Damage %', 'severity_level']]
    infra_events.columns = ['Date', 'Location', 'Type', 'Damage %', 'Severity']
    
    st.dataframe(infra_events, hide_index=True, use_container_width=True)

# ============================================
# RECOMMENDATIONS
# ============================================
st.markdown("---")
st.markdown("## Severity-Based Recommendations")

st.markdown(create_insight_box(
    title="Critical Severity Events (≥9)",
    content=f"""
    <strong>{critical_events:,} critical events</strong> require immediate attention. These events show:
    <ul>
        <li>Average infrastructure damage: <strong>{filtered_df[filtered_df['severity_level']>=9]['infrastructure_damage_index'].mean():.1%}</strong></li>
        <li>Average affected population: <strong>{filtered_df[filtered_df['severity_level']>=9]['affected_population'].mean():,.0f}</strong></li>
        <li>Average response time: <strong>{filtered_df[filtered_df['severity_level']>=9]['response_time_hours'].mean():.1f} hours</strong></li>
    </ul>
    <strong>Recommendation:</strong> Enhance early warning systems and pre-position resources in high-risk areas.
    """,
    box_type="warning"
), unsafe_allow_html=True)

st.markdown(create_insight_box(
    title="Infrastructure Protection",
    content=f"""
    Infrastructure damage averages <strong>{avg_infra_damage:.1%}</strong> across all events, with critical events reaching up to 
    <strong>{filtered_df['infrastructure_damage_index'].max():.1%}</strong>.
    <br><br>
    <strong>Recommendation:</strong> Invest in resilient infrastructure in high-risk zones and implement stricter building codes.
    """,
    box_type="info"
), unsafe_allow_html=True)

# ============================================
# DOWNLOAD
# ============================================
st.markdown("---")
col1, col2 = st.columns([3, 1])

with col1:
    st.info("Download severity analysis data for detailed review and reporting.")

with col2:
    csv = severity_stats.to_csv()
    st.download_button(
        label="📥 Download Data",
        data=csv,
        file_name='severity_impact_analysis.csv',
        mime='text/csv'
    )