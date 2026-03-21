import streamlit as st
from PIL import Image
from utils.predict import predict_image, pneumonia_model, lung_model, pneumonia_classes, lung_classes
from utils.report import generate_pdf

st.set_page_config(page_title="AI Healthcare System", layout="centered")

# Navigation
st.title("🩺 AI Healthcare Diagnosis System")

menu = st.radio("Select Option", ["Home", "Pneumonia", "Lung Cancer", "Treatment Recommendation"])

# ---------------- HOME ----------------
if menu == "Home":
    st.subheader("Welcome")
    st.write("Select a module from above")

# ---------------- PNEUMONIA ----------------
elif menu == "Pneumonia":
    st.header("Pneumonia Detection")

    file = st.file_uploader("Upload Chest X-ray", type=["jpg", "png", "jpeg"])

    if file:
        img = Image.open(file)

        st.image(img, caption="Uploaded Image")

        label, conf, out_img = predict_image(pneumonia_model, img, pneumonia_classes)

        st.success(f"Prediction: {label}")
        st.info(f"Confidence: {conf:.2f}")

        st.image(out_img, caption="Output Image")

        if st.button("Download Report"):
            pdf = generate_pdf(img, out_img, label, conf)

            with open(pdf, "rb") as f:
                st.download_button("Download PDF", f, file_name="report.pdf")

# ---------------- LUNG CANCER ----------------
elif menu == "Lung Cancer":
    st.header("Lung Cancer Detection")

    file = st.file_uploader("Upload CT Scan", type=["jpg", "png", "jpeg"])

    if file:
        img = Image.open(file)

        st.image(img, caption="Uploaded Image")

        label, conf, out_img = predict_image(lung_model, img, lung_classes)

        st.success(f"Prediction: {label}")
        st.info(f"Confidence: {conf:.2f}")

        st.image(out_img, caption="Output Image")

        if st.button("Download Report"):
            pdf = generate_pdf(img, out_img, label, conf)

            with open(pdf, "rb") as f:
                st.download_button("Download PDF", f, file_name="report.pdf")

# ---------------- TREATMENT ----------------
elif menu == "Treatment Recommendation":
    st.header("Treatment Recommendation")

    disease = st.selectbox("Select Disease", ["Pneumonia", "Lung Cancer"])

    if disease == "Pneumonia":
        st.write("• Antibiotics (for bacterial)")
        st.write("• Rest and hydration")
        st.write("• Oxygen therapy (severe cases)")

    elif disease == "Lung Cancer":
        st.write("• Surgery")
        st.write("• Chemotherapy")
        st.write("• Radiation therapy")