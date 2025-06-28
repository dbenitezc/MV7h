import requests
import os
from datetime import datetime
from reportlab.pdfgen import canvas

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

# Guardar mensajes del log
log = []

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    message = f"✅ Usuario creado: {user_data}"
    print(message)
    log.append(message)
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    message = f"✅ Task creado: {task_data}"
    print(message)
    log.append(message)
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    if response.status_code == 200:
        message = f"Task {task_id} borrado."
    else:
        message = f"No se pudo borrar el task {task_id}."
    print(message)
    log.append(message)

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    if response.status_code == 200:
        message = f"Usuario {user_id} borrado."
    else:
        message = f"No se pudo borrar al usuario: {user_id}."
    print(message)
    log.append(message)

def generate_pdf_report():
    i = 1
    while os.path.exists(f"report_{i}.pdf"):
        i += 1
    filename = f"report_{i}.pdf"

    # Crear PDF
    c = canvas.Canvas(filename)
    c.setFont("Helvetica", 12)
    c.drawString(200, 800, "Reporte de test de integración")
    c.setFont("Helvetica", 10)
    c.drawString(50, 780, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y = 760

    for entry in log:
        if y < 50:
            c.showPage()
            y = 800
        c.drawString(50, y, entry)
        y -= 20

    c.save()
    print(f"Reporte generado: {filename}")

def integration_test():
    try:
        # Step 1: Create user
        user_id = create_user("Camilo")

        # Step 2: Create task
        task_id = create_task(user_id, "Realizar actividad de clase 2")

        # Step 3: Verify task
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        assert any(t["id"] == task_id for t in user_tasks), "❌ Task not found"
        log.append("✅ Task correctly linked to user.")
        print("✅ Task correctly linked to user.")

    except Exception as e:
        message = f"❌ Test Fallado: {str(e)}"
        print(message)
        log.append(message)

    finally:
        # limpieza de recursos
        try:
            delete_task(task_id)
        except:
            log.append("Eliminación de Task fallido.")
        try:
            delete_user(user_id)
        except:
            log.append("Eliminación de usuario fallida.")

        # verificar
        try:
            tasks = get_tasks()
            assert not any(t["id"] == task_id for t in tasks), "❌ Task no fué borrado"
            log.append("✅ verificacion completa.")
        except Exception as e:
            log.append(f"verificacion fallada: {str(e)}")

        # Generate PDF
        generate_pdf_report()

if __name__ == "__main__":
    integration_test()