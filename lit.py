from pandas.io.parquet import json
import streamlit as st
import requests

# ユーザーリストの作成
users = ["01", "02", "03"]

# ユーザーを選択するセレクトボックス
selected_user = st.selectbox("人を選択してください", users)

# ボタンを押して時刻を記録
if st.button("出勤"):
    response = requests.post("http://localhost:8000/record_time/", json={"name": selected_user})
    if response.status_code == 200:
        data = response.json()
        st.write(f"{data['user']} {data['time']} 記録しました。")
    else:
        st.write("エラーが発生しました")

if st.button("退勤"):
    end_response = requests.post("http://localhost:8000/end_time/", json={"name": selected_user})
    if end_response.status_code == 200:
        data = end_response.json()
        st.write(f"{data['user']} {data['time']} 退勤を記録しました。")
    else:
        st.write("エラーが発生しました")


