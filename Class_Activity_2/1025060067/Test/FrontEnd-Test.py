import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

# Endpoints for direct API calls for cleanup and verification
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

# Global list to store test results
test_results = []

def generate_pdf_report(results, filename_prefix="Frontend_Test_Report"):
    if not os.path.exists("reports"):
        os.makedirs("reports")

    # Get sequential number
    report_number = 1
    while os.path.exists(f"reports/{filename_prefix}_{report_number}.pdf"):
        report_number += 1
    
    filename = f"reports/{filename_prefix}_{report_number}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Frontend Integration Test Report", styles['h1']))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 12))

    for result in results:
        style = styles['Normal']
        if "FAILED" in result:
            style = styles['Code'] # Can be customized
            story.append(Paragraph(f"<font color='red'>{result}</font>", style))
        else:
            story.append(Paragraph(result, style))
        story.append(Spacer(1, 6))

    try:
        doc.build(story)
        print(f"📊 PDF report generated: {filename}")
        test_results.append(f"📊 PDF report generated: {filename}")
    except Exception as e:
        print(f"❌ Error generating PDF report: {e}")
        test_results.append(f"❌ Error generating PDF report: FAILED - {e}")

def delete_user_api(user_id):
    try:
        response = requests.delete(f"{USERS_URL}/{user_id}")
        response.raise_for_status()
        print(f"🗑️ User with ID {user_id} deleted via API.")
        test_results.append(f"🗑️ User deletion (ID: {user_id}) via API: PASSED")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ User deletion failed via API for ID {user_id}: {e}")
        test_results.append(f"❌ User deletion (ID: {user_id}) via API: FAILED - {e}")
        return False

def get_user_api(user_id):
    try:
        response = requests.get(f"{USERS_URL}/{user_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def delete_task_api(task_id):
    try:
        response = requests.delete(f"{TASKS_URL}/{task_id}")
        response.raise_for_status()
        print(f"🗑️ Task with ID {task_id} deleted via API.")
        test_results.append(f"🗑️ Task deletion (ID: {task_id}) via API: PASSED")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Task deletion failed via API for ID {task_id}: {e}")
        test_results.append(f"❌ Task deletion (ID: {task_id}) via API: FAILED - {e}")
        return False

def get_task_api(task_id):
    try:
        response = requests.get(f"{TASKS_URL}/{task_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def abrir_frontend(driver):
    try:
        driver.get("http://localhost:5000")
        time.sleep(2)
        test_results.append("✅ Frontend opened successfully.")
    except Exception as e:
        test_results.append(f"❌ Failed to open frontend: {e}")
        raise

def crear_usuario(driver, wait):
    try:
        username_input = driver.find_element(By.ID, "username")
        username_input.send_keys("Ana")
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
        time.sleep(2)

        user_result = driver.find_element(By.ID, "user-result").text
        print("Resultado usuario:", user_result)
        assert "Usuario creado con ID" in user_result
        user_id = ''.join(filter(str.isdigit, user_result))
        test_results.append(f"✅ User created successfully via UI. ID: {user_id}")
        return user_id
    except AssertionError:
        test_results.append(f"❌ User creation via UI: FAILED - Assertion failed for result text.")
        raise
    except Exception as e:
        test_results.append(f"❌ User creation via UI: FAILED - {e}")
        raise

def crear_tarea(driver, wait, user_id):
    try:
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
        task_result = driver.find_element(By.ID, "task-result")
        print("Texto en task_result:", task_result.text)
        assert "Tarea creada con ID" in task_result.text
        task_id = ''.join(filter(str.isdigit, task_result.text))
        test_results.append(f"✅ Task created successfully via UI. ID: {task_id}")
        return task_id
    except AssertionError:
        test_results.append(f"❌ Task creation via UI: FAILED - Assertion failed for result text.")
        raise
    except Exception as e:
        test_results.append(f"❌ Task creation via UI: FAILED - {e}")
        raise


def ver_tareas(driver):
    try:
        driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
        time.sleep(2)

        tasks = driver.find_element(By.ID, "tasks").text
        print("Tareas:", tasks)
        assert "Terminar laboratorio" in tasks
        test_results.append("✅ Task visibility verification via UI: PASSED")
    except AssertionError:
        test_results.append(f"❌ Task visibility verification via UI: FAILED - Assertion failed for task in list.")
        raise
    except Exception as e:
        test_results.append(f"❌ Task visibility verification via UI: FAILED - {e}")
        raise


def main():
    options = Options()
    # options.add_argument('--headless')  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)
    
    user_id = None
    task_id = None
    global test_results # Ensure test_results is cleared for each run
    test_results = []

    try:
        wait = WebDriverWait(driver, 10)
        
        abrir_frontend(driver)
        user_id = crear_usuario(driver, wait)
        task_id = crear_tarea(driver, wait, user_id)
        ver_tareas(driver)
        
        time.sleep(3)

        # Data cleanup
        if task_id:
            deleted_task = delete_task_api(task_id)
            assert deleted_task, f"❌ Task cleanup failed for ID {task_id}."
            retrieved_task = get_task_api(task_id)
            assert retrieved_task is None, f"❌ Task with ID {task_id} still exists after deletion."
            test_results.append(f"✅ Task cleanup and verification for ID {task_id}: PASSED")

        if user_id:
            deleted_user = delete_user_api(user_id)
            assert deleted_user, f"❌ User cleanup failed for ID {user_id}."
            retrieved_user = get_user_api(user_id)
            assert retrieved_user is None, f"❌ User with ID {user_id} still exists after deletion."
            test_results.append(f"✅ User cleanup and verification for ID {user_id}: PASSED")

    except Exception as e:
        print(f"An error occurred during the test: {e}")
        test_results.append(f"❌ OVERALL TEST FAILED: {e}")
    finally:
        driver.quit()
        generate_pdf_report(test_results, "Frontend_Test_Report")

if __name__ == "__main__":
    main()