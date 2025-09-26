#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Date Range Filtering Function
ฟังก์ชันสำหรับกรองข้อมูลตามช่วงวันที่ที่กำหนด
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


def filter_issue_date_range(df: pd.DataFrame, date_column: str = 'issue_d', min_year: int = 2016, max_year: int = 2019) -> pd.DataFrame:
    """
    กรองข้อมูลตามช่วงปีที่กำหนด (default: 2016-2019)
    
    Args:
        df: DataFrame ต้นฉบับ
        date_column: ชื่อคอลัมน์วันที่ (default: 'issue_d')
        min_year: ปีขั้นต่ำ (default: 2016)
        max_year: ปีสูงสุด (default: 2019)
        
    Returns:
        DataFrame ที่กรองตามช่วงปีแล้ว
    """
    if date_column not in df.columns:
        print(f"Warning: Column '{date_column}' not found in DataFrame")
        return df
    
    original_rows = len(df)
    
    # แปลงเป็น datetime ถ้ายังไม่ได้แปลง
    if not pd.api.types.is_datetime64_any_dtype(df[date_column]):
        if df[date_column].dtype == 'object':
            try:
                df = df.copy()
                df[date_column] = pd.to_datetime(df[date_column], format='%b-%Y')
            except:
                try:
                    df[date_column] = pd.to_datetime(df[date_column])
                except:
                    print(f"Error: Cannot convert {date_column} to datetime")
                    return df
    
    # กรองตามช่วงปี
    df_filtered = df[
        (df[date_column].dt.year >= min_year) & 
        (df[date_column].dt.year <= max_year)
    ].copy()
    
    filtered_rows = len(df_filtered)
    removed_rows = original_rows - filtered_rows
    
    if removed_rows > 0:
        print(f"Date filtering: removed {removed_rows:,} rows outside {min_year}-{max_year}")
        print(f"Remaining records: {filtered_rows:,} ({filtered_rows/original_rows*100:.1f}%)")
    
    return df_filtered


if __name__ == "__main__":
    # Example usage
    file_path = '../dataops-foundation-jenkins/data/LoanStats_web_small.csv'
    
    try:
        df = pd.read_csv(file_path, low_memory=False)
        print(f"Original data: {len(df):,} rows")
        
        if 'issue_d' in df.columns:
            filtered_df = filter_issue_date_range(df)
            print(f"Filtered data: {len(filtered_df):,} rows")
        else:
            print("Column 'issue_d' not found in the dataset")
            
    except Exception as e:
        print(f"Error: {e}")
