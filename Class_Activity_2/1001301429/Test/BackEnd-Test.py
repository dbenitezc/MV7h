import requests
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from datetime import datetime


# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

REPORTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports'))


def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("✅ User created:", user_data)
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task created:", task_data)
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def get_task(task_id):
    response = requests.get(f"{TASKS_URL}/{task_id}")
    return response  # no usamos raise_for_status para manejar 404

def get_user(user_id):
    response = requests.get(f"{USERS_URL}/{user_id}")
    return response

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()

def get_next_report_filename():
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return os.path.join(REPORTS_DIR, f"report_{timestamp}.pdf")

def generate_pdf_report(content_lines):
    filename = get_next_report_filename()
    c = canvas.Canvas(filename, pagesize=LETTER)
    width, height = LETTER
    y = height - 50

    for line in content_lines:
        c.drawString(50, y, line)
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    print(f"📄 PDF report saved as: {filename}")


def integration_test():
    log = []

    # Agrega la fecha y hora actual
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log.append(f"🕒 Report generated on: {now}")

    try:
        log.append("Running integration test...")
        # Step 1: Create user
        user_id = create_user("Camilo")
        log.append(f"User created with ID: {user_id}")


        # Step 2: Create task for that user
        task_id = create_task(user_id, "Prepare presentation")
        log.append(f"Task created with ID: {task_id}")


        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]

        assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
        print("✅ Test completed: task was successfully registered and linked to the user.")
        log.append("Task was successfully registered.")


        #Step 4: Delete task created for test
        delete_task(task_id)
        delete_user(user_id)
        print("✅ Cleanup completed: task and user deleted.")
        log.append("Task and user deleted.")

        #Step 5: Verify deletion
        task_response = get_task(task_id)
        user_response = get_user(user_id)

        assert task_response.status_code == 404, "❌ Task was not deleted properly"
        assert user_response.status_code == 404, "❌ User was not deleted properly"
        log.append("Confirmed: Task and user were properly deleted.")


        print("✅ Verified: task and user were properly deleted.")
        log.append("✅ TEST PASSED")
    except Exception as e:
        log.append(f"❌ TEST FAILED: {str(e)}")

    # Generate the PDF report at the end
    generate_pdf_report(log)



if __name__ == "__main__":
    integration_test()