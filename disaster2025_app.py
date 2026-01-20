"""
Global Disaster Events Dashboard - Home Page
Main entry point for the multipage Streamlit application
"""
import streamlit as st
from utils import (
    load_data, 
    apply_custom_css,
    page_header,
    create_metric_card,
    create_insight_box,
    COLOR_GRADIENTS
)

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Global Disaster Events Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_css()

# Load data
df = load_data()

# ============================================
# HEADER
# ============================================
page_header(
    "Global Disaster Events Dashboard",
    "Understanding Patterns, Impact, and Response in Natural Disasters",
    "🌍"
)

# ============================================
# WELCOME SECTION
# ============================================
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ## Welcome to the Disaster Analytics Platform
    This comprehensive dashboard provides deep insights into global disaster events, 
    helping stakeholders make data-driven decisions for disaster preparedness, response, and recovery.
    
    ### What You'll Find Here:
    
    - **Overview**: Executive summary with key metrics and trends
    - **Temporal Analysis**: Time-based patterns and seasonal trends
    - **Disaster Types**: Deep dive into different disaster categories
    - **Geographic Analysis**: Spatial distribution and hotspot identification
    - **Severity & Impact**: Understanding the scale of damage
    - **Response Analysis**: Evaluating emergency response effectiveness
    - **Correlations**: Discovering relationships between variables
    
    ### Use Cases:
        
    - Emergency management planning
    - Resource allocation optimization
    - Risk assessment and insurance
    - Policy development and advocacy
    - Academic research and analysis
    """)

with col2:
    # Dataset summary card
    st.markdown(create_metric_card(
        title="Dataset Overview",
        value=f"{len(df):,}",
        delta=f"Events analyzed",
        gradient_colors=COLOR_GRADIENTS['purple']
    ), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(create_metric_card(
        title="Time Span",
        value=f"{(df['date'].max() - df['date'].min()).days}",
        delta="Days of data",
        gradient_colors=COLOR_GRADIENTS['blue']
    ), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown(create_metric_card(
        title="Global Coverage",
        value=f"{df['location'].nunique()}",
        delta="Unique locations",
        gradient_colors=COLOR_GRADIENTS['green']
    ), unsafe_allow_html=True)

# ============================================
# QUICK STATS OVERVIEW
# ============================================
st.markdown("---")
st.markdown("## Quick Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    major_disasters = len(df[df['is_major_disaster'] == 1])
    st.markdown(create_metric_card(
        title="Major Disasters",
        value=f"{major_disasters:,}",
        delta=f"{major_disasters/len(df)*100:.1f}% of total",
        gradient_colors=COLOR_GRADIENTS['fire']
    ), unsafe_allow_html=True)

with col2:
    total_affected = df['affected_population'].sum()
    st.markdown(create_metric_card(
        title="People Affected",
        value=f"{total_affected/1e6:.1f}M",
        delta=f"Across all events",
        gradient_colors=COLOR_GRADIENTS['pink']
    ), unsafe_allow_html=True)

with col3:
    total_loss = df['estimated_economic_loss_usd'].sum()
    st.markdown(create_metric_card(
        title="Economic Impact",
        value=f"${total_loss/1e9:.1f}B",
        delta="Total losses",
        gradient_colors=COLOR_GRADIENTS['orange']
    ), unsafe_allow_html=True)

with col4:
    disaster_types = df['disaster_type'].nunique()
    st.markdown(create_metric_card(
        title="Disaster Types",
        value=f"{disaster_types}",
        delta="Different categories",
        gradient_colors=COLOR_GRADIENTS['mint']
    ), unsafe_allow_html=True)

# ============================================
# KEY INSIGHTS
# ============================================
st.markdown("---")
st.markdown("## Key Insights")

# Calculate key insights
most_common_disaster = df['disaster_type'].mode()[0]
most_common_count = df['disaster_type'].value_counts().iloc[0]
peak_month = df.groupby('month_name').size().idxmax()
most_affected_location = df.groupby('location')['affected_population'].sum().idxmax()
avg_response = df['response_time_hours'].mean()

col1, col2 = st.columns(2)

with col1:
    st.markdown(create_insight_box(
        title="Most Frequent Disaster",
        content=f"<strong>{most_common_disaster}</strong> is the most common disaster type, occurring <strong>{most_common_count:,} times</strong> ({most_common_count/len(df)*100:.1f}% of all events). This highlights the need for specialized preparedness measures.",
        box_type="info"
    ), unsafe_allow_html=True)
    
    st.markdown(create_insight_box(
        title="Geographic Concentration",
        content=f"<strong>{most_affected_location}</strong> has the highest cumulative affected population, indicating a critical need for enhanced disaster resilience infrastructure and emergency response capabilities in this region.",
        box_type="warning"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_insight_box(
        title="Seasonal Pattern",
        content=f"<strong>{peak_month}</strong> shows the highest disaster frequency, suggesting seasonal vulnerability that could inform proactive resource allocation and preparedness campaigns during this period.",
        box_type="info"
    ), unsafe_allow_html=True)
    
    st.markdown(create_insight_box(
        title="Response Efficiency",
        content=f"The average response time is <strong>{avg_response:.1f} hours</strong>. Continued investment in early warning systems and response infrastructure could further reduce this time and save more lives.",
        box_type="success"
    ), unsafe_allow_html=True)

# ============================================
# NAVIGATION GUIDE
# ============================================
st.markdown("---")
st.markdown("## Navigation Guide")

nav_col1, nav_col2, nav_col3 = st.columns(3, border=True)

with nav_col1:
    st.markdown("""
    #### Analysis Pages
    - **Overview**: High-level metrics and trends
    - **Temporal Analysis**: Time patterns
    - **Disaster Types**: Category breakdown
    """)

with nav_col2:
    st.markdown("""
    #### Spatial & Impact
    - **Geographic Analysis**: Location insights
    - **Severity & Impact**: Damage assessment
    - **Response Analysis**: Effectiveness metrics
    """)

with nav_col3:
    st.markdown("""
    #### Advanced Analysis
    - **Correlations**: Variable relationships
    - **Custom Filters**: In the sidebar
    - **Data Export**: Download filtered data
    """)

# ============================================
# METHODOLOGY
# ============================================
st.markdown("---")
st.markdown("## Methodology")

with st.expander("Data Sources & Processing"):
    st.markdown("""
    ### Data Collection
    This dashboard analyzes a comprehensive dataset of global disaster events with the following characteristics:
    
    - **Total Events**: 20,000+ disaster occurrences
    - **Variables**: 13 core metrics including temporal, geographic, severity, and response data
    - **Coverage**: Global scope with detailed location information
    
    ### Data Processing Pipeline
    1. **Cleaning**: Removed duplicates, handled missing values, validated data ranges
    2. **Feature Engineering**: Created temporal features (month, quarter, week) and categorical variables
    3. **Categorization**: Classified severity, economic impact, and response times into meaningful groups
    4. **Validation**: Ensured data integrity through statistical checks and domain knowledge validation
    
    ### Analysis Techniques
    - **Descriptive Statistics**: Central tendency and distribution analysis
    - **Temporal Analysis**: Time series and seasonal decomposition
    - **Geographic Analysis**: Spatial clustering and hotspot identification
    - **Correlation Analysis**: Pearson correlation for continuous variables
    - **Comparative Analysis**: Cross-category comparisons and rankings
    """)

with st.expander("Metrics Definitions"):
    st.markdown("""
    ### Key Metrics Explained
    
    **Severity Level** (1-10 scale)
    - Low (1-3): Minor disruptions, limited impact
    - Medium (4-6): Moderate damage, localized effects
    - High (7-8): Significant damage, regional impact
    - Critical (9-10): Catastrophic damage, widespread effects
    
    **Economic Loss Categories**
    - Minor: < $1 Million
    - Moderate: $1M - $10M
    - Severe: $10M - $100M
    - Catastrophic: > $100M
    
    **Response Time Categories**
    - Immediate: < 6 hours
    - Fast: 6-24 hours
    - Moderate: 24-72 hours
    - Slow: > 72 hours
    
    **Infrastructure Damage Index**
    - Scale from 0 to 1
    - Represents percentage of infrastructure affected
    - Higher values indicate more severe damage
    """)

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>🌍 Global Disaster Events Dashboard 2025</strong></p>
    <p>Data-Driven Insights for Disaster Management and Preparedness</p>
    <p style='font-size: 0.9rem;'>Navigate using the sidebar to explore different aspects of the data</p>
</div>
""", unsafe_allow_html=True)