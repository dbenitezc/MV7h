import time
import os
import shutil
import subprocess
import random
import requests
import matplotlib.pyplot as plt
from fpdf import FPDF

services = []

def iniciar_services():
    global services
    services = [
        subprocess.Popen(["python", "Task_Service/main.py"]),
        subprocess.Popen(["python", "Users_Service/main.py"])
    ]
    time.sleep(3)

def cerrar_services():
    for proc in services:
        proc.terminate()
        proc.wait()

# --- Lógica del test ---

USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

def create_user(name):
    response = requests.post(USERS_URL, json={"name": name})
    response.raise_for_status()
    user_data = response.json()
    return user_data["id"]

def create_task(user_id, description):
    response = requests.post(TASKS_URL, json={
        "title": description,
        "user_id": user_id
    })
    response.raise_for_status()
    task_data = response.json()
    return task_data["id"]

def get_tasks():
    response = requests.get(TASKS_URL)
    response.raise_for_status()
    return response.json()

def generar_reporte_pdf(info_test):
    os.makedirs("Test/reports", exist_ok=True)
    pdf_path = os.path.join("Test/reports", "Results-BackEnd-Test.pdf")

    total = len(info_test)
    exitosos = sum(1 for _, _, ok in info_test if ok)
    fallos = total - exitosos

    labels = ['Éxito', 'Fallo']
    values = [exitosos, fallos]
    colors = ['#4CAF50', '#F44336']

    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=colors)
    plt.title("Resultados de pruebas (BackEnd)")
    plt.xlabel("Estado")
    plt.ylabel("Cantidad")
    plt.tight_layout()

    graph_image_path = os.path.join("Test/reports", "grafica_resultados.png")
    plt.savefig(graph_image_path)
    plt.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Reporte de Pruebas API - BackEnd", ln=True, align='C')
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

# --- Main ---

def main():
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

        asignaciones = list(zip(nombres, random.sample(tareas, len(tareas))))
        info_test = []

        for nombre, tarea in asignaciones:
            user_id = create_user(nombre)
            task_id = create_task(user_id, tarea)

            tasks = get_tasks()
            linked = any(t["id"] == task_id and t["user_id"] == user_id for t in tasks)

            info_test.append((user_id, tarea, linked))

        generar_reporte_pdf(info_test)

    finally:
        cerrar_services()
        if os.path.exists("instance") and os.path.isdir("instance"):
            shutil.rmtree("instance")

if __name__ == "__main__":
    main()
