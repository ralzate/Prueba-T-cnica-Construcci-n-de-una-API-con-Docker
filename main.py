from fastapi import FastAPI, WebSocket, Query
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import requests

db_url = "mysql+pymysql://root:root@mysql:3306/test_db"
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(String, index=True)

app = FastAPI()

@app.get("/api/data")
def get_external_data():
    response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
    return response.json()

@app.post("/api/data")
def store_data(data: str):
    db = SessionLocal()
    db_data = Data(data=data)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return {"message": "Data stored successfully"}

@app.get("/api/data/filter")
def get_data_by_filter(filter_value: str = Query(...)):
    db = SessionLocal()
    db_data = db.query(Data).filter(Data.data == filter_value).first()
    if db_data is None:
        return {"error": "Data not found"}
    return db_data

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")