## This project will help you to make ATS system friendly resume.

# Overview :

This project helps users create an ATS (Applicant Tracking System) friendly resume. Many companies use ATS software to filter job applications before they reach recruiters. By optimizing your resume for ATS, you can improve your chances of getting noticed by potential employers.

# Features :

--> Generates ATS-compatible resumes.

--> Provides formatting tips to improve ATS readability.

--> Ensures proper keyword optimization for job applications.

--> Supports multiple resume templates.

# Project Understanding :

*Step-1* = First create your google api key 

    GOOGLE_API_KEY = " your api key "

*Step-2* = Install all the required library's

    streamlit
    PyPDF2
    google.generativeai
    python-dotenv

*Step-3* = Write the code in *app.py* file

    import streamlit as st
    import google.generativeai as genai
    import os
    import PyPDF2 as pdf
    from dotenv import load_dotenv

    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    # Custom CSS to improve the app styling
    st.markdown("""  your markdown  """)

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

    input_propmt = """ Your propmt  """ 

    # Build your Streamlit ui
    # Input fields for job description and resume upload
    jd = st.text_area("Paste the Job Description", height=150)
    uploaded_file = st.file_uploader("Upload Your Resume (PDF)", type="pdf", help="Please upload 
    the PDF version of your resume.")

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

*Step-4* = Run the *app.py* file in terminal

    streamlit run app.py

# Output :

# Usage :

--> Enter your resume details in the provided input fields.

--> Select the best format based on your industry and job role.

--> Download and submit your resume to job portals.
    

    

    


        

    

    

    
