"""
রিপোর্ট জেনারেশন মডিউল (CSV, Excel, TXT)
"""
import pandas as pd
import os
from datetime import datetime
from .logger import setup_logger

logger = setup_logger()

def ensure_reports_dir():
    """reports ফোল্ডার তৈরি করে (না থাকলে)"""
    os.makedirs('reports', exist_ok=True)

def export_cleaned_data(df: pd.DataFrame) -> str:
    """
    ক্লিন করা ডেটা CSV আকারে রিপোর্ট ফোল্ডারে সেভ করে
    """
    ensure_reports_dir()
    file_path = 'reports/cleaned_data.csv'
    df.to_csv(file_path, index=False)
    logger.info(f"✅ ক্লিন ডেটা সেভ হয়েছে: {file_path}")
    return file_path

def export_insights_excel(insights: dict) -> str:
    """
    সব অ্যানালাইসিস ফল একটি Excel ফাইলে একাধিক শিটে সেভ করে
    """
    ensure_reports_dir()
    file_path = 'reports/analysis_report.xlsx'
    
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        # 1. Branch Sales
        insights['branch_sales'].to_excel(writer, sheet_name='Branch Sales')
        
        # 2. Product Sales
        insights['product_sales'].to_excel(writer, sheet_name='Product Sales')
        
        # 3. Pareto Analysis
        insights['pareto'].to_excel(writer, sheet_name='Pareto Analysis', index=False)
        
        # 4. Segmentation (MultiIndex - flatten করে দেওয়া ভালো)
        seg = insights['segmentation']
        # MultiIndex কে ফ্ল্যাট করা
        seg.columns = ['_'.join(col).strip() for col in seg.columns.values]
        seg.reset_index(inplace=True)  # Customer type, Gender কে কলাম বানানো
        seg.to_excel(writer, sheet_name='Segmentation', index=False)
        
        # 5. Outliers
        outliers = insights['outliers']
        if not outliers.empty:
            outliers.to_excel(writer, sheet_name='Outliers', index=False)
        else:
            # খালি শিট না রেখে একটি মেসেজ দেওয়া
            pd.DataFrame({'Message': ['No outliers detected!']}).to_excel(writer, sheet_name='Outliers', index=False)
        
        # 6. (অতিরিক্ত) Summary Statistics
        summary_stats = insights.get('summary_stats')
        if summary_stats is not None:
            summary_stats.to_excel(writer, sheet_name='Summary Stats')
    
    logger.info(f"✅ এক্সেল রিপোর্ট সেভ হয়েছে: {file_path}")
    return file_path

def export_summary_text(insights: dict, df: pd.DataFrame) -> str:
    """
    কনসোলের ইনসাইট রিপোর্টকে একটি টেক্সট ফাইল হিসেবে সেভ করে
    """
    ensure_reports_dir()
    file_path = 'reports/summary_report.txt'
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("         ব্যবসায়িক ইনসাইট রিপোর্ট\n")
        f.write("         Supermarket Sales Analysis\n")
        f.write(f"         রিপোর্ট জেনারেট: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")
        
        # 1. Branch
        branch = insights['branch_sales']
        f.write(f"📌 শাখা পারফরম্যান্স:\n")
        f.write(f"   শীর্ষ শাখা: {branch.index[0]} (মোট: ${branch.values[0]:,.2f})\n")
        f.write(f"   দ্বিতীয়: {branch.index[1]} (${branch.values[1]:,.2f})\n\n")
        
        # 2. Product
        product = insights['product_sales']
        f.write(f"📌 পণ্যライン টপ ৩:\n")
        for i in range(min(3, len(product))):
            f.write(f"   {i+1}. {product.index[i]}: ${product.values[i]:,.2f}\n")
        f.write("\n")
        
        # 3. Pareto
        pareto = insights['pareto']
        p80_count = (pareto['Cumulative %'] <= 80).sum()
        f.write(f"📌 পারেটো অ্যানালাইসিস:\n")
        f.write(f"   {p80_count} টি পণ্যライン ৮০%% বিক্রি তৈরি করছে।\n\n")
        
        # 4. Day
        day = insights['day_sales']
        f.write(f"📌 সপ্তাহের দিন:\n")
        f.write(f"   সেরা দিন: {day.index[0]} (${day.values[0]:,.2f})\n")
        f.write(f"   সবচেয়ে কম: {day.index[-1]} (${day.values[-1]:,.2f})\n\n")
        
        # 5. Segmentation (সংশোধিত অংশ)
        seg = insights['segmentation']
        try:
            # মাল্টি-ইনডেক্স চেক করা
            if ('Sales', 'mean') in seg.columns:
                mean_series = seg[('Sales', 'mean')]
            elif 'Sales' in seg.columns and 'mean' in seg.columns:
                mean_series = seg['Sales']['mean'] if isinstance(seg['Sales'], pd.DataFrame) else seg['mean']
            else:
                raise KeyError("Segmentation columns not found")
            
            top_seg = mean_series.idxmax()
            f.write(f"📌 টপ কাস্টমার সেগমেন্ট:\n")
            f.write(f"   {top_seg[0]} - {top_seg[1]} (গড় খরচ: ${mean_series.max():,.2f})\n\n")
        except Exception as e:
            logger.warning(f"Segmentation data issue: {e}")
            f.write("📌 টপ কাস্টমার সেগমেন্ট:\n")
            f.write("   ডেটা পাওয়া যায়নি।\n\n")
        
        # 6. Outliers
        outliers = insights['outliers']
        f.write(f"📌 হাই-ভ্যালু অর্ডার (আউটলায়ার):\n")
        f.write(f"   মোট {len(outliers)} টি অস্বাভাবিক বড় অর্ডার শনাক্ত হয়েছে।\n")
        if not outliers.empty:
            f.write(f"   সর্বোচ্চ অর্ডার মূল্য: ${outliers['Sales'].max():,.2f}\n\n")
        else:
            f.write("   কোনো আউটলায়ার নেই।\n\n")
        
        # 7. Basic Stats
        f.write("📌 মৌলিক পরিসংখ্যান:\n")
        f.write(f"   মোট বিক্রি: ${df['Sales'].sum():,.2f}\n")
        f.write(f"   গড় বিক্রি: ${df['Sales'].mean():,.2f}\n")
        f.write(f"   মোট অর্ডার: {len(df)} টি\n")
        
        f.write("\n" + "="*60 + "\n")
        f.write("রিপোর্ট শেষ - এই ইনসাইটগুলো ব্যবসার উন্নতিতে সাহায্য করবে\n")
        f.write("="*60 + "\n")
    
    logger.info(f"✅ টেক্সট রিপোর্ট সেভ হয়েছে: {file_path}")
    return file_path

def generate_all_reports(insights: dict, df: pd.DataFrame) -> dict:
    """
    সব রিপোর্ট একসাথে জেনারেট করে
    """
    logger.info("📄 রিপোর্ট জেনারেশন শুরু...")
    reports = {
        'cleaned_data': export_cleaned_data(df),
        'excel_report': export_insights_excel(insights),
        'text_report': export_summary_text(insights, df)
    }
    logger.info("✅ সব রিপোর্ট তৈরি সম্পন্ন!")
    return reports