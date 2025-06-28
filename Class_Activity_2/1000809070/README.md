# 🧪 Class Activity 2 - Integration Testing Report

## 👨‍💻 Autor
- ID: 1000809070
- Nombre: Jacel Thomás Enciso Pinzon
---

## ✅ Cambios realizados

### 1. Endpoints nuevos

Se agregaron nuevos endpoints a los servicios para permitir **eliminación de datos** y así cumplir con la limpieza después de los tests.

#### 🔹 En `Users_Service/main.py`

```python
@service_a.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Usuario eliminado'}), 200
    return jsonify({'error': 'Usuario no existente'}), 404

```
#### 🔹 En `Task_Service/main.py`

```python
@service_b.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': f'Tarea {task_id} eliminada'}), 200
    return jsonify({'error': 'Tarea no encontrada'}), 404
```

### 2. Tests de integración

#### 🧪 Nuevas funciones para limpieza:
* delete_user(user_id)
* delete_task(task_id)

#### 📄 Generación automática de PDF:
Se añadió integración con reportlab para guardar los resultados del test en archivos como report_1.pdf, report_2.pdf, etc.

```python
 from reportlab.pdfgen import canvas
```
Incluyen:

* Título y fecha del test
* Resultados paso a paso
* Mensajes de limpieza exitosa o errores

#### 🧹 Verificación de limpieza:
Después de eliminar los datos, se verifica que la tarea haya sido correctamente eliminada de la base de datos.
```python
tasks = get_tasks()
assert not any(t["id"] == task_id for t in tasks), "❌ Task was not deleted"
```

---
## ▶️ Ejecución del test
Para ejecutar los tests, se debe correr el archivo `BackEnd-Test.py` que contiene las funciones de prueba.
Asegúrate de tener los servicios corriendo.
```bash
cd Class_Activity_2/1000809070
python Test\BackEnd-Test.py
```