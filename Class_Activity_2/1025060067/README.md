# Class Activity 2 
### Implemented Features

#### 1. Data Cleanup

To ensure that all data added during test execution is deleted afterward, and to verify its proper deletion, the following modifications were made:

* **Backend Services (`main_Users_Service.py` and `main_Task_Service.py`):**
    * Added new `DELETE` endpoints for both `/users/<int:user_id>` and `/tasks/<int:task_id>`. These endpoints allow for the removal of specific user and task records from their respective databases.
    * **Code Added:**
        * `@service_a.route('/users/<int:user_id>', methods=['DELETE'])` function in `main_Users_Service.py`.
        * `@service_b.route('/tasks/<int:task_id>', methods=['DELETE'])` function in `main_Task_Service.py`.

* **Backend Test (`BackEnd-Test.py`):**
    * Implemented `delete_user` and `delete_task` helper functions to interact with the new DELETE endpoints.
    * The `integration_test` function now captures the `user_id` and `task_id` of the created entities.
    * A `finally` block was added to the `integration_test` function to ensure that cleanup operations are always attempted, even if earlier test steps fail.
    * After creating and verifying the user and task, the test now calls the `delete_task` and `delete_user` functions.
    * Assertions were added to verify that the `delete` operations were successful and that the deleted entities are no longer retrievable from the respective services (e.g., `get_user` and `get_task` return `None`).
    * **Code Modified/Added:**
        * `delete_user(user_id)` function.
        * `delete_task(task_id)` function.
        * `get_user(user_id)` and `get_task(task_id)` helper functions for verification after deletion.
        * Cleanup logic and verification assertions within the `integration_test`'s `finally` block.

* **Frontend Test (`FrontEnd-Test.py`):**
    * Similar to the backend test, `delete_user_api` and `delete_task_api` helper functions were added to directly call the backend DELETE endpoints using `requests`.
    * The `crear_usuario` and `crear_tarea` functions were modified to extract and return the `user_id` and `task_id` from the UI's success messages.
    * The `main` function now stores these IDs.
    * A `finally` block was added to `main` to perform cleanup.
    * Assertions were included to confirm successful deletion and that the entities are no longer present in the backend.
    * **Code Modified/Added:**
        * `delete_user_api(user_id)` function.
        * `delete_task_api(task_id)` function.
        * `get_user_api(user_id)` and `get_task_api(task_id)` functions for verification.
        * Logic to capture `user_id` and `task_id` from UI output.
        * Cleanup logic and verification assertions within the `main` function's `finally` block.

#### 2. Automatic PDF Report Generation

To automatically save test results in sequentially numbered PDF files, the following was implemented:

* **Shared Reporting Logic:**
    * A `generate_pdf_report` function was created and integrated into both `BackEnd-Test.py` and `FrontEnd-Test.py`.
    * This function uses the `reportlab` library to create PDF documents.
    * It dynamically generates a filename with a sequential number (e.g., `Backend_Test_Report_1.pdf`, `Backend_Test_Report_2.pdf`) to prevent overwriting previous reports.
    * The function takes a list of test results (strings indicating pass/fail) and formats them into the PDF. Failed tests are highlighted in red.
    * A `reports` directory is created if it does not already exist to store the generated PDFs.
    * **Code Added:**
        * `generate_pdf_report(results, filename_prefix)` function in both test files.
        * Import statements for `reportlab` components (`SimpleDocTemplate`, `Paragraph`, `Spacer`, `getSampleStyleSheet`, `letter`).
        * Import `os` and `datetime` for file system operations and timestamping reports.
* **Integration with Tests:**
    * A global `test_results` list was introduced in both `BackEnd-Test.py` and `FrontEnd-Test.py` to accumulate the outcome of each test step and assertion.
    * Each significant action (e.g., user creation, task creation, verification, cleanup) appends a success or failure message to this list.
    * The `generate_pdf_report` function is called in the `finally` block of the main test execution function (`integration_test` in Backend, `main` in Frontend) to ensure a report is always generated at the end of the test run.
    * **Code Modified/Added:**
        * `test_results = []` global variable and `global test_results` usage.
        * `test_results.append(...)` statements throughout the test functions.
        * Call to `generate_pdf_report()` in the `finally` block of the main test function.

### Setup and Running the Tests

1.  [cite_start]**Install Dependencies:** Ensure `pip install flask flask_sqlalchemy requests reportlab selenium` is run to install all necessary libraries[cite: 1].
2.  **Run Backend Services:**
    * Start `main_Users_Service.py`: `python main_Users_Service.py`
    * Start `main_Task_Service.py`: `python main_Task_Service.py`
3.  **Run Frontend Service:**
    * Start `main_Front_End.py`: `python main_Front_End.py`
4.  **Run Tests:**
    * For Backend Integration Test: `python BackEnd-Test.py`
    * For Frontend Integration Test: `python FrontEnd-Test.py`

After running the tests, a `reports` folder will be created (if it doesn't exist), containing the PDF reports of the test executions.

### Conclusion

The implemented features successfully address the requirements for data cleanup and automatic PDF report generation. The tests now create, verify, and then meticulously remove the data, ensuring a clean state after execution. Furthermore, the detailed PDF reports provide clear and persistent records of test outcomes, enhancing the traceability and analysis of integration test runs.
