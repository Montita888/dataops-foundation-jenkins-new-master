# Data Directory

ไฟล์นี้เป็นโฟลเดอร์สำหรับเก็บข้อมูล

## ข้อมูลที่ต้องการ:
- `LoanStats_web_small.csv` - ไฟล์ข้อมูล loan สำหรับการทดสอบ ETL

## หมายเหตุ:
- ใน Jenkins pipeline ข้อมูลจะถูกอ่านจาก workspace ที่ clone มาจาก Git
- สำหรับการทดสอบ local ให้ copy ไฟล์จาก `../dataops-foundation-jenkins/data/LoanStats_web_small.csv`

## Symlink (สำหรับ Linux/Mac):
```bash
ln -s ../dataops-foundation-jenkins/data/LoanStats_web_small.csv data/LoanStats_web_small.csv
```

## Copy (สำหรับ Windows):
```cmd
copy ..\dataops-foundation-jenkins\data\LoanStats_web_small.csv data\
```
