import sys
import os
from turtle import pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import load_data
from src.data_cleaner import clean_data
from src.analyzer import generate_all_insights
from src.visualizer import save_visualizations
from src.config import DATA_PATH
from src.logger import setup_logger
from src.report_generator import generate_all_reports   # ← ইম্পোর্ট করা আছে

# গ্লোবাল লগার
logger = setup_logger()

def print_insight_report(insights: dict) -> None:
    """ইনসাইট প্রিন্ট (লগার দিয়ে) - Segmentation এরর হ্যান্ডলিং সহ"""
    logger.info("="*60)
    logger.info("ব্যবসায়িক ইনসাইট রিপোর্ট")
    logger.info("="*60)
    
    branch = insights['branch_sales']
    logger.info(f"শাখা পারফরম্যান্স: {branch.index[0]} (সর্বোচ্চ: ${branch.values[0]:,.2f})")
    
    pareto = insights['pareto']
    p80_count = (pareto['Cumulative %'] <= 80).sum()
    logger.info(f"পারেটো: {p80_count} টি পণ্যライン ৮০% বিক্রি তৈরি করছে।")
    
    day = insights['day_sales']
    logger.info(f"সেরা দিন: {day.index[0]} (${day.values[0]:,.2f})")
    
    outliers = insights['outliers']
    logger.info(f"হাই-ভ্যালু অর্ডার: {len(outliers)} টি")
    
    # Segmentation অংশটি নিরাপদভাবে হ্যান্ডেল করা
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
        logger.info(f"টপ সেগমেন্ট: {top_seg[0]} - {top_seg[1]} (গড়: ${mean_series.max():.2f})")
    except Exception as e:
        logger.warning(f"Segmentation data issue: {e}")
        logger.info("টপ সেগমেন্ট: ডেটা পাওয়া যায়নি")
    
    logger.info("="*60)

def main():
    """মেইন পাইপলাইন"""
    logger.info("🚀 Supermarket Sales Pipeline শুরু হচ্ছে...")
    
    try:
        # 1. ডেটা লোড
        df = load_data(DATA_PATH)
        
        # 2. ডেটা ক্লিন
        df = clean_data(df)
        
        # 3. ফিচার ইঞ্জিনিয়ারিং
        logger.info("ফিচার ইঞ্জিনিয়ারিং: Day of Week যোগ করা হচ্ছে")
        df['Day_of_Week'] = df['Date'].dt.day_name()
        
        # 4. অ্যানালাইসিস
        logger.info("অ্যানালাইসিস চলছে...")
        insights = generate_all_insights(df)
        
        # 5. ভিজুয়ালাইজেশন
        logger.info("ভিজুয়ালাইজেশন তৈরি হচ্ছে...")
        save_visualizations(df)
        
        # 6. রিপোর্ট জেনারেশন (Excel, CSV, TXT)
        logger.info("রিপোর্ট জেনারেট করা হচ্ছে...")
        generate_all_reports(insights, df)   # ← এই লাইনটি যোগ করা হলো
        
        # 7. কনসোল রিপোর্ট
        print_insight_report(insights)
        
        logger.info("✅ পুরো পাইপলাইন সফলভাবে সম্পন্ন হয়েছে!")
        
    except FileNotFoundError as e:
        logger.critical(str(e))
        print(f"\n{str(e)}")
        sys.exit(1)
    except KeyError as e:
        logger.critical(str(e))
        print(f"\n{str(e)}")
        sys.exit(1)
    except ValueError as e:
        logger.critical(str(e))
        print(f"\n{str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"অপ্রত্যাশিত এরর: {str(e)}", exc_info=True)
        print(f"\n❌ অপ্রত্যাশিত সমস্যা! বিস্তারিত লগ ফাইলে দেখুন।")
        sys.exit(1)

if __name__ == "__main__":
    main()