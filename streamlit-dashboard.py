import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="Global Disaster Events Dashboard 2025",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .insight-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================
@st.cache_data
def load_data():
    df = pd.read_csv('disaster_events.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# ============================================
# HEADER SECTION
# ============================================
st.markdown('<h1 class="main-header">🌍 Global Disaster Events Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Understanding Patterns, Impact, and Response in Natural Disasters</p>', unsafe_allow_html=True)


# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🌍 Global Disaster Events Dashboard 2025 | Data-Driven Insights for Disaster Management</p>
    <p>Created with Streamlit • Data processed with Python & Pandas</p>
</div>
""", unsafe_allow_html=True)
