## 🧪 Test Results Summary

- ✔️ A user and a task are successfully created and associated via both the BackEnd API and FrontEnd UI.
- ✔️ Data cleanup is correctly performed after each test: the task and user created are deleted automatically.
- ✔️ Verifications confirm that the deleted data no longer exists in the system.
- ✔️ Each test run generates an automatic PDF report with a timestamp, stored in the `reports` folder.

  ### 1. `integration_test.py` (BackEnd)
- ✅ Functions added:
  - `delete_user(user_id)`
 ```
def delete_user(user_id):
    response = requests.delete(f"{USERS_URL}/{user_id}")
    response.raise_for_status()

@service_a.route('/users/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error' : 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200 
```
  - `delete_task(task_id)`
```
@service_b.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):   
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error' : 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200

def delete_task(task_id):
    response = requests.delete(f"{TASKS_URL}/{task_id}")
    response.raise_for_status()
```
  - `get_user(user_id)`
```
@service_a.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'id': user.id, 'name': user.name})
    return jsonify({'error': 'User not found'}), 404

def get_user(user_id):
    response = requests.get(f"{USERS_URL}/{user_id}")
    return response
```
  - `get_task(task_id)`
```
@service_b.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify({'id': task.id, 'title': task.title, 'user_id': task.user_id}), 200

def get_task(task_id):
    response = requests.get(f"{TASKS_URL}/{task_id}")
    return response  # no usamos raise_for_status para manejar 404
```
  - `generate_pdf_report(...)`
* Backend Test
```
def get_next_report_filename():
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return os.path.join(REPORTS_DIR, f"report_{timestamp}.pdf")

def generate_pdf_report(content_lines):
    filename = get_next_report_filename()
    c = canvas.Canvas(filename, pagesize=LETTER)
    width, height = LETTER
    y = height - 50

    for line in content_lines:
        c.drawString(50, y, line)
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    print(f"📄 PDF report saved as: {filename}")
```
* Fronted Test
```
def generar_pdf(log):
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(REPORTS_DIR, f"frontend_report_{timestamp}.pdf")

    c = canvas.Canvas(filename, pagesize=LETTER)
    width, height = LETTER
    y = height - 50

    for line in log:
        c.drawString(50, y, line)
        y -= 20
        if y < 50:
            c.showPage()
            y = height - 50

    c.save()
    print("📄 PDF generado:", filename)
```
- ✅ `integration_test()` enhanced to:
  - Clean up created data.
  - Verify deletion by checking 404 responses.
  - Generate a PDF report after execution.

### 2. `frontend_test.py` (FrontEnd Selenium Test)
- ✅ New logging mechanism to collect and summarize test output.
- ✅ Uses Selenium to:
  - Create a user and task via UI.
  - Verify data presence in task list.
- ✅ A PDF report is generated at the end of each run, stored in `../reports`.

### Autor
Andres Camilo Orduz Lunar
1001301429
