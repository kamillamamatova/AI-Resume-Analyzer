# Imports the function that extracts text from PDFs
from extractor import extract_text_from_pdf
# Imports thet function that analyzes resumes using OpenAI
from analyzer import get_resume_feedback

# 1. Extracts text from a PDF

# Defines the path to the PDF
pdf_path = "sample_resume.pdf"
# Calls the function to extract text from the PDF
resume_text = extract_text_from_pdf(pdf_path)

# 2. Get feedback from OpenAI

# Calls the function to analyze the resume and get feedback
feedback = get_resume_feedback(resume_text)

# 3. Prints the feedback
print("\nFeedback:")
print(feedback)
