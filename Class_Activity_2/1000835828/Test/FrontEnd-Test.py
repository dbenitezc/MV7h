



import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pdf_report import generate_pdf_report  # Importar la función de generación de PDF

def abrir_frontend(driver):
    """Abre la aplicación frontend en el navegador"""
    driver.get("http://localhost:5000")
    time.sleep(2)  # Da tiempo a que cargue la página

def crear_usuario(driver, wait):
    """Completa el formulario de creación de usuario y lo envía"""
    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys("Ana")
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
    time.sleep(2)

    user_result = driver.find_element(By.ID, "user-result").text
    print("Resultado usuario:", user_result)
    assert "Usuario creado con ID" in user_result
    user_id = ''.join(filter(str.isdigit, user_result))  # Extrae el ID numérico
    return user_id

def crear_tarea(driver, wait, user_id):
    """Completa el formulario de creación de tareas y lo envía"""
    task_input = driver.find_element(By.ID, "task")
    task_input.send_keys("Terminar laboratorio")
    time.sleep(1)

    userid_input = driver.find_element(By.ID, "userid")
    userid_input.send_keys(user_id)
    userid_input.send_keys('\t')  # Forzar el foco fuera del input
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

def ver_tareas(driver, wait):
    """Actualiza la lista de tareas y devuelve su contenido"""
    actualizar_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Actualizar lista de tareas')]"))
    )
    actualizar_btn.click()
    time.sleep(1)
    return driver.find_element(By.ID, "tasks").text

def limpiar_y_verificar(driver, wait):
    """Realiza la limpieza de datos y verifica su eliminación"""
    # Hacer clic en el botón de limpieza
    clean_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Eliminar Datos de Prueba')]"))
    )
    clean_btn.click()
    time.sleep(2)
    
    # Verificar mensaje de éxito
    cleanup_result = wait.until(
        EC.visibility_of_element_located((By.ID, "cleanup-result"))
    ).text
    assert "eliminados" in cleanup_result, f"Limpieza falló: {cleanup_result}"
    
    # Verificar que las tareas ya no aparecen
    tasks_text = ver_tareas(driver, wait)
    assert "Terminar laboratorio" not in tasks_text, "Tarea de prueba no fue eliminada"
    print("✅ FrontEnd: Verificación de limpieza completada")

def capture_screenshot(driver, name):
    """Captura una pantalla y guarda en archivo"""
    screenshot_dir = "test_screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(screenshot_dir, f"{name}_{timestamp}.png")
    driver.save_screenshot(filename)
    return filename

def main():
    test_results = []  # Almacenar resultados para el reporte PDF
    screenshots = []   # Almacenar capturas de pantalla
    
    # Configuración del navegador
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument('--headless')  # Descomentar para modo headless
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1200, 800)  # Tamaño fijo para capturas consistentes
    wait = WebDriverWait(driver, 15)

    try:
        print("\n" + "="*50)
        print("🚀 Iniciando prueba FrontEnd")
        print("="*50)
        test_results.append(("Prueba FrontEnd iniciada", True))
        
        # Paso 1: Abrir frontend
        abrir_frontend(driver)
        screenshots.append(capture_screenshot(driver, "frontend_abierto"))
        test_results.append(("Frontend abierto correctamente", True))
        
        # Paso 2: Crear usuario
        print("\n🔹 Creando usuario de prueba...")
        user_id = crear_usuario(driver, wait)
        screenshots.append(capture_screenshot(driver, "usuario_creado"))
        test_results.append((f"Usuario creado con ID {user_id}", True))
        
        # Paso 3: Crear tarea
        print("\n🔹 Creando tarea de prueba...")
        crear_tarea(driver, wait, user_id)
        screenshots.append(capture_screenshot(driver, "tarea_creada"))
        test_results.append(("Tarea 'Terminar laboratorio' creada", True))
        
        # Paso 4: Verificar tarea
        print("\n🔹 Verificando tarea creada...")
        tasks_text = ver_tareas(driver, wait)
        screenshots.append(capture_screenshot(driver, "tareas_verificadas"))
        
        task_found = "Terminar laboratorio" in tasks_text
        assert task_found, "Tarea no encontrada en la lista"
        test_results.append(("Tarea verificada en la lista", True))
        
        # Paso 5: Limpieza y verificación
        print("\n" + "="*50)
        print("🧹 Realizando limpieza de datos de prueba")
        print("="*50)
        test_results.append(("Inicio de limpieza de datos", True))
        
        limpiar_y_verificar(driver, wait)
        screenshots.append(capture_screenshot(driver, "limpieza_completada"))
        test_results.append(("Limpieza de datos completada", True))
        
        time.sleep(2)  # Tiempo para observar resultados
        print("\n✅✅✅ Todas las pruebas FrontEnd completadas con éxito ✅✅✅")
        test_results.append(("Todas las pruebas completadas con éxito", True))
        
    except Exception as e:
        error_msg = f"Error durante la prueba: {str(e)}"
        print(f"❌ {error_msg}")
        test_results.append((error_msg, False))
        
        # Capturar pantalla de error si es posible
        if 'driver' in locals() and driver is not None:
            try:
                screenshots.append(capture_screenshot(driver, "error_final"))
                print(f"📸 Captura de pantalla de error guardada")
            except Exception as screenshot_error:
                print(f"⚠️ No se pudo capturar pantalla de error: {screenshot_error}")
    finally:
        # Cerrar el navegador si está abierto
        if 'driver' in locals() and driver is not None:
            driver.quit()
        
        # Generar reporte PDF
        print("\n📊 Generando reporte PDF...")
        try:
            report_path = generate_pdf_report("FrontEnd Test", test_results, screenshots)
            print(f"📄 Reporte PDF generado: {report_path}")
        except Exception as pdf_error:
            print(f"❌ Error generando reporte PDF: {pdf_error}")
            # Guardar resultados en archivo de texto como respaldo con codificación UTF-8
            backup_report = "test_reports/frontend_test_results.txt"
            try:
                with open(backup_report, "w", encoding="utf-8") as f:
                    f.write("Resultados de prueba:\n")
                    for result, success in test_results:
                        # Reemplazar emojis por texto descriptivo
                        clean_result = result
                        clean_result = clean_result.replace("✅", "[SUCCESS] ")
                        clean_result = clean_result.replace("❌", "[ERROR] ")
                        status = "Éxito" if success else "Fallo"
                        f.write(f"{status}: {clean_result}\n")
                print(f"📝 Resultados guardados en: {backup_report}")
            except Exception as file_error:
                print(f"⚠️ Error guardando archivo de respaldo: {file_error}")

if __name__ == "__main__":
    main()