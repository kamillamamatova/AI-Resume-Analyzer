# ✮ AI Resume Analyzer ✮

An intelligent resume review app that uses OpenAI's GPT-3.5 to give you actionable feedback on your resume. Upload your PDF resume and get personalized suggestions in seconds.

---

## Features

- Upload your resume in PDF format
- AI-powered feedback from OpenAI GPT-3.5
- Suggestions on formatting, clarity, and technical skills
- Light and dark mode options
- Downloadable feedback or send it via email

---

## How It Works

1. Drop a PDF file into the app.
2. The app will extract the content using 'PyPDF2'.
3. The extracted content is sent to OpenAI's API.
4. Feedback is generated — including improvement tips and a numeric score
5. (Optional) You can download the feedback or email it to yourself

---

## Project Setup Steps

### ① Project Initialization
- Create project folder
- Set up a virtual environment
- Install dependencies via `pip install -r requirements.txt`

### ② PDF Extraction
- Built `extractor.py` using `PyPDF2`
- Verified accurate text extraction from sample resumes

### ③ AI Integration
- Added OpenAI integration with GPT-3.5 using the `openai` library
- Wrote `analyzer.py` to generate smart resume feedback

### ④ Feature Integration
- Combined `extractor.py` + `analyzer.py`
- Unified workflow to extract and analyze resume text in a single flow

### ⑤ Frontend with Streamlit
- Created `app.py` for the user interface
- Added file upload, real-time feedback, and download options

### ⑥ Final Enhancements
- Added dark mode + theming
- Integrated resume scoring and email feedback features

---

## Instalation Instructions
'''bash
# Clone the repository
https://github.com/kamillamamatova/AI-Resume-Analyzer.git

cd AI-Resume-Analyzer

# Create and activate a virtual environment
python -m venv env
source env/bin/activate # On Windows: env/Scripts/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.p
'''

---

## (Visual)

## (Live Demo Link)

## © Author & Credits
Created and maintained by **Kamilla Mamatova**  
If you found this helpful, feel free to star the repo and share!

---
