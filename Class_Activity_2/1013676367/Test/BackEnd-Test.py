import requests
from fpdf import FPDF
import os
import datetime

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name, results):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("✅ User created:", user_data)
    results.append(f"User created:{user_data}")
    return user_data["id"]

def create_task(user_id, description, results):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task created:", task_data)
    results.append(f"Task created: {task_data}")
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def create_pdf(results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Resultados de Pruebas BackEnd", ln=True, align="C")
    pdf.ln(10)

    pdf.multi_cell(100, 10,"Test performed: " + str(datetime.datetime.now().date()))

    for line in results:
        pdf.multi_cell(0, 10, line.encode('ascii', 'ignore').decode())

    path = os.getcwd()
    dr='\\'
    folder = 'Test'
    new_folder = 'BackEnd_reports'

    new_path = path + dr + folder + dr  + new_folder

    if not os.path.exists(new_path):
        os.makedirs(new_path)
    
    dirs = os.listdir(new_path)

    num = 0
    for item in dirs:
        if os.path.isfile(new_path + dr + item):
            num+=1

    pdf_filename = os.path.join(new_path, f"Report_{num}.pdf")
    pdf.output(pdf_filename)
    print("PDF generado como 'resultados_BackEnd_Test.pdf'")

def integration_test():
    results = []

    # Step 1: Create user
    user_id = create_user("Camilo", results)

    # Step 2: Create task for that user
    task_id = create_task(user_id, "Prepare presentation", results)

    # Step 3: Verify that the task is registered and associated with the user
    tasks = get_tasks()
    user_tasks = [t for t in tasks if t["user_id"] == user_id]
    try:
        assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
        print("✅ Test completed: task was successfully registered and linked to the user.")
        results.append("Test completed: task was successfully registered and linked to the user.")
        
    except Exception as e:
        results.append(f"❌ Assertion failed: {e}")
    
    requests.get(f'http://127.0.0.1:5001/users/delete/{user_id}')
    if requests.get(f'http://127.0.0.1:5001/users/delete/{user_id}').status_code == 404:
        results.append(f"Eliminated User: {user_id}")

    requests.get(f'http://127.0.0.1:5002/tasks/delete/{task_id}')
    if requests.get(f'http://127.0.0.1:5002/tasks/delete/{task_id}').status_code == 404:
        results.append(f"Eliminated Task: {user_id}")
    create_pdf(results)


if __name__ == "__main__":
    integration_test()