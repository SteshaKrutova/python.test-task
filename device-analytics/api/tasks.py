from celery import Celery
from statistics import median

celery_app = Celery("tasks", broker="redis://redis:6379/0")

@celery_app.task
def calculate_statistics(data: list[dict]) -> dict:
    values_x = [item["x"] for item in data]
    values_y = [item["y"] for item in data]
    values_z = [item["z"] for item in data]
    return {
        "min": {"x": min(values_x), "y": min(values_y), "z": min(values_z)},
        "max": {"x": max(values_x), "y": max(values_y), "z": max(values_z)},
        "count": len(data),
        "sum": {"x": sum(values_x), "y": sum(values_y), "z": sum(values_z)},
        "median": {"x": median(values_x), "y": median(values_y), "z": median(values_z)}
    }
