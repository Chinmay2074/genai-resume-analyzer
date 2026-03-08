import streamlit as st
import PyPDF2
import google.generativeai as genai

st.title("AI Resume Analyzer")

api_key = st.text_input("AIzaSyCGVqPHkyEjv3SI1KGBBs9FFh7s-HRZkKI")

uploaded_file = st.file_uploader("Upload Resume PDF", type="pdf")

job_description = st.text_area("Paste Job Description")

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

if st.button("Analyze Resume"):

    if api_key and uploaded_file and job_description:

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-pro")

        resume_text = extract_text_from_pdf(uploaded_file)

        prompt = f"""
        Analyze the resume against the job description.

        Resume:
        {resume_text}

        Job Description:
        {job_description}

        Give:
        1. Match Score
        2. Key Skills
        3. Missing Skills
        4. Suggestions
        """

        response = model.generate_content(prompt)

        st.subheader("AI Analysis")
        st.write(response.text)

    else:
        st.warning("Please upload resume, job description and API key")
