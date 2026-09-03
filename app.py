"""
Supermarket Sales Analysis - Streamlit Dashboard
"""
import streamlit as st
import pandas as pd
import sys
import os
from PIL import Image

# Add src module to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import load_data
from src.data_cleaner import clean_data
from src.analyzer import generate_all_insights

# ========== Page Configuration ==========
st.set_page_config(
    page_title="Supermarket Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== Sidebar - CSV Upload ==========
st.sidebar.header("⚙️ Control Panel")
st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader("📂 Upload your CSV file", type=['csv'])

st.sidebar.markdown("---")
st.sidebar.info(
    "**Default Dataset:** Kaggle Supermarket Sales\n\n"
    "If you don't upload, the default dataset will be used."
)

# ========== Load Data ==========
@st.cache_data
def load_and_process_data(file):
    """
    Load and clean data. Uses Streamlit's @st.cache_data to cache in memory.
    """
    if file is not None:
        df = pd.read_csv(file)
        df_clean = clean_data(df)
    else:
        df_clean = load_data()
        df_clean = clean_data(df_clean)
    
    # Add Day of Week
    df_clean['Day_of_Week'] = df_clean['Date'].dt.day_name()
    return df_clean

df = load_and_process_data(uploaded_file)

@st.cache_data
def get_insights_data(dataframe):
    return generate_all_insights(dataframe)

insights = get_insights_data(df)

# ========== Main Page Tabs ==========
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Visualizations", "💡 Insights"])

# ---------- Tab 1: Overview ----------
with tab1:
    st.header("📋 Dataset Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_sales = df['Total'].sum()
    avg_rating = df['Rating'].mean()
    total_orders = len(df)
    total_branches = df['Branch'].nunique()
    
    col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
    col2.metric("⭐ Average Rating", f"{avg_rating:.2f}")
    col3.metric("🧾 Total Orders", total_orders)
    col4.metric("🏢 Branches", total_branches)
    
    st.markdown("---")
    
    st.subheader("📄 First 5 Rows of Data")
    st.dataframe(df.head(), use_container_width=True)
    
    with st.expander("📐 Data Structure Details"):
        col_info = pd.DataFrame({
            'Column Name': df.columns,
            'Data Type': df.dtypes.astype(str),
            'Unique Values': [df[col].nunique() for col in df.columns],
            'Missing Values': [df[col].isnull().sum() for col in df.columns]
        })
        st.dataframe(col_info, use_container_width=True)

# ---------- Tab 2: Visualizations ----------
with tab2:
    st.header("📈 Visualization Gallery")
    st.markdown("Here are the charts saved in the `visualizations/` folder:")
    
    viz_path = "visualizations/"
    image_files = [
        ("Sales by Branch", "01_branch_sales.png"),
        ("Sales by Product Line", "02_product_sales.png"),
        ("Sales Distribution", "03_sales_distribution.png"),
        ("Unit Price vs Total", "04_price_vs_total.png"),
        ("Branch-wise Boxplot", "05_branch_boxplot.png"),
        ("Correlation Heatmap", "06_correlation_heatmap.png")
    ]
    
    cols = st.columns(3)
    for idx, (title, filename) in enumerate(image_files):
        col = cols[idx % 3]
        with col:
            filepath = os.path.join(viz_path, filename)
            if os.path.exists(filepath):
                image = Image.open(filepath)
                st.image(image, caption=title, use_container_width=True)
            else:
                st.warning(f"⚠️ {filename} not found. Please run main.py first.")

# ---------- Tab 3: Insights ----------
with tab3:
    st.header("💡 Business Insights Report")
    st.markdown("Key decisions derived from the data analysis:")
    
    # Branch
    branch = insights['branch_sales']
    st.subheader("🏬 1. Branch Performance")
    st.write(f"**Top Branch:** `{branch.index[0]}` (Total Sales: `${branch.values[0]:,.2f}`)")
    st.write(f"**Second:** `{branch.index[1]}` (${branch.values[1]:,.2f})")
    st.progress(branch.values[0] / branch.sum())
    
    # Pareto
    pareto = insights['pareto']
    p80_count = (pareto['Cumulative %'] <= 80).sum()
    st.subheader("📦 2. Pareto Analysis (80/20 Rule)")
    st.write(f"Out of {len(pareto)} product lines, **{p80_count}** contribute to 80% of total sales.")
    st.dataframe(pareto.style.format({'Total Sales': '${:,.2f}', 'Cumulative %': '{:.2f}%'}), use_container_width=True)
    
    # Day
    day = insights['day_sales']
    st.subheader("📅 3. Weekly Trend")
    st.write(f"**Busiest Day:** `{day.index[0]}` (Sales: `${day.values[0]:,.2f}`)")
    st.write(f"**Slowest Day:** `{day.index[-1]}` (Sales: `${day.values[-1]:,.2f}`)")
    
    # Segmentation
    seg = insights['segmentation']
    top_seg = seg['Total']['mean'].idxmax()
    st.subheader("👥 4. Customer Segmentation")
    st.write(f"**Top Group:** `{top_seg[0]}` - `{top_seg[1]}` (Avg. Spend: `${seg['Total']['mean'].max():.2f}`)")
    
    # Outliers
    outliers = insights['outliers']
    st.subheader("🚀 5. High-Value Orders (Outliers)")
    st.write(f"Detected **{len(outliers)}** unusually large orders.")
    if not outliers.empty:
        st.dataframe(outliers[['Invoice ID', 'Branch', 'Product line', 'Total']].head(), use_container_width=True)
    
    st.markdown("---")
    st.success("✅ These insights can directly help improve business decisions!")

# ========== Footer ==========
st.sidebar.markdown("---")
st.sidebar.caption("Dashboard v1.0 | Built by You")