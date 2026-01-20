"""
Geographic Analysis Page - Spatial patterns and location insights
"""
import streamlit as st
import plotly.express as px

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
st.set_page_config(page_title="Geographic Analysis", page_icon="🗺️", layout="wide")
apply_custom_css()

# Header
page_header("Geographic Analysis", "Spatial Distribution and Location Hotspots", "🗺️")

# Sidebar
st.sidebar.header("🔍 Filters")
df = load_data()
filtered_df = apply_filters(df)

# ============================================
# GEOGRAPHIC METRICS
# ============================================
st.markdown("## 🌍 Geographic Metrics")

col1, col2, col3, col4 = st.columns(4)

unique_locations = filtered_df['location'].nunique()
most_affected_loc = filtered_df.groupby('location')['affected_population'].sum().idxmax()
most_affected_count = filtered_df.groupby('location')['affected_population'].sum().max()
most_frequent_loc = filtered_df['location'].value_counts().idxmax()
most_frequent_count = filtered_df['location'].value_counts().max()

with col1:
    st.markdown(create_metric_card(
        title="Unique Locations",
        value=f"{unique_locations:,}",
        delta="Global coverage",
        gradient_colors=COLOR_GRADIENTS['blue']
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_metric_card(
        title="Most Affected",
        value=most_affected_loc[:15],
        delta=f"{most_affected_count/1e6:.1f}M people",
        gradient_colors=COLOR_GRADIENTS['fire']
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_metric_card(
        title="Highest Frequency",
        value=most_frequent_loc[:15],
        delta=f"{most_frequent_count} events",
        gradient_colors=COLOR_GRADIENTS['purple']
    ), unsafe_allow_html=True)

with col4:
    avg_per_location = len(filtered_df) / unique_locations
    st.markdown(create_metric_card(
        title="Avg Per Location",
        value=f"{avg_per_location:.1f}",
        delta="Events per location",
        gradient_colors=COLOR_GRADIENTS['green']
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Insight
st.markdown(create_insight_box(
    title="Geographic Distribution Insight",
    content=f"""
    Disasters are distributed across <strong>{unique_locations:,} unique locations</strong> globally.
    <strong>{most_affected_loc}</strong> has been the most affected with <strong>{most_affected_count/1e6:.1f} million people</strong> impacted,
    while <strong>{most_frequent_loc}</strong> experienced the highest frequency with <strong>{most_frequent_count} events</strong>.
    """,
    box_type="info"
), unsafe_allow_html=True)

# ============================================
# MAIN MAP
# ============================================
st.markdown("---")
st.markdown("## Global Distribution Map")

# Create size and color variables
map_df = filtered_df.copy()
map_df['size'] = map_df['affected_population'].clip(upper=map_df['affected_population'].quantile(0.95))

fig_map = px.scatter_geo(
    map_df,
    lat='latitude',
    lon='longitude',
    color='severity_level',
    size='size',
    hover_data={
        'location': True,
        'disaster_type': True,
        'date': True,
        'affected_population': ':,',
        'estimated_economic_loss_usd': ':$,.0f',
        'latitude': False,
        'longitude': False,
        'size': False
    },
    title='Global Distribution of Disaster Events',
    color_continuous_scale='Reds',
    size_max=15,
    projection='natural earth'
)
fig_map.update_layout(height=600, margin=dict(l=0, r=0, t=50, b=0))
st.plotly_chart(fig_map, use_container_width=True)

# ============================================
# TOP LOCATIONS ANALYSIS
# ============================================
st.markdown("---")
st.markdown("## Top Affected Locations")

col1, col2 = st.columns(2)

with col1:
    # By event count
    st.markdown("##### By Event Frequency")
    top_freq = filtered_df['location'].value_counts().head(15).reset_index()
    top_freq.columns = ['Location', 'Events']
    
    fig1 = px.bar(
        top_freq,
        y='Location',
        x='Events',
        orientation='h',
        color='Events',
        color_continuous_scale='Viridis',
        text='Events'
    )
    fig1.update_traces(textposition='outside')
    fig1.update_layout(height=500, showlegend=False)
    fig1.update_yaxes(categoryorder='total ascending')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # By affected population
    st.markdown("##### By Total Affected Population")
    top_affected = filtered_df.groupby('location')['affected_population'].sum().sort_values(ascending=False).head(15).reset_index()
    top_affected.columns = ['Location', 'Total Affected']
    
    fig2 = px.bar(
        top_affected,
        y='Location',
        x='Total Affected',
        orientation='h',
        color='Total Affected',
        color_continuous_scale='Reds',
        text='Total Affected'
    )
    fig2.update_traces(textposition='outside', texttemplate='%{text:,.0f}')
    fig2.update_layout(height=500, showlegend=False)
    fig2.update_yaxes(categoryorder='total ascending')
    st.plotly_chart(fig2, use_container_width=True)

# ============================================
# LOCATION COMPARISONS
# ============================================
st.markdown("---")
st.markdown("## Location Comparisons")

col1, col2 = st.columns(2)

with col1:
    # Economic loss by location
    st.markdown("##### Economic Loss by Location (Top 10)")
    top_loss = filtered_df.groupby('location')['estimated_economic_loss_usd'].sum().sort_values(ascending=False).head(10).reset_index()
    top_loss.columns = ['Location', 'Total Loss']
    top_loss['Total Loss (B)'] = top_loss['Total Loss'] / 1e9
    
    fig3 = px.bar(
        top_loss,
        x='Location',
        y='Total Loss (B)',
        color='Total Loss (B)',
        color_continuous_scale='Oranges',
        text='Total Loss (B)'
    )
    fig3.update_traces(texttemplate='$%{text:.2f}B', textposition='outside')
    fig3.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    # Disaster diversity by location
    st.markdown("##### Disaster Type Diversity (Top 10)")
    disaster_diversity = filtered_df.groupby('location')['disaster_type'].nunique().sort_values(ascending=False).head(10).reset_index()
    disaster_diversity.columns = ['Location', 'Unique Types']
    
    fig4 = px.bar(
        disaster_diversity,
        x='Location',
        y='Unique Types',
        color='Unique Types',
        color_continuous_scale='Blues',
        text='Unique Types'
    )
    fig4.update_traces(textposition='outside')
    fig4.update_layout(height=400, showlegend=False, xaxis_tickangle=-45)
    st.plotly_chart(fig4, use_container_width=True)

# ============================================
# TREEMAP
# ============================================
st.markdown("---")
st.markdown("## Hierarchical View: Location → Disaster Type")

# Prepare treemap data
treemap_data = filtered_df.groupby(['location', 'disaster_type']).agg({
    'event_id': 'count',
    'affected_population': 'sum'
}).reset_index()
treemap_data.columns = ['Location', 'Disaster Type', 'Events', 'Total Affected']

# Filter to top 10 locations for clarity
top_10_locs = filtered_df['location'].value_counts().head(10).index
treemap_data_filtered = treemap_data[treemap_data['Location'].isin(top_10_locs)]

fig5 = px.treemap(
    treemap_data_filtered,
    path=['Location', 'Disaster Type'],
    values='Events',
    color='Total Affected',
    color_continuous_scale='RdYlBu_r',
    title='Top 10 Locations: Events and Impact by Disaster Type'
)
fig5.update_layout(height=600)
fig5.update_traces(textposition='middle center', textinfo='label+value')
st.plotly_chart(fig5, use_container_width=True)

# ============================================
# BUBBLE CHART
# ============================================
st.markdown("---")
st.markdown("## Location Impact Analysis")

# Aggregate by location
location_summary = filtered_df.groupby('location').agg({
    'event_id': 'count',
    'affected_population': 'sum',
    'estimated_economic_loss_usd': 'sum',
    'severity_level': 'mean'
}).reset_index()
location_summary.columns = ['Location', 'Events', 'Total Affected', 'Total Loss', 'Avg Severity']

# Filter top 30 for visibility
location_summary_top = location_summary.nlargest(30, 'Events')

fig6 = px.scatter(
    location_summary_top,
    x='Total Affected',
    y='Total Loss',
    size='Events',
    color='Avg Severity',
    hover_data=['Location'],
    title='Location Impact: Affected Population vs Economic Loss',
    color_continuous_scale='Reds',
    size_max=50,
    labels={
        'Total Affected': 'Total Affected Population',
        'Total Loss': 'Total Economic Loss ($)',
        'Avg Severity': 'Avg Severity Level'
    }
)
fig6.update_layout(height=500)
st.plotly_chart(fig6, use_container_width=True)

# ============================================
# GEOGRAPHIC CONCENTRATION ANALYSIS
# ============================================
st.markdown("---")
st.markdown("## Geographic Distribution Patterns")
# Events per location distribution
st.markdown("##### Events per Location Distribution")
    
events_per_location = filtered_df.groupby('location').size().reset_index()
events_per_location.columns = ['Location', 'Events']
    
    # Create histogram of events per location
fig7a = px.histogram(
        events_per_location,
        x='Events',
        nbins=20,
        title='How Many Events Does Each Location Experience?',
        labels={'Events': 'Number of Events', 'count': 'Number of Locations'},
        color_discrete_sequence=['#4cc2a6']
    )
fig7a.update_layout(height=400, showlegend=False)
st.plotly_chart(fig7a, use_container_width=True)
    
st.info(f"**Insight**: Most locations experience few events, while a small number of locations are disaster hotspots.")

# ============================================
# LOCATION DETAILS TABLE
# ============================================
st.markdown("---")
st.markdown("## Detailed Location Statistics")

# Comprehensive location table
location_stats = filtered_df.groupby('location').agg({
    'event_id': 'count',
    'affected_population': ['sum', 'mean'],
    'estimated_economic_loss_usd': ['sum', 'mean'],
    'response_time_hours': 'mean',
    'severity_level': 'mean',
    'infrastructure_damage_index': 'mean',
    'is_major_disaster': 'sum'
}).round(2)

location_stats.columns = [
    'Events', 'Total Affected', 'Avg Affected',
    'Total Loss ($)', 'Avg Loss ($)', 'Avg Response (h)',
    'Avg Severity', 'Avg Infra Damage', 'Major Disasters'
]

location_stats = location_stats.sort_values('Events', ascending=False).head(20)

st.dataframe(
    location_stats,
    use_container_width=True,
    column_config={
        "Total Affected": st.column_config.NumberColumn(format="%d"),
        "Avg Affected": st.column_config.NumberColumn(format="%.0f"),
        "Total Loss ($)": st.column_config.NumberColumn(format="$%.0f"),
        "Avg Loss ($)": st.column_config.NumberColumn(format="$%.0f"),
        "Avg Response (h)": st.column_config.NumberColumn(format="%.1f"),
        "Avg Severity": st.column_config.NumberColumn(format="%.2f"),
        "Avg Infra Damage": st.column_config.NumberColumn(format="%.2f")
    }
)
# ============================================
# DOWNLOAD
# ============================================
st.markdown("---")
col1, col2 = st.columns([3, 1])

with col1:
    st.info("Download location statistics for further geographic analysis.")

with col2:
    csv = location_stats.to_csv()
    st.download_button(
        label="📥 Download Data",
        data=csv,
        file_name='geographic_analysis.csv',
        mime='text/csv'
    )
    