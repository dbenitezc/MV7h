# Actividad de clase 2 - Informe de Pruebas

## ✅ Objetivo

Este proyecto implementa pruebas de integración para una aplicación compuesta por tres servicios: FrontEnd, BackEnd de Usuarios y BackEnd de Tareas. Se añadieron las siguientes mejoras a los scripts de prueba:

1. **Limpieza automática de datos**: Toda la información creada durante las pruebas es eliminada al finalizar.
2. **Generación automática de reporte PDF**: Los resultados de cada prueba son almacenados en archivos PDF numerados, sin sobrescribir reportes previos.

---

## 🧪 Resultados de las pruebas

- **Prueba de BackEnd**: Se validó exitosamente la creación y posterior eliminación de un usuario y una tarea.  
  - ✔️ Usuario creado
  - ✔️ Tarea creada y asociada
  - ✔️ Datos eliminados correctamente
  - 📄 Reporte generado en `Test/reports/test_report_2.pdf`

- **Prueba de FrontEnd**: Se automatizó el uso de la interfaz gráfica usando Selenium.  
  - ✔️ Usuario creado vía interfaz
  - ✔️ Tarea asociada al usuario creada vía interfaz
  - ✔️ Verificación de tareas en pantalla
  - ✔️ Eliminación de datos mediante llamadas HTTP (ya que el frontend no soporta eliminación en la UI)
  - 📄 Reporte generado en `Test/reports/test_report_4.pdf`

---

## 🛠️ Cambios realizados en el código

### 1. **Scripts de prueba**
- Se agregaron funciones `borrar_datos(...)` en ambos scripts (`BackEnd-Test.py` y `FrontEnd-Test.py`) que usan `requests.delete(...)` para eliminar usuarios y tareas creados durante la prueba.
- Se implementó la función `generate_pdf_report(...)` usando `fpdf` para generar reportes automáticos.
- En el script de frontend, se mejoraron los `wait` con `expected_conditions` para asegurar sincronización con la interfaz.

### 2. **Servicios Flask**
Se agregaron endoints de `DELETE` en los servicios de usuarios y tareas, para que la eliminación de usuarios creados en el testing se realizara correctamente

## 📌 Notas finales
- Ya que el frontend no tiene soporte visual para eliminar usuarios ni tareas. La eliminación se realiza directamente vía HTTP desde los scripts de prueba.
- Los reportes son secuenciales y no sobrescriben los anteriores.