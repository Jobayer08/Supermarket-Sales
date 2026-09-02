import pandas as pd
from .config import STRING_COLUMNS
from .logger import setup_logger

logger = setup_logger()

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    ডেটা ক্লিনিং (ডুপ্লিকেট, টাইপ কনভার্সন, স্ট্রিপিং)
    """
    if not isinstance(df, pd.DataFrame):
        logger.error("ইনপুট DataFrame নয়")
        raise TypeError("❌ clean_data() প্যারামিটারটি অবশ্যই pandas DataFrame হতে হবে।")
    
    logger.info("ডেটা ক্লিনিং শুরু...")
    df_clean = df.copy()
    
    try:
        # Date কনভার্ট
        df_clean['Date'] = pd.to_datetime(df_clean['Date'], errors='coerce')
        # errors='coerce' দিলে ভুল তারিখগুলো NaT (Not a Time) হয়ে যাবে, যা পরে হ্যান্ডেল করা যায়
        
        # স্ট্রিপিং
        for col in STRING_COLUMNS:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].astype(str).str.strip()
        
        # ডুপ্লিকেট
        initial_len = len(df_clean)
        df_clean.drop_duplicates(inplace=True)
        if len(df_clean) < initial_len:
            logger.info(f"ডুপ্লিকেট সরানো হয়েছে: {initial_len - len(df_clean)} টি")
        
        # নেগেটিভ ভ্যালু চেক (Total)
        if (df_clean['Sales'] < 0).any():
            logger.warning("নেগেটিভ টোটাল মান পাওয়া গেছে! এগুলো ০ দিয়ে রিপ্লেস করা হচ্ছে।")
            df_clean.loc[df_clean['Sales'] < 0, 'Sales'] = 0
        
        # অবৈধ রেটিং
        invalid = df_clean[(df_clean['Rating'] < 0) | (df_clean['Rating'] > 10)]
        if len(invalid) > 0:
            logger.warning(f"অবৈধ রেটিং ({len(invalid)} টি) পাওয়া গেছে। এগুলো ড্রপ করা হচ্ছে।")
            df_clean = df_clean[(df_clean['Rating'] >= 0) & (df_clean['Rating'] <= 10)]
        
        logger.info("✅ ডেটা ক্লিনিং সম্পন্ন হয়েছে।")
        return df_clean
        
    except KeyError as e:
        logger.exception("ক্লিনিং-এ কলাম না পাওয়া গেছে")
        raise KeyError(f"❌ কলাম পাওয়া যায়নি: {str(e)}. ডেটা কি আগে থেকেই ক্লিন করা?")
    except Exception as e:
        logger.exception("ক্লিনিং-এ অজানা এরর")
        raise RuntimeError(f"❌ ক্লিনিং প্রক্রিয়া ব্যর্থ: {str(e)}")