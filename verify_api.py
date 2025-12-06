from fastapi.testclient import TestClient
from app.main import app
from app.models.models import Priority, TaskType

client = TestClient(app)

def test_flow():
    print("Starting verification...")

    # 1. Signup
    print("Testing Signup...")
    signup_data = {
        "email": "test@student.com",
        "password": "password123",
        "full_name": "Test Student",
        "school": "UNILAG",
        "department": "Computer Science",
        "level": "300"
    }
    response = client.post("/api/v1/auth/signup", params=signup_data)
    if response.status_code == 400 and "already exists" in response.text:
        print("User already exists, proceeding to login.")
    else:
        assert response.status_code == 200, f"Signup failed: {response.text}"
        print("Signup successful.")

    # 2. Login
    print("Testing Login...")
    login_data = {
        "username": "test@student.com",
        "password": "password123"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Login successful.")

    # 3. Create Task
    print("Testing Create Task...")
    task_data = {
        "title": "Finish Backend Project",
        "description": "Complete the Campulse MVP backend.",
        "due_date": "2025-12-31T23:59:59",
        "priority": "High",
        "type": "Assignment",
        "user_id": 1 # This will be ignored/overwritten by the backend
    }
    response = client.post("/api/v1/tasks/", json=task_data, headers=headers)
    assert response.status_code == 200, f"Create Task failed: {response.text}"
    task_id = response.json()["id"]
    print("Create Task successful.")

    # 4. Get Tasks
    print("Testing Get Tasks...")
    response = client.get("/api/v1/tasks/", headers=headers)
    assert response.status_code == 200, f"Get Tasks failed: {response.text}"
    tasks = response.json()
    assert len(tasks) > 0
    print(f"Get Tasks successful. Found {len(tasks)} tasks.")

    # 5. Get Opportunities
    print("Testing Get Opportunities...")
    response = client.get("/api/v1/opportunities/")
    assert response.status_code == 200, f"Get Opportunities failed: {response.text}"
    opportunities = response.json()
    assert len(opportunities) > 0
    print(f"Get Opportunities successful. Found {len(opportunities)} opportunities.")

    # 6. Bookmark Opportunity
    print("Testing Bookmark Opportunity...")
    opp_id = opportunities[0]["id"]
    response = client.post(f"/api/v1/opportunities/{opp_id}/bookmark", headers=headers)
    assert response.status_code == 200, f"Bookmark Opportunity failed: {response.text}"
    print("Bookmark Opportunity successful.")

    # 7. Get Tutors
    print("Testing Get Tutors...")
    response = client.get("/api/v1/tutors/")
    assert response.status_code == 200, f"Get Tutors failed: {response.text}"
    tutors = response.json()
    assert len(tutors) > 0
    print(f"Get Tutors successful. Found {len(tutors)} tutors.")

    print("ALL TESTS PASSED!")

if __name__ == "__main__":
    test_flow()
