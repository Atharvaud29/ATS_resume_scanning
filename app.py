import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configure the generative AI library with your API key from the environment
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Custom CSS to improve the app styling
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f9;
    }
    .title {
        text-align: center;
        color: #4a90e2;
        font-size: 48px;
        font-weight: bold;
    }
    .subtitle {
        text-align: center;
        color: #555;
        font-size: 24px;
        margin-bottom: 30px;
    }
    .markdown-text {
        font-size: 16px;
        line-height: 1.6;
    }
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #357ab7;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to get the response from the Gemini model
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(input_text)
    return response.text

# Function to extract text from an uploaded PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    # Loop through each page of the PDF
    for page in range(len(reader.pages)):
        page_obj = reader.pages[page]
        text += str(page_obj.extract_text())
    return text

# Prompt Template with placeholders for resume text and job description
input_prompt = """
Hey, act like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of tech fields such as Software Engineering, Data Science, Data Analysis,
Big Data Engineering, Machine Learning Engineer, MLops Engineer and Data Scientist. Your task is to evaluate the resume based on the given job description.
Consider that the job market is very competitive and provide the best assistance for improving the resumes.
Assign the percentage matching based on the JD and identify the missing keywords with high accuracy.
**Resume:** 
{text}

**Job Description:** 
{jd}

Please provide the response as one single string with the following structure:
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
"""

# Page Header with Markdown
st.markdown("<div class='title'>Smart ATS</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Improve Your Resume with Intelligent Analysis</div>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="markdown-text">
    <p>Welcome! This tool helps you evaluate your resume against a job description using a state-of-the-art generative AI model.</p>
    <ul>
        <li>Paste the job description in the text area below.</li>
        <li>Upload your resume in PDF format.</li>
        <li>Click the **Submit** button to receive your ATS analysis.</li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# Input fields for job description and resume upload
jd = st.text_area("Paste the Job Description", height=150)
uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", help="Please upload the PDF version of your resume.")

# Submit button
submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        resume_text = input_pdf_text(uploaded_file)
        formatted_prompt = input_prompt.format(text=resume_text, jd=jd)
        response = get_gemini_response(formatted_prompt)
        st.markdown("### ATS Analysis")
        st.markdown(f"<div class='markdown-text'>{response}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please upload a resume in PDF format.")
