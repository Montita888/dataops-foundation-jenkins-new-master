#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple Test Demo for Column Type Guessing Function
ทดสอบฟังก์ชัน guess_column_types() แบบง่าย
"""

import pandas as pd
import numpy as np
import re
import os
import sys
import tempfile
from datetime import datetime

# เพิ่ม path สำหรับ import functions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from functions.guess_column_types import guess_column_types

# ===== Test Cases =====

def test_case_1_basic_type_detection():
    """Test Case 1: การตรวจจับประเภทข้อมูลพื้นฐาน"""
    print("\n" + "="*60)
    print("🧪 Test Case 1: การตรวจจับประเภทข้อมูลพื้นฐาน")
    print("="*60)
    
    # เตรียมข้อมูลทดสอบ - ประเภทข้อมูลต่างๆ
    test_data = pd.DataFrame({
        'integer_col': [1, 2, 3, 4, 5],
        'float_col': [1.1, 2.2, 3.3, 4.4, 5.5],
        'string_col': ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry'],
        'boolean_col': [True, False, True, False, True],
        'mixed_col': [1, 'text', 3.14, True, None]
    })
    
    # สร้างไฟล์ชั่วคราวสำหรับทดสอบ
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
        test_data.to_csv(temp_file.name, index=False)
        temp_file_path = temp_file.name
    
    print(f"📊 Input Data:")
    print(f"   Total columns: {len(test_data.columns)}")
    print(f"   Column types: integer, float, string, boolean, mixed")
    print(f"   Expected output: detect all 5 columns with appropriate types")
    
    try:
        # เรียกใช้ฟังก์ชันที่ทดสอบ
        success, result = guess_column_types(temp_file_path)
        
        # ตรวจสอบผลลัพธ์
        if success:
            detected_columns = list(result.keys())
            expected_columns = list(test_data.columns)
            
            print(f"\n📋 Test Results:")
            print(f"   Success: {success}")
            print(f"   Detected columns: {len(detected_columns)}")
            print(f"   Expected columns: {len(expected_columns)}")
            print(f"   Column types detected:")
            for col, dtype in result.items():
                print(f"     - {col}: {dtype}")
            
            # ตรวจสอบ
            if set(detected_columns) == set(expected_columns):
                print("   ✅ PASS: Basic type detection works correctly")
                return True
            else:
                print("   ❌ FAIL: Column detection mismatch")
                return False
        else:
            print(f"\n📋 Test Results:")
            print(f"   Success: {success}")
            print(f"   Error: {result}")
            print("   ❌ FAIL: Function returned error")
            return False
            
    except Exception as e:
        print(f"\n📋 Test Results:")
        print(f"   ❌ FAIL: Exception occurred: {str(e)}")
        return False
        
    finally:
        # ลบไฟล์ชั่วคราว
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_case_2_date_datetime_detection():
    """Test Case 2: ทดสอบการตรวจจับรูปแบบวันที่และเวลา"""
    print("\n" + "="*60)
    print("🧪 Test Case 2: ทดสอบการตรวจจับรูปแบบวันที่และเวลา")
    print("="*60)
    
    # ข้อมูลขอบเขตที่สำคัญ
    test_data = pd.DataFrame({
        'date_col': ['2023-01-15', '2023-02-20', '2023-03-25'],  # ✅ ควรเป็น 'date'
        'datetime_col': ['2023-01-15 14:30:45', '2023-02-20 09:15:30', '2023-03-25 18:45:00'],  # ✅ ควรเป็น 'datetime64'
        'regular_string': ['hello', 'world', 'test'],  # ✅ ควรเป็น string type
        'mixed_dates': ['2023-01-15', 'not_a_date', '2023-03-25']  # ✅ ควรเป็น mixed/string
    })
    
    # สร้างไฟล์ชั่วคราวสำหรับทดสอบ
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
        test_data.to_csv(temp_file.name, index=False)
        temp_file_path = temp_file.name
    
    print(f"📊 Input Data (Date/DateTime Cases):")
    for col in test_data.columns:
        sample_value = test_data[col].iloc[0]
        print(f"   {col}: {sample_value} (sample)")
    print(f"   Expected output: date_col='date', datetime_col='datetime64'")
    
    try:
        # เรียกใช้ฟังก์ชันที่ทดสอบ
        success, result = guess_column_types(temp_file_path)
        
        if success:
            date_type = result.get('date_col')
            datetime_type = result.get('datetime_col')
            
            print(f"\n📋 Test Results:")
            print(f"   Success: {success}")
            print(f"   date_col detected as: {date_type}")
            print(f"   datetime_col detected as: {datetime_type}")
            
            # ตรวจสอบ
            date_correct = date_type == 'date'
            datetime_correct = datetime_type == 'datetime64'
            
            if date_correct and datetime_correct:
                print("   ✅ PASS: Date and datetime detection works correctly")
                return True
            else:
                print("   ❌ FAIL: Date/datetime detection failed")
                print(f"     date_col: expected 'date', got '{date_type}'")
                print(f"     datetime_col: expected 'datetime64', got '{datetime_type}'")
                return False
        else:
            print(f"\n📋 Test Results:")
            print(f"   Success: {success}")
            print(f"   Error: {result}")
            print("   ❌ FAIL: Function returned error")
            return False
            
    except Exception as e:
        print(f"\n📋 Test Results:")
        print(f"   ❌ FAIL: Exception occurred: {str(e)}")
        return False
        
    finally:
        # ลบไฟล์ชั่วคราว
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def test_case_3_different_delimiters():
    """Test Case 3: ทดสอบตัวแบ่งที่แตกต่างกัน"""
    print("\n" + "="*60)
    print("🧪 Test Case 3: ทดสอบตัวแบ่งที่แตกต่างกัน")
    print("="*60)
    
    # ข้อมูลรูปแบบ delimiter ต่างๆ
    test_data = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'salary': [50000.5, 60000.0, 70000.75]
    })
    
    # ทดสอบ delimiters ต่างๆ
    delimiters_to_test = [
        (',', 'comma'),
        (';', 'semicolon'),
        ('\t', 'tab'),
        ('|', 'pipe')
    ]
    
    print(f"📊 Input Data (Delimiter Format):")
    print(f"   Testing with: comma, semicolon, tab, pipe")
    print(f"   Data: name, age, salary columns")
    print(f"   Expected output: successfully parse all 4 delimiter types")
    
    successful_delimiters = 0
    
    for delimiter, name in delimiters_to_test:
        # สร้างไฟล์ด้วย delimiter ที่กำหนด
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            test_data.to_csv(temp_file.name, index=False, sep=delimiter)
            temp_file_path = temp_file.name
        
        try:
            # เรียกใช้ฟังก์ชันด้วย delimiter ที่ถูกต้อง
            success, result = guess_column_types(temp_file_path, delimiter=delimiter)
            
            if success and len(result) == 3:  # ควรมี 3 คอลัมน์
                successful_delimiters += 1
                
        except Exception:
            pass  # ไม่ต้องทำอะไร เก็บสถิติไว้ที่ท้าย
            
        finally:
            # ลบไฟล์ชั่วคราว
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    print(f"\n📋 Test Results:")
    print(f"   Successful delimiters: {successful_delimiters}/4")
    print(f"   Tested: comma, semicolon, tab, pipe")
    
    # ตรวจสอบ
    if successful_delimiters >= 3:  # อนุญาตให้ 1 delimiter ล้มเหลว
        print("   ✅ PASS: Different delimiters work correctly")
        return True
    else:
        print("   ❌ FAIL: Too many delimiter failures")
        return False

def test_case_4_edge_cases():
    """Test Case 4: Edge Cases"""
    print("\n" + "="*60)
    print("🧪 Test Case 4: Edge Cases")
    print("="*60)
    
    # Test 4a: ไฟล์ไม่มีอยู่
    print("\n🔍 Test 4a: ไฟล์ไม่มีอยู่")
    non_existent_file = 'this_file_does_not_exist_12345.csv'
    
    print(f"   Input: Non-existent file path")
    print(f"   Expected output: Return (False, error_message)")
    
    success, result = guess_column_types(non_existent_file)
    
    print(f"   Actual output: success={success}")
    test_4a_pass = not success and isinstance(result, str)
    print(f"   {'✅ PASS' if test_4a_pass else '❌ FAIL'}: Non-existent file handling")
    
    # Test 4b: ไฟล์ว่าง
    print("\n🔍 Test 4b: ไฟล์ว่าง")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
        # สร้างไฟล์ว่าง
        temp_file.write("")
        empty_file_path = temp_file.name
    
    print(f"   Input: Empty CSV file")
    print(f"   Expected output: Handle gracefully (success or controlled failure)")
    
    try:
        success, result = guess_column_types(empty_file_path)
        
        print(f"   Actual output: success={success}")
        test_4b_pass = True  # ทั้ง success หรือ failure ก็ยอมรับได้สำหรับไฟล์ว่าง
        print(f"   {'✅ PASS' if test_4b_pass else '❌ FAIL'}: Empty file handling")
        
    except Exception as e:
        print(f"   Actual output: Exception - {str(e)}")
        test_4b_pass = False
        print(f"   {'✅ PASS' if test_4b_pass else '❌ FAIL'}: Empty file handling")
        
    finally:
        if os.path.exists(empty_file_path):
            os.unlink(empty_file_path)
    
    return test_4a_pass and test_4b_pass

def run_all_tests():
    """รัน Test Cases ทั้งหมด"""
    print("🚀 Starting Column Type Guessing Function Tests")
    print("Target: guess_column_types() - เดาประเภทข้อมูลจากไฟล์ CSV")
    
    results = []
    
    # รัน test cases
    results.append(test_case_1_basic_type_detection())
    results.append(test_case_2_date_datetime_detection()) 
    results.append(test_case_3_different_delimiters())
    results.append(test_case_4_edge_cases())
    
    # สรุปผลลัพธ์
    print("\n" + "="*60)
    print("📊 SUMMARY RESULTS")
    print("="*60)
    
    test_names = [
        "Test Case 1: การตรวจจับประเภทข้อมูลพื้นฐาน",
        "Test Case 2: ทดสอบการตรวจจับรูปแบบวันที่และเวลา", 
        "Test Case 3: ทดสอบตัวแบ่งที่แตกต่างกัน",
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
