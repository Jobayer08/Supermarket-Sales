"""
ডেটা অ্যানালাইসিস ও ইনসাইট জেনারেশনের মডিউল
"""
import pandas as pd
import numpy as np

def get_branch_sales(df: pd.DataFrame) -> pd.Series:
    """শাখা অনুযায়ী মোট বিক্রি রিটার্ন করে"""
    return df.groupby('Branch')['Total'].sum().sort_values(ascending=False)

def get_product_sales(df: pd.DataFrame) -> pd.Series:
    """পণ্যライン অনুযায়ী মোট বিক্রি রিটার্ন করে"""
    return df.groupby('Product line')['Total'].sum().sort_values(ascending=False)

def get_day_sales(df: pd.DataFrame) -> pd.Series:
    """সপ্তাহের দিন অনুযায়ী মোট বিক্রি রিটার্ন করে"""
    return df.groupby('Day_of_Week')['Total'].sum().sort_values(ascending=False)

def get_segmentation(df: pd.DataFrame) -> pd.DataFrame:
    """কাস্টমার টাইপ ও জেন্ডার ভিত্তিক সেগমেন্টেশন"""
    return df.groupby(['Customer type', 'Gender']).agg({
        'Total': ['sum', 'mean', 'count'],
        'Rating': 'mean'
    })

def detect_outliers_iqr(df: pd.DataFrame, column: str = 'Total') -> pd.DataFrame:
    """IQR পদ্ধতিতে আউটলায়ার শনাক্ত করে"""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return df[(df[column] < lower) | (df[column] > upper)]

def get_pareto_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """পারেটো অ্যানালাইসিস (৮০/২০ নিয়ম)"""
    product_sales = get_product_sales(df)
    cumulative = (product_sales.cumsum() / product_sales.sum()) * 100
    pareto_df = pd.DataFrame({
        'Product Line': product_sales.index,
        'Total Sales': product_sales.values,
        'Cumulative %': cumulative.values
    })
    return pareto_df

def generate_all_insights(df: pd.DataFrame) -> dict:
    """সব ইনসাইট একত্রে একটি ডিকশনারিতে রিটার্ন করে"""
    insights = {
        'branch_sales': get_branch_sales(df),
        'product_sales': get_product_sales(df),
        'day_sales': get_day_sales(df),
        'segmentation': get_segmentation(df),
        'outliers': detect_outliers_iqr(df),
        'pareto': get_pareto_analysis(df)
    }
    return insights