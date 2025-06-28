import time
import re
import requests
import sys
import os
import glob
from io import StringIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Backend URLs for cleanup
BACKEND_USERS_URL = "http://localhost:5001/users"
BACKEND_TASKS_URL = "http://localhost:5002/tasks"

def print_step(step, message):
    print(f"\n🔹 PASO {step}: {message}")

def generate_pdf_report(content, result, filename):
    """Genera un reporte PDF con el contenido capturado y el resultado de la prueba"""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y_position = height - 40
    line_height = 12
    
    # Título y metadatos
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y_position, "Reporte de Prueba Frontend")
    y_position -= line_height * 2
    
    # Resultado destacado
    c.setFont("Helvetica-Bold", 14)
    c.setFillColorRGB(0, 0.5, 0) if "SUCCESS" in result else c.setFillColorRGB(0.8, 0, 0)
    c.drawString(50, y_position, f"Resultado: {result}")
    c.setFillColorRGB(0, 0, 0)  # Restaurar color negro
    y_position -= line_height * 3
    
    # Encabezado de sección
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_position, "Detalles de la Ejecución:")
    y_position -= line_height * 1.5
    
    # Contenido de consola
    c.setFont("Courier", 10)
    for line in content.split('\n'):
        if y_position < 50:  # Nueva página si se llena
            c.showPage()
            y_position = height - 40
            c.setFont("Courier", 10)
        c.drawString(50, y_position, line)
        y_position -= line_height
    
    # Pie de página
    c.showPage()
    c.setFont("Helvetica", 10)
    c.drawString(50, 50, f"Reporte generado el: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    c.save()

def abrir_frontend(driver):
    """Abre la aplicación frontend en el navegador"""
    print("Abriendo la aplicación frontend...")
    driver.get("http://localhost:5000")
    time.sleep(2)

def crear_usuario(driver, wait):
    """Crea un nuevo usuario y devuelve su ID"""
    print("Creando nuevo usuario...")
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    print("Resultado usuario:", user_result)
    assert "Usuario creado con ID" in user_result, "Error al crear usuario"
    
    # Extraer ID numérico del resultado
    user_id = ''.join(filter(str.isdigit, user_result))
    return user_id

def crear_tarea(driver, wait, user_id):
    """Crea una nueva tarea y devuelve su ID"""
    print(f"Creando tarea para usuario {user_id}...")
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys("Terminar laboratorio")
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
    userid_input.send_keys(user_id)
    userid_input.send_keys('\t')  # Salir del campo para activar validación
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
    print("Resultado tarea:", task_result.text)
    assert "Tarea creada con ID" in task_result.text, "Error al crear tarea"
    
    # Extraer ID de la tarea del texto
    task_id = re.search(r'ID:?\s*(\d+)', task_result.text).group(1)
    return task_id

def ver_tareas(driver):
    """Verifica que la tarea aparece en la lista"""
    print("Actualizando lista de tareas...")
    driver.find_element(By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]").click()
    time.sleep(2)

    tasks = driver.find_element(By.ID, "tasks").text
    print("Tareas actuales:", tasks)
    assert "Terminar laboratorio" in tasks, "La tarea no aparece en la lista"
    return tasks

def eliminar_tarea_via_api(task_id):
    """Elimina una tarea usando la API del backend"""
    try:
        print(f"Intentando eliminar tarea {task_id} via API...")
        response = requests.delete(f"{BACKEND_TASKS_URL}/{task_id}")
        response.raise_for_status()
        print(f"✅ Tarea {task_id} eliminada correctamente")
        return True
    except Exception as e:
        print(f"❌ Error eliminando tarea {task_id}: {str(e)}")
        return False

def eliminar_usuario_via_api(user_id):
    """Elimina un usuario usando la API del backend"""
    try:
        print(f"Intentando eliminar usuario {user_id} via API...")
        response = requests.delete(f"{BACKEND_USERS_URL}/{user_id}")
        response.raise_for_status()
        print(f"✅ Usuario {user_id} eliminado correctamente")
        return True
    except Exception as e:
        print(f"❌ Error eliminando usuario {user_id}: {str(e)}")
        return False

def frontend_integration_test():
    # Redirigir salida estándar para capturar todo
    original_stdout = sys.stdout
    sys.stdout = captured_stdout = StringIO()
    
    print("🚀 Iniciando prueba de integración de frontend")
    
    # Configurar navegador (modo visible)
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1200,800")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    
    user_id = None
    task_id = None
    test_result = "ERROR: No se ejecutaron pruebas"
    
    try:
        # PASO 1: Abrir frontend
        print_step(1, "Abriendo la aplicación frontend")
        abrir_frontend(driver)
        print("✅ Frontend cargado correctamente")
        time.sleep(1)

        # PASO 2: Crear usuario
        print_step(2, "Creando nuevo usuario")
        user_id = crear_usuario(driver, wait)
        print(f"✅ Usuario creado ID: {user_id}")
        time.sleep(1)

        # PASO 3: Crear tarea
        print_step(3, "Creando nueva tarea")
        task_id = crear_tarea(driver, wait, user_id)
        print(f"✅ Tarea creada ID: {task_id}")
        time.sleep(1)

        # PASO 4: Verificar tareas
        print_step(4, "Verificando lista de tareas")
        tasks_list = ver_tareas(driver)
        assert "Terminar laboratorio" in tasks_list
        print("✅ Tarea encontrada en la lista")
        time.sleep(1)

        test_result = "SUCCESS"
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("El navegador permanecerá abierto para inspección...")
        print("Presione Ctrl+C en la terminal para finalizar y generar el reporte.")
        
        # Mantener el navegador abierto hasta que el usuario lo cierre
        while True:
            time.sleep(10)
    
    except Exception as e:
        test_result = f"FAILURE: {str(e)}"
        print(f"\n❌❌❌ PRUEBA FALLIDA: {str(e)}")
    
    finally:
        # Limpieza cuando el usuario cierra el programa
        print("\n🧹 Realizando limpieza final...")
        if task_id:
            eliminar_tarea_via_api(task_id)
        if user_id:
            eliminar_usuario_via_api(user_id)
        
        # Cerrar navegador
        driver.quit()
        print("✅ Limpieza completada")
        print("✅ Navegador cerrado")
        
        # Restaurar salida estándar y obtener contenido capturado
        sys.stdout = original_stdout
        captured_content = captured_stdout.getvalue()
        print(captured_content)  # Mostrar en consola real
        
        # Generar reporte PDF
        existing_reports = glob.glob("frontend_test_report_*.pdf")
        report_numbers = [int(f.split('_')[3].split('.')[0]) 
                          for f in existing_reports if f.startswith('frontend_test_report_')]
        next_num = max(report_numbers) + 1 if report_numbers else 1
        filename = f"frontend_test_report_{next_num:03d}.pdf"
        
        generate_pdf_report(captured_content, test_result, filename)
        print(f"\n📄 Reporte PDF generado: {filename}")
        
        return test_result

if __name__ == "__main__":
    frontend_integration_test()