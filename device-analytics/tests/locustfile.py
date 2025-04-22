from locust import HttpUser, task, between

class DeviceUser(HttpUser):
    wait_time = between(1, 5)  # Время ожидания между запросами (1–5 секунд)

    @task
    def add_device_data(self):
        device_id = "device1"
        data = {
            "x": 1.23,
            "y": 4.56,
            "z": 7.89
        }
        self.client.post(f"/api/devices/{device_id}/data", json=data)

    @task
    def get_device_analytics(self):
        device_id = "device1"
        start_date = "2023-01-01"
        end_date = "2023-12-31"
        self.client.get(f"/api/devices/{device_id}/analytics?start_date={start_date}&end_date={end_date}")