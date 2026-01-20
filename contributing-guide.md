# Contributing to Global Disaster Events Dashboard

First off, thank you for considering contributing to this project! 🎉

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

This project and everyone participating in it is governed by our commitment to creating a welcoming and inclusive environment. Please be respectful and constructive in all interactions.

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs **actual behavior**
- **Screenshots** if applicable
- **Environment details** (OS, Python version, browser)
- **Error messages** or console output

**Bug Report Template:**
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. Scroll to '...'
4. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g., Windows 10, macOS 12.0]
 - Python Version: [e.g., 3.9.7]
 - Browser: [e.g., Chrome 96]
 - Streamlit Version: [e.g., 1.30.0]

**Additional context**
Any other relevant information.
```

### 💡 Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- **Clear title and description**
- **Use case** explaining why this would be useful
- **Proposed solution** if you have one in mind
- **Alternative solutions** you've considered
- **Mockups or examples** if applicable

### 🔧 Code Contributions

#### Types of Contributions

1. **New Visualizations**: Add new chart types or analytics
2. **New Pages**: Create additional analysis pages
3. **Performance Improvements**: Optimize data processing or rendering
4. **UI/UX Enhancements**: Improve design and user experience
5. **Documentation**: Improve README, docstrings, or add tutorials
6. **Bug Fixes**: Fix reported issues
7. **Tests**: Add test coverage

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/disaster-dashboard.git
cd disaster-dashboard
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Feature Branch

```bash
git checkout -b feature/YourFeatureName
```

### 5. Make Changes and Test

```bash
# Run the dashboard
streamlit run app.py

# Test your changes thoroughly
```

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use meaningful variable and function names
- Maximum line length: 100 characters
- Use docstrings for functions and classes

**Example:**
```python
def calculate_severity_score(severity_level, infrastructure_damage):
    """
    Calculate a composite severity score.
    
    Args:
        severity_level (int): Severity level from 1-10
        infrastructure_damage (float): Damage index from 0-1
        
    Returns:
        float: Composite severity score
    """
    return (severity_level * 0.7) + (infrastructure_damage * 10 * 0.3)
```

### File Organization

- **Pages**: Keep page files focused on specific analysis
- **Utils**: Place reusable functions in appropriate utility files
- **Styling**: Maintain consistent styling in `utils/styling.py`
- **Data**: Keep data processing in `utils/data_loader.py`

### Chart Standards

- Use Plotly for all new visualizations
- Include informative titles and axis labels
- Add hover data for context
- Use consistent color schemes from `COLOR_GRADIENTS`
- Ensure charts are responsive (`use_container_width=True`)

**Example:**
```python
fig = px.bar(
    data,
    x='category',
    y='value',
    color='category',
    title='Clear, Descriptive Title',
    labels={'category': 'Category Name', 'value': 'Value (units)'},
    color_discrete_sequence=px.colors.qualitative.Set3
)
fig.update_layout(height=400, showlegend=False)
st.plotly_chart(fig, use_container_width=True)
```

### Documentation

- Add docstrings to all functions
- Update README.md if adding features
- Include inline comments for complex logic
- Document any new dependencies

## Submitting Changes

### Pull Request Process

1. **Update Documentation**
   - Update README.md with details of changes
   - Add docstrings to new functions
   - Update requirements.txt if adding dependencies

2. **Test Thoroughly**
   - Test on multiple browsers if UI changes
   - Verify all filters still work
   - Check mobile responsiveness
   - Test with different data subsets

3. **Commit Messages**
   - Use clear, descriptive commit messages
   - Reference issue numbers if applicable
   
   ```bash
   git commit -m "Add cumulative impact chart to Overview page (#42)"
   ```

4. **Create Pull Request**
   - Fill out the PR template completely
   - Link related issues
   - Add screenshots for UI changes
   - Request review from maintainers

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed:
- [ ] Tested locally
- [ ] Tested on multiple browsers
- [ ] Tested filters work correctly
- [ ] Verified mobile responsiveness

## Screenshots (if applicable)
Add screenshots here

## Checklist
- [ ] Code follows project style guidelines
- [ ] Added docstrings and comments
- [ ] Updated documentation
- [ ] Changes generate no new warnings
- [ ] Updated requirements.txt if needed

## Related Issues
Fixes #(issue number)
```

### Code Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged
4. Delete your feature branch after merge

## Specific Contribution Ideas

### Easy (Good First Issues)

- [ ] Add new color gradient options
- [ ] Improve mobile layouts
- [ ] Add more insight boxes
- [ ] Fix typos in documentation
- [ ] Add tooltips to charts

### Medium

- [ ] Create new visualization types
- [ ] Add data validation checks
- [ ] Improve filter performance
- [ ] Add new analysis page
- [ ] Enhance existing charts

### Advanced

- [ ] Implement caching strategies
- [ ] Add machine learning predictions
- [ ] Create automated testing suite
- [ ] Build REST API endpoints
- [ ] Add real-time data integration

## Style Guidelines

### Metric Cards

Use the standardized metric card function:

```python
st.markdown(create_metric_card(
    title="Your Metric",
    value=f"{value}",
    delta="Additional info",
    icon="🎯",
    gradient_colors=COLOR_GRADIENTS['blue']
), unsafe_allow_html=True)
```

### Insight Boxes

Use consistent insight boxes:

```python
st.markdown(create_insight_box(
    title="Your Insight",
    content="Your <strong>formatted</strong> insight text.",
    box_type="info"  # or "warning" or "success"
), unsafe_allow_html=True)
```

### Page Headers

Use standardized headers:

```python
page_header("Page Title", "Page Subtitle", "🎯")
```

## Questions?

Feel free to:
- Open an issue with the "question" label
- Reach out via email or LinkedIn (see README)
- Ask in your pull request


Thank you for contributing! 🚀
