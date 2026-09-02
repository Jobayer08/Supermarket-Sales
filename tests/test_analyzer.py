"""
analyzer মডিউলের ইউনিট টেস্ট
"""
import pytest
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analyzer import (
    get_branch_sales,
    get_product_sales,
    detect_outliers_iqr,
    get_segmentation
)

# প্রতিটি টেস্টের জন্য একটি সাধারণ ডামি ডেটাফ্রেম তৈরি করা (Fixture)
@pytest.fixture
def sample_df():
    """টেস্টের জন্য একটি ছোট ডামি ডেটাফ্রেম তৈরি করে"""
    return pd.DataFrame({
        'Branch': ['A', 'A', 'B', 'B', 'C'],
        'Product line': ['Food', 'Sports', 'Food', 'Sports', 'Food'],
        'Sales': [100, 200, 150, 50, 500],
        'Rating': [4.0, 5.0, 3.0, 4.5, 2.0],
        'Customer type': ['Member', 'Normal', 'Member', 'Member', 'Normal'],
        'Gender': ['Female', 'Male', 'Male', 'Female', 'Female']
    })

def test_get_branch_sales(sample_df):
    """শাখা অনুযায়ী বিক্রির যোগফল সঠিক কিনা চেক"""
    result = get_branch_sales(sample_df)
    
    # Branch A: 100+200 = 300, Branch B: 150+50 = 200, Branch C: 500
    assert result['A'] == 300
    assert result['B'] == 200
    assert result['C'] == 500
    assert len(result) == 3  # মোট ৩টি শাখা

def test_get_product_sales(sample_df):
    """পণ্যライン অনুযায়ী বিক্রির যোগফল সঠিক কিনা চেক"""
    result = get_product_sales(sample_df)
    
    # Food: 100 (A) + 150 (B) + 500 (C) = 750, Sports: 200 (A) + 50 (B) = 250
    assert result['Food'] == 750
    assert result['Sports'] == 250

def test_detect_outliers_iqr(sample_df):
    """IQR পদ্ধতিতে আউটলায়ার ডিটেকশন সঠিক কিনা"""
    # এই ডেটাতে C Branch-এর 500 মানটি আউটলায়ার হবে (অন্যগুলো ৫০-২০০ এর মধ্যে)
    result = detect_outliers_iqr(sample_df, column='Sales')
    
    # আউটলায়ার হিসেবে কেবল 500 থাকা উচিত (C ব্রাঞ্চের সারি)
    assert len(result) == 1
    assert result['Sales'].iloc[0] == 500

def test_get_segmentation_shape(sample_df):
    """সেগমেন্টেশন ডেটাফ্রেমের সঠিক আকৃতি আছে কিনা"""
    result = get_segmentation(sample_df)
    
    # Customer type (Member/Normal) X Gender (Male/Female) = মোট ৪টি কম্বিনেশন
    # আমাদের ডেটাতে Member-Female (1), Member-Male (2), Normal-Female (2), Normal-Male (1) -> ৪টি
    assert len(result) == 4
    assert 'Sales' in result.columns.get_level_values(0)  # MultiIndex চেক