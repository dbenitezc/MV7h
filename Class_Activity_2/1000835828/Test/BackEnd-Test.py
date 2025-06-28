
import requests
import os
from datetime import datetime
from pdf_report import generate_pdf_report  # Importar la función de generación de PDF


# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"
CLEANUP_USERS_URL = "http://localhost:5001/test/cleanup"
CLEANUP_TASKS_URL = "http://localhost:5002/test/cleanup"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    print("✅ User created:", user_data)
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    print("✅ Task created:", task_data)
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    tasks = response.json()
    return tasks

def get_users():
    response = requests.get(USERS_URL)
    response.raise_for_status()
    return response.json()

def cleanup_test_data():
    """Elimina datos de prueba de ambos servicios"""
    # Eliminar tareas de prueba
    tasks_response = requests.delete(CLEANUP_TASKS_URL)
    if tasks_response.status_code == 200:
        print("🧹 Tareas de prueba eliminadas:", tasks_response.json().get('message'))
    else:
        print("⚠️ Error eliminando tareas:", tasks_response.text)
    
    # Eliminar usuarios de prueba
    users_response = requests.delete(CLEANUP_USERS_URL)
    if users_response.status_code == 200:
        print("🧹 Usuarios de prueba eliminados:", users_response.json().get('message'))
    else:
        print("⚠️ Error eliminando usuarios:", users_response.text)

def verify_cleanup():
    """Verifica que los datos de prueba fueron eliminados"""
    # Verificar usuarios
    users = get_users()
    test_users = [u for u in users if u['name'] in ['Ana', 'Camilo']]
    assert len(test_users) == 0, f"❌ Usuarios de prueba no eliminados: {test_users}"
    
    # Verificar tareas
    tasks = get_tasks()
    test_tasks = [t for t in tasks if t['title'] in ['Terminar laboratorio', 'Prepare presentation']]
    assert len(test_tasks) == 0, f"❌ Tareas de prueba no eliminadas: {test_tasks}"
    
    print("✅ Verificación de limpieza completada: todos los datos de prueba fueron eliminados")

# def integration_test():
#     print("\n" + "="*50)
#     print("🔥 Iniciando prueba de integración")
#     print("="*50)
    
#     # Paso 1: Crear usuario
#     user_id = create_user("Camilo")

#     # Paso 2: Crear tarea para ese usuario
#     task_id = create_task(user_id, "Prepare presentation")

#     # Paso 3: Verificar que la tarea está registrada y asociada al usuario
#     tasks = get_tasks()
#     user_tasks = [t for t in tasks if t["user_id"] == user_id]

#     assert any(t["id"] == task_id for t in user_tasks), "❌ La tarea no fue registrada correctamente"
#     print("✅ Prueba completada: la tarea fue registrada y vinculada al usuario correctamente")
    
#     # Paso 4: Limpieza de datos de prueba
#     print("\n" + "="*50)
#     print("🧼 Realizando limpieza de datos de prueba")
#     print("="*50)
#     cleanup_test_data()
    
#     # Paso 5: Verificar que los datos fueron eliminados
#     verify_cleanup()
def integration_test():
    test_results = []  # Almacenar resultados para el reporte PDF
    
    try:
        print("\n" + "="*50)
        print("🔥 Iniciando prueba de integración")
        print("="*50)
        test_results.append(("Prueba de integración iniciada", True))
        
        # Paso 1: Crear usuario
        user_id = create_user("Camilo")
        test_results.append(("Usuario 'Camilo' creado exitosamente", True))
        
        # Paso 2: Crear tarea para ese usuario
        task_id = create_task(user_id, "Prepare presentation")
        test_results.append(("Tarea 'Prepare presentation' creada exitosamente", True))
        
        # Paso 3: Verificar que la tarea está registrada y asociada al usuario
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]
        
        task_registered = any(t["id"] == task_id for t in user_tasks)
        assert task_registered, "❌ La tarea no fue registrada correctamente"
        test_results.append(("Tarea registrada y vinculada al usuario correctamente", True))
        print("✅ Prueba completada: la tarea fue registrada y vinculada al usuario correctamente")
        
        # Paso 4: Limpieza de datos de prueba
        print("\n" + "="*50)
        print("🧼 Realizando limpieza de datos de prueba")
        print("="*50)
        test_results.append(("Inicio de limpieza de datos de prueba", True))
        
        cleanup_test_data()
        test_results.append(("Limpieza de datos completada", True))
        
        # Paso 5: Verificar que los datos fueron eliminados
        verify_cleanup()
        test_results.append(("Verificación de limpieza completada", True))
        
        print("\n✅✅✅ Todas las pruebas completadas con éxito ✅✅✅")
        test_results.append(("Todas las pruebas completadas con éxito", True))
        
    except Exception as e:
        error_msg = f"❌ Error durante la prueba: {str(e)}"
        print(error_msg)
        test_results.append((error_msg, False))
        raise
    finally:
        # Generar reporte PDF
        report_path = generate_pdf_report("Backend Integration Test", test_results)
        print(f"\n📄 Reporte PDF generado: {report_path}")


if __name__ == "__main__":
    integration_test()