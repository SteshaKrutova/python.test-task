from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from typing import List
from api.database import get_db  # Импортируем функцию для работы с базой данных
from api.models import DeviceData  # Импортируем модель данных

app = FastAPI()

# Модель данных для входных данных
class DeviceDataInput(BaseModel):
    x: float
    y: float
    z: float

# Добавление данных устройства
@app.post("/api/devices/{device_id}/data")
async def add_device_data(
    device_id: str,
    data: DeviceDataInput,
    db: Session = Depends(get_db)  # Получаем сессию базы данных
):
    # Создаем новую запись в базе данных
    new_data = DeviceData(
        device_id=device_id,
        x=data.x,
        y=data.y,
        z=data.z,
        timestamp=datetime.utcnow()
    )
    db.add(new_data)  # Добавляем запись
    db.commit()  # Сохраняем изменения
    db.refresh(new_data)  # Обновляем объект для получения ID
    return {"status": "success", "device_id": device_id, "timestamp": new_data.timestamp}

# Получение аналитики по данным устройства
@app.get("/api/devices/{device_id}/analytics")
async def get_device_analytics(
    device_id: str,
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)  # Получаем сессию базы данных
):
    # Фильтруем данные по device_id и временному диапазону
    filtered_data = (
        db.query(DeviceData)
        .filter(
            DeviceData.device_id == device_id,
            DeviceData.timestamp.between(start_date, end_date)
        )
        .all()
    )

    # Если данных нет, возвращаем ошибку 404
    if not filtered_data:
        raise HTTPException(status_code=404, detail="No data found for the given period")

    # Вычисляем метрики для координат x, y, z
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

# Импортируем функцию median из модуля statistics
from statistics import median
