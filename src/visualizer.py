"""
ভিজুয়ালাইজেশন তৈরির মডিউল
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
from .config import VIZ_PATH, FIGURE_SIZE, PLOT_STYLE

# স্টাইল সেট করা
sns.set_style(PLOT_STYLE)
plt.rcParams['figure.figsize'] = FIGURE_SIZE

def ensure_directory(path: str) -> None:
    """ফোল্ডার না থাকলে তৈরি করে"""
    os.makedirs(path, exist_ok=True)

def save_visualizations(df: pd.DataFrame) -> None:
    """
    সব ভিজুয়ালাইজেশন তৈরি করে VIZ_PATH ফোল্ডারে সেভ করে
    """
    ensure_directory(VIZ_PATH)
    
    # ১. শাখা অনুযায়ী বিক্রি
    plt.figure()
    branch_sales = df.groupby('Branch')['Total'].sum().sort_values(ascending=False)
    sns.barplot(x=branch_sales.index, y=branch_sales.values, palette='viridis')
    plt.title('Branch-wise Total Sales', fontsize=16)
    plt.xlabel('Branch')
    plt.ylabel('Total Sales ($)')
    plt.tight_layout()
    plt.savefig(f'{VIZ_PATH}01_branch_sales.png', dpi=300)
    plt.close()
    
    # ২. পণ্যライン অনুযায়ী বিক্রি
    plt.figure()
    product_sales = df.groupby('Product line')['Total'].sum().sort_values(ascending=False)
    sns.barplot(x=product_sales.values, y=product_sales.index, palette='magma')
    plt.title('Product Line-wise Total Sales', fontsize=16)
    plt.xlabel('Total Sales ($)')
    plt.ylabel('Product Line')
    plt.tight_layout()
    plt.savefig(f'{VIZ_PATH}02_product_sales.png', dpi=300)
    plt.close()
    
    # ৩. ডিস্ট্রিবিউশন
    plt.figure()
    sns.histplot(df['Total'], bins=20, kde=True, color='blue')
    plt.title('Distribution of Total Sales', fontsize=16)
    plt.xlabel('Total Sales ($)')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(f'{VIZ_PATH}03_sales_distribution.png', dpi=300)
    plt.close()
    
    # ৪. স্ক্যাটার প্লট
    plt.figure()
    sns.scatterplot(x='Unit price', y='Total', data=df, hue='Branch', alpha=0.7)
    plt.title('Unit Price vs Total Sales (by Branch)', fontsize=16)
    plt.xlabel('Unit Price ($)')
    plt.ylabel('Total Sales ($)')
    plt.legend(title='Branch')
    plt.tight_layout()
    plt.savefig(f'{VIZ_PATH}04_price_vs_total.png', dpi=300)
    plt.close()
    
    # ৫. বক্স প্লট
    plt.figure()
    sns.boxplot(x='Branch', y='Total', data=df, palette='Set2')
    plt.title('Sales Distribution by Branch (Box Plot)', fontsize=16)
    plt.xlabel('Branch')
    plt.ylabel('Total Sales ($)')
    plt.tight_layout()
    plt.savefig(f'{VIZ_PATH}05_branch_boxplot.png', dpi=300)
    plt.close()
    
    # ৬. হিটম্যাপ
    plt.figure(figsize=(8, 6))
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', square=True, linewidths=0.5)
    plt.title('Correlation Matrix', fontsize=16)
    plt.tight_layout()
    plt.savefig(f'{VIZ_PATH}06_correlation_heatmap.png', dpi=300)
    plt.close()
    
    print(f"✅ সব ভিজুয়ালাইজেশন '{VIZ_PATH}' ফোল্ডারে সেভ করা হয়েছে।")