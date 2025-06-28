# import os
# from datetime import datetime
# from fpdf import FPDF
# import unicodedata

# def generate_pdf_report(test_name, test_results, screenshots=None):
#     """
#     Genera un reporte PDF con numeración secuencial
    
#     Args:
#         test_name (str): Nombre de la prueba
#         test_results (list): Lista de tuplas (mensaje, éxito)
#         screenshots (list): Rutas de capturas de pantalla (opcional)
#     """
#     # Crear carpeta de reportes si no existe
#     report_dir = "test_reports"
#     os.makedirs(report_dir, exist_ok=True)
    
#     # Determinar el siguiente número de secuencia
#     existing_reports = [f for f in os.listdir(report_dir) if f.startswith("report_") and f.endswith(".pdf")]
#     next_num = max([int(f.split('_')[1].split('.')[0]) for f in existing_reports] or [0]) + 1
    
#     # Configurar PDF
#     pdf = FPDF()
#     pdf.add_page()
    
#     # Usar fuente compatible con Unicode
#     pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
#     pdf.set_font('DejaVu', '', 12)
    
#     # Encabezado
#     pdf.set_font('DejaVu', 'B', 16)
#     pdf.cell(200, 10, txt=f"Reporte de Prueba: {test_name}", ln=1, align='C')
#     pdf.set_font('DejaVu', '', 12)
#     pdf.cell(200, 10, txt=f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=1)
#     pdf.cell(200, 10, txt=f"Número de Reporte: {next_num}", ln=1)
#     pdf.ln(10)
    
#     # Resultados de la prueba
#     pdf.set_font('DejaVu', 'B', 14)
#     pdf.cell(200, 10, txt="Resultados de la Prueba:", ln=1)
#     pdf.set_font('DejaVu', '', 12)
    
#     for result, success in test_results:
#         color = (0, 128, 0) if success else (255, 0, 0)  # Verde para éxito, rojo para fallo
#         pdf.set_text_color(*color)
        
#         # Normalizar texto y reemplazar caracteres problemáticos
#         clean_text = unicodedata.normalize('NFKD', result).encode('latin-1', 'ignore').decode('latin-1')
#         pdf.cell(200, 10, txt=f"- {clean_text}", ln=1)
    
#     pdf.set_text_color(0, 0, 0)  # Volver a color negro
    
#     # Agregar capturas de pantalla si existen
#     if screenshots:
#         pdf.ln(10)
#         pdf.set_font('DejaVu', 'B', 14)
#         pdf.cell(200, 10, txt="Capturas de Pantalla:", ln=1)
#         pdf.set_font('DejaVu', '', 12)
        
#         for idx, screenshot in enumerate(screenshots, 1):
#             if os.path.exists(screenshot):
#                 pdf.add_page()
#                 pdf.cell(200, 10, txt=f"Captura {idx}:", ln=1)
#                 pdf.image(screenshot, x=10, y=30, w=180)
    
#     # Guardar reporte
#     filename = os.path.join(report_dir, f"report_{next_num}.pdf")
#     pdf.output(filename)
#     return filename


import os
from datetime import datetime
from fpdf import FPDF
import unicodedata
import re

def clean_text_for_pdf(text):
    """Limpia el texto para hacerlo compatible con PDF"""
    # Reemplazar emojis con texto descriptivo
    text = text.replace("✅", "[SUCCESS] ")
    text = text.replace("❌", "[ERROR] ")
    text = text.replace("⚠️", "[WARNING] ")
    
    # Reemplazar bullet points con guiones
    text = text.replace("•", "-")
    
    # Normalizar caracteres Unicode
    text = unicodedata.normalize('NFKD', text).encode('latin-1', 'ignore').decode('latin-1')
    
    # Eliminar caracteres no imprimibles
    text = re.sub(r'[^\x00-\x7F]', '', text)
    
    return text

def generate_pdf_report(test_name, test_results, screenshots=None):
    """
    Genera un reporte PDF con numeración secuencial
    
    Args:
        test_name (str): Nombre de la prueba
        test_results (list): Lista de tuplas (mensaje, éxito)
        screenshots (list): Rutas de capturas de pantalla (opcional)
    """
    # Crear carpeta de reportes si no existe
    report_dir = "test_reports"
    os.makedirs(report_dir, exist_ok=True)
    
    # Determinar el siguiente número de secuencia
    existing_reports = [f for f in os.listdir(report_dir) if f.startswith("report_") and f.endswith(".pdf")]
    next_num = max([int(f.split('_')[1].split('.')[0]) for f in existing_reports] or [0]) + 1
    
    # Configurar PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Usar fuente estándar que soporta mejor los caracteres
    pdf.set_font("Arial", size=12)
    
    # Encabezado
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=clean_text_for_pdf(f"Reporte de Prueba: {test_name}"), ln=1, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=clean_text_for_pdf(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"), ln=1)
    pdf.cell(200, 10, txt=clean_text_for_pdf(f"Número de Reporte: {next_num}"), ln=1)
    pdf.ln(10)
    
    # Resultados de la prueba
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=clean_text_for_pdf("Resultados de la Prueba:"), ln=1)
    pdf.set_font("Arial", size=12)
    
    for result, success in test_results:
        color = (0, 128, 0) if success else (255, 0, 0)  # Verde para éxito, rojo para fallo
        pdf.set_text_color(*color)
        
        # Limpiar el texto para PDF
        clean_text = clean_text_for_pdf(result)
        pdf.cell(200, 10, txt=f"- {clean_text}", ln=1)
    
    pdf.set_text_color(0, 0, 0)  # Volver a color negro
    
    # Agregar capturas de pantalla si existen
    if screenshots:
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt=clean_text_for_pdf("Capturas de Pantalla:"), ln=1)
        pdf.set_font("Arial", size=12)
        
        for idx, screenshot in enumerate(screenshots, 1):
            if os.path.exists(screenshot):
                pdf.add_page()
                pdf.cell(200, 10, txt=clean_text_for_pdf(f"Captura {idx}:"), ln=1)
                pdf.image(screenshot, x=10, y=30, w=180)
    
    # Guardar reporte
    filename = os.path.join(report_dir, f"report_{next_num}.pdf")
    pdf.output(filename)
    return filename