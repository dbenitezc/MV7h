import requests
import os
from fpdf import FPDF
from datetime import datetime

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    return user_data["id"]

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    return response.json()["id"]

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()

def get_tasks():
    return requests.get(TASKS_URL).json()

def generate_pdf_report(content):
    os.makedirs("reports", exist_ok=True)
    index = 1
    while os.path.exists(f"reports/test_report_{index}.pdf"):
        index += 1

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in content.splitlines():
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(f"reports/test_report_{index}.pdf")

def integration_test():
    log = []
    try:
        log.append("INTEGRATION TEST STARTED")
        user_id = create_user("Camilo_Test")
        log.append(f"PASS: Created user ID: {user_id}")

        task_id = create_task(user_id, "Prepare presentation (test)")
        log.append(f"PASS: Created task ID: {task_id}")

        tasks = get_tasks()
        assert any(t["id"] == task_id for t in tasks), "FAIL: Task not found in list"
        log.append("PASS: Verified task exists")

        # Cleanup
        delete_task(task_id)
        delete_user(user_id)
        log.append("Deleted task and user")

        # Verify deletion
        tasks = get_tasks()
        assert not any(t["id"] == task_id for t in tasks), "FAIL: Task still exists after deletion"
        log.append("PASS: Verified task deletion")

        log.append("BACKEND TEST PASSED")
    except Exception as e:
        log.append(f"Test Failed: {str(e)}")
    finally:
        generate_pdf_report("\n".join(log))

if __name__ == "__main__":
    integration_test()