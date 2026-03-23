import streamlit as st
import smtplib
from email.message import EmailMessage
from datetime import date
import os
import threading

# ----------------- CONFIG -----------------
st.set_page_config(page_title="Treatment")

# ----------------- DARK THEME STYLE -----------------
st.markdown("""
<style>
section[data-testid="stSidebar"] {display: none;}
button[kind="header"] {display: none;}
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stApp {background-color: #0b1f3a; color: #ffffff;}
h1, h2, h3 {color: #00c6ff; text-align: center;}

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
div.stButton > button:hover {background-color: #0077cc; color: #ffffff;}
p, span {color: #ffffff;}
.stFileUploader > div > div {background-color: #1a2a4c !important; color: #ffffff !important;}
hr {border: 1px solid #00c6ff;}
</style>
""", unsafe_allow_html=True)

# ----------------- NAVBAR -----------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🏠 Home"): st.switch_page("app.py")
with col2:
    if st.button("🫁 Pneumonia"): st.switch_page("pages/pneumonia.py")
with col3:
    if st.button("🧬 Lung Cancer"): st.switch_page("pages/lungcancer.py")
with col4:
    if st.button("💊 Treatment"): st.switch_page("pages/treatment.py")

st.markdown("---")
st.title("💊 Book Appointment")

# ----------------- FORM -----------------
name = st.text_input("Enter Name")
email = st.text_input("Enter Email")
phone = st.text_input("Enter Phone Number")
disease = st.selectbox("Select Disease", ["Pneumonia", "Lung Cancer"])

# ----------------- HOSPITAL SELECTION -----------------
hospital = None
if disease == "Pneumonia":
    hospital = st.selectbox("Select Hospital", ["Omni Hospital (10:00 AM)", "Kamineni Hospital (2:00 PM)"])
elif disease == "Lung Cancer":
    hospital = st.selectbox("Select Hospital", ["Yashoda Hospital (11:00 AM)", "Apollo Hospital (4:00 PM)"])

appointment_date = st.date_input("Select Appointment Date", min_value=date.today())
report = st.file_uploader("Upload Report (PDF)", type=["pdf"])

# ----------------- EMAIL FUNCTION -----------------
def send_email(to_email, subject, body, attachment=None):
    try:
        sender_email = os.environ.get("EMAIL_ADDRESS")
        sender_password = os.environ.get("EMAIL_PASSWORD")  # App password from Render env

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to_email
        msg.set_content(body)

        if attachment:
            msg.add_attachment(
                attachment.read(),
                maintype='application',
                subtype='pdf',
                filename=attachment.name
            )

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
    except Exception as e:
        st.error(f"Email sending failed: {e}")

# Async version to avoid blocking Streamlit UI
def send_email_async(*args, **kwargs):
    threading.Thread(target=send_email, args=args, kwargs=kwargs).start()

# ----------------- HOSPITAL EMAIL MAP -----------------
hospital_emails = {
    "Omni Hospital (10:00 AM)": "omnihospital@email.com",
    "Kamineni Hospital (2:00 PM)": "kamineni@email.com",
    "Yashoda Hospital (11:00 AM)": "yashoda@email.com",
    "Apollo Hospital (4:00 PM)": "apollo@email.com"
}

# ----------------- SUBMIT BUTTON -----------------
if st.button("Submit Appointment"):
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
            send_email_async(hospital_email, "New Patient Appointment", hospital_body, report)

            # Confirmation Email to User
            user_body = f"""
Hello {name},

Your appointment is confirmed.
Hospital: {hospital}
Date: {appointment_date}

Please carry your reports.

Thank you!
"""
            send_email_async(email, "Appointment Confirmation", user_body)

            st.success("✅ Appointment Booked & Emails Sent!")
        except Exception as e:
            st.error(f"Error: {e}")
