import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from fpdf import FPDF
import requests
import os
import datetime

def abrir_frontend(driver, results):
    # Opens the frontend application in the browser
    driver.get("http://localhost:5000")
    time.sleep(2)  # Give the page time to load
    results.append("Frontend abierto en http://localhost:5000")

def crear_usuario(driver, wait, results):
    # Fills out the user creation form and submits it
    # Then retrieves and returns the newly created user ID
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    print("Resultado usuario:", user_result)
    results.append(f"Resultado usuario: {user_result}")
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))  # Extract numeric ID from result
    return user_id

def crear_tarea(driver, wait, user_id, results):
    # Fills out the task creation form with a task and user ID, then submits it
    # Waits until the confirmation text appears and asserts the result
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys("Terminar laboratorio")
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
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
    print("Texto en task_result:", task_result.text)
    results.append(f"Texto en task_result: {task_result.text}")
    assert "Tarea creada con ID" in task_result.text
    task_id = ''.join(filter(str.isdigit, task_result.text))
    return task_id 

def ver_tareas(driver, results):
    # Clicks the button to refresh the task list and verifies the new task appears
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas:", tasks)
    results.append(f"Tareas: {tasks}")
    assert "Terminar laboratorio" in tasks

def create_pdf(results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Resultados de Pruebas FrontEnd", ln=True, align="C")
    pdf.ln(10)
    pdf.multi_cell(100, 10,"Test performed: " + str(datetime.datetime.now().date()))

    for line in results:
        pdf.multi_cell(0, 10, line.encode('ascii', 'ignore').decode())

    path = os.getcwd()
    dr='\\'
    folder = 'Test'
    new_folder = 'FrontEnd_reports'

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
    print("PDF generado como 'resultados_FrontEnd_Test.pdf'")

def main():
    # Main test runner that initializes the browser and runs the full E2E flow
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)

    results = []
    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver, results)
        user_id = crear_usuario(driver, wait, results)
        task_id = crear_tarea(driver, wait, user_id, results)
        ver_tareas(driver, results)
        time.sleep(3)  # Final delay to observe results if not running headless
        
        requests.get(f'http://127.0.0.1:5001/users/delete/{user_id}')
        if requests.get(f'http://127.0.0.1:5001/users/delete/{user_id}').status_code == 404:
            results.append(f"Eliminated User: {user_id}")

        requests.get(f'http://127.0.0.1:5002/tasks/delete/{task_id}')
        if requests.get(f'http://127.0.0.1:5002/tasks/delete/{task_id}').status_code == 404:
            results.append(f"Eliminated Task: {user_id}")
        create_pdf(results)
        time.sleep(3)

    finally:
        driver.quit()  # Always close the browser at the end

if __name__ == "__main__":
    main()
