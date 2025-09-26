#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Missing Values Cleaning Function
ฟังก์ชันสำหรับทำความสะอาดข้อมูลที่มี missing values
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


def clean_missing_values(df, max_null_percentage=30):
    """
    ลบคอลัมน์ที่มี missing values เกินเปอร์เซ็นต์ที่กำหนด
    
    Args:
        df: DataFrame ต้นฉบับ
        max_null_percentage: เปอร์เซ็นต์สูงสุดของ null ที่ยอมรับได้ (default: 30)
        
    Returns:
        DataFrame ที่กรองคอลัมน์ที่มี null values มากแล้ว
    """
    if df.empty:
        print("Warning: Input DataFrame is empty")
        return df
    
    original_columns = len(df.columns)
    
    # คำนวณ percentage ของ missing values ของแต่ละคอลัมน์
    missing_percentage = df.isnull().mean() * 100
    
    # กรองคอลัมน์ที่มี null เกินกว่า max_null_percentage ออกไป
    columns_to_keep = missing_percentage[missing_percentage <= max_null_percentage].index.tolist()
    
    # สร้าง DataFrame ใหม่จากคอลัมน์ที่เลือก
    filtered_df = df[columns_to_keep]
    
    removed_columns = original_columns - len(filtered_df.columns)
    
    if removed_columns > 0:
        print(f"Missing values cleaning: removed {removed_columns} columns with >{max_null_percentage}% null values")
        print(f"Remaining columns: {len(filtered_df.columns)}/{original_columns} ({len(filtered_df.columns)/original_columns*100:.1f}%)")
    else:
        print(f"Missing values cleaning: all {original_columns} columns kept (≤{max_null_percentage}% null values)")
    
    return filtered_df


if __name__ == "__main__":
    # Example usage
    file_path = '../dataops-foundation-jenkins/data/LoanStats_web_small.csv'
    
    try:
        df = pd.read_csv(file_path, low_memory=False)
        print(f"Original data: {len(df):,} rows, {len(df.columns)} columns")
        
        # Show missing percentage for first few columns
        missing_pct = df.isnull().mean() * 100
        print("\nMissing percentage (top 10 columns):")
        for col, pct in missing_pct.head(10).items():
            print(f"   {col}: {pct:.1f}%")
        
        cleaned_df = clean_missing_values(df, max_null_percentage=30)
        print(f"\nCleaned data: {len(cleaned_df):,} rows, {len(cleaned_df.columns)} columns")
        
    except Exception as e:
        print(f"Error: {e}")
