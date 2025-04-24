from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import List
from api.database import get_db
from api.models import DeviceData

app = FastAPI()

# Модель данных
class DeviceDataInput(BaseModel):
    x: float
    y: float
    z: float

# Добавление данных устройства
@app.post("/api/devices/{device_id}/data")
async def add_device_data(device_id: str, data: DeviceDataInput, db: Session = Depends(get_db)):
    new_data = DeviceData(
        device_id=device_id,
        x=data.x,
        y=data.y,
        z=data.z,
        timestamp=datetime.utcnow()
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return {"status": "success", "device_id": device_id, "timestamp": new_data.timestamp}

# Получение аналитики
@app.get("/api/devices/{device_id}/analytics")
async def get_device_analytics(
    device_id: str,
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
):
    filtered_data = (
        db.query(DeviceData)
        .filter(DeviceData.device_id == device_id, DeviceData.timestamp.between(start_date, end_date))
        .all()
    )
    if not filtered_data:
        raise HTTPException(status_code=404, detail="No data found for the given period")

    values_x = [item.x for item in filtered_data]
    values_y = [item.y for item in filtered_data]
    values_z = [item.z for item in filtered_data]

    return {
        "min": {"x": min(values_x), "y": min(values_y), "z": min(values_z)},
        "max": {"x": max(values_x), "y": max(values_y), "z": max(values_z)},
        "count": len(filtered_data),
        "sum": {"x": sum(values_x), "y": sum(values_y), "z": sum(values_z)},
        "median": {
            "x": median(values_x),
            "y": median(values_y),
            "z": median(values_z)
        }
    }

from statistics import median  # Не забудьте импортировать функцию median
