import streamlit as st
import PyPDF2
import google.generativeai as genai

st.title("🧠 AI Resume Analyzer")

api_key = st.text_input("Enter Gemini API Key", type="password")

uploaded_file = st.file_uploader("Upload Resume PDF", type="pdf")

job_description = st.text_area("Paste Job Description")

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


if st.button("Analyze Resume"):

    if not api_key:
        st.warning("Please enter Gemini API key")
    
    elif not uploaded_file:
        st.warning("Please upload resume")
    
    elif not job_description:
        st.warning("Please paste job description")

    else:

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-1.5-flash-latest")

        resume_text = extract_text_from_pdf(uploaded_file)

        prompt = f"""
        You are an HR recruiter.

        Compare the following resume with the job description.

        Resume:
        {resume_text}

        Job Description:
        {job_description}

        Provide:
        1. Match score out of 100
        2. Matching skills
        3. Missing skills
        4. HR recommendation
        """

        with st.spinner("Analyzing resume..."):
            response = model.generate_content(prompt)

        st.subheader("📊 Analysis Result")
        st.write(response.text)
