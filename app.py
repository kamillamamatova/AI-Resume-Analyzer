# Library that builds the web interface
import streamlit as st
# Imports the function that extracts text from PDFs
from extractor import extract_text_from_pdf
# Imports the function that analyzes resumes using OpenAI
from analyzer import get_resume_feedback, get_resume_scores
# Imports base64 so I can create downloadable files later
import base64
# Imports environment variables
import os
# Imports .env file variales
from dotenv import load_dotenv
# Timestamping saved feedback
import datetime
# Sending emails
import smtplib
# Formatting email
from email.mime.text import MIMEText
# Allows attachments
from email.mime.multipart import MIMEMultipart
# Allows plots
import matplotlib.pyplot as plt
# Spreadsheets
import pandas as pd

# Load the environment variables
load_dotenv()

# Sets the title and layout
st.set_page_config(page_title = "AI Resume Analyzer", layout = "centered")

# Initialize session state variables
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "scores" not in st.session_state:
    st.session_state.scores = None
if "resume_text" not in st.session_state:
    st.session_state.resume_text = None

# Displays the title of the web app
st.title("📄 AI Resume Analyzer")
# Displays a short description of the web app
st.write("This app allows you to upload a resume and get feedback using OpenAI's GPT-3.5 model.")

# Creates a file uploader widget in the UI
# Only PDF files are allowed
uploaded_file = st.file_uploader("Upload your PDF resume", type = "pdf")

# Text input for optional job description comparison
job_description = st.text_area("Paste Job Description (optional for comparison)", height=150)

# Text input for optional email address
email_address = st.text_input("Enter your email address (optional)")

# Only runs if the user has uploaded a file
if uploaded_file:
    # Saves the uploaded file to the local machinery as "temp_resume.pdf"
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())
    # Calls the function to extract text from the PDF
    st.session_state.resume_text = extract_text_from_pdf("temp_resume.pdf")

if uploaded_file and (st.session_state.feedback is None or st.session_state.scores is None):
    # Shows a loading animation of a spinner while the AI is working
    with st.spinner("Analyzing your resume..."):
        try:
            # Calls the function to analyze the resume and get feedback
            feedback = get_resume_feedback(st.session_state.resume_text)
            scores = get_resume_scores(st.session_state.resume_text)
            st.session_state.feedback = feedback
            st.session_state.scores = scores
        except:
            st.error("Failed to analyze the resume. Please check your OpenAI and quota.")
            st.stop()
    
# Only displays results if the analysis is successful
if st.session_state.feedback and st.session_state.scores:
    # Displays feedback and scores
    st.subheader("AI Feedback")
    st.write(st.session_state.feedback)

    st.subheader("Resume Score Breakdown")
    categories = ["formatting", "clarity", "relevance", "technical_skills"]
    values = [st.session_state.scores.get(c, 70) for c in categories]

    for category, val in zip(categories, values):
        st.write(f"{category.replace('_', ' ').capitalize()}: **{val}/100**")
        # Draws a progress bar
        st.progress(val / 100)

    st.subheader("Overall Score")
    st.write(f"Your resume score: **{st.session_state.scores.get('overall', 70)}/100**")
    st.progress(st.session_state.scores.get("overall", 70) / 100)

    # Add bar chart
    st.subheader("Visual Breakdown (Bar Chart)")
    chart_data = pd.DataFrame({"Category": categories, "Score": values})
    st.bar_chart(chart_data.set_index("Category"))

    # Add line chart
    st.subheader("Visual Breakdown (Line Chart)")
    st.line_chart(chart_data.set_index("Category"))

    # A helper function that creates a download link for the feedback
    def get_download_link(text, filename, label):
        # Convert text to base64
        b64 = base64.b64encode(text.encode()).decode()
        # A donwload link (HTML)
        button_html = f'''
            <a href="data:file/txt;base64,{b64}" download="{filename}">
                <button class="download-button">{label}</button>
            </a>
        '''
        return button_html
    
    # Display the download link
    st.markdown(get_download_link(st.session_state.feedback, "resume_feedback.txt", "Download Feedback"), unsafe_allow_html = True)

    # Save feedback history
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"feedback_{timestamp}.txt", "w") as f:
        f.write(st.session_state.feedback)

    # Option to email feedback
    if email_address:
        try: 
            message = MIMEMultipart()
            message["From"] = os.getenv["EMAIL"]
            message["To"] = email_address
            message["Subject"] = "AI Resume Feedback"

            body = MIMEText(st.session_state.feedback, "plain")
            message.attach(body)

            # Simple Mail Transfer Protocol
            # 587 is the port number
            server = smtplib.SMTP("smtp.gmail.com", 587)
            # Upgrades the connection to use TLS encryption, which keeps the email and login credintials secure during transmission
            server.starttls()
            # Logs in to the email server
            server.login(os.getenv("EMAIL"), os.getenv("EMAIL_PASSWORD"))
            # Sends the email
            server.send_message(message)
            # Quits the server
            server.quit()
            # Shows a success message in the Streamlit app
            st.success("Feedback sent to your email!")
        # If any error , show an error message
        except Exception as e:
            st.error("Failed to send email. Check credentials.")

    # Copy to clipboard button
    st.text_area("Copy feedback", st.session_state.feedback, height=200)
    st.success("You can highlight and copy the feedback above.")

    # Toast-style success message
    st.info("Feedback is ready! You can download or copy it.")

    # Compare with job description
    if job_description:
        resume_words = set(st.session_state.resume_text.lower().split())
        job_words = set(job_description.lower().split())
        common_words = resume_words & job_words
        match_percentage = (len(common_words) / len(job_words)) * 100 if job_words else 0
        st.subheader("Resume and Job Description Match")
        st.write(f"Your resume matches approximately **{match_percentage:.2f}%** of the job description.")

# Reset button to clear session state
tooltip = "Click to clear the uploaded resume and feedback"
if st.button("Reset App", help = tooltip):
    st.session_state.feedback = None
    st.session_state.scores = None
    st.session_state.resume_text = ""
    st.rerun()