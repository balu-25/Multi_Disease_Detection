import streamlit as st
from PIL import Image
from utils.predict import predict_image, lung_model, lung_classes
from utils.report import generate_pdf

st.set_page_config(page_title="Lung Cancer")

# -------- DARK THEME STYLE & NAVBAR --------
st.markdown("""
    <style>
    /* Hide sidebar and menu */
    section[data-testid="stSidebar"] {display: none;}
    button[kind="header"] {display: none;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* App background */
    .stApp {
        background-color: #0b1f3a;
        color: #ffffff;
    }

    /* Headings */
    h1, h2, h3 {
        color: #00c6ff;
        text-align: center;
    }

    /* Navbar buttons */
    div.stButton > button {
        background-color: #00509e;
        color: #ffffff;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #0077cc;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# -------- NAVBAR --------
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🏠 Home"):
        st.switch_page("app.py")

with col2:
    if st.button("🫁 Pneumonia"):
        st.switch_page("pages/pneumonia.py")

with col3:
    if st.button("🧬 Lung Cancer"):
        st.switch_page("pages/lungcancer.py")

with col4:
    if st.button("💊 Treatment"):
        st.switch_page("pages/treatment.py")

st.markdown("---")
st.title("🧬 Lung Cancer Detection")

# -------- FILE UPLOADER & PREDICTION --------
file = st.file_uploader("Upload CT Scan", type=["jpg", "png", "jpeg"])

if file:
    img = Image.open(file)
    st.image(img, use_container_width=True)

    with st.spinner("Analyzing..."):
        label, conf, out_img = predict_image(lung_model, img, lung_classes)

    st.success(f"Prediction: {label}")
    st.info(f"Confidence: {conf:.2%}")
    st.progress(int(conf * 100))

    st.image(out_img, use_container_width=True)

    if st.button("Download Report"):
        pdf_bytes = generate_pdf(img, out_img, label, conf)

        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name="medical_report.pdf",
            mime="application/pdf"
        )
