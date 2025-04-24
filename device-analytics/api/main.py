from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Модель данных
class DeviceData(BaseModel):
    x: float
    y: float
    z: float

# Пример хранилища данных
data_store = []

@app.post("/api/devices/{device_id}/data")
async def add_device_data(device_id: str, data: DeviceData):
    timestamp = datetime.utcnow()
    data_store.append({"device_id": device_id, "data": data.dict(), "timestamp": timestamp})
    return {"status": "success", "device_id": device_id, "timestamp": timestamp}

@app.get("/api/devices/{device_id}/analytics")
async def get_device_analytics(device_id: str, start_date: str, end_date: str):
    filtered_data = [
        item for item in data_store
        if item["device_id"] == device_id and start_date <= item["timestamp"] <= end_date
    ]
    if not filtered_data:
        raise HTTPException(status_code=404, detail="No data found for the given period")
    values_x = [item["data"]["x"] for item in filtered_data]
    values_y = [item["data"]["y"] for item in filtered_data]
    values_z = [item["data"]["z"] for item in filtered_data]
    return {
        "min": {"x": min(values_x), "y": min(values_y), "z": min(values_z)},
        "max": {"x": max(values_x), "y": max(values_y), "z": max(values_z)},
        "count": len(filtered_data),
        "sum": {"x": sum(values_x), "y": sum(values_y), "z": sum(values_z)},
        "median": {"x": median(values_x), "y": median(values_y), "z": median(values_z)}
    }



# Подключение папки static для обслуживания статических файлов
# app.mount("/static", StaticFiles(directory="static"), name="static")
