"""
লগিং কনফিগারেশন মডিউল
"""
import logging
import os
from datetime import datetime

def setup_logger(name: str = "supermarket_analysis") -> logging.Logger:
    """
    কনসোল ও ফাইলে লগ লেখার জন্য Logger সেটআপ করে।
    লগ ফাইল 'logs/' ফোল্ডারে তৈরি হবে।
    """
    # logs ফোল্ডার তৈরি (না থাকলে)
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # লগ ফাইলের নাম: project_name_YYYYMMDD.log
    log_file = os.path.join(log_dir, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")
    
    # লগার তৈরি
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # সব লেভেল ক্যাপচার করবে
    
    # ফাইল হ্যান্ডলার (সব লেভেল ফাইলে যাবে)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # কনসোল হ্যান্ডলার (শুধু INFO ও তার উপরে কনসোলে দেখাবে)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # ফরম্যাট নির্ধারণ (সময়, লেভেল, মেসেজ)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # হ্যান্ডলার যোগ করা (যেন ডুপ্লিকেট না হয়)
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger