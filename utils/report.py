from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

def create_report(input_img, output_img, label, confidence):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    doc = SimpleDocTemplate(temp_file.name)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("Medical Diagnosis Report", styles['Title']))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"Prediction: {label}", styles['Normal']))
    elements.append(Paragraph(f"Confidence: {confidence:.2f}", styles['Normal']))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Input Image:", styles['Heading2']))
    elements.append(Image(input_img, width=200, height=200))

    elements.append(Paragraph("Annotated Image:", styles['Heading2']))
    elements.append(Image(output_img, width=200, height=200))

    doc.build(elements)

    return temp_file.name