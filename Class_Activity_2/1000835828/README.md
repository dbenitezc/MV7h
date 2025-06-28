# Class activity 2
## Cristhian Alejandro Alarcón Florido CC 1000835828
## Descripción del Proyecto
Este proyecto implementa un sistema distribuido con backend en microservicios para gestionar usuarios y tareas, con una interfaz frontend y pruebas automatizadas. Las dos funcionalidades principales agregadas son:

- Limpieza de datos de prueba - Elimina automáticamente datos generados durante pruebas

- Generación de reportes PDF - Crea reportes secuenciales con resultados de pruebas

## Requisitos del Sistema
Dependencias:

``` bash
pip install -r requirements.txt
```
Contenido de requeriments.txt
```bash
Flask==3.0.0
Flask-Cors==4.0.0
Flask-SQLAlchemy==3.1.1
selenium==4.15.2
fpdf==1.7.2
requests==2.31.0
webdriver-manager==4.0.1
```
## Configuración de Puertos

| Servicio    | Puerto | Archivo Principal       |
|-------------|--------|-------------------------|
| Frontend    | 5000   | `Front-End/main.py`      |
| Userservice | 5001   | `Users_Service/main.py`  |
| Taskservice | 5002   | `Task_Service/main.py`   |

## Intrucciones de ejecución

1. Iniciar los servicios
Abre tres terminales diferentes:

Terminal 1 - Userservice:
``` bash
cd Users_Service
python main.py
```
Terminal 2 - Taskservice:

``` bash
cd Task_Service
python main.py
```
Terminal 3 - Frontend:

``` bash
cd Front-End
python main.py
```

2. Ejecutar pruebas
Pruebas Backend:
```bash
cd Test
python BackEnd-Test.py
```
Pruebas Frontend:
```bash
cd Test
python FrontEnd-Test.py
```
## Funcionalidades Implementadas
## Limpieza de Datos de Prueba
Objetivo: Eliminar automáticamente los datos creados durante las pruebas
Implementación:

Nuevos endpoints DELETE en los servicios:

- DELETE /test/cleanup (Userservice)

- DELETE /test/cleanup (Taskservice)

Otras implementaciones:

- Botón "Eliminar Datos de Prueba" en el frontend

- Verificación automática en pruebas

### Secciones de código agregadas:
```bash
Users_Service/main.py:
  • Ruta: @service_a.route('/test/cleanup', methods=['DELETE'])
  
Task_Service/main.py:
  • Ruta: @service_b.route('/test/cleanup', methods=['DELETE'])
  
Front-End/main.py:
  • HTML: <div class="card"> (Panel de limpieza)
  • JavaScript: function limpiarDatosPrueba()

Test/BackEnd-Test.py:
  • Función: cleanup_test_data()
  • Función: verify_cleanup()

Test/FrontEnd-Test.py:
  • Función: limpiar_y_verificar(driver, wait)
```
## Código más detallado de las secciones modificadas/agregadas:
### Backend
- Users_Service/main.py:
```py
@service_a.route('/test/cleanup', methods=['DELETE'])
def cleanup_test_users():
    # Elimina usuarios de prueba
    test_users = User.query.filter(User.name.in_(['Ana', 'Camilo'])).all()
    for user in test_users:
        db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'{len(test_users)} usuarios de prueba eliminados'}), 200
```
- Task_Service/main.py:
``` py
@service_b.route('/test/cleanup', methods=['DELETE'])
def cleanup_test_tasks():
    # Elimina tareas de prueba
    test_tasks = Task.query.filter(Task.title.in_(['Terminar laboratorio', 'Prepare presentation'])).all()
    for task in test_tasks:
        db.session.delete(task)
    db.session.commit()
    return jsonify({'message': f'{len(test_tasks)} tareas de prueba eliminadas'}), 200
```
### Frontend
- Front-End/main.py:
``` py
<!-- Panel de limpieza -->
<div class="card">
  <h2>🧹 Limpieza de Datos</h2>
  <button class='cleanup-btn' onclick='limpiarDatosPrueba()'>Eliminar Datos de Prueba</button>
  <div id="cleanup-result" class="result"></div>
</div>

<script>
function limpiarDatosPrueba() {
  // Llama a los endpoints de limpieza
  fetch('http://localhost:5002/test/cleanup', {method: 'DELETE'})
    .then(...)
    .then(() => {
      fetch('http://localhost:5001/test/cleanup', {method: 'DELETE'})
    })
    .then(...)
}
</script>
```

- Test/BackEnd-Test.py:

```py
def cleanup_test_data():
    # Llama a los endpoints de limpieza
    requests.delete(CLEANUP_TASKS_URL)
    requests.delete(CLEANUP_USERS_URL)

def verify_cleanup():
    # Verifica que los datos fueron eliminados
    users = get_users()
    tasks = get_tasks()
    assert not any(u['name'] in ['Ana', 'Camilo'] for u in users)
    assert not any(t['title'] in ['Terminar laboratorio', 'Prepare presentation'] for t in tasks)
```
- Test/FrontEnd-Test.py:
```py
def limpiar_y_verificar(driver, wait):
    # Hace clic en el botón de limpieza y verifica
    driver.find_element(...).click()
    assert "eliminados" in driver.find_element(...).text
    assert "Terminar laboratorio" not in ver_tareas(driver, wait)
```


## Generación Automática de Reportes PDF
Objetivo: Crear reportes secuenciales con resultados de pruebas
Implementación:

- Numeración automática de reportes (report_1.pdf, report_2.pdf, etc.)

- Captura de resultados y capturas de pantalla

- Almacenamiento organizado en carpetas

Secciones de código agregadas:
``` bash
Test/pdf_report.py (NUEVO ARCHIVO):
  • Función: generate_pdf_report()
  • Función: clean_text_for_pdf()

Test/BackEnd-Test.py:
  • Integración: test_results = []
  • Llamada: generate_pdf_report(...)

Test/FrontEnd-Test.py:
  • Función: capture_screenshot()
  • Variables: test_results y screenshots
  • Llamada: generate_pdf_report(...)
```
## Estructura de archivos generados
```bash
Test/
├── test_reports/            # Reportes PDF secuenciales
│   ├── report_1.pdf         # Ej: Backend Test Report
│   ├── report_2.pdf         # Ej: Frontend Test Report
│   └── ...
│
├── test_screenshots/        # Capturas de pruebas Frontend
│   ├── frontend_abierto_20230628_153045.png
│   ├── usuario_creado_20230628_153047.png
│   └── ...
│
└── frontend_test_results.txt  # Respaldo en caso de error
```
## Código más detallado de las secciones agregadas/modificadas:

### Modulo de reportes:
- Test/pdf_report.py
``` py
def generate_pdf_report(test_name, test_results, screenshots=None):
    # Genera reporte PDF con numeración secuencial
    next_num = determinar_numero_secuencia()
    pdf = FPDF()
    # ... (configuración del PDF)
    
    # Agrega resultados
    for result, success in test_results:
        pdf.set_text_color(0,128,0) if success else (255,0,0)
        pdf.cell(200, 10, txt=f"- {clean_text(result)}", ln=1)
    
    # Agrega capturas de pantalla
    if screenshots:
        for screenshot in screenshots:
            pdf.add_page()
            pdf.image(screenshot, x=10, y=30, w=180)
    
    # Guarda con nombre secuencial
    filename = f"test_reports/report_{next_num}.pdf"
    pdf.output(filename)
    return filename
```
### Integración en pruebas:
- Test/BackEnd-Test.py:

``` py
def integration_test():
    test_results = []
    try:
        # Ejecuta pruebas
        test_results.append(("Paso 1: Crear usuario", True))
        # ...
    finally:
        # Genera reporte PDF
        generate_pdf_report("Backend Test", test_results)
```
- Test/FrontEnd-Test.py:
```py
def main():
    test_results = []
    screenshots = []
    try:
        # Ejecuta pruebas y captura pantallas
        test_results.append(("Frontend abierto", True))
        screenshots.append(capture_screenshot(driver, "paso1"))
        # ...
    finally:
        # Genera reporte con capturas
        generate_pdf_report("Frontend Test", test_results, screenshots)
```
### Función de captura de pantalla:
- Test/FrontEnd-Test.py:

```py
def capture_screenshot(driver, name):
    # Guarda captura con timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_screenshots/{name}_{timestamp}.png"
    driver.save_screenshot(filename)
    return filename
```