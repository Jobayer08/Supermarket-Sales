"""
প্রজেক্টের সব কনফিগারেশন ও কনস্ট্যান্ট
"""
import os

# ডেটা ফাইল পাথ (main.py থেকে রান করলে data/ ফোল্ডার এক্সেস করা যায়)
DATA_PATH = 'data/supermarket_sales.csv'

# ভিজুয়ালাইজেশন সেভ করার পাথ
VIZ_PATH = 'visualizations/'

# চার্টের ডিফল্ট সাইজ
FIGURE_SIZE = (10, 6)

# ক্যাটাগরিক্যাল কলামের তালিকা (যেগুলোতে স্ট্রিপিং প্রয়োগ করব)
STRING_COLUMNS = ['Branch', 'City', 'Customer type', 'Gender', 'Product line', 'Payment']

# ভিজুয়ালাইজেশন স্টাইল
PLOT_STYLE = 'darkgrid'

LOG_NAME = "supermarket_analysis"
EXPECTED_COLUMNS = ['Invoice ID', 'Branch', 'City', 'Customer type', 'Gender', 
                    'Product line', 'Unit price', 'Quantity', 'Tax 5%', 'Sales', 
                    'Date', 'Time', 'Payment', 'cogs', 'gross margin percentage', 
                    'gross income', 'Rating']  # ডেটা ভ্যালিডেশনের জন্য