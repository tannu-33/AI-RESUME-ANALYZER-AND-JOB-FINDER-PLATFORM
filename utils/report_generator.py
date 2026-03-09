from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
import os


def generate_report(data, filename="outputs/report.pdf"):
    doc = SimpleDocTemplate(filename)
    elements = []

    styles = getSampleStyleSheet()

    elements.append(Paragraph("Resume Analysis Report", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    for key, value in data.items():
        elements.append(Paragraph(f"<b>{key}</b>: {value}", styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)

    return filename