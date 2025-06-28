
import requests
from utils import generate_pdf_report

USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    return response.json()["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={"title": description, "user_id": user_id})
    response.raise_for_status()
    return response.json()["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    return response.json()

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()

def integration_test():
    results = []
    try:
        user_id = create_user("Test User")
        results.append("✅ Usuario creado correctamente")

        task_id = create_task(user_id, "Test Task")
        results.append("✅ Tarea creada y asociada")

        tasks = get_tasks()
        if any(task["id"] == task_id for task in tasks):
            results.append("✅ Tarea verificada correctamente")

        # Eliminación
        delete_task(task_id)
        delete_user(user_id)
        results.append("✅ Datos eliminados")

        # Verificación de eliminación
        tasks = get_tasks()
        if not any(task["id"] == task_id for task in tasks):
            results.append("✅ Verificación de eliminación exitosa")
        else:
            results.append("❌ La tarea aún existe tras intentar eliminarla")

    except Exception as e:
        results.append(f"❌ Error durante la prueba: {e}")

    generate_pdf_report(results)

if __name__ == "__main__":
    integration_test()
