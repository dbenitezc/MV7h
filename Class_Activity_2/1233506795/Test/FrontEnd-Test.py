import time
import shutil
import os
import random
import shutil
import subprocess
import matplotlib.pyplot as plt
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


services = []

def iniciar_services():
    global services
    services = [
        subprocess.Popen(["python", "Task_Service/main.py"]),
        subprocess.Popen(["python", "Users_Service/main.py"]),
        subprocess.Popen(["python", "Front-End/main.py"])
    ]
    time.sleep(3)  # Dar tiempo a que arranquen

def cerrar_services():
    for proc in services:
        proc.terminate()
        proc.wait()

def abrir_frontend(driver):
    # Opens the frontend application in the browser
    driver.get("http://localhost:5000")
    time.sleep(2)  # Give the page time to load

def crear_usuario(driver,name, wait):
    # Fills out the user creation form and submits it
    # Then retrieves and returns the newly created user ID
    username_input = driver.find_element(By.ID, "username")
    username_input.clear()  # Clear any existing text
    username_input.send_keys(name)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))  # Extract numeric ID from result
    return user_id

def crear_tarea(driver, wait, user_id, task):
    # Fills out the task creation form with a task and user ID, then submits it
    # Waits until the confirmation text appears and asserts the result
    task_input = driver.find_element(By.ID, "task")
    task_input.clear()  # Clear any existing text
    task_input.send_keys(task)
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
    userid_input.clear()  # Clear any existing text
    userid_input.send_keys(user_id)
    userid_input.send_keys('\t')  # Force focus out of the input to trigger validation
    time.sleep(1)

    crear_tarea_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))
    )
    crear_tarea_btn.click()
    time.sleep(2)

    wait.until(
        EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID")
    )
    task_result = driver.find_element(By.ID, "task-result")
    assert "Tarea creada con ID" in task_result.text, "Error al crear la tarea"

def tarea_asignada(task_info, tasks):
    user_id, tarea = task_info
    for t in tasks:
        if tarea in t and f"(Usuario ID: {user_id})" in t:
            return True
    return False

def ver_tareas(driver, task_info_list):
    # Refresh task list
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    task_text = driver.find_element(By.ID, "tasks").text

    results = []
    for user_id, tarea in task_info_list:
        entry = f"{tarea} (Usuario ID: {user_id})"
        found = entry in task_text
        results.append((user_id, tarea, found))
    return results

def generar_reporte_pdf(info_test):
    os.makedirs("Test/reports", exist_ok=True)
    pdf_path = os.path.join("Test/reports", "Results-FrontEnd-Test.pdf")

    total = len(info_test)
    exitosos = sum(1 for _, _, ok in info_test if ok)
    fallos = total - exitosos

    labels = ['Éxito', 'Fallo']
    values = [exitosos, fallos]
    colors = ['#4CAF50', '#F44336']

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=colors)
    plt.title("Resultados de pruebas")
    plt.xlabel("Estado")
    plt.ylabel("Cantidad")
    plt.tight_layout()

    graph_image_path = os.path.join("Test/reports", "grafica_resultados.png")
    plt.savefig(graph_image_path)
    plt.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Reporte de Pruebas E2E - Tareas Asignadas", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    for user_id, tarea, estado in info_test:
        status = "Éxito" if estado else "Fallo"
        pdf.cell(0, 10, f"Usuario {user_id} - Tarea: '{tarea}' -> {status}", ln=True)

    pdf.ln(10)
    pdf.image(graph_image_path, w=160)
    pdf.output(pdf_path)
    print(f"✅ PDF generado en: {pdf_path}")

    if os.path.exists(graph_image_path):
        os.remove(graph_image_path)



def main():
    options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    nombres = [
        "Carlos", "Luisa", "Pedro", "María", "Andrés",
        "Sofía", "Juan", "Valentina", "Mateo", "Camila"
    ]

    tareas = [
        "Escribir informe", "Hacer llamada", "Actualizar base de datos",
        "Enviar correo", "Revisar código", "Preparar reunión",
        "Limpiar backlog", "Documentar API", "Optimizar consulta", "Analizar logs"
    ]
    
    try:
        
        iniciar_services()
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        asignaciones = list(zip(nombres, random.sample(tareas, len(tareas))))

        info_test = []
        for nombre, tarea in asignaciones:
            user_id = crear_usuario(driver, nombre, wait)
            crear_tarea(driver, wait, user_id, tarea)
            info_test.append((user_id, tarea))

        # Verifica todas las tareas al final
        time.sleep(2)
        data_test = ver_tareas(driver, info_test)

        # Genera PDF con los datos verificados
        generar_reporte_pdf(data_test)

    finally:
        cerrar_services()
        if os.path.exists("instance") and os.path.isdir("instance"):
            shutil.rmtree("instance")
        driver.quit()

if __name__ == "__main__":
    main()
