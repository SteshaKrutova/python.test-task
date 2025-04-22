# Модели базы данных с использованием SQLAlchemy.
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Строка подключения
DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/mydb"

# Создание движка
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание базового класса для моделей
Base = declarative_base()

# Тестирование подключения
try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Error: {e}")

# Модель данных устройства
class DeviceData(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    timestamp = Column(DateTime)