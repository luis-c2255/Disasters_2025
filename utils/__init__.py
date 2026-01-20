"""
Utils package for disaster dashboard
"""
from .data_loader import load_data, apply_filters, get_summary_stats
from .styling import (
    apply_custom_css, 
    create_metric_card, 
    create_insight_box,
    page_header,
    COLOR_GRADIENTS,
    CHART_COLORS
)

__all__ = [
    'load_data',
    'apply_filters',
    'get_summary_stats',
    'apply_custom_css',
    'create_metric_card',
    'create_insight_box',
    'page_header',
    'COLOR_GRADIENTS',
    'CHART_COLORS'
]
