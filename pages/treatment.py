import streamlit as st
import yagmail
import tempfile
from datetime import date

st.set_page_config(page_title="Treatment")

# -------- DARK THEME STYLE --------
st.markdown("""
    <style>
    section[data-testid="stSidebar"] {display: none;}
    button[kind="header"] {display: none;}
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .stApp {
        background-color: #0b1f3a;
        color: #ffffff;
    }

    h1, h2, h3 {
        color: #00c6ff;
        text-align: center;
    }

    div.stTextInput > label, 
    div.stTextInput > div > input,
    div.stSelectbox > label, 
    div.stSelectbox > div > div > div,
    div.stDateInput > label,
    div.stDateInput > div > div > input,
    div.stFileUploader > label,
    div.stFileUploader > div > div > input {
        color: #ffffff;
        background-color: #1a2a4c;
    }

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
    }

    p, span {
        color: #ffffff;
    }

    .stFileUploader > div > div {
        background-color: #1a2a4c !important;
    }

    hr {
        border: 1px solid #00c6ff;
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
st.title("💊 Book Appointment")

# -------- EMAIL FUNCTION (YAGMAIL) --------
def send_email(to_email, subject, body, attachment=None):
    sender_email = "pramidibalu25@gmail.com"
    sender_password = "fxjjvgkqupszcxqh"  # App Password

    try:
        yag = yagmail.SMTP(user=sender_email, password=sender_password)

        if attachment:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(attachment.read())
                tmp_path = tmp.name

            yag.send(
                to=to_email,
                subject=subject,
                contents=body,
                attachments=tmp_path
            )
        else:
            yag.send(
                to=to_email,
                subject=subject,
                contents=body
            )

    except Exception as e:
        st.error("❌ Email sending failed")
        st.text(str(e))
        raise e

# -------- HOSPITAL EMAIL MAP --------
hospital_emails = {
    "Omni Hospital (10:00 AM)": "omnihospital@email.com",
    "Kamineni Hospital (2:00 PM)": "kamineni@email.com",
    "Yashoda Hospital (11:00 AM)": "yashoda@email.com",
    "Apollo Hospital (4:00 PM)": "apollo@email.com"
}

# -------- FORM --------
with st.form("appointment_form"):

    name = st.text_input("Enter Name")
    email = st.text_input("Enter Email")
    phone = st.text_input("Enter Phone Number")

    disease = st.selectbox("Select Disease", ["Pneumonia", "Lung Cancer"])

    if disease == "Pneumonia":
        hospital = st.selectbox(
            "Select Hospital",
            ["Omni Hospital (10:00 AM)", "Kamineni Hospital (2:00 PM)"]
        )
    else:
        hospital = st.selectbox(
            "Select Hospital",
            ["Yashoda Hospital (11:00 AM)", "Apollo Hospital (4:00 PM)"]
        )

    appointment_date = st.date_input("Select Appointment Date", min_value=date.today())
    report = st.file_uploader("Upload Report (PDF)", type=["pdf"])

    submit = st.form_submit_button("Submit Appointment")

# -------- SUBMIT LOGIC --------
if submit:
    if not name or not email or not phone or not hospital:
        st.error("Please fill all details")

    else:
        try:
            hospital_email = hospital_emails[hospital]

            # Email to Hospital
            hospital_body = f"""
New Appointment Request

Name: {name}
Email: {email}
Phone: {phone}
Disease: {disease}
Hospital: {hospital}
Date: {appointment_date}
"""
            send_email(hospital_email, "New Patient Appointment", hospital_body, report)

            # Email to User
            user_body = f"""
Hello {name},

Your appointment is confirmed.

Hospital: {hospital}
Date: {appointment_date}

Please carry your reports.

Thank you!
"""
            send_email(email, "Appointment Confirmation", user_body)

            st.success("✅ Appointment Booked & Emails Sent!")

        except Exception as e:
            st.error(f"Error: {e}")
