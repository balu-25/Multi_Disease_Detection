import streamlit as st
import numpy as np
import cv2
from PIL import Image
import tempfile
from utils.predict import predict_pneumonia, predict_lung, annotate_image
from utils.report import create_report

st.set_page_config(page_title="Medical AI System", layout="centered")

# Navigation
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to(page):
    st.session_state.page = page

# ---------------- HOME ----------------
if st.session_state.page == "home":
    st.title("🩺 Medical AI Diagnosis System")

    st.button("Pneumonia Detection", on_click=go_to, args=("pneumonia",))
    st.button("Lung Cancer Detection", on_click=go_to, args=("lung",))
    st.button("Treatment Recommendation", on_click=go_to, args=("treatment",))


# ---------------- PNEUMONIA ----------------
elif st.session_state.page == "pneumonia":
    st.title("Pneumonia Detection")

    file = st.file_uploader("Upload Chest X-ray", type=["jpg", "png", "jpeg"])

    if file:
        image = Image.open(file)
        img_np = np.array(image)

        label, confidence = predict_pneumonia(img_np)
        annotated = annotate_image(img_np, label)

        st.image(image, caption="Uploaded Image")
        st.image(annotated, caption="Prediction")

        st.success(f"Prediction: {label} ({confidence:.2f})")

        # Save temp images
        input_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name

        cv2.imwrite(input_path, img_np)
        cv2.imwrite(output_path, annotated)

        if st.button("Download Report"):
            pdf = create_report(input_path, output_path, label, confidence)
            with open(pdf, "rb") as f:
                st.download_button("Download PDF", f, file_name="report.pdf")

    st.button("Back", on_click=go_to, args=("home",))


# ---------------- LUNG ----------------
elif st.session_state.page == "lung":
    st.title("Lung Cancer Detection")

    file = st.file_uploader("Upload CT Scan", type=["jpg", "png", "jpeg"])

    if file:
        image = Image.open(file)
        img_np = np.array(image)

        label, confidence = predict_lung(img_np)
        annotated = annotate_image(img_np, label)

        st.image(image)
        st.image(annotated)

        st.success(f"Prediction: {label} ({confidence:.2f})")

        input_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name
        output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name

        cv2.imwrite(input_path, img_np)
        cv2.imwrite(output_path, annotated)

        if st.button("Download Report"):
            pdf = create_report(input_path, output_path, label, confidence)
            with open(pdf, "rb") as f:
                st.download_button("Download PDF", f, file_name="report.pdf")

    st.button("Back", on_click=go_to, args=("home",))


# ---------------- TREATMENT ----------------
elif st.session_state.page == "treatment":
    st.title("Treatment Recommendation")

    name = st.text_input("Name")
    email = st.text_input("Email")
    disease = st.selectbox("Select Disease", ["Pneumonia", "Lung Cancer"])

    if st.button("Submit"):
        st.success("Recommendation sent (we can integrate hospital logic next)")

    st.button("Back", on_click=go_to, args=("home",))