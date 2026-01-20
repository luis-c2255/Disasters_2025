"""
Response Analysis Page - Evaluating emergency response effectiveness
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
    COLOR_GRADIENTS
)

# Page config
st.set_page_config(page_title="Response Analysis", page_icon="🚨", layout="wide")
apply_custom_css()

# Header
page_header("Response Analysis", "Evaluating Emergency Response Effectiveness", "🚨")

# Sidebar
st.sidebar.header("🔍 Filters")
df = load_data()
filtered_df = apply_filters(df)

# ============================================
# RESPONSE METRICS
# ============================================
st.markdown("## Response Metrics")

# Calculate metrics
overall_avg_response = filtered_df['response_time_hours'].mean()
median_response = filtered_df['response_time_hours'].median()
fastest_response = filtered_df['response_time_hours'].min()
slowest_response = filtered_df['response_time_hours'].max()
immediate_responses = len(filtered_df[filtered_df['response_time_hours'] < 6])
most_common_aid = filtered_df['aid_provided'].mode()[0]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(create_metric_card(
        title="Avg Response Time",
        value=f"{overall_avg_response:.1f}h",
        delta=f"Median: {median_response:.1f}h",
        gradient_colors=COLOR_GRADIENTS['blue']
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_metric_card(
        title="Fastest Response",
        value=f"{fastest_response:.1f}h",
        delta=f"Slowest: {slowest_response:.1f}h",
        gradient_colors=COLOR_GRADIENTS['green']
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_metric_card(
        title="Immediate Response",
        value=f"{immediate_responses:,}",
        delta=f"{immediate_responses/len(filtered_df)*100:.1f}% (<6h)",
        gradient_colors=COLOR_GRADIENTS['purple']
    ), unsafe_allow_html=True)

with col4:
    st.markdown(create_metric_card(
        title="Primary Aid Type",
        value=most_common_aid[:12],
        delta="Most common",
        gradient_colors=COLOR_GRADIENTS['pink']
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Insight
st.markdown(create_insight_box(
    title="Response Effectiveness Overview",
    content=f"""
    The average response time is <strong>{overall_avg_response:.1f} hours</strong>, with <strong>{immediate_responses:,} events 
    ({immediate_responses/len(filtered_df)*100:.1f}%)</strong> receiving immediate response (under 6 hours). 
    The fastest recorded response was <strong>{fastest_response:.1f} hours</strong>, while the slowest took 
    <strong>{slowest_response:.1f} hours</strong>. <strong>{most_common_aid}</strong> is the most commonly provided aid type.
    """,
    box_type="info"
), unsafe_allow_html=True)

# ============================================
# RESPONSE TIME DISTRIBUTION
# ============================================
st.markdown("---")
st.markdown("## Response Time Distribution")

col1, col2 = st.columns(2)

with col1:
    # Histogram of response times
    st.markdown("##### Response Time Histogram")
    
    fig1 = px.histogram(
        filtered_df,
        x='response_time_hours',
        nbins=50,
        color_discrete_sequence=['#667eea'],
        title='Distribution of Response Times',
        labels={'response_time_hours': 'Response Time (hours)', 'count': 'Number of Events'}
    )
    fig1.add_vline(x=overall_avg_response, line_dash="dash", 
                   annotation_text=f"Avg: {overall_avg_response:.1f}h", line_color="red")
    fig1.update_layout(height=400)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Response categories pie chart
    st.markdown("##### Response Categories")
    
    response_cats = filtered_df['response_category'].value_counts().reindex([
        'Immediate (<6h)', 'Fast (6-24h)', 'Moderate (24-72h)', 'Slow (>72h)'
    ], fill_value=0).reset_index()
    response_cats.columns = ['Category', 'Count']
    
    fig2 = px.pie(
        response_cats,
        values='Count',
        names='Category',
        title='Proportion by Response Speed',
        hole=0.4,
        color_discrete_sequence=['#00ff00', '#90EE90', '#FFD700', '#FF4500']
    )
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

# ============================================
# RESPONSE BY DISASTER TYPE
# ============================================
st.markdown("---")
st.markdown("## Response Time by Disaster Type")

col1, col2 = st.columns(2)

with col1:
    # Average response time by type
    st.markdown("##### Average Response Time")
    
    response_by_type = filtered_df.groupby('disaster_type')['response_time_hours'].mean().sort_values(ascending=False).reset_index()
    response_by_type.columns = ['Disaster Type', 'Avg Response Time (h)']
    
    fig3 = px.bar(
        response_by_type,
        y='Disaster Type',
        x='Avg Response Time (h)',
        orientation='h',
        color='Avg Response Time (h)',
        color_continuous_scale='RdYlGn_r',
        text='Avg Response Time (h)',
        title='Average Response Time by Disaster Type'
    )
    fig3.update_traces(texttemplate='%{text:.1f}h', textposition='outside')
    fig3.update_layout(height=450, showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    # Box plot: Response time distribution by type
    st.markdown("##### Response Time Distribution")
    
    fig4 = px.box(
        filtered_df,
        x='disaster_type',
        y='response_time_hours',
        color='disaster_type',
        title='Response Time Distribution by Disaster Type',
        labels={'response_time_hours': 'Response Time (hours)',
                'disaster_type': 'Disaster Type'}
    )
    fig4.update_layout(height=450, showlegend=False, xaxis_tickangle=-45)
    st.plotly_chart(fig4, use_container_width=True)

# ============================================
# RESPONSE VS SEVERITY
# ============================================
st.markdown("---")
st.markdown("## Response Time vs Severity")

col1, col2 = st.columns(2)

with col1:
    # Scatter: Response time vs severity
    st.markdown("##### Response Time vs Severity Level")
    
    fig5 = px.scatter(
        filtered_df.sample(min(1000, len(filtered_df))),
        x='severity_level',
        y='response_time_hours',
        color='disaster_type',
        size='affected_population',
        hover_data=['location', 'date'],
        title='Response Time vs Severity (sample)',
        trendline='ols',
        labels={
            'severity_level': 'Severity Level',
            'response_time_hours': 'Response Time (hours)'
        }
    )
    fig5.update_layout(height=450)
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    # Box plot: Response time by severity category
    st.markdown("##### Response by Severity Category")
    
    fig6 = px.box(
        filtered_df,
        x='severity_category',
        y='response_time_hours',
        color='severity_category',
        color_discrete_map={
            'Low': '#90EE90',
            'Medium': '#FFD700',
            'High': '#FFA500',
            'Critical': '#FF4500'
        },
        category_orders={'severity_category': ['Low', 'Medium', 'High', 'Critical']},
        title='Response Time by Severity Category',
        labels={'response_time_hours': 'Response Time (hours)',
                'severity_category': 'Severity Category'}
    )
    fig6.update_layout(height=450, showlegend=False)
    st.plotly_chart(fig6, use_container_width=True)

# ============================================
# RESPONSE VS IMPACT
# ============================================
st.markdown("---")
st.markdown("## Response Time vs Impact")

col1, col2 = st.columns(2)

with col1:
    # Scatter: Response time vs affected population
    st.markdown("##### Response vs Affected Population")
    
    fig7 = px.scatter(
        filtered_df,
        x='response_time_hours',
        y='affected_population',
        color='severity_category',
        color_discrete_map={
            'Low': '#90EE90',
            'Medium': '#FFD700',
            'High': '#FFA500',
            'Critical': '#FF4500'
        },
        hover_data=['location', 'disaster_type'],
        title='Response Time vs Affected Population',
        trendline='ols',
        labels={
            'response_time_hours': 'Response Time (hours)',
            'affected_population': 'Affected Population',
            'severity_category': 'Severity Category'
        }
    )
    fig7.update_layout(height=400)
    st.plotly_chart(fig7, use_container_width=True)

with col2:
    # Scatter: Response time vs economic loss
    st.markdown("##### Response vs Economic Loss")
    
    fig8 = px.scatter(
        filtered_df,
        x='response_time_hours',
        y='estimated_economic_loss_usd',
        color='disaster_type',
        hover_data=['location', 'severity_level'],
        title='Response Time vs Economic Loss',
        trendline='ols',
        labels={
            'response_time_hours': 'Response Time (hours)',
            'estimated_economic_loss_usd': 'Economic Loss ($)',
            'disaster_type': 'Disaster Type'
        }
    )
    fig8.update_yaxes(type='log')
    fig8.update_layout(height=400)
    st.plotly_chart(fig8, use_container_width=True)

# ============================================
# RESPONSE TRENDS OVER TIME
# ============================================
st.markdown("---")
st.markdown("## Response Trends Over Time")

# Monthly average response time
monthly_response = filtered_df.groupby(filtered_df['date'].dt.to_period('M'))['response_time_hours'].mean().reset_index()
monthly_response.columns = ['Month', 'Avg Response Time']
monthly_response['Month'] = monthly_response['Month'].astype(str)

# Add rolling average
monthly_response['MA_3'] = monthly_response['Avg Response Time'].rolling(window=3, min_periods=1).mean()

fig9 = go.Figure()
fig9.add_trace(go.Scatter(
    x=monthly_response['Month'],
    y=monthly_response['Avg Response Time'],
    name='Monthly Avg',
    mode='lines+markers',
    line=dict(color='lightblue', width=2)
))
fig9.add_trace(go.Scatter(
    x=monthly_response['Month'],
    y=monthly_response['MA_3'],
    name='3-Month Moving Avg',
    mode='lines',
    line=dict(color='#667eea', width=3)
))
fig9.add_hline(y=overall_avg_response, line_dash="dash", 
               annotation_text=f"Overall Avg: {overall_avg_response:.1f}h", 
               line_color="red")
fig9.update_layout(
    title='Response Time Trends Over Time',
    xaxis_title='Month',
    yaxis_title='Average Response Time (hours)',
    height=450,
    hovermode='x unified'
)
st.plotly_chart(fig9, use_container_width=True)

# ============================================
# AID DISTRIBUTION ANALYSIS
# ============================================
st.markdown("---")
st.markdown("## Aid Distribution Analysis")

col1, col2 = st.columns(2)

with col1:
    # Pie chart: Aid type distribution
    st.markdown("##### Aid Type Distribution")
    
    aid_dist = filtered_df['aid_provided'].value_counts().reset_index()
    aid_dist.columns = ['Aid Type', 'Count']
    
    fig10 = px.pie(
        aid_dist,
        values='Count',
        names='Aid Type',
        title='Distribution of Aid Types',
        hole=0.3,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig10.update_traces(textposition='inside', textinfo='percent+label')
    fig10.update_layout(height=400)
    st.plotly_chart(fig10, use_container_width=True)

with col2:
    # Bar chart: Aid by disaster type
    st.markdown("##### Primary Aid by Disaster Type")
    
    aid_by_type = filtered_df.groupby('disaster_type')['aid_provided'].agg(lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Unknown').reset_index()
    aid_by_type.columns = ['Disaster Type', 'Primary Aid']
    aid_count = filtered_df.groupby('disaster_type').size().reset_index()
    aid_count.columns = ['Disaster Type', 'Count']
    aid_by_type = aid_by_type.merge(aid_count, on='Disaster Type')
    
    fig11 = px.bar(
        aid_by_type,
        x='Disaster Type',
        y='Count',
        color='Primary Aid',
        title='Aid Type Distribution by Disaster Type',
        text='Primary Aid'
    )
    fig11.update_layout(height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig11, use_container_width=True)

# ============================================
# AID VS DISASTER TYPE HEATMAP
# ============================================
st.markdown("---")
st.markdown("## Aid Type vs Disaster Type Heatmap")

# Create crosstab
aid_disaster_crosstab = pd.crosstab(
    filtered_df['disaster_type'],
    filtered_df['aid_provided'],
    normalize='index'
) * 100

fig12 = px.imshow(
    aid_disaster_crosstab,
    labels=dict(x="Aid Type", y="Disaster Type", color="Percentage (%)"),
    color_continuous_scale='Blues',
    aspect='auto',
    title='Aid Type Distribution by Disaster Type (%)',
    text_auto='.1f'
)
fig12.update_layout(height=500)
st.plotly_chart(fig12, use_container_width=True)

# ============================================
# RESPONSE EFFICIENCY SCORING
# ============================================
st.markdown("---")
st.markdown("## Response Efficiency Analysis")

# Calculate efficiency score
# Lower response time = higher score
# Adjusted by severity (higher severity should have faster response)

efficiency_df = filtered_df.copy()
max_response = efficiency_df['response_time_hours'].max()

# Efficiency score: (1 - normalized_response_time) * severity_weight
efficiency_df['response_score'] = (1 - efficiency_df['response_time_hours'] / max_response) * 100
efficiency_df['severity_weight'] = efficiency_df['severity_level'] / 10
efficiency_df['efficiency_score'] = efficiency_df['response_score'] * (1 + efficiency_df['severity_weight'])

# Group by disaster type
efficiency_by_type = efficiency_df.groupby('disaster_type')['efficiency_score'].mean().sort_values(ascending=False).reset_index()
efficiency_by_type.columns = ['Disaster Type', 'Efficiency Score']

col1, col2 = st.columns(2)

with col1:
    st.markdown("##### Top Performing Response Types")
    top_efficient = efficiency_by_type.head(5)
    
    fig13 = px.bar(
        top_efficient,
        x='Efficiency Score',
        y='Disaster Type',
        orientation='h',
        color='Efficiency Score',
        color_continuous_scale='Greens',
        text='Efficiency Score',
        title='Highest Response Efficiency by Disaster Type'
    )
    fig13.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig13.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig13, use_container_width=True)

with col2:
    st.markdown("##### Areas for Improvement")
    low_efficient = efficiency_by_type.tail(5).sort_values('Efficiency Score')
    
    fig14 = px.bar(
        low_efficient,
        x='Efficiency Score',
        y='Disaster Type',
        orientation='h',
        color='Efficiency Score',
        color_continuous_scale='Reds',
        text='Efficiency Score',
        title='Lowest Response Efficiency by Disaster Type'
    )
    fig14.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig14.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig14, use_container_width=True)

st.info("**Efficiency Score** combines response speed with severity weighting. Higher scores indicate faster responses relative to disaster severity.")

# ============================================
# DETAILED STATISTICS TABLE
# ============================================
st.markdown("---")
st.markdown("## Detailed Response Statistics")

response_stats = filtered_df.groupby('disaster_type').agg({
    'event_id': 'count',
    'response_time_hours': ['mean', 'median', 'min', 'max', 'std'],
    'aid_provided': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Various'
}).round(2)

response_stats.columns = [
    'Events', 'Avg Response (h)', 'Median Response (h)', 
    'Min Response (h)', 'Max Response (h)', 'Std Dev (h)', 'Primary Aid'
]

response_stats = response_stats.sort_values('Avg Response (h)', ascending=False)

st.dataframe(
    response_stats,
    use_container_width=True,
    column_config={
        "Events": st.column_config.NumberColumn(format="%d"),
        "Avg Response (h)": st.column_config.NumberColumn(format="%.1f"),
        "Median Response (h)": st.column_config.NumberColumn(format="%.1f"),
        "Min Response (h)": st.column_config.NumberColumn(format="%.1f"),
        "Max Response (h)": st.column_config.NumberColumn(format="%.1f"),
        "Std Dev (h)": st.column_config.NumberColumn(format="%.1f")
    }
)

# ============================================
# BEST & WORST RESPONSES
# ============================================
st.markdown("---")
st.markdown("## Best & Worst Response Cases")

col1, col2 = st.columns(2)

with col1:
    st.markdown("##### Fastest Responses")
    fastest_events = filtered_df.nsmallest(10, 'response_time_hours')[
        ['date', 'location', 'disaster_type', 'response_time_hours', 'severity_level', 'aid_provided']
    ].copy()
    fastest_events['date'] = fastest_events['date'].dt.strftime('%Y-%m-%d')
    fastest_events.columns = ['Date', 'Location', 'Type', 'Response (h)', 'Severity', 'Aid']
    
    st.dataframe(fastest_events, hide_index=True, use_container_width=True)

with col2:
    st.markdown("##### Slowest Responses")
    slowest_events = filtered_df.nlargest(10, 'response_time_hours')[
        ['date', 'location', 'disaster_type', 'response_time_hours', 'severity_level', 'aid_provided']
    ].copy()
    slowest_events['date'] = slowest_events['date'].dt.strftime('%Y-%m-%d')
    slowest_events.columns = ['Date', 'Location', 'Type', 'Response (h)', 'Severity', 'Aid']
    
    st.dataframe(slowest_events, hide_index=True, use_container_width=True)

# ============================================
# RECOMMENDATIONS
# ============================================
st.markdown("---")
st.markdown("## Response Improvement Recommendations")

# Calculate key metrics for recommendations
avg_critical_response = filtered_df[filtered_df['severity_level'] >= 9]['response_time_hours'].mean()
slow_responses = len(filtered_df[filtered_df['response_time_hours'] > 72])

st.markdown(create_insight_box(
    title="Critical Events Response",
    content=f"""
    Critical events (severity ≥9) currently average <strong>{avg_critical_response:.1f} hours</strong> response time. 
    Priority should be given to reducing this through:
    <ul>
        <li>Pre-positioning emergency resources in high-risk areas</li>
        <li>Enhanced early warning systems integration</li>
        <li>Improved coordination between response agencies</li>
    </ul>
    """,
    box_type="warning"
), unsafe_allow_html=True)

st.markdown(create_insight_box(
    title="Slow Response Events",
    content=f"""
    <strong>{slow_responses:,} events ({slow_responses/len(filtered_df)*100:.1f}%)</strong> experienced slow response times (>72 hours). 
    <br><br>
    <strong>Recommendations:</strong>
    <ul>
        <li>Identify geographic and disaster-type patterns in slow responses</li>
        <li>Increase resource availability in underserved areas</li>
        <li>Implement tiered response protocols based on severity</li>
    </ul>
    """,
    box_type="info"
), unsafe_allow_html=True)

# ============================================
# DOWNLOAD
# ============================================
st.markdown("---")
col1, col2 = st.columns([3, 1])

with col1:
    st.info("Download response analysis data for operational review and improvement planning.")

with col2:
    csv = response_stats.to_csv()
    st.download_button(
        label="📥 Download Data",
        data=csv,
        file_name='response_analysis.csv',
        mime='text/csv'
    )