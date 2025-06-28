import time
import requests
import os
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def generate_pdf_report(content):
    os.makedirs("reports", exist_ok=True)
    index = 1
    while os.path.exists(f"reports/test_report_{index}.pdf"):
        index += 1

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    def clean_latin1(text):
        return ''.join(c for c in text if ord(c) < 256)

    for line in content.splitlines():
        pdf.cell(200, 10, txt=clean_latin1(line), ln=True)

    pdf.output(f"reports/test_report_{index}.pdf")

def abrir_frontend(driver):
    driver.get("http://localhost:5000")
    time.sleep(2)

def crear_usuario(driver, wait, log):
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana_Test")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    log.append(f"Usuario result: {user_result}")
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))
    return user_id

def crear_tarea(driver, wait, user_id, log):
    driver.find_element(By.ID, "task").send_keys("Terminar laboratorio (test)")
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
    userid_input.send_keys(user_id)
    userid_input.send_keys('\t')
    time.sleep(1)

    crear_tarea_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Crear Tarea']"))
    )
    crear_tarea_btn.click()

    # 🔁 Esperar hasta que aparezca el texto esperado
    wait.until(
        EC.text_to_be_present_in_element((By.ID, "task-result"), "Tarea creada con ID")
    )

    result_element = driver.find_element(By.ID, "task-result")
    result = result_element.text.strip()
    log.append(f"Tarea result: {result}")

    assert "Tarea creada con ID" in result, f"Respuesta inesperada: {result}"
    return ''.join(filter(str.isdigit, result))

def borrar_datos(user_id, task_id, log):
    try:
        if task_id:
            requests.delete(f"http://localhost:5002/tasks/{task_id}")
            log.append(f"Deleted task ID {task_id}")
        if user_id:
            requests.delete(f"http://localhost:5001/users/{user_id}")
            log.append(f"Deleted user ID {user_id}")
    except Exception as e:
        log.append(f"Error deleting data: {str(e)}")

def ver_tareas(driver, log):
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)
    tasks = driver.find_element(By.ID, "tasks").text
    log.append(f"Tareas: {tasks}")
    assert "Terminar laboratorio" in tasks

def main():
    options = Options()
    # options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    log = []

    try:
        wait = WebDriverWait(driver, 10)
        abrir_frontend(driver)
        log.append("Abierto FrontEnd")

        user_id = crear_usuario(driver, wait, log)
        log.append(f"Usuario creado: {user_id}")

        task_id = crear_tarea(driver, wait, user_id, log)
        log.append(f"Tarea creada: {task_id}")

        ver_tareas(driver, log)

        borrar_datos(user_id, task_id, log)

        log.append("FRONTEND TEST PASSED")
    except Exception as e:
        log.append(f"Test fallido: {str(e)}")
    finally:
        driver.quit()
        generate_pdf_report("\n".join(log))

if __name__ == "__main__":
    main()
