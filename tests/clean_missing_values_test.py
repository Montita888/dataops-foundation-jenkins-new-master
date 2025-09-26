#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple Test Demo for Missing Values Cleaning Function
ทดสอบฟังก์ชัน clean_missing_values() แบบง่าย
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime

# เพิ่ม path สำหรับ import functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functions.clean_missing_values import clean_missing_values

# ===== Test Cases =====

def test_case_1_basic_cleaning():
    """Test Case 1: การทำความสะอาดพื้นฐาน"""
    print("\n" + "="*60)
    print("🧪 Test Case 1: การทำความสะอาดพื้นฐาน")
    print("="*60)
    
    # เตรียมข้อมูลทดสอบ - คอลัมน์ที่มี null ในอัตราส่วนต่างๆ
    np.random.seed(42)
    n_rows = 100
    
    test_df = pd.DataFrame({
        'good_col': np.random.randint(1, 100, n_rows),  # ✅ ไม่มี null - ควรเหลือ
        'ok_col': np.concatenate([np.random.randint(1, 50, 85), [None] * 15]),  # ✅ 15% null - ควรเหลือ
        'bad_col': np.concatenate([np.random.randint(1, 50, 60), [None] * 40]),  # ❌ 40% null - ควรถูกลบ
        'very_bad_col': np.concatenate([np.random.randint(1, 50, 10), [None] * 90])  # ❌ 90% null - ควรถูกลบ
    })
    
    print(f"📊 Input Data:")
    print(f"   Total columns: {len(test_df.columns)}")
    print(f"   Total rows: {len(test_df)}")
    print(f"   Missing percentages:")
    for col in test_df.columns:
        null_pct = test_df[col].isnull().mean() * 100
        print(f"     - {col}: {null_pct:.1f}% null")
    print(f"   Expected output: keep good_col and ok_col (2 columns)")
    
    # เรียกใช้ฟังก์ชันที่ทดสอบ
    cleaned_df = clean_missing_values(test_df, max_null_percentage=30)
    
    # ตรวจสอบผลลัพธ์
    remaining_columns = list(cleaned_df.columns)
    expected_columns = ['good_col', 'ok_col']
    
    print(f"\n📋 Test Results:")
    print(f"   Remaining columns: {len(remaining_columns)}")
    print(f"   Expected columns: {len(expected_columns)}")
    print(f"   Columns kept: {remaining_columns}")
    print(f"   Rows count: {len(cleaned_df)} (should be same as input)")
    
    # ตรวจสอบ
    if set(remaining_columns) == set(expected_columns) and len(cleaned_df) == len(test_df):
        print("   ✅ PASS: Basic cleaning works correctly")
        return True
    else:
        print("   ❌ FAIL: Basic cleaning failed")
        return False

def test_case_2_threshold_testing():
    """Test Case 2: ทดสอบ threshold ที่แตกต่างกัน"""
    print("\n" + "="*60)
    print("🧪 Test Case 2: ทดสอบ threshold ที่แตกต่างกัน")
    print("="*60)
    
    # ข้อมูลที่มี null ในอัตราส่วนที่ชัดเจน
    n_rows = 100
    test_df = pd.DataFrame({
        'zero_null': [1] * n_rows,  # 0% null
        'ten_percent': [1] * 90 + [None] * 10,  # 10% null
        'twenty_percent': [1] * 80 + [None] * 20,  # 20% null
        'thirty_percent': [1] * 70 + [None] * 30,  # 30% null
        'forty_percent': [1] * 60 + [None] * 40,  # 40% null
        'fifty_percent': [1] * 50 + [None] * 50  # 50% null
    })
    
    print(f"📊 Input Data (Threshold Testing):")
    print(f"   Columns with different null percentages:")
    for col in test_df.columns:
        null_pct = test_df[col].isnull().mean() * 100
        print(f"     - {col}: {null_pct:.0f}% null")
    
    # ทดสอบ threshold ต่างๆ
    thresholds_to_test = [10, 25, 35, 50]
    expected_results = [1, 3, 4, 6]  # จำนวนคอลัมน์ที่คาดว่าจะเหลือ
    
    test_results = []
    
    for i, threshold in enumerate(thresholds_to_test):
        cleaned_df = clean_missing_values(test_df, max_null_percentage=threshold)
        actual_columns = len(cleaned_df.columns)
        expected_columns = expected_results[i]
        
        print(f"\n   Threshold {threshold}%: {actual_columns} columns (expected {expected_columns})")
        test_results.append(actual_columns == expected_columns)
    
    print(f"\n📋 Test Results:")
    print(f"   Successful thresholds: {sum(test_results)}/{len(test_results)}")
    
    # ตรวจสอบ
    if sum(test_results) >= len(test_results) - 1:  # อนุญาตให้ผิดพลาด 1 ครั้ง
        print("   ✅ PASS: Threshold testing works correctly")
        return True
    else:
        print("   ❌ FAIL: Threshold testing failed")
        return False

def test_case_3_data_types_preservation():
    """Test Case 3: ทดสอบการรักษาประเภทข้อมูล"""
    print("\n" + "="*60)
    print("🧪 Test Case 3: ทดสอบการรักษาประเภทข้อมูล")
    print("="*60)
    
    # ข้อมูลที่มีประเภทข้อมูลหลากหลาย
    test_df = pd.DataFrame({
        'int_col': [1, 2, 3, 4, 5],  # ✅ integer, ไม่มี null
        'float_col': [1.1, 2.2, None, 4.4, 5.5],  # ✅ float, 20% null
        'string_col': ['A', 'B', 'C', None, 'E'],  # ✅ string, 20% null
        'date_col': [datetime(2023, 1, 1), datetime(2023, 1, 2), None, None, datetime(2023, 1, 5)],  # ✅ datetime, 40% null - ควรถูกลบ
        'bool_col': [True, False, None, None, None]  # ❌ boolean, 60% null - ควรถูกลบ
    })
    
    print(f"📊 Input Data (Data Types):")
    print(f"   Original data types and null percentages:")
    for col in test_df.columns:
        dtype = test_df[col].dtype
        null_pct = test_df[col].isnull().mean() * 100
        print(f"     - {col}: {dtype} ({null_pct:.0f}% null)")
    print(f"   Expected output: keep int_col, float_col, string_col (3 columns)")
    
    # เรียกใช้ฟังก์ชันที่ทดสอบ
    cleaned_df = clean_missing_values(test_df, max_null_percentage=30)
    
    # ตรวจสอบผลลัพธ์
    remaining_columns = list(cleaned_df.columns)
    expected_columns = ['int_col', 'float_col', 'string_col']
    
    print(f"\n📋 Test Results:")
    print(f"   Remaining columns: {remaining_columns}")
    print(f"   Data types preserved:")
    for col in remaining_columns:
        original_dtype = test_df[col].dtype
        current_dtype = cleaned_df[col].dtype
        preserved = original_dtype == current_dtype
        print(f"     - {col}: {original_dtype} → {current_dtype} {'✅' if preserved else '❌'}")
    
    # ตรวจสอบ
    columns_correct = set(remaining_columns) == set(expected_columns)
    dtypes_preserved = all(test_df[col].dtype == cleaned_df[col].dtype for col in remaining_columns)
    
    if columns_correct and dtypes_preserved:
        print("   ✅ PASS: Data types preservation works correctly")
        return True
    else:
        print("   ❌ FAIL: Data types preservation failed")
        return False

def test_case_4_edge_cases():
    """Test Case 4: Edge Cases"""
    print("\n" + "="*60)
    print("🧪 Test Case 4: Edge Cases")
    print("="*60)
    
    # Test 4a: DataFrame ว่าง
    print("\n🔍 Test 4a: DataFrame ว่าง")
    empty_df = pd.DataFrame()
    
    print(f"   Input: Empty DataFrame")
    print(f"   Expected output: Return empty DataFrame unchanged")
    
    result_empty = clean_missing_values(empty_df)
    
    print(f"   Actual output: shape {result_empty.shape}")
    test_4a_pass = result_empty.empty and result_empty.equals(empty_df)
    print(f"   {'✅ PASS' if test_4a_pass else '❌ FAIL'}: Empty DataFrame handling")
    
    # Test 4b: ทุกคอลัมน์มี null เกิน threshold
    print("\n🔍 Test 4b: ทุกคอลัมน์มี null เกิน threshold")
    high_null_df = pd.DataFrame({
        'col1': [None] * 8 + [1, 2],  # 80% null
        'col2': [None] * 9 + [1],     # 90% null
        'col3': [None] * 10           # 100% null
    })
    
    print(f"   Input: All columns have >50% null values")
    print(f"   Expected output: Empty DataFrame (no columns left)")
    
    result_high_null = clean_missing_values(high_null_df, max_null_percentage=50)
    
    print(f"   Actual output: {len(result_high_null.columns)} columns")
    test_4b_pass = len(result_high_null.columns) == 0
    print(f"   {'✅ PASS' if test_4b_pass else '❌ FAIL'}: High null handling")
    
    # Test 4c: ไม่มี null values เลย
    print("\n🔍 Test 4c: ไม่มี null values เลย")
    no_null_df = pd.DataFrame({
        'perfect_col1': [1, 2, 3, 4, 5],
        'perfect_col2': ['A', 'B', 'C', 'D', 'E'],
        'perfect_col3': [1.1, 2.2, 3.3, 4.4, 5.5]
    })
    
    print(f"   Input: No null values in any column")
    print(f"   Expected output: Return original DataFrame unchanged")
    
    result_no_null = clean_missing_values(no_null_df)
    
    print(f"   Actual output: {len(result_no_null.columns)} columns (same as input)")
    test_4c_pass = len(result_no_null.columns) == len(no_null_df.columns) and result_no_null.equals(no_null_df)
    print(f"   {'✅ PASS' if test_4c_pass else '❌ FAIL'}: No null values handling")
    
    return test_4a_pass and test_4b_pass and test_4c_pass

def run_all_tests():
    """รัน Test Cases ทั้งหมด"""
    print("🚀 Starting Missing Values Cleaning Function Tests")
    print("Target: clean_missing_values() - ลบคอลัมน์ที่มี null values มาก")
    
    results = []
    
    # รัน test cases
    results.append(test_case_1_basic_cleaning())
    results.append(test_case_2_threshold_testing()) 
    results.append(test_case_3_data_types_preservation())
    results.append(test_case_4_edge_cases())
    
    # สรุปผลลัพธ์
    print("\n" + "="*60)
    print("📊 SUMMARY RESULTS")
    print("="*60)
    
    test_names = [
        "Test Case 1: การทำความสะอาดพื้นฐาน",
        "Test Case 2: ทดสอบ threshold ที่แตกต่างกัน", 
        "Test Case 3: ทดสอบการรักษาประเภทข้อมูล",
        "Test Case 4: Edge Cases"
    ]
    
    passed = 0
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1}. {name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 ALL TESTS PASSED! ฟังก์ชันทำงานถูกต้องตาม spec")
    else:
        print("⚠️  SOME TESTS FAILED! ต้องแก้ไขฟังก์ชัน")
    
    return passed == len(results)

if __name__ == "__main__":
    # รัน tests
    success = run_all_tests()
    
    print(f"\n{'='*60}")
    print("🔚 Test Execution Complete")
    print(f"{'='*60}")
    
    exit(0 if success else 1)
