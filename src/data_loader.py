import pandas as pd
import sys
from .config import DATA_PATH, EXPECTED_COLUMNS
from .logger import setup_logger

logger = setup_logger()

def load_data(file_path: str = DATA_PATH) -> pd.DataFrame:
    """
    CSV ফাইল লোড করে, ভ্যালিডেশন করে।
    """
    logger.info(f"ডেটা লোড করা শুরু: {file_path}")
    
    try:
        df = pd.read_csv(file_path)
        logger.debug(f"ফাইল সাইজ: {sys.getsizeof(df)} বাইটস")
        
    except FileNotFoundError:
        logger.error(f"ফাইল পাওয়া যায়নি: '{file_path}'")
        raise FileNotFoundError(f"❌ ডেটা ফাইল '{file_path}' খুঁজে পাওয়া যায়নি। দয়া করে ফাইলটি 'data/' ফোল্ডারে রাখুন।")
        
    except pd.errors.EmptyDataError:
        logger.error("ফাইলটি সম্পূর্ণ খালি (Empty CSV)")
        raise ValueError("❌ CSV ফাইলটি খালি। কোনো ডেটা নেই।")
        
    except pd.errors.ParserError:
        logger.error("CSV পার্সিং-এ সমস্যা (ভুল ফরম্যাট)")
        raise ValueError("❌ CSV ফাইলটি সঠিক ফরম্যাটে নেই। কমা (,) দিয়ে আলাদা করা ফাইল দিন।")
        
    except Exception as e:
        logger.exception("অজানা এরর হয়েছে")  # exception() পুরো ট্রেসব্যাক লগ করে
        raise RuntimeError(f"❌ ডেটা লোডে সমস্যা: {str(e)}")
    
    # --- ডেটা ভ্যালিডেশন (কলাম চেক) ---
    missing_cols = [col for col in EXPECTED_COLUMNS if col not in df.columns]
    if missing_cols:
        logger.error(f"প্রত্যাশিত কলাম পাওয়া যায়নি: {missing_cols}")
        raise KeyError(f"❌ ডেটাসেটে '{missing_cols}' কলাম নেই। ডেটাসেটটি কি সঠিক?")
    
    # ডেটা খালি কিনা চেক
    if df.empty:
        logger.warning("ডেটাফ্রেম খালি (০ সারি)")
        raise ValueError("❌ ডেটাফ্রেমে কোনো সারি নেই।")
    
    logger.info(f"✅ ডেটা সফলভাবে লোড হয়েছে। {df.shape[0]} সারি, {df.shape[1]} কলাম।")
    return df