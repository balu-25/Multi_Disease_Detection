from fpdf import FPDF
import tempfile
from datetime import datetime

class StyledPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 18)
        self.set_text_color(0, 102, 204)
        self.cell(0, 10, "AI Medical Diagnosis Report", ln=True, align="C")

        self.ln(3)
        self.set_draw_color(0, 102, 204)
        self.set_line_width(0.5)
        self.line(10, 22, 200, 22)
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(120)
        self.cell(
            0, 10,
            f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            align="C"
        )


def generate_pdf(user_image, pred_image, label, confidence):
    pdf = StyledPDF()
    pdf.add_page()

    # ===== Prediction Section =====
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "Prediction Summary", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.ln(2)

    # Highlight box
    pdf.set_fill_color(230, 240, 255)
    pdf.cell(0, 10, f"Prediction: {label}", ln=True, fill=True)
    pdf.cell(0, 10, f"Confidence: {confidence*100:.2f}%", ln=True, fill=True)

    pdf.ln(8)

    # ===== Image Section =====
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Image Analysis", ln=True)

    pdf.ln(5)

    # Convert images
    user_image = user_image.convert("RGB")
    pred_image = pred_image.convert("RGB")

    temp1 = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    temp2 = tempfile.NamedTemporaryFile(delete=False, suffix=".png")

    user_image.save(temp1.name, format="PNG")
    pred_image.save(temp2.name, format="PNG")

    # ===== Input Image =====
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Input Image", ln=True, align="C")

    pdf.image(temp1.name, x=30, w=150)  # centered wide image

    pdf.ln(10)

    # ===== Predicted Image =====
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Predicted Image", ln=True, align="C")

    pdf.image(temp2.name, x=30, w=150)

    pdf.ln(10)

    # ===== Notes Section =====
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Medical Note", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(
        0, 8,
        "This report is generated using an AI-based diagnostic system. "
        "You can download this report for your records. Please consult a healthcare professional for a comprehensive diagnosis and treatment plan based on these results."
        "Go to treatment recommendations for more information."
    )

    pdf.ln(5)

    # ===== Signature Section =====
    pdf.set_font("Arial", "I", 11)
    pdf.cell(0, 10, "Authorized by: AI Diagnostic System", ln=True, align="R")

    # ===== Return as bytes =====
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_bytes
