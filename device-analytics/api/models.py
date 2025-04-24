from sqlalchemy import Column, Integer, String, Float, DateTime
from api.database import Base

class DeviceData(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    timestamp = Column(DateTime)
