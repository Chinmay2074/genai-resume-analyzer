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
        extracted = page.extract_text()
        if extracted:
            text += extracted
    return text

if st.button("Analyze Resume"):

    if api_key and uploaded_file and job_description:

        try:
            genai.configure(api_key=api_key)

            # Multiple model names try karo (library version ke hisaab se)
            model = None
            for name in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]:
                try:
                    model = genai.GenerativeModel(name)
                    break
                except Exception:
                    continue

            resume_text = extract_text_from_pdf(uploaded_file)

            if not resume_text.strip():
                st.error("Resume se text extract nahi hua. Please check your PDF.")
            else:
                prompt = f"""
                Analyze the resume against the job description and provide a detailed report.

                Resume:
                {resume_text}

                Job Description:
                {job_description}

                Give:
                1. Match Score (out of 100)
                2. Key Matching Skills
                3. Missing Skills
                4. Improvement Suggestions
                """

                with st.spinner("Analyzing your resume..."):
                    response = model.generate_content(prompt)

                st.subheader("📊 AI Analysis")
                st.write(response.text)

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("💡 Fix karo: Terminal mein yeh run karo → `pip install --upgrade google-generativeai`")

    else:
        st.warning("⚠️ Please provide API Key, upload resume, and paste job description.")
