from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import sqlite3

app = FastAPI()

# SQLiteデータベースの初期化
def init_db():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            check_in_time TEXT,
            check_out_time TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# 従業員のデータモデル
class Employee(BaseModel):
    name: str

# 出勤エンドポイント
@app.post("/check_in")
def check_in(employee: Employee):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    # 現在の日時と日付
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    today = datetime.now().strftime("%Y-%m-%d")
    
    # データベースに出勤データを挿入
    cursor.execute('''
        INSERT INTO attendance (employee_name, check_in_time, check_out_time, date)
        VALUES (?, ?, NULL, ?)
    ''', (employee.name, now, today))
    
    conn.commit()
    conn.close()
    return {"message": "出勤登録完了"}

# 退勤エンドポイント
@app.post("/check_out")
def check_out(employee: Employee):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    # 現在の日時
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 出勤している従業員を検索し、退勤時刻を更新
    cursor.execute('''
        UPDATE attendance
        SET check_out_time = ?
        WHERE employee_name = ? AND check_out_time IS NULL AND date = ?
    ''', (now, employee.name, datetime.now().strftime("%Y-%m-%d")))

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="出勤記録が見つかりません")
    
    conn.commit()
    conn.close()
    return {"message": "退勤登録完了"}

# 出退勤の全データを取得するエンドポイント
@app.get("/attendance")
def get_attendance():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT employee_name, check_in_time, IFNULL(check_out_time, "未退勤"), date FROM attendance
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [{"従業員名": row[0], "出勤時刻": row[1], "退勤時刻": row[2], "日付": row[3]} for row in rows]

