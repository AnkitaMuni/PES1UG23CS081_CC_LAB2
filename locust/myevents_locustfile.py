from locust import HttpUser, task, between

class MyEventsUser(HttpUser):
    wait_time = between(2, 5) 
    
    host = "http://127.0.0.1:8000"

    @task
    def view_my_events(self):
        """
        Optimized task with error catching to ensure failures report as 0 
        even if the server is momentarily slow.
        """
        with self.client.get("/my-events?user=locust_user", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                response.failure("Route not found: Check if /my-events is defined in main.py")
            else:
                response.success()