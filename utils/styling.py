"""
Styling utilities for the disaster dashboard
"""
import streamlit as st
import plotly.express as px

def apply_custom_css():
    """Apply custom CSS styling to the dashboard"""
    st.markdown("""
        <style>
        /* Main header styling */
        .main-header {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            padding: 1rem 0;
        }
        
        .sub-header {
            font-size: 1.5rem;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        /* Insight box styling */
        .insight-box {
            background: linear-gradient(135deg, hsla(209, 62%, 50%, 1) 0%, hsla(186, 100%, 44%, 1) 100%);
            padding: 1.5rem;
            border-radius: 15px;
            border-left: 5px solid #D6FBFF;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .insight-box h1 {
            margin-top: 0;
        }
        
        .insight-box p {
            font-size: 1.05rem;
            line-height: 1.6;
        }
        
        /* Warning box */
        .warning-box {
            background: linear-gradient(135deg, #c75a5a 0%, #a83f3f 100%);
            padding: 1.5rem;
            border-radius: 15px;
            border-left: 5px solid #fff5f5;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Success box */
        .success-box {
            background: linear-gradient(135deg, #5fae82 0%, #3f8f66 100%);
            padding: 1.5rem;
            border-radius: 15px;
            border-left: 5px solid #f0fff4;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Metric card styling */
        .metric-card {
            background: linear-gradient(135deg, hsla(162, 53%, 54%, 1) 0%, hsla(186, 100%, 69%, 1) 100%);
            padding: 1.5rem 1rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
            border: 2px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.2s, box-shadow 0.2s;
            height: 100%;
            text-align: center;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
        }
        
        .metric-title {
            color: rgba(255, 255, 255, 0.9);
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            text-align: center;
        }
        
        .metric-value {
            color: white;
            font-size: 2rem;
            font-weight: bold;
            margin: 0.5rem 0;
            text-align: center;
        }
        
        .metric-delta {
            color: rgba(255, 255, 255, 0.8);
            font-size: 0.85rem;
            margin-top: 0.5rem;
        }
        
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Custom dataframe styling */
        .dataframe {
            font-size: 0.9rem;
        }
        </style>
    """, unsafe_allow_html=True)

def create_metric_card(title, value, delta, gradient_colors):
    """Create a beautiful metric card with custom gradient"""
    card_html = f"""
    <div class="metric-card" style="background: linear-gradient(135deg, {gradient_colors[0]} 0%, {gradient_colors[1]} 100%);">
        <div style="display: flex; align-items: flex-start; justify-content: space-between;">
            <div style="flex: 1;">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-delta">{delta}</div>
        </div>
    </div>
    """
    return card_html

def create_insight_box(title, content, box_type="info"):
    """Create an insight box with different styles"""
    box_class = {
        "info": "insight-box",
        "warning": "warning-box",
        "success": "success-box"
    }.get(box_type, "insight-box")
    
    icon = {
        "info": "💡",
        "warning": "⚠️",
        "success": "✅"
    }.get(box_type, "💡")
    
    return f"""
    <div class="{box_class}">
        <h4>{icon} {title}</h4>
        <p>{content}</p>
    </div>
    """

def page_header(title, subtitle=None, icon="🌍"):
    """Create a consistent page header"""
    st.markdown(f'<h1 class="main-header">{icon} {title}</h1>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p class="sub-header">{subtitle}</p>', unsafe_allow_html=True)

# Color palettes for consistency
COLOR_GRADIENTS = {
    'purple': ["#667eea", "#764ba2"],
    'pink': ["#f093fb", "#f5576c"],
    'blue': ["#4facfe", "#00f2fe"],
    'orange': ["#fa709a", "#fee140"],
    'green': ["#56ab2f", "#a8e063"],
    'sunset': ["#ff6e7f", "#bfe9ff"],
    'ocean': ["#2e3192", "#1bffff"],
    'fire': ["#ff0844", "#ffb199"],
    'mint': ["#30cfd0", "#330867"],
    'berry': ["#8e2de2", "#4a00e0"]
}

# Chart color schemes
CHART_COLORS = {
    'severity': {
        'Low': '#90EE90',
        'Medium': '#FFD700',
        'High': '#FFA500',
        'Critical': '#FF4500'
    },
    'sequential_red': 'Reds',
    'sequential_blue': 'Blues',
    'sequential_green': 'Greens',
    'diverging': 'RdBu_r',
    'categorical': px.colors.qualitative.Set3
}
