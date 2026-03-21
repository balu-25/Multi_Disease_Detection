from fpdf import FPDF
import tempfile

def generate_pdf(user_image, pred_image, label, confidence):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Medical Diagnosis Report", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Prediction: {label}", ln=True)
    pdf.cell(200, 10, txt=f"Confidence: {confidence:.2f}", ln=True)

    # Save temp images
    temp1 = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    temp2 = tempfile.NamedTemporaryFile(delete=False, suffix=".png")

    user_image.save(temp1.name)
    pred_image.save(temp2.name)

    pdf.ln(10)
    pdf.image(temp1.name, x=10, w=80)
    pdf.image(temp2.name, x=110, w=80)

    pdf_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    pdf.output(pdf_path)

    return pdf_path