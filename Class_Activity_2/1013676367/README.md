# Sistema de Gestión de Usuarios y Tareas

Jesus David Giraldo Gomez - 1013676367

Este proyecto tiene como objetivo implementar un sistema completo de gestión de usuarios y tareas mediante una arquitectura de microservicios en Flask, con énfasis en pruebas de integración automatizadas y generación de reportes. La actividad se centra en:

* Pruebas de integración automatizadas para validar la comunicación entre componentes

* Limpieza automática de datos después de cada ejecución de pruebas

* Generación de reportes en PDF con resultados

* Verificación de consistencia del sistema post-ejecución


## Tecnologías utilizadas

|Componente	|Tecnologías|
|--------------|--------------|
|Backend	|Python, Flask, REST APIs|
|Frontend	|HTML, JavaScript|
|Pruebas |Backend	requests, pytest|
|Pruebas |Frontend	Selenium WebDriver|
|Reportes	|FPDF (generación PDF)|


## Instalación
```bash
clone https://github.com/SwEng2-2025i/MV7h.git
cd Class_Activity_2
cd 1013676367
pip install -r requirements.txt
```
### Iniciar servicios de Usuarios
```bash
cd Users_Service
flask run

```
### Iniciar servicios de Task
```bash
cd Task_Service
flask run

```

### Iniciar servicios de FrontEnd
```bash
cd Front-End
flask run

```

---
## Estructura del proyecto

```bash
📦 Proyecto
├── 📂 Front-End/
│   └── main.py
├── 📂 instance/
│   ├── tasks.db
│   └── users.db
├── 📂 Task_Service/
│   └── main.py
├── 📂 Test/
│   ├── BackEnd-Test.py
│   └── FrontEnd-Test.py
├── 📂 Users_Service/
│   └── main.py
├── README.md                
└── requirements.txt 
```

## Funcionalidades Implementadas

### Limpieza automática post-pruebas

Se implementaron endpoints específicos en los microservicios para garantizar la limpieza de datos de prueba:

#### Users_Service:
```bash
GET /users/delete/<user_id>
```


```python
@service_a.route('/users/delete/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    try:
        rows_deleted = User.query.filter_by(id=user_id).delete()
        if rows_deleted == 0:
            raise ValueError(f"No se encontró el usuario con ID: {user_id}")
        db.session.commit()
        return jsonify({'delete user': f'{user_id}'})
    except Exception as e:
        return jsonify({'error': f'Error de conexión al usuarios: {str(e)}'}), 500

```
* Elimina un usuario específico por ID
* Retorna código 200 si la operación fue exitosa

#### Task_Service:
```bash
GET /tasks/delete/<task_id>
```

```python
@service_b.route('/tasks/delete/<int:task_id>', methods=['GET'])
def delete_tasks(task_id):
    try:
        rows_deleted = Task.query.filter_by(id=task_id).delete()
        if rows_deleted == 0:
            raise ValueError(f"No se encontró la tarea con ID: {task_id}")
        db.session.commit()
        return jsonify({'delete task': f'{task_id}'})
    except Exception as e:
        return jsonify({'error': f'Error de conexión a tarea: {str(e)}'}), 500

```
* Elimina una tarea específica por ID
* Retorna código 204 (No Content) al completarse

### Flujo de limpieza:

* Las pruebas registran IDs de recursos creados

* Al finalizar la ejecución, invocan los endpoints de limpieza
---
### Generación Automática de Reportes PDF

* Librería FPDF para generación programática de documentos
* Numeración secuencial automática (Report_1.pdf, Report_2.pdf, ...)
* en Test/BackEnd_reports and Test/ ordenados secuencialmente

```python
def create_pdf(results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Resultados de Pruebas", ln=True, align="C")
    pdf.ln(10)

    for line in results:
        pdf.multi_cell(0, 10, line.encode('ascii', 'ignore').decode())
    path = os.getcwd()
    dr='\\'
    folder = 'Test'
    new_folder = 'BackEnd_reports' #FrontEnd_reports
    new_path = path + dr + folder + dr  + new_folder

    if not os.path.exists(new_path):
        os.makedirs(new_path)
    dirs = os.listdir(new_path)
    num = 0
    for item in dirs:
        if os.path.isfile(new_path + dr + item):
            num+=1

    pdf_filename = os.path.join(new_path, f"Report_{num}.pdf")
    pdf.output(pdf_filename)
    print("PDF generado como 'resultados_BackEnd_Test.pdf'") #FrontEnd_reports
```

#### Estructura de reportes:

```bash
📦 Test
├── 📂 BackEnd_reports
│   ├── Report_1.pdf
│   ├── Report_2.pdf
│   └── ...
└── 📂 FrontEnd_reports
    ├── Report_1.pdf
    ├── Report_2.pdf
    └── ...

```
___
## Cómo Ejecutar las Pruebas
### Preparación:
```bash
pip install fpdf selenium requests pytest fpdf
```
### Ejecutar pruebas Backend:
```bash
python Backend.py
```
### Ejecutar pruebas Frontend:
```bash
python Frontend.py
```
### Ver reportes generados:
* Backend: Test/BackEnd_reports/Report_*.pdf
* Frontend: Test/FrontEnd_reports/Report_*.pdf
