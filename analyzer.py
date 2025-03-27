from openai import OpenAI
from dotenv import load_dotenv
import os
# JavaScript Object Notation
# Lightweight format for storing and transporting data
import json

load_dotenv()

# Create OpenAI client instance
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# This function takes in resume text and returns feedback
# This is the core function that I'll call from other files
def get_resume_feedback(resume_text):
    # Multi-line f string - a string that that spans multiple lines and allows for string insertion using {}
    # The actual resume content will be insterted into the string
    # The triple quotes allow for multi-line strings
    prompt = f"""
You are a professional resume analyzer. Analyze the following resume and give:
1. Feedback on formatting, grammar, and clarity.
2. Suggestions on how to improve or add technical skills.
3. A summary of strengths and weaknesses.

Resume:
"""
    prompt += resume_text
    prompt += """
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content

def get_resume_scores(resume_text):
    prompt = f"""
You are a resume expert. Given the following resume:
"""
    prompt += resume_text
    prompt += """

Please give detailed ratings from 0 to 100 for:
- Formatting
- Clarity
- Relevance to Industry
- Technical Skills
- Overall quality

Return a JSON object like this:
{"formatting": 88, "clarity": 92, "relevance": 85, "technical_skills": 90, "overall": 87}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200
        )
        return json.loads(response.choices[0].message.content.strip())
    except:
        return {"formatting": 70, "clarity": 70, "relevance": 70, "technical_skills": 70, "overall": 70}
