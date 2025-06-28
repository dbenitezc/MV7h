import requests
import random
import time
import sys
import os
import glob
from io import StringIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"
TEST_USER = f"TestUser-{random.randint(1000,9999)}"
DELAY = 0.5 

def print_step(step, message):
    print(f"\n🔹 PASO {step}: {message}")

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    return response.json()["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
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

def user_exists(user_id):
    response = requests.get(f"{USERS_URL}/{user_id}")
    return response.status_code == 200

def task_exists(task_id):
    response = requests.get(f"{TASKS_URL}")
    tasks = response.json()
    return any(task['id'] == task_id for task in tasks)

def generate_pdf_report(content, result, filename):
    """Generate PDF report with captured console output and test result"""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    y_position = height - 40
    line_height = 14
    
    # Title and metadata
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y_position, "Backend Integration Test Report")
    y_position -= line_height * 2
    
    # Test result highlight
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y_position, f"Final Result: {result}")
    y_position -= line_height * 2
    
    # Console output
    c.setFont("Courier", 10)
    for line in content.split('\n'):
        if y_position < 40:  # New page on overflow
            c.showPage()
            y_position = height - 40
            c.setFont("Courier", 10)
        c.drawString(40, y_position, line)
        y_position -= line_height
    c.save()

def integration_test():
    print("🚀 Iniciando prueba de integración mejorada")
    user_id = None
    tasks_creadas = []
    
    try:
        print_step(1, f"Creando usuario: {TEST_USER}")
        user_id = create_user(TEST_USER)
        print(f"✅ Usuario creado ID: {user_id}")
        time.sleep(DELAY)

        print_step(2, "Creando tareas para el usuario")
        tarea1 = create_task(user_id, "Revisar documentación")
        tarea2 = create_task(user_id, "Preparar demostración")
        tarea3 = create_task(user_id, "Enviar reporte final")
        tasks_creadas = [tarea1, tarea2, tarea3]
        print(f"✅ Tareas creadas IDs: {', '.join(map(str, tasks_creadas))}")
        time.sleep(DELAY)

        print_step(3, "Verificando existencia de recursos")
        assert user_exists(user_id), "❌ Usuario no existe después de creación"
        print("✅ Usuario verificado")
        
        for t_id in tasks_creadas:
            assert task_exists(t_id), f"❌ Tarea {t_id} no existe"
        print("✅ Todas las tareas existen")
        time.sleep(DELAY)

        print_step(4, "Probando eliminación individual de tareas")
        tarea_a_eliminar = tasks_creadas.pop(1)
        print(f"Eliminando tarea ID: {tarea_a_eliminar}")
        delete_task(tarea_a_eliminar)
        time.sleep(DELAY)
        
        assert not task_exists(tarea_a_eliminar), "❌ Tarea no fue eliminada"
        print(f"✅ Tarea {tarea_a_eliminar} eliminada correctamente")
        
        for t_id in tasks_creadas:
            assert task_exists(t_id), f"❌ Tarea {t_id} fue eliminada por error"
        print("✅ Otras tareas permanecen intactas")
        time.sleep(DELAY)

        print_step(5, f"Eliminando usuario ID: {user_id}")
        delete_user(user_id)
        time.sleep(DELAY)
        
        assert not user_exists(user_id), "❌ Usuario no fue eliminado"
        print("✅ Usuario eliminado correctamente")
        
        print_step(6, "Verificando estado final de tareas")
        for t_id in tasks_creadas:
            assert task_exists(t_id), f"❌ Tarea {t_id} fue eliminada con el usuario"
        print("✅ Tareas permanecen existiendo después de eliminar usuario (comportamiento esperado)")
        
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")

    except Exception as e:
        print(f"\n❌❌❌ PRUEBA FALLIDA: {str(e)}")
        raise e

    finally:
        print("\n🧹 Realizando limpieza final...")
        if user_exists(user_id):
            delete_user(user_id)
            print(f"Usuario {user_id} eliminado")
        
        for t_id in tasks_creadas:
            try:
                if task_exists(t_id):
                    delete_task(t_id)
                    print(f"Tarea {t_id} eliminada")
            except:
                pass
        time.sleep(DELAY)
        print("✅ Limpieza completada")

if __name__ == "__main__":
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    sys.stdout = captured_stdout = StringIO()
    sys.stderr = sys.stdout 

    test_result = "SUCCESS"
    try:
        integration_test()
    except Exception as e:
        test_result = f"FAILURE: {str(e)}"
    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        
        captured_content = captured_stdout.getvalue()
        print(captured_content)
        
        existing_reports = glob.glob("test_report_*.pdf")
        report_numbers = [int(f.split('_')[2].split('.')[0]) 
                          for f in existing_reports if f.endswith('.pdf')]
        next_num = max(report_numbers) + 1 if report_numbers else 1
        filename = f"test_report_{next_num:03d}.pdf"
        
        generate_pdf_report(captured_content, test_result, filename)
        print(f"\nPDF report generated: {filename}")