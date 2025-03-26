# AI-Resume-Analyzer
Users upload their resume and AI analyzes it and gives feedback on what they can improve.

## Features
- Upload any PDF resume
- Gives OpenAI to analyze the content
- Gives targeted feedback and suggestions
- Keeps your resume private

## How Tt Works
1. Drop a file into the app.
2. The app will extract the content using 'PyPDF2'.
3. The extracted content is sent to OpenAI's API.
4. You get smart suggestions to enhance your resume.

## Steps

  The first step is to set up my project using terminal. I am creating a project folder, a virtual environment, installing the required packages, and then creating a file.
  The second step is to use PyPDF2 to read resume text from a PDF. I am creating the extractor.py file and testing it out before adding AI to this.
  The third step is to add OpenAI API integration using the extract_text_from_pdf() function, which will send the resume text to OpenAI GPT 3.5, and then get back AI-powered feedback.
  The fourth step is to connect extractor.py with analyzer.py. I am going to create a script that combines both. It will use the extract_text_from_pdf() function to get the resume text. Then it will pass that text into the get_resume_feedback().
  The fifth step is to build an app with Streamlit. This will allow users to upload their resumes via their browsers, get feedback instantly from OpenAI, and make my project more interactive and shareable.
  The sixth step is to upgrade the app by adding dark mode, colors, and a download link - for a better user experience.

## Instalation Instructions
  ...

## (Visual)

## (Live Demo Link)
