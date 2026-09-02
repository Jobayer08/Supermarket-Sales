# 🛒 Supermarket Sales Analysis

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-green)](https://pandas.pydata.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()

A professional end-to-end data analysis project that processes supermarket sales data to extract actionable business insights.

---

## 📋 Project Overview

This project demonstrates a complete data analytics workflow using a real-world supermarket sales dataset. It covers everything from raw data loading and cleaning to exploratory data analysis (EDA), visualization, and business insight generation. The entire codebase follows industry-standard practices, including:

- Modular Python code architecture
- Comprehensive error handling and logging
- Unit testing with `pytest`
- Version control with Git and GitHub
- Professional documentation

## 🎯 Problem Statement

A supermarket chain wants to derive meaningful insights from their sales data to optimize operations and increase revenue. Specifically, they need to answer:

- Which branch generates the highest sales?
- Which product lines are the most profitable?
- Which days of the week have the highest sales volume?
- How do customer segments (Member vs. Normal, Gender) affect spending?
- How can we identify and manage unusually large (high-value) orders?

## ✨ Features

- **Data Loading:** Robust CSV import with file validation and custom error messages.
- **Data Cleaning:** Handling missing values, removing duplicates, correcting data types (e.g., `Date` to `datetime`), and stripping strings.
- **Exploratory Data Analysis (EDA):** Group-by aggregations, Pareto (80/20) analysis, statistical summaries, and IQR-based outlier detection.
- **Data Visualization:** Generation of 6 professional charts using Matplotlib and Seaborn.
- **Insight Generation:** Automated report generation using the **Finding → Reason → Business Insight → Action** framework.
- **Logging:** Detailed execution logs (INFO, WARNING, ERROR) saved to the `logs/` folder for debugging and auditing.
- **Testing:** Unit tests for core analysis and cleaning functions using `pytest`.
- **Modular Code:** Well-organized `src/` directory for maintainability and scalability.

## 📊 Dataset

**Source:** [Kaggle - Supermarket Sales](https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales)

- **Total Records:** 1,000
- **Total Columns:** 17
- **Key Columns:** Invoice ID, Branch, City, Customer type, Gender, Product line, Unit price, Quantity, Tax 5%, Total, Date, Time, Payment, cogs, gross margin percentage, gross income, Rating.

## 🛠️ Tech Stack

- **Python** 3.9+
- **Pandas** & **NumPy** – Data manipulation
- **Matplotlib** & **Seaborn** – Data visualization
- **Pytest** – Unit testing
- **Git** – Version control

## 🔧 Installation Guide

### 1. Clone the Repository
```bash
git clone [https://github.com/your-username/supermarket-sales-analysis](https://github.com/Jobayer08/Supermarket-Sales).git
cd supermarket-sales-analysis

2. Create and Activate Virtual Environment
bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
3. Install Required Packages
bash
pip install -r requirements.txt
4. Download the Dataset
Download the CSV file from Kaggle and place it in the data/ folder as supermarket_sales.csv.

🚀 Usage Instructions
To run the entire analysis pipeline:

bash
python main.py
To run only the unit tests:

bash
pytest
Generated visualizations will be saved as PNG files in the visualizations/ folder. Logs will be written to the logs/ folder.

📁 Project Structure
text
supermarket-sales-analysis/
│
├── data/                      # Raw dataset
│   └── supermarket_sales.csv
│
├── logs/                      # Auto-generated log files
├── notebooks/                 # Jupyter Notebooks for exploration
├── reports/                   # Generated reports (PDF/Excel)
├── src/                       # Core Python modules
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── data_cleaner.py
│   ├── analyzer.py
│   ├── visualizer.py
│   └── logger.py
│
├── tests/                     # Unit tests
│   ├── __init__.py
│   ├── test_data_cleaner.py
│   └── test_analyzer.py
│
├── visualizations/            # Exported PNG charts
├── .gitignore
├── main.py                    # Main entry point
├── README.md
└── requirements.txt
📈 Results & Visualizations
Chart	Description
https://visualizations/01_branch_sales.png	Total sales per branch (Branch C leads).
https://visualizations/02_product_sales.png	Revenue by product line (Food & Beverages is top).
https://visualizations/03_sales_distribution.png	Distribution of total sales (right-skewed).
https://visualizations/04_price_vs_total.png	Relationship between Unit Price and Total Sales.
https://visualizations/05_branch_boxplot.png	Sales variability and outliers by branch.
https://visualizations/06_correlation_heatmap.png	Correlation matrix of numeric features.
💡 Key Insights (Executive Summary)
Branch Performance: Branch C generates the highest revenue (~$110K), surpassing other branches by 5%. This suggests its location or management strategies are highly effective.

Pareto Principle (80/20 Rule): 6 out of 9 product lines account for 80% of total sales. Food & Beverages and Sports & Travel are the top performers and deserve priority in marketing and inventory.

Weekly Trend: Saturday records the highest sales, indicating that weekend staffing and promotional efforts should be maximized.

Customer Segmentation: The Member-Female segment has the highest average spending (~$345). This group is ideal for targeted loyalty campaigns.

High-Value Orders: 4 outliers (orders > $899) were identified. These should be tracked separately for dedicated customer relationship management and bulk-order discounts.

🔮 Future Scope
Streamlit Dashboard: Build an interactive web application where users can upload custom CSVs and view live analysis and charts.

Time Series Forecasting: Integrate Machine Learning models (Prophet/ARIMA) to forecast monthly or weekly sales.

Database Integration: Connect to PostgreSQL or SQLite for persistent data storage and querying.

CI/CD Pipeline: Automate testing and deployment using GitHub Actions.

📝 License
This project is licensed under the MIT License. You are free to use, modify, and distribute this software.

🔗 Live Demo: (Coming Soon)
✍️ Author: [Abdul Jobayer] - [[Link to your GitHub Profile](https://github.com/Jobayer08)]

⭐ If you found this project helpful, please consider giving it a star on GitHub!