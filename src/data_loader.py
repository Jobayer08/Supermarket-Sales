"""
ডেটা লোড করার মডিউল
"""
import pandas as pd
from .config import DATA_PATH

def load_data(file_path: str = DATA_PATH) -> pd.DataFrame:
    """
    CSV ফাইল থেকে ডেটা লোড করে DataFrame আকারে রিটার্ন করে।
    
    Parameters:
    file_path (str): CSV ফাইলের পাথ। ডিফল্ট: config.DATA_PATH
    
    Returns:
    pd.DataFrame: লোড করা ডেটা
    
    Raises:
    FileNotFoundError: ফাইল না পাওয়া গেলে।
    """
    try:
        df = pd.read_csv(file_path)
        print(f"✅ ডেটা সফলভাবে লোড হয়েছে। মোট {df.shape[0]} টি সারি ও {df.shape[1]} টি কলাম।")
        return df
    except FileNotFoundError:
        print(f"❌ এরর: '{file_path}' ফাইলটি পাওয়া যায়নি। পাথ ঠিক আছে কিনা চেক করুন।")
        raise