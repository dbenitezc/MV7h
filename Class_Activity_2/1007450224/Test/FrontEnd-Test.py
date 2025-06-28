
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from utils import generate_pdf_report

def test_frontend():
    results = []
    try:
        driver = webdriver.Chrome()
        driver.get("http://localhost:5000")
        time.sleep(2)

        username_input = driver.find_element(By.ID, "username")
        username_input.send_keys("Ana")
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[contains(text(), 'Crear Usuario')]").click()
        time.sleep(2)

        user_result = driver.find_element(By.ID, "user-result").text
        if "Usuario creado con ID" in user_result:
            results.append("✅ Usuario creado vía interfaz correctamente")
        else:
            results.append("❌ Usuario no fue creado correctamente")

        driver.quit()

    except Exception as e:
        results.append(f"❌ Error en prueba de interfaz: {e}")

    generate_pdf_report(results)

if __name__ == "__main__":
    test_frontend()
