# ETL CI/CD Pipeline Manual

## 📋 ภาพรวม

Pipeline นี้เป็น automated ETL (Extract, Transform, Load) process ที่ใช้ Jenkins สำหรับ CI/CD โดยประมวลผลข้อมูล loan statistics และ deploy ลงฐานข้อมูล MSSQL

## 🏗️ โครงสร้าง Pipeline

```
🔄 Checkout & Setup
    ↓
🐍 Python Environment
    ↓
🧪 Unit Tests (Parallel)
    ├── Test: guess_column_types
    ├── Test: filter_issue_date_range
    └── Test: clean_missing_values
    ↓
🔍 ETL Validation
    ↓
🔄 ETL Processing
    ↓
📤 Deploy to Database
    ↓
🧹 Cleanup
```

## 🔧 Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `DB_SERVER` | 34.10.241.203 | ที่อยู่ database server |
| `DB_NAME` | TestDB | ชื่อ database |
| `DB_USERNAME` | SA | username สำหรับเชื่อมต่อ DB |
| `DB_PASSWORD` | credentials('mssql-password') | รหัสผ่านจาก Jenkins credentials |
| `PYTHON_VERSION` | 3.9 | version ของ Python ที่ใช้ |
| `VIRTUAL_ENV` | venv | ชื่อโฟลเดอร์ virtual environment |
| `DATA_FILE` | data/LoanStats_web_small.csv | path ของไฟล์ข้อมูล |
| `MAX_NULL_PERCENTAGE` | 30 | เปอร์เซ็นต์ null values สูงสุดที่ยอมรับ |
| `MIN_YEAR` | 2016 | ปีเริ่มต้นของข้อมูล |
| `MAX_YEAR` | 2019 | ปีสิ้นสุดของข้อมูล |

## 📝 ขั้นตอนการทำงานโดยละเอียด

### Stage 1: 🔄 Checkout & Setup
**หน้าที่:**
- แสดงข้อมูลการ build (build number, branch, workspace)
- ตรวจสอบไฟล์ที่จำเป็น:
  - `functions/__init__.py`
  - `etl_pipeline.py`
- หากไฟล์ไม่ครบ จะหยุด pipeline ทันที

**ผลลัพธ์ที่ได้:**
```
=== Simple ETL CI/CD Pipeline Started ===
Build: 7
Branch: origin/master
Workspace: /var/jenkins_home/workspace/dataops-foundation-jenkins-new
✅ Project structure verified
```

### Stage 2: 🐍 Python Environment
**หน้าที่:**
1. ลบ virtual environment เก่า (ถ้ามี)
2. สร้าง virtual environment ใหม่
3. เปิดใช้งาน virtual environment
4. อัพเดท pip เป็นเวอร์ชันล่าสุด
5. ติดตั้ง Python packages:
   - pandas, numpy, sqlalchemy, pymssql
   - pytest, pytest-cov
6. ทดสอบว่าติดตั้งสำเร็จหรือไม่

**คำสั่งที่รัน:**
```bash
rm -rf venv
python3 -m venv venv
. venv/bin/activate
python -m pip install --upgrade pip
pip install pandas numpy sqlalchemy pymssql
pip install pytest pytest-cov
```

### Stage 3: 🧪 Unit Tests (Parallel)
**หน้าที่:**
- รัน unit tests แบบ parallel (พร้อมกัน 3 tests)
- ทดสอบ 3 functions หลัก:

#### Test 1: guess_column_types
- ทดสอบการเดาประเภทข้อมูลของคอลัมน์
- ตรวจสอบการตรวจจับ: integer, float, string, boolean, date, datetime
- ทดสอบ delimiter ที่แตกต่างกัน: comma, semicolon, tab, pipe

#### Test 2: filter_issue_date_range
- ทดสอบการกรองข้อมูลตามช่วงวันที่ 2016-2019
- ทดสอบ boundary cases
- ทดสอบรูปแบบข้อมูล string dates

#### Test 3: clean_missing_values
- ทดสอบการลบคอลัมน์ที่มี null values เกิน threshold
- ทดสอบ threshold ที่แตกต่างกัน
- ทดสอบการรักษาประเภทข้อมูล

**ผลลัพธ์ที่ได้:**
```
🎯 Overall Result: 4/4 tests passed
🎉 ALL TESTS PASSED! ฟังก์ชันทำงานถูกต้องตาม spec
```

### Stage 4: 🔍 ETL Validation
**หน้าที่:**
- รันเฉพาะเมื่อ tests ก่อนหน้าผ่าน
- ทดสอบการ import functions
- ตรวจสอบว่าไฟล์ข้อมูลมีอยู่และอ่านได้หรือไม่

**การตรวจสอบ:**
```python
from functions import guess_column_types, filter_issue_date_range, clean_missing_values
df = pd.read_csv('data/LoanStats_web_small.csv', low_memory=False, nrows=10)
```

### Stage 5: 🔄 ETL Processing
**หน้าที่:**
- รัน ETL pipeline แบบ dry-run (ไม่ deploy ลง database)
- ทดสอบว่า ETL process ทำงานได้ปกติ

**ขั้นตอน ETL:**
1. **Analyzing Column Types** - วิเคราะห์ประเภทข้อมูล 144 คอลัมน์
2. **Loading Data** - โหลดข้อมูล 14,422 rows
3. **Cleaning Missing Values** - ลบ 44 คอลัมน์ที่มี null > 30%
4. **Filtering Date Range** - กรองข้อมูลปี 2016-2019
5. **Final Data Cleanup** - ได้ข้อมูลสุดท้าย 9,424 rows
6. **Creating Star Schema** - สร้าง dimension และ fact tables

### Stage 6: 📤 Deploy to Database
**หน้าที่:**
- รัน ETL pipeline แบบ production (deploy จริงลง database)
- ใช้ flag `--deploy` เพื่อ save ข้อมูลลง database

**ผลลัพธ์การ Deploy:**
```
📊 home_ownership_dim: 4 records in database
📊 loan_status_dim: 6 records in database  
📊 issue_d_dim: 30 records in database
📊 loans_fact: 9,424 records in database
```

## 🧹 Post Actions

### Always (รันทุกครั้ง)
- แสดงสรุปผลการ build
- ลบ virtual environment และ cache files:
  ```bash
  rm -rf venv
  find . -name "*.pyc" -delete
  find . -name "__pycache__" -type d -exec rm -rf {} +
  ```

### Success (รันเมื่อสำเร็จ)
```
🎉 ETL Pipeline succeeded!
✅ All tests passed
✅ ETL processing completed
✅ Deployed to MSSQL database
```

### Failure (รันเมื่อล้มเหลว)
```
❌ ETL Pipeline failed!
Please check the console output for details.
```

## ⚙️ การตั้งค่า Pipeline

### Options
- **Build Retention**: เก็บ build logs 30 วัน หรือสูงสุด 20 builds
- **Timeout**: หาก pipeline รันเกิน 20 นาที จะหยุดอัตโนมัติ
- **Timestamps**: แสดงเวลาในทุกบรรทัดของ console output

### When Conditions
- Stage 4-6 จะรันเฉพาะเมื่อ `currentBuild.result != 'FAILURE'`
- ป้องกันการรัน stage ต่อไปเมื่อมี error ก่อนหน้า

## 🔐 Security

### Jenkins Credentials
- รหัสผ่าน database เก็บใน Jenkins Credentials Store
- ใช้ `credentials('mssql-password')` เพื่อดึงค่า
- ไม่ hardcode sensitive information ใน code

### Environment Isolation
- ใช้ virtual environment แยกแต่ละ build
- ลบ environment หลังแต่ละ build เสร็จ
- ป้องกันการปนเปื้อนระหว่าง builds

## 📊 ข้อมูลที่ประมวลผล

### Input Data
- **ไฟล์**: `data/LoanStats_web_small.csv`
- **ขนาดเริ่มต้น**: 14,422 rows, 144 columns
- **ประเภทข้อมูล**: Loan statistics data

### Output Data (Star Schema)
- **home_ownership_dim**: 4 records
- **loan_status_dim**: 6 records  
- **issue_d_dim**: 30 records
- **loans_fact**: 9,424 records

### Data Transformation
- ลบคอลัมน์ที่มี null values > 30%
- กรองข้อมูลเฉพาะปี 2016-2019
- สร้าง star schema สำหรับ data warehouse

## 🎯 จุดเด่นของ Pipeline

### 1. Performance Optimization
- รัน unit tests แบบ parallel ประหยัดเวลา
- ใช้ virtual environment แยกแต่ละ build

### 2. Error Handling
- ใช้ `when` conditions เพื่อหยุด pipeline เมื่อมี error
- ใช้ `||` operator เพื่อป้องกัน cleanup commands ล้มเหลว

### 3. Maintenance
- Auto cleanup หลังแต่ละ build
- Build retention policy เพื่อจัดการ disk space

### 4. Monitoring
- Timestamps ใน console output
- Timeout protection
- Detailed status messages

## 🚀 การใช้งาน

### Prerequisites
1. Jenkins server ที่ติดตั้งแล้ว
2. Python 3.9+ บน Jenkins agent
3. Access ถึง MSSQL database
4. Jenkins credentials สำหรับ database password

### การรัน Pipeline
1. Push code ไป Git repository
2. Jenkins จะ trigger pipeline อัตโนมัติ
3. ดู progress ใน Jenkins dashboard
4. ตรวจสอบผลลัพธ์ใน console output

### การ Debug
1. ดู console output สำหรับ error messages
2. ตรวจสอบ test results ใน parallel stages  
3. ตรวจสอบการเชื่อมต่อ database
4. ตรวจสอบไฟล์ข้อมูลที่ path ที่กำหนด

---

**หมายเหตุ:** Manual นี้อัพเดทล่าสุดเมื่อ July 24, 2025