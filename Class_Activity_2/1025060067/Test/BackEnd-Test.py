import requests
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

# Endpoints
USERS_URL = "http://localhost:5001/users"
TASKS_URL = "http://localhost:5002/tasks"

# Global list to store test results
test_results = []

def create_user(name):
    try:
        response = requests.post(USERS_URL, json={"name": name})
        response.raise_for_status()
        user_data = response.json()
        print(f"✅ User created: {user_data}")
        test_results.append("✅ User creation: PASSED")
        return user_data["id"]
    except requests.exceptions.RequestException as e:
        print(f"❌ User creation failed: {e}")
        test_results.append(f"❌ User creation: FAILED - {e}")
        return None

def get_user(user_id):
    try:
        response = requests.get(f"{USERS_URL}/{user_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def delete_user(user_id):
    try:
        response = requests.delete(f"{USERS_URL}/{user_id}")
        response.raise_for_status()
        print(f"🗑️ User with ID {user_id} deleted.")
        test_results.append(f"🗑️ User deletion (ID: {user_id}): PASSED")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ User deletion failed for ID {user_id}: {e}")
        test_results.append(f"❌ User deletion (ID: {user_id}): FAILED - {e}")
        return False

def create_task(user_id, description):
    try:
        response = requests.post(TASKS_URL, json={
            "title": description,
            "user_id": user_id
        })
        response.raise_for_status()
        task_data = response.json()
        print(f"✅ Task created: {task_data}")
        test_results.append("✅ Task creation: PASSED")
        return task_data["id"]
    except requests.exceptions.RequestException as e:
        print(f"❌ Task creation failed: {e}")
        test_results.append(f"❌ Task creation: FAILED - {e}")
        return None

def get_tasks():
    try:
        response = requests.get(TASKS_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to get tasks: {e}")
        test_results.append(f"❌ Get tasks: FAILED - {e}")
        return []

def get_task(task_id):
    try:
        response = requests.get(f"{TASKS_URL}/{task_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

def delete_task(task_id):
    try:
        response = requests.delete(f"{TASKS_URL}/{task_id}")
        response.raise_for_status()
        print(f"🗑️ Task with ID {task_id} deleted.")
        test_results.append(f"🗑️ Task deletion (ID: {task_id}): PASSED")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Task deletion failed for ID {task_id}: {e}")
        test_results.append(f"❌ Task deletion (ID: {task_id}): FAILED - {e}")
        return False

def generate_pdf_report(results, filename_prefix="Backend_Test_Report"):
    if not os.path.exists("reports"):
        os.makedirs("reports")

    # Get sequential number
    report_number = 1
    while os.path.exists(f"reports/{filename_prefix}_{report_number}.pdf"):
        report_number += 1
    
    filename = f"reports/{filename_prefix}_{report_number}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Backend Integration Test Report", styles['h1']))
    story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 12))

    for result in results:
        style = styles['Normal']
        if "FAILED" in result:
            style = styles['Code'] # Or a custom style for errors
            story.append(Paragraph(f"<font color='red'>{result}</font>", style))
        else:
            story.append(Paragraph(result, style))
        story.append(Spacer(1, 6))

    try:
        doc.build(story)
        print(f"📊 PDF report generated: {filename}")
        test_results.append(f"📊 PDF report generated: {filename}")
    except Exception as e:
        print(f"❌ Error generating PDF report: {e}")
        test_results.append(f"❌ Error generating PDF report: FAILED - {e}")

def integration_test():
    user_id = None
    task_id = None
    global test_results # Ensure test_results is cleared for each run
    test_results = []

    try:
        # Step 1: Create user
        user_id = create_user("Camilo")
        assert user_id is not None, "❌ User creation failed, user_id is None."
        test_results.append("Assertion: User ID is not None: PASSED")

        # Step 2: Create task for that user
        task_id = create_task(user_id, "Prepare presentation")
        assert task_id is not None, "❌ Task creation failed, task_id is None."
        test_results.append("Assertion: Task ID is not None: PASSED")

        # Step 3: Verify that the task is registered and associated with the user
        tasks = get_tasks()
        user_tasks = [t for t in tasks if t["user_id"] == user_id]

        assert any(t["id"] == task_id for t in user_tasks), "❌ The task was not correctly registered"
        print("✅ Test completed: task was successfully registered and linked to the user.")
        test_results.append("✅ Verification of task registration and linkage: PASSED")

        # Step 4: Verify data cleanup (after the main test)
        # Delete task
        deleted_task = delete_task(task_id)
        assert deleted_task, f"❌ Task with ID {task_id} was not deleted."
        if deleted_task:
            # Verify task is no longer present
            retrieved_task = get_task(task_id)
            assert retrieved_task is None, "❌ Deleted task is still present."
            print(f"✅ Verification: Task with ID {task_id} successfully deleted and not found.")
            test_results.append(f"✅ Verification: Task with ID {task_id} deleted and not found: PASSED")


        # Delete user
        deleted_user = delete_user(user_id)
        assert deleted_user, f"❌ User with ID {user_id} was not deleted."
        if deleted_user:
            # Verify user is no longer present
            retrieved_user = get_user(user_id)
            assert retrieved_user is None, "❌ Deleted user is still present."
            print(f"✅ Verification: User with ID {user_id} successfully deleted and not found.")
            test_results.append(f"✅ Verification: User with ID {user_id} deleted and not found: PASSED")

    except AssertionError as ae:
        print(f"❌ Assertion Failed: {ae}")
        test_results.append(f"❌ ASSERTION FAILED: {ae}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        test_results.append(f"❌ UNEXPECTED ERROR: {e}")
    finally:
        generate_pdf_report(test_results, "Backend_Test_Report")


if __name__ == "__main__":
    integration_test()