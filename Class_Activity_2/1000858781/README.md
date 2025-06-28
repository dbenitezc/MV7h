## 📌 Cambios Clave en los Servicios

### Endpoints Modificados

#### `task_service.py`

```python
# Nuevo endpoint para eliminar tareas por ID
@service_b.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': f'Tarea con ID {task_id} eliminada'}), 200

```

#### `users_service.py`

# Endpoint actualizado para eliminar usuarios

```python
@service_a.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'Usuario con ID {user_id} eliminado correctamente'}), 200
```

### Funciones de elminacion en los test

```python
def delete_task(task_id):
    """Elimina una tarea usando el servicio API"""
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()

def delete_user(user_id):
    """Elimina un usuario usando el servicio API"""
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()
```

### Sistema de generacion de reportes en pdf

```python
class PDFReport(FPDF):
    def __init__(self, test_name):
        super().__init__()
        self.test_name = test_name
        self.report_content = []
        self.report_number = self.get_next_report_number()
        self.filename = f"reports/backend_report_{self.report_number:03d}.pdf"

    def get_next_report_number(self):
        counter = 1
        while os.path.exists(f"reports/backend_report_{counter:03d}.pdf"):
            counter += 1
        return counter

    def add_test_step(self, step, message):
        self.report_content.append(f"{step}: {message}")

    def generate(self):
        self.add_page()
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, f'Backend Test Report #{self.report_number}', 0, 1, 'C')
        self.ln(10)

        self.set_font('Arial', '', 12)
        self.cell(0, 10, f'Test Name: {self.test_name}', 0, 1)
        self.cell(0, 10, f'Execution Date: {time.strftime("%Y-%m-%d %H:%M:%S")}', 0, 1)
        self.ln(10)

        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Test Steps and Results:', 0, 1)
        self.ln(5)

        self.set_font('Courier', '', 10)
        for line in self.report_content:
            self.multi_cell(0, 5, line)
            self.ln(2)

        self.output(self.filename)
        return self.filename
```

### Resultados de los tests

#### Backend

- Creación exitosa de usuario y tarea
- Verificación de existencia de la tarea
- Eliminación por ID
- Confirmación de eliminación
- Eliminación del usuario
- Generación de reporte PDF

#### Frontend

- Creación de usuario desde la UI
- Creación de tarea desde la UI
- Verificación visual de tarea
- Eliminación por la API anteriormente creada
- Desaparición visual de tarea
- Generación de reporte PDF con pasos
