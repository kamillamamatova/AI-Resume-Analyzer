# Gives access to OpenAI's API
import openai
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

# Create OpenAI client instance
client = OpenAI()

openai.api_key = os.getenv("OPENAI_API_KEY")

# This function takes in resume text and returns feedback
# This is the core function that I'll call from other files
def get_resume_feedback(resume_text):
    # Multi-line f string - a string that that spans multiple lines and allows for string insertion using {}
    # The actual resume content will be insterted into the string
    # The triple quotes allow for multi-line strings
    prompt = f""" 
You are a professional resume analyzer. Analyze the following resume and give:
1. Feedback on formating, grammar, and clarity.
2. Suggestions on how to improve or add technical skills.
3. A summary of strengths and weaknesses.

Resume:
\"\"\"
{resume_text}
\"\"\"
"""
    # Returns the full response from the AI
    response = openai.ChatCompletion.create(
        # Tells AI to use GPT-3.5
        mode = "gpt-3.5-turbo",
        # Chat history
        messages = [{"role": "user", "content": prompt}],
        # Controls creativity of the AI (0.7 is more creative)
        tempreture = 0.7,
        # Limits how long the response can be
        max_tokens = 500
    )
    # Grabs the actual response which is nested in the choices key
    return response.choices[0].message.content