import time
import requests
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER

# Rutas para servicios
TASKS_URL = "http://localhost:5002/tasks"
USERS_URL = "http://localhost:5001/users"

# Rutas de PDF
REPORTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'reports'))

def generar_pdf(log):
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(REPORTS_DIR, f"frontend_report_{timestamp}.pdf")

    c = canvas.Canvas(filename, pagesize=LETTER)
    width, height = LETTER
    y = height - 50

    for line in log:
        c.drawString(50, y, line)
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    print("📄 PDF generado:", filename)


def abrir_frontend(driver):
    driver.get("http://localhost:5000")
    time.sleep(2)


def crear_usuario(driver, wait, log):
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    log.append(f"Resultado usuario: {user_result}")
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))
    log.append(f"✅ Usuario creado con ID: {user_id}")
    return user_id


def crear_tarea(driver, wait, user_id, log):
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys("Terminar laboratorio")
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
    userid_input.send_keys(user_id)
    userid_input.send_keys('\t')
    time.sleep(1)

    crear_tarea_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))
    )
    crear_tarea_btn.click()
    time.sleep(2)

    wait.until(
        EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID")
    )
    task_result = driver.find_element(By.ID, "task-result").text
    log.append(f"Resultado tarea: {task_result}")
    assert "Tarea creada con ID" in task_result
    task_id = ''.join(filter(str.isdigit, task_result))
    log.append(f"✅ Tarea creada con ID: {task_id}")
    return task_id


def ver_tareas(driver, log):
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)
    tasks = driver.find_element(By.ID, "tasks").text
    log.append(f"📋 Lista de tareas: {tasks}")
    return tasks

def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()


def main():
    log = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log.append(f"🕒 Test iniciado: {timestamp}")

    options = Options()
    # options.add_argument('--headless')  # Descomenta para ejecución sin ventana
    driver = webdriver.Chrome(options=options)

    user_id = None
    task_id = None

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait, log)
        task_id = crear_tarea(driver, wait, user_id, log)

        tareas = ver_tareas(driver, log)
        assert "Terminar laboratorio" in tareas, "❌ La tarea no aparece en la lista"
        log.append("✅ Verificado que la tarea aparece en la lista.")

        # Limpieza usando requests
        delete_task(task_id)
        delete_user(user_id)
        print("✅ Cleanup completed: task and user deleted.")
        log.append("🧹 Tarea y usuario eliminados desde el frontend.")

        # Verificación de eliminación
        log.append("✅ TEST PASSED")

    except Exception as e:
        log.append(f"❌ TEST FAILED: {str(e)}")

    finally:
        driver.quit()
        generar_pdf(log)


if __name__ == "__main__":
    main()
