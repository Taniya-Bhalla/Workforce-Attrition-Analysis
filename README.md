# Workforce Attrition Patterns and Risk Hotspot Analysis

## Project Overview

This project presents an interactive HR analytics dashboard developed to
analyze employee attrition patterns and identify workforce risk hotspots
at Palo Alto Networks.

The dashboard transforms employee HR data into interactive visual
insights that can help identify departments, job roles, demographic
groups, tenure stages, and workplace factors associated with employee
attrition.

## Project Objectives

-   Analyze overall employee attrition patterns.
-   Identify departments and job roles with higher attrition risk.
-   Explore attrition across age and gender groups.
-   Analyze employee education and marital-status patterns.
-   Examine tenure and career-stage related attrition.
-   Study the relationship between overtime and employee attrition.
-   Analyze the impact of business travel and distance from home.
-   Compare employee experience and compensation-related patterns.
-   Provide key insights and business-oriented recommendations.

## Dashboard Features

The interactive dashboard includes:

-   Five KPI cards for quick workforce-level metrics.
-   Department and Job Role filters.
-   Overtime and Business Travel filters.
-   Attrition distribution analysis.
-   Exited employee profile analysis.
-   Department-wise attrition rate.
-   Job Role-wise attrition rate.
-   High-risk area identification.
-   Age and Gender analysis.
-   Education and Education Field analysis.
-   Marital Status analysis.
-   Tenure bucket analysis.
-   Years Since Last Promotion analysis.
-   Career Stage analysis.
-   Overtime and Business Travel analysis.
-   Distance From Home analysis.
-   Job Satisfaction and Monthly Income analysis.
-   Dynamic Key Insights and Business Recommendations.

## Technologies Used

-   **Python** -- Core programming and data analysis.
-   **Pandas** -- Data loading, filtering, transformation, and
    calculations.
-   **Streamlit** -- Interactive web dashboard development.
-   **Plotly** -- Interactive data visualizations.
-   **VS Code** -- Development environment.

## Dataset

The project uses the `Palo Alto Networks.csv` employee HR dataset.

The dataset is analyzed to understand workforce characteristics and
employee attrition patterns across multiple dimensions such as
department, job role, age, tenure, overtime, business travel, and other
employee attributes.

## Project Structure

``` text
Workforce-Attrition-Analysis/
│
├── Hr_dashboard.py
├── Palo Alto Networks.csv
├── requirements.txt
└── README.md
```

## Installation

Clone or download the repository and install the required Python
libraries:

``` bash
pip install -r requirements.txt
```

## Run the Dashboard

Start the Streamlit application using:

``` bash
python -m streamlit run Hr_dashboard.py
```

The dashboard will open in your web browser.

## Interactive Analysis

Users can apply filters from the sidebar to explore specific workforce
segments. The dashboard updates the displayed KPIs, charts, and analysis
according to the selected filters.

This allows users to investigate attrition patterns from different
business perspectives rather than relying only on static charts.

## Key Analysis Areas

### Workforce Attrition

Provides an overview of retained and exited employees and the overall
attrition rate.

### Department and Job Role

Helps identify areas of the organization where employee attrition is
comparatively higher.

### Demographics

Examines attrition patterns across age and gender groups.

### Tenure and Career Stage

Explores whether attrition is concentrated among early-tenure employees
or more experienced employees.

### Workload and Mobility

Analyzes overtime, business travel, and distance from home as potential
workforce risk factors.

### Experience and Compensation

Examines employee job satisfaction and monthly income in relation to
attrition patterns.

## Business Value

The dashboard is designed to support data-driven HR decision-making by
highlighting workforce segments that may require closer attention.

The insights can help HR teams consider targeted retention strategies,
workload management, employee engagement initiatives, and workforce
planning.

## Internship Context

This dashboard was developed as a **Data Analyst Internship Project** to
demonstrate practical skills in:

-   Data analysis
-   Exploratory data analysis
-   Data visualization
-   Interactive dashboard development
-   Business insight generation
-   Workforce analytics

## Author

**Taniya**\
Data Analyst Intern

## Project Status

The dashboard is developed using Python, Pandas, Streamlit, and Plotly.
Deployment and the live dashboard link can be added to this README after
deployment.

## Live Dashboard

🚀 **[View Live Dashboard]-https://taniya-workforce-attrition.streamlit.app/
