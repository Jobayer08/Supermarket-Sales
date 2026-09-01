"""
Supermarket Sales Analysis - Main Pipeline
এই স্ক্রিপ্ট পুরো অ্যানালাইসিস পাইপলাইন চালায়।
"""
import sys
import os

# src মডিউল ইম্পোর্ট করার জন্য পাথ অ্যাড করা (প্রয়োজন হলে)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import load_data
from src.data_cleaner import clean_data
from src.analyzer import generate_all_insights, detect_outliers_iqr
from src.visualizer import save_visualizations
from src.config import DATA_PATH

def print_insight_report(insights: dict) -> None:
    """ইনসাইট রিপোর্ট কনসোলে প্রিন্ট করে"""
    print("\n" + "="*60)
    print("         ব্যবসায়িক ইনসাইট রিপোর্ট")
    print("         Supermarket Sales Analysis")
    print("="*60)
    
    # Branch
    branch = insights['branch_sales']
    top_branch = branch.index[0]
    print(f"\n📌 শাখা পারফরম্যান্স: {top_branch} শাখায় সবচেয়ে বেশি বিক্রি (${branch.values[0]:,.2f})")
    
    # Pareto
    pareto = insights['pareto']
    p80_count = (pareto['Cumulative %'] <= 80).sum()
    print(f"\n📌 পারেটো অ্যানালাইসিস: {p80_count} টি পণ্যライン ৮০% বিক্রি তৈরি করছে।")
    
    # Day
    day = insights['day_sales']
    print(f"\n📌 সেরা দিন: {day.index[0]} (মোট বিক্রি: ${day.values[0]:,.2f})")
    
    # Outliers
    outliers = insights['outliers']
    print(f"\n📌 হাই-ভ্যালু অর্ডার: {len(outliers)} টি অস্বাভাবিক বড় অর্ডার শনাক্ত হয়েছে।")
    
    # Segmentation
    seg = insights['segmentation']
    top_seg = seg['Total']['mean'].idxmax()
    top_val = seg['Total']['mean'].max()
    print(f"\n📌 টপ সেগমেন্ট: {top_seg[0]} - {top_seg[1]} (গড় খরচ: ${top_val:.2f})")
    
    print("\n" + "="*60 + "\n")

def main():
    """প্রধান ফাংশন"""
    print("🚀 Supermarket Sales Analysis Pipeline শুরু হচ্ছে...")
    
    try:
        # Step 1: Load
        df = load_data(DATA_PATH)
        
        # Step 2: Clean
        df = clean_data(df)
        
        # Step 3: Add Day of Week
        df['Day_of_Week'] = df['Date'].dt.day_name()
        
        # Step 4: Analyze
        print("\n🔍 অ্যানালাইসিস চলছে...")
        insights = generate_all_insights(df)
        
        # Step 5: Visualize
        print("\n📊 ভিজুয়ালাইজেশন তৈরি হচ্ছে...")
        save_visualizations(df)
        
        # Step 6: Report
        print_insight_report(insights)
        
        print("✅ পুরো পাইপলাইন সফলভাবে সম্পন্ন হয়েছে!")
        
    except Exception as e:
        print(f"\n❌ পাইপলাইনে এরর হয়েছে: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()