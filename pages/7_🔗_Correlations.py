"""
Correlations Page - Discovering relationships between variables
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from sklearn.preprocessing import MinMaxScaler
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
st.set_page_config(page_title="Correlations", page_icon="🔗", layout="wide")
apply_custom_css()

# Header
page_header("Correlation Analysis", "Discovering Relationships Between Variables", "🔗")

# Sidebar
st.sidebar.header("🔍 Filters")
df = load_data()
filtered_df = apply_filters(df)

# ============================================
# CALCULATE CORRELATIONS
# ============================================

# Select numeric columns for correlation
numeric_cols = [
    'severity_level',
    'affected_population',
    'estimated_economic_loss_usd',
    'response_time_hours',
    'infrastructure_damage_index'
]

corr_matrix = filtered_df[numeric_cols].corr()

# Find strongest correlations
corr_pairs = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        corr_pairs.append({
            'var1': corr_matrix.columns[i],
            'var2': corr_matrix.columns[j],
            'correlation': corr_matrix.iloc[i, j]
        })

corr_pairs_df = pd.DataFrame(corr_pairs).sort_values('correlation', key=abs, ascending=False)

strongest_positive = corr_pairs_df[corr_pairs_df['correlation'] > 0].iloc[0]
strongest_negative = corr_pairs_df[corr_pairs_df['correlation'] < 0].iloc[0] if len(corr_pairs_df[corr_pairs_df['correlation'] < 0]) > 0 else None

# ============================================
# CORRELATION METRICS
# ============================================
st.markdown("## Correlation Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(create_metric_card(
        title="Strongest Positive",
        value=f"{abs(strongest_positive['correlation']):.3f}",
        delta=f"{strongest_positive['var1'][:15]} ↔ {strongest_positive['var2'][:15]}",
        gradient_colors=COLOR_GRADIENTS['green']
    ), unsafe_allow_html=True)

with col2:
    if strongest_negative is not None:
        st.markdown(create_metric_card(
            title="Strongest Negative",
            value=f"{abs(strongest_negative['correlation']):.3f}",
            delta=f"{strongest_negative['var1'][:15]} ↔ {strongest_negative['var2'][:15]}",
            gradient_colors=COLOR_GRADIENTS['fire']
        ), unsafe_allow_html=True)
    else:
        st.markdown(create_metric_card(
            title="Strongest Negative",
            value="N/A",
            delta="No negative correlations",
            gradient_colors=COLOR_GRADIENTS['fire']
        ), unsafe_allow_html=True)

with col3:
    avg_correlation = corr_pairs_df['correlation'].abs().mean()
    st.markdown(create_metric_card(
        title="Avg Correlation",
        value=f"{avg_correlation:.3f}",
        delta="Absolute value",
        gradient_colors=COLOR_GRADIENTS['blue']
    ), unsafe_allow_html=True)

with col4:
    strong_correlations = len(corr_pairs_df[corr_pairs_df['correlation'].abs() > 0.5])
    st.markdown(create_metric_card(
        title="Strong Relationships",
        value=f"{strong_correlations}",
        delta="|r| > 0.5",
        gradient_colors=COLOR_GRADIENTS['purple']
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Insight
st.markdown(create_insight_box(
    title="Key Correlation Insights",
    content=f"""
    The strongest positive correlation is between <strong>{strongest_positive['var1']}</strong> and 
    <strong>{strongest_positive['var2']}</strong> (r = {strongest_positive['correlation']:.3f}). 
    {'The strongest negative correlation is between <strong>' + strongest_negative['var1'] + '</strong> and <strong>' + strongest_negative['var2'] + '</strong> (r = ' + f"{strongest_negative['correlation']:.3f}" + ').' if strongest_negative is not None else 'No significant negative correlations detected.'}
    Overall, <strong>{strong_correlations} variable pairs</strong> show strong relationships (|r| > 0.5).
    """,
    box_type="info"
), unsafe_allow_html=True)

# ============================================
# CORRELATION MATRIX HEATMAP
# ============================================
st.markdown("---")
st.markdown("## Correlation Matrix")

# Create more readable labels
label_mapping = {
    'severity_level': 'Severity',
    'affected_population': 'Affected Pop.',
    'estimated_economic_loss_usd': 'Economic Loss',
    'response_time_hours': 'Response Time',
    'infrastructure_damage_index': 'Infrastructure Damage'
}

corr_matrix_labeled = corr_matrix.copy()
corr_matrix_labeled.index = [label_mapping.get(x, x) for x in corr_matrix_labeled.index]
corr_matrix_labeled.columns = [label_mapping.get(x, x) for x in corr_matrix_labeled.columns]

fig1 = px.imshow(
    corr_matrix_labeled,
    text_auto='.3f',
    aspect='auto',
    color_continuous_scale='RdBu_r',
    color_continuous_midpoint=0,
    title='Correlation Matrix of Key Variables',
    labels=dict(color="Correlation")
)
fig1.update_layout(height=600)
fig1.update_xaxes(side="bottom")
st.plotly_chart(fig1, use_container_width=True)

# ============================================
# SCATTER MATRIX
# ============================================
st.markdown("---")
st.markdown("## Scatter Matrix - Pairwise Relationships")

# Sample data for performance
sample_df = filtered_df[numeric_cols].sample(min(1000, len(filtered_df)))

fig2 = px.scatter_matrix(
    sample_df,
    dimensions=numeric_cols,
    color=filtered_df.sample(min(1000, len(filtered_df)))['severity_level'],
    title='Pairwise Scatter Plots (sample of 1000 events)',
    labels={col: label_mapping.get(col, col) for col in numeric_cols},
    color_continuous_scale='Viridis'
)
fig2.update_traces(diagonal_visible=False, showupperhalf=False)
fig2.update_layout(height=800)
st.plotly_chart(fig2, use_container_width=True)

# ============================================
# TOP CORRELATIONS ANALYSIS
# ============================================
st.markdown("---")
st.markdown("## Top Correlations Deep Dive")

# Get top 3 positive correlations
top_3_correlations = corr_pairs_df[corr_pairs_df['correlation'] > 0].head(3)

for idx, row in top_3_correlations.iterrows():
    var1 = row['var1']
    var2 = row['var2']
    corr_val = row['correlation']
    
    st.markdown(f"### {idx + 1}. {label_mapping.get(var1, var1)} vs {label_mapping.get(var2, var2)} (r = {corr_val:.3f})")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Scatter plot with trendline
        fig_scatter = px.scatter(
            filtered_df.sample(min(1000, len(filtered_df))),
            x=var1,
            y=var2,
            color='disaster_type',
            trendline='ols',
            hover_data=['location', 'date'],
            labels={
                var1: label_mapping.get(var1, var1),
                var2: label_mapping.get(var2, var2)
            },
            title=f'{label_mapping.get(var1, var1)} vs {label_mapping.get(var2, var2)}'
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        # Statistical details
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            filtered_df[var1].dropna(), 
            filtered_df[var2].dropna()
        )
        
        st.markdown("**Statistical Details:**")
        st.metric("Correlation (r)", f"{corr_val:.4f}")
        st.metric("R² Value", f"{r_value**2:.4f}")
        st.metric("P-value", f"{p_value:.2e}")
        st.metric("Slope", f"{slope:.2e}")
        
        if p_value < 0.001:
            st.success("✅ Highly significant (p < 0.001)")
        elif p_value < 0.05:
            st.success("✅ Significant (p < 0.05)")
        else:
            st.warning("⚠️ Not statistically significant")
    
    st.markdown("---")

# ============================================
# CORRELATION BY DISASTER TYPE
# ============================================
st.markdown("---")
st.markdown("## Correlations by Disaster Type")

# Calculate correlations for each disaster type
disaster_types_list = filtered_df['disaster_type'].unique()

correlation_by_type = []
for disaster_type in disaster_types_list:
    type_df = filtered_df[filtered_df['disaster_type'] == disaster_type]
    if len(type_df) > 10:  # Only if enough samples
        type_corr = type_df[numeric_cols].corr()
        # Get severity vs economic loss correlation
        sev_econ_corr = type_corr.loc['severity_level', 'estimated_economic_loss_usd']
        sev_pop_corr = type_corr.loc['severity_level', 'affected_population']
        
        correlation_by_type.append({
            'Disaster Type': disaster_type,
            'Severity-Economic Loss': sev_econ_corr,
            'Severity-Population': sev_pop_corr,
            'Sample Size': len(type_df)
        })

corr_by_type_df = pd.DataFrame(correlation_by_type).sort_values('Severity-Economic Loss', ascending=False)

col1, col2 = st.columns(2)

with col1:
    st.markdown("##### Severity-Economic Loss Correlation")
    
    fig_type_corr1 = px.bar(
        corr_by_type_df,
        x='Disaster Type',
        y='Severity-Economic Loss',
        color='Severity-Economic Loss',
        color_continuous_scale='RdYlGn',
        color_continuous_midpoint=0,
        text='Severity-Economic Loss',
        title='Severity vs Economic Loss by Disaster Type'
    )
    fig_type_corr1.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_type_corr1.update_layout(height=450, xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig_type_corr1, use_container_width=True)

with col2:
    st.markdown("##### Severity-Population Correlation")
    
    fig_type_corr2 = px.bar(
        corr_by_type_df,
        x='Disaster Type',
        y='Severity-Population',
        color='Severity-Population',
        color_continuous_scale='RdYlGn',
        color_continuous_midpoint=0,
        text='Severity-Population',
        title='Severity vs Affected Population by Disaster Type'
    )
    fig_type_corr2.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig_type_corr2.update_layout(height=450, xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig_type_corr2, use_container_width=True)

# ============================================
# PARALLEL COORDINATES
# ============================================
st.markdown("---")
st.markdown("## Parallel Coordinates - Multi-Dimensional View")

# Normalize data for parallel coordinates

parallel_df = filtered_df[numeric_cols + ['disaster_type']].copy()
scaler = MinMaxScaler()
parallel_df[numeric_cols] = scaler.fit_transform(parallel_df[numeric_cols])

# Sample for performance
parallel_sample = parallel_df.sample(min(500, len(parallel_df)))

fig3 = px.parallel_coordinates(
    parallel_sample,
    dimensions=numeric_cols,
    color='severity_level',
    labels={col: label_mapping.get(col, col) for col in numeric_cols},
    color_continuous_scale='Viridis',
    title='Multi-Dimensional Variable Relationships (normalized, sample)'
)
fig3.update_layout(height=600)
st.plotly_chart(fig3, use_container_width=True)

st.info("**Note**: All variables are normalized to 0-1 scale for comparison. Lines represent individual events, colored by severity level.")

# ============================================
# CORRELATION TRENDS OVER TIME
# ============================================
st.markdown("---")
st.markdown("## Correlation Trends Over Time")

# Calculate rolling correlations
quarterly_corr = []
for quarter in filtered_df['date'].dt.to_period('Q').unique():
    quarter_df = filtered_df[filtered_df['date'].dt.to_period('Q') == quarter]
    if len(quarter_df) > 20:  # Minimum sample size
        quarter_corr_matrix = quarter_df[numeric_cols].corr()
        quarterly_corr.append({
            'Quarter': str(quarter),
            'Severity-Economic Loss': quarter_corr_matrix.loc['severity_level', 'estimated_economic_loss_usd'],
            'Severity-Population': quarter_corr_matrix.loc['severity_level', 'affected_population'],
            'Response-Severity': quarter_corr_matrix.loc['response_time_hours', 'severity_level']
        })

if quarterly_corr:
    quarterly_corr_df = pd.DataFrame(quarterly_corr)
    
    fig_trend = go.Figure()
    
    fig_trend.add_trace(go.Scatter(
        x=quarterly_corr_df['Quarter'],
        y=quarterly_corr_df['Severity-Economic Loss'],
        name='Severity-Economic Loss',
        mode='lines+markers',
        line=dict(width=3)
    ))
    
    fig_trend.add_trace(go.Scatter(
        x=quarterly_corr_df['Quarter'],
        y=quarterly_corr_df['Severity-Population'],
        name='Severity-Population',
        mode='lines+markers',
        line=dict(width=3)
    ))
    
    fig_trend.add_trace(go.Scatter(
        x=quarterly_corr_df['Quarter'],
        y=quarterly_corr_df['Response-Severity'],
        name='Response-Severity',
        mode='lines+markers',
        line=dict(width=3)
    ))
    
    fig_trend.update_layout(
        title='Correlation Trends Over Time (Quarterly)',
        xaxis_title='Quarter',
        yaxis_title='Correlation Coefficient',
        height=450,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_trend, use_container_width=True)
else:
    st.info("Insufficient data for quarterly correlation analysis.")

# ============================================
# CORRELATION SIGNIFICANCE TABLE
# ============================================
st.markdown("---")
st.markdown("## Correlation Significance Table")

# Calculate p-values for all correlations
significance_data = []
for i, row in corr_pairs_df.iterrows():
    var1 = row['var1']
    var2 = row['var2']
    
    # Calculate correlation and p-value
    corr_coef, p_value = stats.pearsonr(
        filtered_df[var1].dropna(),
        filtered_df[var2].dropna()
    )
    
    # Determine significance
    if p_value < 0.001:
        significance = '***'
        sig_level = 'p < 0.001'
    elif p_value < 0.01:
        significance = '**'
        sig_level = 'p < 0.01'
    elif p_value < 0.05:
        significance = '*'
        sig_level = 'p < 0.05'
    else:
        significance = 'ns'
        sig_level = 'Not significant'
    
    significance_data.append({
        'Variable 1': label_mapping.get(var1, var1),
        'Variable 2': label_mapping.get(var2, var2),
        'Correlation': corr_coef,
        'P-value': p_value,
        'Significance': significance,
        'Interpretation': sig_level
    })

significance_df = pd.DataFrame(significance_data).sort_values('Correlation', key=abs, ascending=False)

st.dataframe(
    significance_df,
    use_container_width=True,
    column_config={
        "Correlation": st.column_config.NumberColumn(format="%.4f"),
        "P-value": st.column_config.NumberColumn(format="%.2e")
    },
    hide_index=True
)

st.markdown("""
**Significance Levels:**
- *** : p < 0.001 (Highly significant)
- ** : p < 0.01 (Very significant)
- * : p < 0.05 (Significant)
- ns : Not significant
""")

# ============================================
# KEY FINDINGS
# ============================================
st.markdown("---")
st.markdown("## Key Correlation Findings")

# Calculate additional insights
high_severity_corr_pop = filtered_df[filtered_df['severity_level'] >= 7][['severity_level', 'affected_population']].corr().iloc[0, 1]
high_severity_corr_econ = filtered_df[filtered_df['severity_level'] >= 7][['severity_level', 'estimated_economic_loss_usd']].corr().iloc[0, 1]

col1, col2 = st.columns(2)

with col1:
    st.markdown(create_insight_box(
        title="Severity Relationships",
        content=f"""
        Severity shows strong positive correlations with both population impact and economic loss:
        <ul>
            <li>Severity ↔ Economic Loss: <strong>r = {corr_matrix.loc['severity_level', 'estimated_economic_loss_usd']:.3f}</strong></li>
            <li>Severity ↔ Affected Population: <strong>r = {corr_matrix.loc['severity_level', 'affected_population']:.3f}</strong></li>
            <li>For high-severity events (≥7), population correlation increases to <strong>r = {high_severity_corr_pop:.3f}</strong></li>
        </ul>
        This confirms that severity is a reliable predictor of disaster impact.
        """,
        box_type="info"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_insight_box(
        title="Response Time Patterns",
        content=f"""
        Response time shows interesting relationships:
        <ul>
            <li>Response ↔ Severity: <strong>r = {corr_matrix.loc['response_time_hours', 'severity_level']:.3f}</strong></li>
            <li>Response ↔ Economic Loss: <strong>r = {corr_matrix.loc['response_time_hours', 'estimated_economic_loss_usd']:.3f}</strong></li>
        </ul>
        {'Response times tend to be faster for more severe events, suggesting effective prioritization.' if corr_matrix.loc['response_time_hours', 'severity_level'] < 0 else 'Response times show positive correlation with severity, indicating potential for improvement in critical event response.'}
        """,
        box_type="success" if corr_matrix.loc['response_time_hours', 'severity_level'] < 0 else "warning"
    ), unsafe_allow_html=True)

# ============================================
# PREDICTIVE INSIGHTS
# ============================================
st.markdown("---")
st.markdown("## Predictive Insights")

st.markdown("""
Based on the correlation analysis, the following variables are most predictive of disaster impact:

1. **Severity Level** - Strongest overall predictor of both human and economic impact
2. **Infrastructure Damage Index** - Closely related to economic losses
3. **Affected Population** - Strong indicator of overall disaster magnitude

**Recommendations for Prediction Models:**
- Use severity level as primary predictor for impact assessment
- Infrastructure damage can serve as early indicator of economic losses
- Multi-variable models combining these factors will provide most accurate predictions
""")

# ============================================
# DOWNLOAD
# ============================================
st.markdown("---")
col1, col2 = st.columns([3, 1])

with col1:
    st.info("Download correlation analysis data for statistical modeling and further research.")

with col2:
    csv = significance_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data",
        data=csv,
        file_name='correlation_analysis.csv',
        mime='text/csv'
    )