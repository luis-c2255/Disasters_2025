# 🌍 Global Disaster Events Dashboard

![Static Badge](https://img.shields.io/badge/streamlit-app-red?logo=streamlit)
![Static Badge](https://img.shields.io/badge/python-3.10-blue?logo=python)
![Static Badge](https://img.shields.io/badge/License-MIT-orange)
![Static Badge](https://img.shields.io/badge/Plotly-charts-purple?logo=plotly)
![Static Badge](https://img.shields.io/badge/github-repo-green?logo=github)


A comprehensive, interactive dashboard for analyzing global disaster events, built with Python, Streamlit, and Plotly. This project demonstrates end-to-end data science skills from data cleaning to deployment, featuring 70+ interactive visualizations across 8 analytical pages.

![Dashboard Preview](/assets/dash_cover.png)
*Interactive dashboard with real-time filtering and 70+ visualizations*

## 📊 Live Demo

**[View Live Dashboard](https://disasters2025-n4vbncdb9eraqqhciuhc9g.streamlit.app/)** ← Click to explore!

## ✨ Features

### 🎯 **Core Capabilities**
- **8 Interactive Pages**: Home, Overview, Temporal Analysis, Disaster Types, Geographic Analysis, Severity & Impact, Response Analysis, and Correlations
- **70+ Visualizations**: Including maps, heatmaps, scatter plots, time series, radar charts, and more
- **Advanced Filtering**: Filter by date range, disaster type, severity, location, and aid type
- **Real-time Updates**: All metrics and charts update dynamically with filter changes
- **Data Export**: Download filtered datasets from any page for further analysis
- **Mobile Responsive**: Fully responsive design works on all devices

### 📈 **Analytics & Insights**
- Temporal pattern analysis with seasonal trends
- Geographic hotspot identification
- Multi-dimensional disaster type comparisons
- Severity impact assessment
- Response efficiency evaluation
- Statistical correlation analysis with p-values
- Predictive insights and recommendations

### 🎨 **Design Features**
- Beautiful gradient metric cards with hover effects
- Consistent professional styling
- Interactive Plotly charts with zoom, pan, and hover details
- Insight boxes highlighting key findings
- Color-coded severity levels
- Custom CSS for enhanced user experience

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation


1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/disaster-dashboard.git
   cd disaster-dashboard
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the dashboard**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**
   - The dashboard will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in your terminal

## 📁 Project Structure

```
disaster-dashboard/
│
├── app.py                          # Main application (Home page)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── disaster_events_cleaned.csv     # Cleaned dataset
│
├── utils/                          # Shared utilities
│   ├── __init__.py                # Package initialization
│   ├── data_loader.py             # Data loading and filtering
│   └── styling.py                 # CSS styling and UI components
│
├── pages/                          # Dashboard pages
│   ├── 1_📊_Overview.py           # Executive summary
│   ├── 2_📅_Temporal_Analysis.py  # Time-based patterns
│   ├── 3_🌪️_Disaster_Types.py    # Disaster categorization
│   ├── 4_🗺️_Geographic_Analysis.py # Spatial distribution
│   ├── 5_⚠️_Severity_Impact.py    # Damage assessment
│   ├── 6_🚨_Response_Analysis.py   # Response effectiveness
│   └── 7_🔗_Correlations.py       # Statistical relationships
│
└── assets/                         # Images and screenshots
    └── dashboard-preview.gif
```

## 📊 Dashboard Pages

### 🏠 Home
- Welcome section with project overview
- Quick statistics and key insights
- Navigation guide
- Methodology documentation

### 📊 Overview
**8+ visualizations** including:
- Executive KPI cards (events, affected population, economic loss, response time)
- Events timeline with moving average
- Cumulative impact analysis
- Disaster type distribution
- Severity vs economic impact
- Multi-dimensional radar chart
- Top locations and rankings

### 📅 Temporal Analysis
**7+ visualizations** including:
- Monthly event trends
- Seasonal distribution
- Weekly patterns
- Quarterly breakdowns
- Disaster type evolution over time
- Temporal heatmaps

### 🌪️ Disaster Types
**13 visualizations** including:
- Type distribution (pie & bar charts)
- Impact analysis by type
- Severity breakdowns
- Response time comparisons
- Infrastructure damage analysis
- Multi-dimensional comparison radar
- Aid distribution sunburst

### 🗺️ Geographic Analysis
**8+ visualizations** including:
- Interactive world map
- Top affected locations
- Economic loss by location
- Disaster diversity analysis
- Hierarchical treemap
- Impact bubble chart
- Geographic spread timeline

### ⚠️ Severity & Impact
**12+ visualizations** including:
- Severity distribution
- Severity vs population/economic impact
- Infrastructure damage analysis
- Event progression funnel
- Major disasters deep dive
- Extreme events analysis
- Response time by severity

### 🚨 Response Analysis
**14+ visualizations** including:
- Response time distribution
- Response by disaster type
- Response vs severity/impact
- Response trends over time
- Aid distribution analysis
- Aid vs disaster type heatmap
- Efficiency scoring
- Best/worst response cases

### 🔗 Correlations
**10+ visualizations** including:
- Correlation matrix heatmap
- Scatter matrix
- Top correlation deep dives with statistical tests
- Correlations by disaster type
- Parallel coordinates
- Correlation trends over time
- Significance testing with p-values

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core programming language |
| **Streamlit** | Web application framework |
| **Pandas** | Data manipulation and analysis |
| **NumPy** | Numerical computing |
| **Plotly** | Interactive visualizations |
| **Seaborn** | Statistical data visualization |
| **Matplotlib** | Additional plotting |
| **Scikit-learn** | Data normalization and scaling |
| **SciPy** | Statistical analysis |

## 📊 Dataset

The dashboard analyzes a comprehensive dataset of global disaster events with the following features:

- **20,000+ events** across multiple years
- **13 variables** including:
  - Event metadata (ID, type, location, date)
  - Geographic data (latitude, longitude)
  - Severity metrics (level 1-10, infrastructure damage index)
  - Impact data (affected population, economic loss)
  - Response metrics (response time, aid provided)
  - Classification (major disaster flag)

### Data Processing Pipeline
1. **Cleaning**: Removed duplicates, handled missing values, validated ranges
2. **Feature Engineering**: Created temporal features, categorical variables, derived metrics
3. **Validation**: Statistical checks and domain knowledge validation
4. **Categorization**: Severity, economic impact, and response time classifications

## 🎨 Customization

### Changing Colors

Edit `utils/styling.py` to customize gradient colors:

```python
COLOR_GRADIENTS = {
    'purple': ["#667eea", "#764ba2"],
    'pink': ["#f093fb", "#f5576c"],
    'blue': ["#4facfe", "#00f2fe"],
    # Add your custom gradients
}
```

### Adding New Pages

1. Create a new file in `pages/` folder: `8_🔬_Your_Page.py`
2. Use the template structure from existing pages
3. Streamlit automatically detects and adds to navigation

### Modifying Filters

Edit `utils/data_loader.py` to add or modify filters in the `apply_filters()` function.

## 📈 Key Insights

The dashboard reveals several critical patterns:

- **Temporal Patterns**: Certain months show significantly higher disaster frequency
- **Geographic Hotspots**: Specific regions experience disproportionate disaster impact
- **Type Correlations**: Strong relationships between disaster types and response effectiveness
- **Severity Impact**: Clear correlation between severity levels and economic/human impact
- **Response Efficiency**: Average response time varies significantly by disaster type

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](license-file.md) file for details.

## 👤 Author

**Your Name**

- GitHub: [luis-c2255](https://github.com/luis-c2255)
- LinkedIn: [Luis Modesto](www.linkedin.com/in/luis-modesto3986)
- Portfolio: [https://github.com/luis-c2255/luis-c2255.github.io](https://github.com/luis-c2255/luis-c2255.github.io)
- Email: luiscsmodesto@outlook.com

## 🙏 Acknowledgments

- Data visualization inspiration from [Plotly](https://plotly.com/python/)
- Dashboard framework by [Streamlit](https://streamlit.io/)
- Statistical analysis using [SciPy](https://scipy.org/)
- Icons from various emoji sources

## 📚 Documentation

For detailed documentation on:
- **Setup & Installation**: See [Quick Start](#-quick-start) section
- **Page Descriptions**: See [Dashboard Pages](#-dashboard-pages) section
- **Customization Guide**: See [Customization](#-customization) section
- **API Reference**: Check individual page docstrings

## 🐛 Known Issues

- Large datasets (>100k rows) may experience slower filtering performance
- Some browsers may require hardware acceleration for smooth chart interactions
- Mobile view best experienced in landscape mode for complex visualizations

## 🔮 Future Enhancements

- [ ] Machine learning predictions for disaster impact
- [ ] Real-time data integration
- [ ] User authentication and personalized dashboards
- [ ] Advanced geospatial analysis with clustering
- [ ] API endpoints for programmatic access
- [ ] Automated report generation
- [ ] Multi-language support
- [ ] Dark mode theme

## 📊 Performance

- Initial load time: ~2-3 seconds
- Filter update time: <1 second
- Chart rendering: Real-time
- Data processing: Optimized with caching
- Recommended browsers: Chrome, Firefox, Safari, Edge

## 🎓 Learning Resources

This project demonstrates skills in:
- Data cleaning and preprocessing
- Exploratory data analysis (EDA)
- Statistical analysis
- Data visualization
- Web application development
- UI/UX design
- Code organization and documentation
- Version control (Git/GitHub)

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Known Issues](#-known-issues) section
2. Search existing [GitHub Issues](https://github.com/luis-c2255/Disasters_2025/issues)
3. Open a new issue with detailed description
4. Contact via email or LinkedIn

## ⭐ Show Your Support

If this project helped you, please consider:
- Giving it a ⭐ on GitHub
- Sharing it with others
- Contributing improvements
- Providing feedback

## 📸 Screenshots

### Dashboard Overview
![Overview Page](/assets/overview.png)

### Geographic Analysis
![Geographic Map](/assets/geomap.png)

### Correlation Analysis
![Correlation Matrix](/assets/corre.png)

---

<div align="center">

**Made with ❤️ using Python and Streamlit**


</div>
