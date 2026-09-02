"""
data_cleaner মডিউলের ইউনিট টেস্ট
"""
import pytest
import pandas as pd
import sys
import os

# src ফোল্ডারকে পাথে যোগ করা (যাতে ইম্পোর্ট কাজ করে)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_cleaner import clean_data

def test_clean_data_strip():
    """স্ট্রিং কলাম থেকে স্পেস সঠিকভাবে কাটছে কিনা টেস্ট"""
    # ডামি ডেটা (যাতে Date ও Rating আছে, কারণ clean_data এগুলো চেক করে)
    df = pd.DataFrame({
        'Branch': [' A ', 'B  ', '  C'],
        'City': ['  Dhaka', 'Chittagong  ', '  Rajshahi '],
        'Date': ['01/01/2023', '02/01/2023', '03/01/2023'],
        'Product line': ['Health', 'Sports', 'Food'],
        'Sales': [100, 200, 300],
        'Rating': [5.0, 7.0, 9.0]
    })
    
    cleaned_df = clean_data(df)
    
    # চেক করা: স্পেস কাটা হয়েছে কিনা
    assert cleaned_df['Branch'].iloc[0] == 'A'
    assert cleaned_df['Branch'].iloc[1] == 'B'
    assert cleaned_df['Branch'].iloc[2] == 'C'
    assert cleaned_df['City'].iloc[0] == 'Dhaka'

def test_clean_data_invalid_rating():
    """অবৈধ রেটিং (০-১০ এর বাইরে) ড্রপ হচ্ছে কিনা টেস্ট"""
    df = pd.DataFrame({
        'Branch': ['A', 'B'],
        'City': ['X', 'Y'],
        'Date': ['01/01/2023', '02/01/2023'],
        'Product line': ['Food', 'Sports'],
        'Sales': [100, 200],
        'Rating': [15.0, -5.0]  # এই দুটোই ইনভ্যালিড
    })
    
    cleaned_df = clean_data(df)
    
    # যেহেতু দুটো সারিই ইনভ্যালিড, ডেটাফ্রেম খালি হয়ে যাওয়া উচিত
    assert len(cleaned_df) == 0

def test_clean_data_duplicate():
    """ডুপ্লিকেট ডেটা সরানো হচ্ছে কিনা টেস্ট"""
    df = pd.DataFrame({
        'Branch': ['A', 'A', 'B'],
        'City': ['X', 'X', 'Y'],
        'Date': ['01/01/2023', '01/01/2023', '02/01/2023'],
        'Product line': ['Food', 'Food', 'Sports'],
        'Sales': [100, 100, 200],
        'Rating': [5.0, 5.0, 6.0]
    })
    
    cleaned_df = clean_data(df)
    
    # প্রথম দুটি সারি ডুপ্লিকেট, তাই ২টি ইউনিক সারি থাকা উচিত
    assert len(cleaned_df) == 2

def test_clean_data_type():
    """Date কলাম datetime-এ কনভার্ট হচ্ছে কিনা টেস্ট"""
    df = pd.DataFrame({
        'Branch': ['A'],
        'City': ['X'],
        'Date': ['2023-01-01'],
        'Product line': ['Food'],
        'Sales': [100],
        'Rating': [5.0]
    })
    
    cleaned_df = clean_data(df)
    
    # চেক করা: ডেটাটাইপ datetime64[ns] কিনা
    assert pd.api.types.is_datetime64_any_dtype(cleaned_df['Date'])