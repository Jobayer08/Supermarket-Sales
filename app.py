"""
Supermarket Sales Analysis - Streamlit Dashboard
"""
import streamlit as st
import pandas as pd
import sys
import os
from PIL import Image

# src মডিউল ইম্পোর্ট করার জন্য পাথ সেট
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import load_data
from src.data_cleaner import clean_data
from src.analyzer import generate_all_insights, get_branch_sales, get_product_sales

# ========== পেজ কনফিগারেশন ==========
st.set_page_config(
    page_title="Supermarket Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== সাইডবার - CSV আপলোড ==========
st.sidebar.header("⚙️ কন্ট্রোল প্যানেল")
st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader("📂 আপনার CSV ফাইল আপলোড করুন", type=['csv'])

st.sidebar.markdown("---")
st.sidebar.info(
    "**ডিফল্ট ডেটাসেট:** Kaggle Supermarket Sales\n\n"
    "আপলোড না করলে ডিফল্ট ডেটা ব্যবহার করা হবে।"
)

# ========== ডেটা লোড করা ==========
@st.cache_data
def load_and_process_data(file):
    """
    ডেটা লোড ও ক্লিন করে। স্টিমলাইটের @st.cache_data ডেকোরেটর মেমরিতে ক্যাশ করে রাখে,
    যাতে পেজ রিলোডে বারবার লোড না করতে হয়।
    """
    if file is not None:
        # আপলোড করা ফাইল থেকে ডেটা পড়া
        df = pd.read_csv(file)
        # ক্লিনিং ফাংশন কল (আমাদের তৈরি করা)
        # clean_data() ফাংশন 'Date' কনভার্ট, স্ট্রিপিং ইত্যাদি করে
        df_clean = clean_data(df)
    else:
        # ডিফল্ট ফাইল (আমাদের data/ ফোল্ডার থেকে)
        df_clean = load_data()  # এটা data_loader.py থেকে
        df_clean = clean_data(df_clean)
    
    # Day of Week যোগ করা
    df_clean['Day_of_Week'] = df_clean['Date'].dt.day_name()
    return df_clean

# ডেটা লোড
df = load_and_process_data(uploaded_file)

# অ্যানালাইসিস রান (এটাও ক্যাশ করা ভালো)
@st.cache_data
def get_insights_data(dataframe):
    return generate_all_insights(dataframe)

insights = get_insights_data(df)

# ========== মেইন পেজের ট্যাব ==========
tab1, tab2, tab3 = st.tabs(["📊 ওভারভিউ", "📈 ভিজুয়ালাইজেশন", "💡 ইনসাইট রিপোর্ট"])

# ---------- ট্যাব ১: ওভারভিউ ----------
with tab1:
    st.header("📋 ডেটাসেট ওভারভিউ")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_sales = df['Sales'].sum()
    avg_rating = df['Rating'].mean()
    total_orders = len(df)
    total_branches = df['Branch'].nunique()
    
    col1.metric("💰 মোট বিক্রি", f"${total_sales:,.2f}")
    col2.metric("⭐ গড় রেটিং", f"{avg_rating:.2f}")
    col3.metric("🧾 মোট অর্ডার", total_orders)
    col4.metric("🏢 শাখা সংখ্যা", total_branches)
    
    st.markdown("---")
    
    # ডেটার প্রিভিউ
    st.subheader("📄 ডেটার প্রথম ৫টি সারি")
    st.dataframe(df.head(), use_container_width=True)
    
    # ডেটার বিস্তারিত ইনফো
    with st.expander("📐 ডেটা স্ট্রাকচার বিস্তারিত"):
        col_info = pd.DataFrame({
            'Column Name': df.columns,
            'Data Type': df.dtypes.astype(str),
            'Unique Values': [df[col].nunique() for col in df.columns],
            'Missing Values': [df[col].isnull().sum() for col in df.columns]
        })
        st.dataframe(col_info, use_container_width=True)

# ---------- ট্যাব ২: ভিজুয়ালাইজেশন ----------
with tab2:
    st.header("📈 ভিজুয়ালাইজেশন গ্যালারি")
    st.markdown("আমাদের `visualizations/` ফোল্ডারে সেভ করা চার্টগুলো নিচে দেখানো হলো:")
    
    # ভিজুয়ালাইজেশন ফোল্ডার থেকে ছবি লোড করা
    viz_path = "visualizations/"
    image_files = [
        ("শাখা অনুযায়ী বিক্রি", "01_branch_sales.png"),
        ("পণ্যライン অনুযায়ী বিক্রি", "02_product_sales.png"),
        ("বিক্রির ডিস্ট্রিবিউশন", "03_sales_distribution.png"),
        ("ইউনিট প্রাইস vs টোটাল", "04_price_vs_total.png"),
        ("শাখা অনুযায়ী বক্সপ্লট", "05_branch_boxplot.png"),
        ("করিলেশন হিটম্যাপ", "06_correlation_heatmap.png")
    ]
    
    # ৩টি কলামে গ্রিড লেআউট
    cols = st.columns(3)
    for idx, (title, filename) in enumerate(image_files):
        col = cols[idx % 3]
        with col:
            filepath = os.path.join(viz_path, filename)
            if os.path.exists(filepath):
                image = Image.open(filepath)
                st.image(image, caption=title, use_container_width=True)
            else:
                st.warning(f"⚠️ {filename} পাওয়া যায়নি। প্রথমে main.py রান করুন।")

# ---------- ট্যাব ৩: ইনসাইট রিপোর্ট ----------
with tab3:
    st.header("💡 ব্যবসায়িক ইনসাইট রিপোর্ট")
    st.markdown("ডেটা বিশ্লেষণ থেকে প্রাপ্ত গুরুত্বপূর্ণ সিদ্ধান্তগুলো:")
    
    # Branch
    branch = insights['branch_sales']
    st.subheader("🏬 ১. শাখা পারফরম্যান্স")
    st.write(f"**সেরা শাখা:** `{branch.index[0]}` (মোট বিক্রি: `${branch.values[0]:,.2f}`)")
    st.write(f"**দ্বিতীয়:** `{branch.index[1]}` (${branch.values[1]:,.2f})")
    st.progress(branch.values[0] / branch.sum())  # ভিজুয়াল বার
    
    # Pareto
    pareto = insights['pareto']
    p80_count = (pareto['Cumulative %'] <= 80).sum()
    st.subheader("📦 ২. পারেটো অ্যানালাইসিস (৮০/২০ নিয়ম)")
    st.write(f"মোট {len(pareto)} টি পণ্যライン-এর মধ্যে **{p80_count} টি** পণ্যライン ৮০% বিক্রি তৈরি করছে।")
    st.dataframe(pareto.style.format({'Total Sales': '${:,.2f}', 'Cumulative %': '{:.2f}%'}), use_container_width=True)
    
    # Day
    day = insights['day_sales']
    st.subheader("📅 ৩. সপ্তাহের ট্রেন্ড")
    st.write(f"**ব্যস্ততম দিন:** `{day.index[0]}` (বিক্রি: `${day.values[0]:,.2f}`)")
    st.write(f"**সবচেয়ে কম:** `{day.index[-1]}` (বিক্রি: `${day.values[-1]:,.2f}`)")
    
    # Segmentation
    seg = insights['segmentation']
    top_seg = seg['Sales']['mean'].idxmax()
    st.subheader("👥 ৪. কাস্টমার সেগমেন্টেশন")
    st.write(f"**টপ গ্রুপ:** `{top_seg[0]}` - `{top_seg[1]}` (গড় খরচ: `${seg['Sales']['mean'].max():.2f}`)")
    
    # Outliers
    outliers = insights['outliers']
    st.subheader("🚀 ৫. হাই-ভ্যালু অর্ডার (আউটলায়ার)")
    st.write(f"মোট **{len(outliers)}** টি অস্বাভাবিক বড় অর্ডার শনাক্ত হয়েছে।")
    if not outliers.empty:
        st.dataframe(outliers[['Invoice ID', 'Branch', 'Product line', 'Sales']].head(), use_container_width=True)
    
    st.markdown("---")
    st.success("✅ এই ইনসাইটগুলো ব্যবসার উন্নতিতে সরাসরি কাজে লাগবে!")

# ========== ফুটার ==========
st.sidebar.markdown("---")
st.sidebar.caption(f"ড্যাশবোর্ড ভার্সন 1.0 | তৈরি করেছেন আপনিই")