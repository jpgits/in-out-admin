import streamlit as st
import requests
import pandas as pd

# FastAPIエンドポイント
API_URL = "http://localhost:8000"

# 従業員リスト
EMPLOYEE_LIST = ['従業員1', '従業員2', '従業員3', '従業員4', '従業員5',
                 '従業員6', '従業員7', '従業員8', '従業員9', '従業員10',
                 '従業員11', '従業員12']

# 初期状態（全員退勤済みに設定）
initial_status = {employee: {"status": "退勤済み", "check_in_time": None, "check_out_time": None} for employee in EMPLOYEE_LIST}

# 出勤処理
def check_in(employee_name):
    if employee_name:
        response = requests.post(f"{API_URL}/check_in", json={"name": employee_name})
        if response.status_code == 200:
            st.success(f"{employee_name}の出勤が登録されました")
        else:
            st.error("エラーが発生しました")

# 退勤処理
def check_out(employee_name):
    if employee_name:
        response = requests.post(f"{API_URL}/check_out", json={"name": employee_name})
        if response.status_code == 200:
            st.success(f"{employee_name}の退勤が登録されました")
        else:
            st.error("エラーが発生しました")

# 出退勤データを取得して状態を更新
def update_attendance_status():
    response = requests.get(f"{API_URL}/attendance")
    if response.status_code == 200:
        data = response.json()
        # 現在の状態を従業員ごとに更新
        status = initial_status.copy()
        for record in data:
            status[record["従業員名"]]["status"] = "出勤中" if record["退勤時刻"] == "未退勤" else "退勤済み"
            status[record["従業員名"]]["check_in_time"] = record["出勤時刻"].split(" ")[1]  # 時間だけを抽出
            status[record["従業員名"]]["check_out_time"] = None if record["退勤時刻"] == "未退勤" else record["退勤時刻"].split(" ")[1]
        return status
    else:
        st.error("データの取得に失敗しました")
        return initial_status

def display_attendance():
    # 出勤状況を取得して更新
    status = update_attendance_status()

    # データフレーム作成
    df = pd.DataFrame({
        '従業員名': EMPLOYEE_LIST,
        '現状': [status[employee]["status"] for employee in EMPLOYEE_LIST],
        '出勤時刻': [status[employee]["check_in_time"] for employee in EMPLOYEE_LIST],
        '退勤時刻': [status[employee]["check_out_time"] for employee in EMPLOYEE_LIST]
    })
    
    # インデックスを1始まりに設定
    df.index = df.index + 1
    
    # データフレームを表示（高さと幅を調整してスクロールを回避）
    st.dataframe(df, height=480, width=1000)

# UI

# 従業員を選択
employee_name = st.selectbox("従業員名を選択してください", EMPLOYEE_LIST)

# 出勤・退勤ボタン
col1, col2 = st.columns(2)

with col1:
    if st.button("出勤"):
        check_in(employee_name)

with col2:
    if st.button("退勤"):
        check_out(employee_name)
# 出退勤状況の表示
display_attendance()

