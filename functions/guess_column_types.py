#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Column Type Guessing Function
ฟังก์ชันสำหรับเดาประเภทข้อมูลของแต่ละคอลัมน์จากไฟล์ CSV
"""

import re
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


def guess_column_types(file_path, delimiter=',', has_headers=True):
    """
    เดาประเภทข้อมูลของแต่ละคอลัมน์จากไฟล์ CSV
    
    Args:
        file_path: path ของไฟล์ CSV
        delimiter: ตัวแบ่งคอลัมน์ (default: ',')
        has_headers: มี header หรือไม่ (default: True)
        
    Returns:
        tuple: (success: bool, result: dict หรือ error_message: str)
    """
    try:
        # Read the CSV file using the specified delimiter and header settings
        df = pd.read_csv(file_path, sep=delimiter, low_memory=False, header=0 if has_headers else None)

        # Initialize a dictionary to store column data types
        column_types = {}

        # Loop through columns and infer data types
        for column in df.columns:
            # Check for datetime format "YYYY-MM-DD HH:MM:SS"
            is_datetime = all(re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', str(value)) for value in df[column].dropna())

            # Check for date format "YYYY-MM-DD"
            is_date = all(re.match(r'\d{4}-\d{2}-\d{2}', str(value)) for value in df[column].dropna())

            # Assign data type based on format detection
            if is_datetime:
                inferred_type = 'datetime64'
            elif is_date:
                inferred_type = 'date'
            else:
                inferred_type = pd.api.types.infer_dtype(df[column], skipna=True)

            column_types[column] = inferred_type

        return (True, column_types)  # Return success and column types
    except Exception as e:
        return (False, str(e))  # Return error message


if __name__ == "__main__":
    # Example usage
    file_path = '../dataops-foundation-jenkins/data/LoanStats_web_small.csv'
    success, result = guess_column_types(file_path)
    
    if success:
        print("✅ Column types detected successfully:")
        for col, dtype in list(result.items())[:10]:  # Show first 10
            print(f"   {col}: {dtype}")
        print(f"   ... and {len(result)-10} more columns")
    else:
        print(f"❌ Error: {result}")
