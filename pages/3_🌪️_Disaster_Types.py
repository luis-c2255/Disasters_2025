"""
Disaster Types Page - Deep dive into disaster categories
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
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
st.set_page_config(page_title="Disaster Types", page_icon="🌪️", layout="wide")
apply_custom_css()

# Header
page_header("Disaster Types Analysis", "Understanding Different Disaster Categories", "🌪️")

# Sidebar
st.sidebar.header("🔍 Filters")
df = load_data()
filtered_df = apply_filters(df)

# ============================================
# DISASTER TYPE METRICS
# ============================================
st.markdown("## Disaster Type Metrics")

# Calculate metrics
disaster_types_count = filtered_df['disaster_type'].nunique()
most_common = filtered_df['disaster_type'].value_counts().idxmax()
most_common_count = filtered_df['disaster_type'].value_counts().max()
most_damaging = filtered_df.groupby('disaster_type')['estimated_economic_loss_usd'].sum().idxmax()
most_damaging_loss = filtered_df.groupby('disaster_type')['estimated_economic_loss_usd'].sum().max()
highest_severity_type = filtered_df.groupby('disaster_type')['severity_level'].mean().idxmax()
highest_severity_avg = filtered_df.groupby('disaster_type')['severity_level'].mean().max()
fastest_response_type = filtered_df.groupby('disaster_type')['response_time_hours'].mean().idxmin()
fastest_response_time = filtered_df.groupby('disaster_type')['response_time_hours'].mean().min()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(create_metric_card(
        title="Disaster Categories",
        value=f"{disaster_types_count}",
        delta="Unique types",
        gradient_colors=COLOR_GRADIENTS['purple']
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_metric_card(
        title="Most Frequent",
        value=most_common[:12],
        delta=f"{most_common_count} events",
        gradient_colors=COLOR_GRADIENTS['blue']
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_metric_card(
        title="Most Damaging",
        value=most_damaging[:12],
        delta=f"${most_damaging_loss/1e9:.1f}B loss",
        gradient_colors=COLOR_GRADIENTS['fire']
    ), unsafe_allow_html=True)

with col4:
    st.markdown(create_metric_card(
        title="Highest Severity",
        value=highest_severity_type[:9],
        delta=f"{highest_severity_avg:.1f}/10 avg",
        gradient_colors=COLOR_GRADIENTS['orange']
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Insight
st.markdown(create_insight_box(
    title="Disaster Type Insights",
    content=f"""
    The dataset includes <strong>{disaster_types_count} different disaster types</strong>. 
    <strong>{most_common}</strong> is the most frequent with <strong>{most_common_count} occurrences</strong>,
    while <strong>{most_damaging}</strong> causes the most economic damage (${most_damaging_loss/1e9:.1f}B total).
    <strong>{fastest_response_type}</strong> receives the fastest average response time at <strong>{fastest_response_time:.1f} hours</strong>.
    """,
    box_type="info"
), unsafe_allow_html=True)

# ============================================
# DISTRIBUTION OVERVIEW
# ============================================
st.markdown("---")
st.markdown("## Disaster Type Distribution")

col1, col2 = st.columns(2)

with col1:
    # Pie chart
    st.markdown("##### Distribution by Event Count")
    type_counts = filtered_df['disaster_type'].value_counts().reset_index()
    type_counts.columns = ['Disaster Type', 'Count']
    
    fig1 = px.pie(
        type_counts,
        values='Count',
        names='Disaster Type',
        title='Proportion of Each Disaster Type',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    fig1.update_layout(height=450, showlegend=True)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Horizontal bar chart
    st.markdown("##### Event Count by Type")
    type_counts_sorted = type_counts.sort_values('Count', ascending=True)
    
    fig2 = px.bar(
        type_counts_sorted,
        y='Disaster Type',
        x='Count',
        orientation='h',
        color='Count',
        color_continuous_scale='Viridis',
        text='Count'
    )
    fig2.update_traces(textposition='outside')
    fig2.update_layout(height=450, showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

# ============================================
# IMPACT ANALYSIS
# ============================================
st.markdown("---")
st.markdown("## Impact Analysis by Disaster Type")

col1, col2 = st.columns(2)

with col1:
    # Affected population by type
    st.markdown("##### Total Affected Population")
    
    affected_by_type = filtered_df.groupby('disaster_type')['affected_population'].sum().sort_values(ascending=False).reset_index()
    affected_by_type.columns = ['Disaster Type', 'Total Affected']
    affected_by_type['Total Affected (M)'] = affected_by_type['Total Affected'] / 1e6
    
    fig3 = px.bar(
        affected_by_type,
        x='Disaster Type',
        y='Total Affected (M)',
        color='Total Affected (M)',
        color_continuous_scale='Reds',
        text='Total Affected (M)',
        title='Total Population Affected by Disaster Type'
    )
    fig3.update_traces(texttemplate='%{text:.2f}M', textposition='outside')
    fig3.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    # Economic loss by type
    st.markdown("##### Total Economic Loss")
    
    loss_by_type = filtered_df.groupby('disaster_type')['estimated_economic_loss_usd'].sum().sort_values(ascending=False).reset_index()
    loss_by_type.columns = ['Disaster Type', 'Total Loss']
    loss_by_type['Total Loss (B)'] = loss_by_type['Total Loss'] / 1e9
    
    fig4 = px.bar(
        loss_by_type,
        x='Disaster Type',
        y='Total Loss (B)',
        color='Total Loss (B)',
        color_continuous_scale='Oranges',
        text='Total Loss (B)',
        title='Total Economic Loss by Disaster Type'
    )
    fig4.update_traces(texttemplate='$%{text:.2f}B', textposition='outside')
    fig4.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
    st.plotly_chart(fig4, use_container_width=True)

# ============================================
# SEVERITY BREAKDOWN
# ============================================
st.markdown("---")
st.markdown("## Severity Analysis")

col1, col2 = st.columns(2)

with col1:
    # Stacked bar: severity levels within each disaster type
    st.markdown("##### Severity Distribution by Type")
    
    severity_breakdown = filtered_df.groupby(['disaster_type', 'severity_category']).size().reset_index()
    severity_breakdown.columns = ['Disaster Type', 'Severity', 'Count']
    
    # Ensure proper ordering
    severity_breakdown['Severity'] = pd.Categorical(
        severity_breakdown['Severity'],
        categories=['Low', 'Medium', 'High', 'Critical'],
        ordered=True
    )
    severity_breakdown = severity_breakdown.sort_values('Severity')
    
    fig5 = px.bar(
        severity_breakdown,
        x='Disaster Type',
        y='Count',
        color='Severity',
        title='Severity Levels Within Each Disaster Type',
        color_discrete_map=CHART_COLORS['severity'],
        barmode='stack'
    )
    fig5.update_layout(height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    # Box plot: economic loss distribution
    st.markdown("##### Economic Loss Distribution")
    
    fig6 = px.box(
        filtered_df,
        x='disaster_type',
        y='estimated_economic_loss_usd',
        color='disaster_type',
        title='Economic Loss Distribution by Disaster Type',
        labels={'estimated_economic_loss_usd': 'Economic Loss ($)'}
    )
    fig6.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
    fig6.update_yaxes(type='log')  # Log scale for better visibility
    st.plotly_chart(fig6, use_container_width=True)

# ============================================
# RESPONSE TIME ANALYSIS
# ============================================
st.markdown("---")
st.markdown("## Response Time Analysis")

col1, col2 = st.columns(2)

with col1:
    # Average response time by type
    st.markdown("##### Average Response Time")
    
    response_by_type = filtered_df.groupby('disaster_type')['response_time_hours'].mean().sort_values(ascending=False).reset_index()
    response_by_type.columns = ['Disaster Type', 'Avg Response Time (hrs)']
    
    fig7 = px.bar(
        response_by_type,
        y='Disaster Type',
        x='Avg Response Time (hrs)',
        orientation='h',
        color='Avg Response Time (hrs)',
        color_continuous_scale='RdYlGn_r',
        text='Avg Response Time (hrs)',
        title='Average Response Time by Disaster Type'
    )
    fig7.update_traces(texttemplate='%{text:.1f}h', textposition='outside')
    fig7.update_layout(height=450, showlegend=False)
    st.plotly_chart(fig7, use_container_width=True)

with col2:
    # Scatter: Response time vs Severity
    st.markdown("##### Response Time vs Severity")
    
    avg_metrics = filtered_df.groupby('disaster_type').agg({
        'response_time_hours': 'mean',
        'severity_level': 'mean',
        'event_id': 'count'
    }).reset_index()
    avg_metrics.columns = ['Disaster Type', 'Avg Response Time', 'Avg Severity', 'Event Count']
    
    fig8 = px.scatter(
        avg_metrics,
        x='Avg Severity',
        y='Avg Response Time',
        size='Event Count',
        color='Disaster Type',
        hover_data=['Disaster Type', 'Event Count'],
        title='Response Time vs Severity by Disaster Type',
        labels={
            'Avg Response Time': 'Avg Response Time (hours)',
            'Avg Severity': 'Average Severity Level'
        },
        size_max=50
    )
    fig8.add_hline(y=avg_metrics['Avg Response Time'].mean(),
                   line_dash="dash",
                   annotation_text="Overall Avg",
                   line_color="red")
    fig8.update_layout(height=450)
    st.plotly_chart(fig8, use_container_width=True)

# ============================================
# INFRASTRUCTURE DAMAGE
# ============================================
st.markdown("---")
st.markdown("## Infrastructure Damage Analysis")

col1, col2 = st.columns(2)

with col1:
    # Average infrastructure damage by type
    st.markdown("##### Average Infrastructure Damage")
    
    infra_by_type = filtered_df.groupby('disaster_type')['infrastructure_damage_index'].mean().sort_values(ascending=False).reset_index()
    infra_by_type.columns = ['Disaster Type', 'Avg Infrastructure Damage']
    infra_by_type['Damage %'] = infra_by_type['Avg Infrastructure Damage'] * 100
    
    fig9 = px.bar(
        infra_by_type,
        x='Disaster Type',
        y='Damage %',
        color='Damage %',
        color_continuous_scale='YlOrRd',
        text='Damage %',
        title='Average Infrastructure Damage Index by Type'
    )
    fig9.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig9.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
    st.plotly_chart(fig9, use_container_width=True)

with col2:
    # Violin plot: infrastructure damage distribution
    st.markdown("##### Damage Distribution")
    
    fig10 = px.violin(
        filtered_df,
        x='disaster_type',
        y='infrastructure_damage_index',
        color='disaster_type',
        box=True,
        title='Infrastructure Damage Distribution by Type',
        labels={'infrastructure_damage_index': 'Infrastructure Damage Index'}
    )
    fig10.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
    st.plotly_chart(fig10, use_container_width=True)

# ============================================
# MULTI-DIMENSIONAL COMPARISON
# ============================================
st.markdown("---")
st.markdown("## Multi-Dimensional Comparison")

# Calculate comprehensive metrics
comparison_df = filtered_df.groupby('disaster_type').agg({
    'event_id': 'count',
    'affected_population': 'mean',
    'estimated_economic_loss_usd': 'mean',
    'response_time_hours': 'mean',
    'severity_level': 'mean',
    'infrastructure_damage_index': 'mean'
}).reset_index()

comparison_df.columns = [
    'Disaster Type', 'Count', 'Avg Affected', 'Avg Loss',
    'Avg Response', 'Avg Severity', 'Avg Infra Damage'
]

# Normalize for radar chart
scaler = MinMaxScaler()

metrics_to_normalize = ['Avg Severity', 'Avg Affected', 'Avg Loss', 'Avg Infra Damage']
comparison_df[metrics_to_normalize] = scaler.fit_transform(comparison_df[metrics_to_normalize])

# Invert response time (lower is better)
comparison_df['Response Efficiency'] = 1 - scaler.fit_transform(comparison_df[['Avg Response']])

# Get top 5 disaster types
top_5_types = filtered_df['disaster_type'].value_counts().head(5).index.tolist()
top_5_comparison = comparison_df[comparison_df['Disaster Type'].isin(top_5_types)]

fig11 = go.Figure()

for idx, row in top_5_comparison.iterrows():
    fig11.add_trace(go.Scatterpolar(
        r=[
            row['Avg Severity'],
            row['Avg Affected'],
            row['Avg Loss'],
            row['Avg Infra Damage'],
            row['Response Efficiency']
        ],
        theta=['Severity', 'Population Impact', 'Economic Impact', 'Infrastructure Damage', 'Response Efficiency'],
        fill='toself',
        name=row['Disaster Type']
    ))

fig11.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
    showlegend=True,
    title="Multi-Dimensional Disaster Type Comparison (Top 5)",
    height=600
)
st.plotly_chart(fig11, use_container_width=True)

st.info("**Note**: All metrics are normalized to 0-1 scale. Higher values indicate greater impact/severity. Response Efficiency is inverted so higher is better (faster response).")

# ============================================
# COMPREHENSIVE COMPARISON TABLE
# ============================================
st.markdown("---")
st.markdown("## Detailed Comparison Table")

# Create comprehensive table
detailed_comparison = filtered_df.groupby('disaster_type').agg({
    'event_id': 'count',
    'affected_population': ['sum', 'mean', 'max'],
    'estimated_economic_loss_usd': ['sum', 'mean', 'max'],
    'response_time_hours': ['mean', 'min', 'max'],
    'severity_level': 'mean',
    'infrastructure_damage_index': 'mean',
    'is_major_disaster': 'sum'
}).round(2)

detailed_comparison.columns = [
    'Events',
    'Total Affected', 'Avg Affected', 'Max Affected',
    'Total Loss ($)', 'Avg Loss ($)', 'Max Loss ($)',
    'Avg Response (h)', 'Min Response (h)', 'Max Response (h)',
    'Avg Severity', 'Avg Infra Damage', 'Major Disasters'
]

detailed_comparison = detailed_comparison.sort_values('Events', ascending=False)

st.dataframe(
    detailed_comparison,
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
        "Avg Severity": st.column_config.NumberColumn(format="%.2f"),
        "Avg Infra Damage": st.column_config.NumberColumn(format="%.2f"),
        "Major Disasters": st.column_config.NumberColumn(format="%d")
    }
)

# ============================================
# TEMPORAL EVOLUTION
# ============================================
st.markdown("---")
st.markdown("## Temporal Evolution of Disaster Types")

# Disaster types over time
disaster_timeline = filtered_df.groupby([
    filtered_df['date'].dt.to_period('M'),
    'disaster_type'
]).size().reset_index()
disaster_timeline.columns = ['Month', 'Disaster Type', 'Count']
disaster_timeline['Month'] = disaster_timeline['Month'].astype(str)

# Show top 5 types
top_5_timeline = disaster_timeline[disaster_timeline['Disaster Type'].isin(top_5_types)]

fig12 = px.line(
    top_5_timeline,
    x='Month',
    y='Count',
    color='Disaster Type',
    title='Top 5 Disaster Types: Evolution Over Time',
    markers=True,
    line_shape='spline'
)
fig12.update_layout(height=450, hovermode='x unified')
st.plotly_chart(fig12, use_container_width=True)

# ============================================
# AID DISTRIBUTION
# ============================================
st.markdown("---")
st.markdown("## Aid Distribution by Disaster Type")

aid_by_type = filtered_df.groupby(['disaster_type', 'aid_provided']).size().reset_index()
aid_by_type.columns = ['Disaster Type', 'Aid Type', 'Count']

fig13 = px.sunburst(
    aid_by_type,
    path=['Disaster Type', 'Aid Type'],
    values='Count',
    title='Aid Distribution: Disaster Type → Aid Type Hierarchy',
    color='Count',
    color_continuous_scale='Blues'
)
fig13.update_layout(height=600)
st.plotly_chart(fig13, use_container_width=True)

# ============================================
# KEY FINDINGS
# ============================================
st.markdown("---")
st.markdown("## Key Findings by Disaster Type")

# Calculate key findings
findings_df = filtered_df.groupby('disaster_type').agg({
    'event_id': 'count',
    'affected_population': 'mean',
    'estimated_economic_loss_usd': 'mean',
    'severity_level': 'mean',
    'response_time_hours': 'mean'
}).round(2)

findings_df['Impact Score'] = (
    findings_df['severity_level'] * 0.3 +
    (findings_df['affected_population'] / findings_df['affected_population'].max()) * 10 * 0.3 +
    (findings_df['estimated_economic_loss_usd'] / findings_df['estimated_economic_loss_usd'].max()) * 10 * 0.4
).round(2)

findings_df = findings_df.sort_values('Impact Score', ascending=False)

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔴 Highest Impact Disasters")
    high_impact = findings_df.head(5).reset_index()
    high_impact.columns = ['Disaster Type', 'Events', 'Avg Affected', 'Avg Loss', 'Avg Severity', 'Avg Response', 'Impact Score']
    st.dataframe(
        high_impact[['Disaster Type', 'Impact Score', 'Avg Severity', 'Events']],
        hide_index=True,
        use_container_width=True
    )

with col2:
    st.markdown("### 🟢 Lowest Impact Disasters")
    low_impact = findings_df.tail(5).reset_index()
    low_impact.columns = ['Disaster Type', 'Events', 'Avg Affected', 'Avg Loss', 'Avg Severity', 'Avg Response', 'Impact Score']
    st.dataframe(
        low_impact[['Disaster Type', 'Impact Score', 'Avg Severity', 'Events']],
        hide_index=True,
        use_container_width=True
    )

st.info("**Impact Score** is calculated as a weighted combination of severity (30%), normalized affected population (30%), and normalized economic loss (40%).")

# ============================================
# RECOMMENDATIONS
# ============================================
st.markdown("---")
st.markdown("## Recommendations by Disaster Type")

# Create recommendations based on data
recommendations = []

for disaster_type in filtered_df['disaster_type'].unique():
    type_data = filtered_df[filtered_df['disaster_type'] == disaster_type]
    avg_response = type_data['response_time_hours'].mean()
    avg_severity = type_data['severity_level'].mean()
    event_count = len(type_data)
    
    if avg_severity > 7:
        priority = "🔴 HIGH PRIORITY"
    elif avg_severity > 5:
        priority = "🟡 MEDIUM PRIORITY"
    else:
        priority = "🟢 LOW PRIORITY"
    
    recommendation = f"**{disaster_type}** ({priority}): "
    
    if avg_response > 48:
        recommendation += "Improve response time through better preparedness. "
    if avg_severity > 7:
        recommendation += "Enhance early warning systems and evacuation procedures. "
    if event_count > filtered_df['disaster_type'].value_counts().median():
        recommendation += "High frequency - invest in prevention and mitigation strategies."
    
    recommendations.append(recommendation)

# Display recommendations
for rec in recommendations[:5]:  # Show top 5
    st.markdown(rec)

with st.expander("Show All Recommendations"):
    for rec in recommendations[5:]:
        st.markdown(rec)

# ============================================
# DOWNLOAD
# ============================================
st.markdown("---")
col1, col2 = st.columns([3, 1])

with col1:
    st.info("Download detailed disaster type comparison data for further analysis.")

with col2:
    csv = detailed_comparison.to_csv()
    st.download_button(
        label="📥 Download Data",
        data=csv,
        file_name='disaster_types_analysis.csv',
        mime='text/csv'
    )
