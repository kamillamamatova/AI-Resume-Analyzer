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

# Load the environment variables
load_dotenv()

# Sets the title and layout
st.set_page_config(page_title = "AI Resume Analyzer", layout = "centered")

# Theme toggle
theme = st.sidebar.radio("Choose Theme", ["Dark", "Light"])

# Conditional styling based on user's choice using embedded CSS
if theme == "Dark":
    st.markdown("""
        <style>
            body{
                background-color: #0d0f14;
                color: #edf0f5
            }
            reportview-container .main .block-container{
                padding-top: 2rem;
            }
            .stButton>button{
                background-color: #ed61ca;
                color: white;
            }
            .download-button{
                background-color: #ed61ca;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                border-radius: 5px;   
                margin-top: 1rem;
                cursor: pointer; 
            }
        </style>
    """, unsafe_allow_html = True) # unsafe_allow_html is needed to render the CSS
else:
    st.markdown("""
        <style>
            body{
                background-color: #ffffff;
                color: #000000
            }
            .download-button{
                background-color: #007bff;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                border-radius: 5px;   
                margin-top: 1rem;
                cursor: pointer; 
            }
        </style>
    """, unsafe_allow_html = True)

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
    resume_text = extract_text_from_pdf("temp_resume.pdf")

    # Shows a loading animation of a spinner while the AI is working
    with st.spinner("Analyzing your resume..."):
        # Calls the function to analyze the resume and get feedback
        feedback = get_resume_feedback(resume_text)
        scores = get_resume_scores(resume_text)

    # Displays feedback and scores
    st.subheader("AI Feedback")
    st.write(feedback)

    st.subheader("Resume Score Breakdown")
    for category in ("formatting", "clarity", "relevance", "technical_skills"):
        st.write(f"{category.replace('_', ' ').capitalize()}: **{scores[category]}/100**")
        # Draws a progress bar
        st.progress(scores[category] / 100)

    st.subheader("Overall Score")
    st.write(f"Your resume score: **{scores['overall']}/100**")
    st.progress(scores['overall'] / 100)

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
    st.markdown(get_download_link(feedback, "resume_feedback.txt", "Download Feedback"), unsafe_allow_html = True)

    # Save feedback history
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"feedback_{timestamp}.txt", "w") as f:
        f.write(feedback)

    # Option to email feedback
    if email_address:
        try: 
            message = MIMEMultipart()
            message["From"] = os.getenv["EMAIL"]
            message["To"] = email_address
            message["Subject"] = "AI Resume Feedback"

            body = MIMEText(feedback, "plain")
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
    st.text_area("Copy feedback", feedback, height=200)
    st.success("You can highlight and copy the feedback above.")

    # Toast-style success message
    st.info("Feedback is ready! You can download or copy it.")

    # Compare with job description
    if job_description:
        resume_words = set(resume_text.lower().split())
        job_words = set(job_description.lower().split())
        common_words = resume_words & job_words
        match_percentage = (len(common_words) / len(job_words)) * 100 if job_words else 0
        st.subheader("Resume and Job Description Match")
        st.write(f"Your resume matches approximately **{match_percentage:.2f}%** of the job description.")