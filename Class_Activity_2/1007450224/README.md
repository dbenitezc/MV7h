# Actividad de Clase 2 – Pruebas de Integración Mejoradas

## 👤 Estudiante

- **Nombre:** Diego Felipe Benítez Cely  
- **ID:** 1007450224

---

## 🎯 Propósito

Esta actividad implementa pruebas de integración para una aplicación distribuida compuesta por tres servicios: un Front-End, un servicio de usuarios (Users_Service) y un servicio de tareas (Task_Service). La solución desarrollada incluye las siguientes extensiones sobre el ejemplo revisado en clase:

### ✅ Mejoras implementadas

1. **Limpieza automática de datos de prueba**  
   Cada prueba inserta datos temporales (usuarios y tareas) que son eliminados al finalizar la ejecución. Además, se valida que los datos hayan sido correctamente eliminados.

2. **Generación automática de reportes PDF**  
   Los resultados de las pruebas se almacenan en archivos `.pdf` generados por el sistema de manera automática. Cada reporte se guarda con un número secuencial y se conservan todos los reportes previos sin sobrescribir.

---

## 🧪 Resultados de las Pruebas

### 🔹 Back-End

Se ejecutaron las siguientes operaciones:
- Creación de usuario mediante API.
- Creación de tarea asociada a ese usuario.
- Verificación de existencia de la tarea.
- Eliminación de los datos generados.
- Confirmación de eliminación exitosa.

📄 El resultado de esta prueba fue almacenado en:  
`Test/reports/test_report_001.pdf`

### 🔹 Front-End

Se automatizó el uso de la interfaz mediante Selenium:
- Simulación de creación de usuario desde el navegador.
- Verificación de respuesta visual.
- Generación de reporte con el resultado de la interfaz.

📄 El resultado fue almacenado en:  
`Test/reports/test_report_002.pdf`

---

## 🗂️ Archivos modificados / añadidos

- `Test/BackEnd-Test.py` – Ahora incluye limpieza y validación de datos, y genera un PDF.
- `Test/FrontEnd-Test.py` – Automatiza flujo con Selenium y genera su respectivo PDF.
- `Test/utils/generate_pdf_report.py` – Script auxiliar para crear reportes en PDF.
- `requirements.txt` – Se añadió la librería `fpdf`.

---

## ▶️ Instrucciones para ejecución

1. Asegúrate de que todos los servicios estén corriendo en `localhost` con los puertos adecuados:
   - Front-End: `localhost:5000`
   - Users_Service: `localhost:5001`
   - Task_Service: `localhost:5002`

2. Instala dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecuta las pruebas:

```bash
python Test/BackEnd-Test.py
python Test/FrontEnd-Test.py
```

Cada ejecución generará un nuevo archivo PDF en la carpeta `Test/reports/`.
