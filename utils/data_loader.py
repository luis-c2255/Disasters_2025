"""
Data loading and filtering utilities for the disaster dashboard
"""
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    """Load and cache the disaster events dataset"""
    df = pd.read_csv('disaster_events.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

def apply_filters(df):
    """Apply sidebar filters to the dataframe"""
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "📅 Date Range",
        value=(df['date'].min(), df['date'].max()),
        min_value=df['date'].min(),
        max_value=df['date'].max()
    )
    
    # Disaster type filter
    disaster_types = st.sidebar.multiselect(
        "🌪️ Disaster Type",
        options=sorted(df['disaster_type'].unique()),
        default=df['disaster_type'].unique()
    )
    
    # Severity filter
    severity_filter = st.sidebar.multiselect(
        "⚠️ Severity Level",
        options=['Low', 'Medium', 'High', 'Critical'],
        default=df['severity_category'].unique()
    )
    
    # Location filter (top 20 locations + All option)
    top_locations = df['location'].value_counts().head(20).index.tolist()
    location_filter = st.sidebar.multiselect(
        "📍 Location",
        options=['All'] + top_locations,
        default=['All']
    )
    
    # Major disaster filter
    major_only = st.sidebar.checkbox("Show Major Disasters Only", value=False)
    
    # Aid type filter
    aid_types = st.sidebar.multiselect(
        "🏥 Aid Type",
        options=sorted(df['aid_provided'].unique()),
        default=df['aid_provided'].unique()
    )
    
    # Apply filters
    filtered_df = df[
        (df['date'] >= pd.to_datetime(date_range[0])) &
        (df['date'] <= pd.to_datetime(date_range[1])) &
        (df['disaster_type'].isin(disaster_types)) &
        (df['severity_category'].isin(severity_filter)) &
        (df['aid_provided'].isin(aid_types))
    ]
    
    if 'All' not in location_filter and location_filter:
        filtered_df = filtered_df[filtered_df['location'].isin(location_filter)]
    
    if major_only:
        filtered_df = filtered_df[filtered_df['is_major_disaster'] == 1]
    
    # Store filtered data in session state
    st.session_state['filtered_df'] = filtered_df
    st.session_state['original_df'] = df
    
    # Show filter summary
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Filter Summary")
    st.sidebar.info(f"""
    **Total Events:** {len(filtered_df):,}  
    **Filtered:** {len(filtered_df)/len(df)*100:.1f}% of dataset  
    **Date Range:** {len(pd.date_range(date_range[0], date_range[1], freq='D'))} days
    """)
    
    return filtered_df

def get_summary_stats(df):
    """Calculate summary statistics for the dashboard"""
    return {
        'total_events': len(df),
        'major_disasters': len(df[df['is_major_disaster'] == 1]),
        'total_affected': df['affected_population'].sum(),
        'avg_affected': df['affected_population'].mean(),
        'total_economic_loss': df['estimated_economic_loss_usd'].sum(),
        'avg_economic_loss': df['estimated_economic_loss_usd'].mean(),
        'avg_response_time': df['response_time_hours'].mean(),
        'median_response_time': df['response_time_hours'].median(),
        'avg_severity': df['severity_level'].mean(),
        'avg_infrastructure_damage': df['infrastructure_damage_index'].mean(),
        'unique_locations': df['location'].nunique(),
        'unique_disaster_types': df['disaster_type'].nunique(),
        'date_range_days': (df['date'].max() - df['date'].min()).days
    }