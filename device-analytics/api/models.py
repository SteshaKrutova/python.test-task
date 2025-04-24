from sqlalchemy import Column, Integer, String, Float, DateTime
from api.database import Base

# Импортируем Base из database.py
from api.database import Base

# Определение модели данных для таблицы "data"
class DeviceData(Base):
    __tablename__ = "data"  # Название таблицы в базе данных

    # Определение колонок таблицы
    id = Column(Integer, primary_key=True, index=True)  # Первичный ключ
    device_id = Column(String, index=True)  # ID устройства
    x = Column(Float)  # Координата X
    y = Column(Float)  # Координата Y
    z = Column(Float)  # Координата Z
    timestamp = Column(DateTime)  # Временная метка
