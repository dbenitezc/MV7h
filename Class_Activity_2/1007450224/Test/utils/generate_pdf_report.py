
from fpdf import FPDF
import os

def generate_pdf_report(test_results):
    reports_dir = os.path.join(os.path.dirname(__file__), "../reports")
    os.makedirs(reports_dir, exist_ok=True)

    existing = [f for f in os.listdir(reports_dir) if f.endswith(".pdf")]
    next_number = len(existing) + 1
    filename = os.path.join(reports_dir, f"test_report_{next_number:03}.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Test Results Report", ln=True, align='C')
    pdf.ln(10)

    for line in test_results:
        pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(filename)
