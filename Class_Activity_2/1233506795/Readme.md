# Actividad - Class_Activity_2

Este documento describe los cambios introducidos en los scripts de prueba automatizada (`FrontEnd-Test.py` y `BackEnd-Test.py`). Los cambios están enfocados en automatizar la ejecución, mejorar la verificación de resultados y generar reportes.

## Cambios principales

### 1. Automatización del levantamiento y cierre de servicios

#### 🔸 Función nueva: `iniciar_services()`

- Se agregó a ambos scripts.
- Usa `subprocess.Popen()` para levantar los servicios Flask correspondientes.
- Permite que el script funcione de forma independiente sin necesidad de iniciar manualmente `main.py` en cada servicio.

```python
def iniciar_services():
    global services
    services = [
        subprocess.Popen(["python", "Task_Service/main.py"]),
        subprocess.Popen(["python", "Users_Service/main.py"]),
        subprocess.Popen(["python", "Front-End/main.py"])  # Solo en FrontEnd-Test
    ]
    time.sleep(3)
```

#### 🔸 Función nueva: `cerrar_services()`

- Cierra los procesos iniciados automáticamente.

```python
def cerrar_services():
    for proc in services:
        proc.terminate()
        proc.wait()
```

### 2. Generación de reportes en PDF

#### 🔸 Función nueva: `generar_reporte_pdf(info_test)`

- Disponible en ambos scripts.
- Usa `matplotlib` para generar una gráfica de barras con los resultados (éxitos y fallos).
- Usa `fpdf` para generar un PDF detallado con cada asignación y su estado.
- El gráfico temporal se elimina tras insertarse en el PDF.

```python
def generar_reporte_pdf(info_test):
    # Crea gráfico y PDF en Test/reports/
    ...
    plt.savefig(graph_image_path)
    ...
    pdf.output(pdf_path)
    ...
```

### 3. Limpieza automática

- Se agregó en el bloque `finally`:
  - Cierre de servicios
  - Eliminación de carpeta `instance/`
  - En el caso del Front-End, cierre del navegador con `driver.quit()`

```python
finally:
    cerrar_services()
    if os.path.exists("instance") and os.path.isdir("instance"):
        shutil.rmtree("instance")
    driver.quit()  # Solo en FrontEnd-Test
```

---

## Comparación de scripts

### 🔹 Script original `BackEnd-Test.py`
- Tenía funciones básicas para crear usuario y tarea mediante `requests`.
- No generaba reporte.
- Los servicios debían estar levantados manualmente.

#### Actualizaciones 
- Se agregaron `iniciar_services`, `cerrar_services`, y `generar_reporte_pdf`.
- Se automatizó toda la prueba.
- Se incluyó validación de que la tarea esté correctamente asignada.
- Se genera un PDF: `Results-BackEnd-Test.pdf`.

### 🔹 Script original `FrontEnd-Test.py`
- Ejecutaba una sola prueba en navegador.
- No se levantaban servicios automáticamente.
- No había reporte ni verificación masiva.

#### Actualizaciones
- Se agregó lógica para ejecutar 10 pruebas distintas automáticamente.
- Se crearon/modificaron las funciones: `iniciar_services`, `cerrar_services`, `generar_reporte_pdf`, `ver_tareas`, `tarea_asignada`.
- Se valida que las tareas aparezcan asociadas a cada usuario en la interfaz.
- Se genera un PDF: `Results-FrontEnd-Test.pdf`.

---

## Ejecución de pruebas

> **Ya no es necesario levantar manualmente los servicios.**

Desde la carpeta `Test/`, simplemente ejecuta uno de los siguientes comandos:

```bash
python FrontEnd-Test.py
```
o
```bash
python BackEnd-Test.py
```

Cada script inicia sus propios servicios, realiza las pruebas, genera el PDF y cierra todo automáticamente.

---

## Estructura de carpetas esperada

```
1233506795/
├── Users_Service/
│   └── main.py
├── Task_Service/
│   └── main.py
├── Front-End/
│   └── main.py
├── Test/
│   ├── reports/
│   │   ├── Results-BackEnd-Test.pdf
│   │   └── Results-FrontEnd-Test.pdf
│   ├── BackEnd-Test.py
│   └── FrontEnd-Test.py
```
