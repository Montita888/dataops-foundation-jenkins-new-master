#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple Test Demo for Date Filtering Function
ทดสอบฟังก์ชัน filter_issue_date_range() แบบง่าย
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime

# เพิ่ม path สำหรับ import functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functions.filter_issue_date_range import filter_issue_date_range

# ===== Test Cases =====

def test_case_1_basic_filtering():
    """Test Case 1: การกรองพื้นฐาน"""
    print("\n" + "="*60)
    print("🧪 Test Case 1: การกรองพื้นฐาน")
    print("="*60)
    
    # เตรียมข้อมูลทดสอบ - หลายปี
    dates_2015 = pd.date_range('2015-01-01', '2015-12-31', freq='3M')  # ❌ ต้องถูกกรองออก
    dates_2016_2019 = pd.date_range('2016-01-01', '2019-12-31', freq='3M')  # ✅ ต้องเหลืออยู่
    dates_2020 = pd.date_range('2020-01-01', '2020-12-31', freq='3M')  # ❌ ต้องถูกกรองออก
    
    all_dates = list(dates_2015) + list(dates_2016_2019) + list(dates_2020)
    
    test_df = pd.DataFrame({
        'issue_d': all_dates,
        'loan_amnt': np.random.randint(1000, 50000, len(all_dates)),
        'loan_id': range(1, len(all_dates) + 1)
    })
    
    print(f"📊 Input Data:")
    print(f"   Total records: {len(test_df)}")
    print(f"   Years in data: {sorted(test_df['issue_d'].dt.year.unique())}")
    print(f"   Expected output: only 2016-2019 (should be {len(dates_2016_2019)} records)")
    
    # เรียกใช้ฟังก์ชันที่ทดสอบ
    filtered_df = filter_issue_date_range(test_df)
    
    # ตรวจสอบผลลัพธ์
    actual_years = sorted(filtered_df['issue_d'].dt.year.unique())
    expected_count = len(dates_2016_2019)
    actual_count = len(filtered_df)
    
    print(f"\n📋 Test Results:")
    print(f"   Actual records: {actual_count}")
    print(f"   Expected records: {expected_count}")
    print(f"   Years in result: {actual_years}")
    
    # ตรวจสอบ
    if actual_count == expected_count and set(actual_years) <= {2016, 2017, 2018, 2019}:
        print("   ✅ PASS: Basic filtering works correctly")
        return True
    else:
        print("   ❌ FAIL: Basic filtering failed")
        return False

def test_case_2_boundary_testing():
    """Test Case 2: ทดสอบขอบเขต (Boundary Testing)"""
    print("\n" + "="*60)
    print("🧪 Test Case 2: ทดสอบขอบเขต (Boundary Testing)")
    print("="*60)
    
    # ข้อมูลขอบเขตที่สำคัญ
    boundary_dates = [
        datetime(2015, 12, 31),  # ❌ วันสุดท้ายปี 2015 - ต้องถูกกรองออก
        datetime(2016, 1, 1),    # ✅ วันแรกปี 2016 - ต้องเหลืออยู่
        datetime(2019, 12, 31),  # ✅ วันสุดท้ายปี 2019 - ต้องเหลืออยู่
        datetime(2020, 1, 1)     # ❌ วันแรกปี 2020 - ต้องถูกกรองออก
    ]
    
    boundary_df = pd.DataFrame({
        'issue_d': boundary_dates,
        'loan_amnt': [10000, 20000, 30000, 40000],
        'description': ['Last day 2015', 'First day 2016', 'Last day 2019', 'First day 2020']
    })
    
    print(f"📊 Input Data (Boundary Cases):")
    for i, row in boundary_df.iterrows():
        print(f"   {row['description']}: {row['issue_d'].strftime('%Y-%m-%d')}")
    print(f"   Expected output: only 2016-01-01 and 2019-12-31 (2 records)")
    
    # เรียกใช้ฟังก์ชันที่ทดสอบ
    filtered_df = filter_issue_date_range(boundary_df)
    
    # ตรวจสอบผลลัพธ์
    actual_count = len(filtered_df)
    remaining_dates = filtered_df['issue_d'].dt.strftime('%Y-%m-%d').tolist()
    
    print(f"\n📋 Test Results:")
    print(f"   Actual records: {actual_count}")
    print(f"   Expected records: 2")
    print(f"   Remaining dates: {remaining_dates}")
    
    # ตรวจสอบ
    expected_dates = ['2016-01-01', '2019-12-31']
    if actual_count == 2 and set(remaining_dates) == set(expected_dates):
        print("   ✅ PASS: Boundary testing works correctly")
        return True
    else:
        print("   ❌ FAIL: Boundary testing failed")
        return False

def test_case_3_string_format():
    """Test Case 3: ทดสอบรูปแบบข้อมูล String"""
    print("\n" + "="*60)
    print("🧪 Test Case 3: ทดสอบรูปแบบข้อมูล String")
    print("="*60)
    
    # ข้อมูลรูปแบบ string (ตามข้อมูลจริงในระบบ)
    string_dates = [
        'Dec-2015',  # ❌ ปี 2015 - ต้องถูกกรองออก
        'Jan-2016',  # ✅ ปี 2016 - ต้องเหลืออยู่
        'Jun-2017',  # ✅ ปี 2017 - ต้องเหลืออยู่
        'Dec-2019',  # ✅ ปี 2019 - ต้องเหลืออยู่
        'Jan-2020'   # ❌ ปี 2020 - ต้องถูกกรองออก
    ]
    
    string_df = pd.DataFrame({
        'issue_d': string_dates,
        'loan_amnt': [15000, 25000, 35000, 45000, 55000],
        'status': ['Old', 'Valid', 'Valid', 'Valid', 'New']
    })
    
    print(f"📊 Input Data (String Format):")
    for i, row in string_df.iterrows():
        print(f"   {row['issue_d']} ({row['status']})")
    print(f"   Expected output: Jan-2016, Jun-2017, Dec-2019 (3 records)")
    
    # เรียกใช้ฟังก์ชันที่ทดสอบ
    filtered_df = filter_issue_date_range(string_df)
    
    # ตรวจสอบผลลัพธ์
    actual_count = len(filtered_df)
    result_dates = filtered_df['issue_d'].dt.strftime('%b-%Y').tolist()
    is_datetime = pd.api.types.is_datetime64_any_dtype(filtered_df['issue_d'])
    
    print(f"\n📋 Test Results:")
    print(f"   Actual records: {actual_count}")
    print(f"   Expected records: 3")
    print(f"   Result dates: {result_dates}")
    print(f"   Converted to datetime: {is_datetime}")
    
    # ตรวจสอบ
    expected_dates = ['Jan-2016', 'Jun-2017', 'Dec-2019']
    if actual_count == 3 and set(result_dates) == set(expected_dates) and is_datetime:
        print("   ✅ PASS: String format handling works correctly")
        return True
    else:
        print("   ❌ FAIL: String format handling failed")
        return False

def test_case_4_edge_cases():
    """Test Case 4: Edge Cases"""
    print("\n" + "="*60)
    print("🧪 Test Case 4: Edge Cases")
    print("="*60)
    
    # Test 4a: ไม่มีข้อมูลในช่วง 2016-2019
    print("\n🔍 Test 4a: ไม่มีข้อมูลในช่วง 2016-2019")
    old_dates = pd.date_range('2010-01-01', '2015-12-31', freq='6M')
    old_df = pd.DataFrame({
        'issue_d': old_dates,
        'loan_amnt': np.random.randint(1000, 50000, len(old_dates))
    })
    
    print(f"   Input: {len(old_df)} records from 2010-2015")
    print(f"   Expected output: 0 records")
    
    filtered_old = filter_issue_date_range(old_df)
    
    print(f"   Actual output: {len(filtered_old)} records")
    test_4a_pass = len(filtered_old) == 0
    print(f"   {'✅ PASS' if test_4a_pass else '❌ FAIL'}: Empty result handling")
    
    # Test 4b: ไม่มีคอลัมน์ issue_d
    print("\n🔍 Test 4b: ไม่มีคอลัมน์ issue_d")
    no_date_df = pd.DataFrame({
        'loan_amnt': [1000, 2000, 3000],
        'other_column': ['A', 'B', 'C']
    })
    
    print(f"   Input: DataFrame without 'issue_d' column")
    print(f"   Expected output: Return original DataFrame unchanged")
    
    result_no_date = filter_issue_date_range(no_date_df)
    
    test_4b_pass = len(result_no_date) == len(no_date_df) and result_no_date.equals(no_date_df)
    print(f"   Actual output: {len(result_no_date)} records (same as input)")
    print(f"   {'✅ PASS' if test_4b_pass else '❌ FAIL'}: Missing column handling")
    
    return test_4a_pass and test_4b_pass

def run_all_tests():
    """รัน Test Cases ทั้งหมด"""
    print("🚀 Starting Date Filtering Function Tests")
    print("Target: filter_issue_date_range() - เก็บเฉพาะข้อมูลปี 2016-2019")
    
    results = []
    
    # รัน test cases
    results.append(test_case_1_basic_filtering())
    results.append(test_case_2_boundary_testing()) 
    results.append(test_case_3_string_format())
    results.append(test_case_4_edge_cases())
    
    # สรุปผลลัพธ์
    print("\n" + "="*60)
    print("📊 SUMMARY RESULTS")
    print("="*60)
    
    test_names = [
        "Test Case 1: การกรองพื้นฐาน",
        "Test Case 2: ทดสอบขอบเขต", 
        "Test Case 3: รูปแบบข้อมูล String",
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
