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
