"""
ডেটা ক্লিনিং করার মডিউল
"""
import pandas as pd
from .config import STRING_COLUMNS

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    ডেটা ক্লিনিং করে: ডেটাটাইপ কনভার্সন, স্ট্রিপিং, ডুপ্লিকেট রিমুভ।
    
    Parameters:
    df (pd.DataFrame): ইনপুট ডেটা
    
    Returns:
    pd.DataFrame: ক্লিন করা ডেটা
    """
    # 1. ডেটার কপি তৈরি (মূল ডেটা নষ্ট না করতে)
    df_clean = df.copy()
    
    # 2. Date কে datetime-এ কনভার্ট
    df_clean['Date'] = pd.to_datetime(df_clean['Date'])
    
    # 3. স্ট্রিং কলাম থেকে স্পেস সরানো
    for col in STRING_COLUMNS:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].str.strip()
    
    # 4. ডুপ্লিকেট ড্রপ করা (যদি থাকে)
    initial_len = len(df_clean)
    df_clean.drop_duplicates(inplace=True)
    if len(df_clean) < initial_len:
        print(f"🧹 ডুপ্লিকেট ডেটা সরানো হয়েছে: {initial_len - len(df_clean)} টি সারি।")
    
    # 5. ইন্ভ্যালিড রেটিং চেক (ঐচ্ছিক সতর্কতা)
    invalid_ratings = df_clean[(df_clean['Rating'] < 0) | (df_clean['Rating'] > 10)]
    if len(invalid_ratings) > 0:
        print(f"⚠️ সতর্কতা: {len(invalid_ratings)} টি সারিতে অবৈধ রেটিং (০-১০ এর বাইরে) পাওয়া গেছে।")
    
    print("✅ ডেটা ক্লিনিং সম্পন্ন হয়েছে।")
    return df_clean