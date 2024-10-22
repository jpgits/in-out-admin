from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class User(BaseModel):
    name: str

# 時刻を記録するためのエンドポイント
@app.post("/record_time/")
def record_time(user: User):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"user": user.name, "time": current_time}

@app.post("/end_time/")
def end_time(user: User):
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    return {"user": user.name, "time": current_time}
