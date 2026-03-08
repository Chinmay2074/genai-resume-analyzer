import streamlit as st
import PyPDF2
import google.generativeai as genai

st.set_page_config(page_title="AI Resume Analyzer", page_icon="🧠")
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

            # Updated Model Selection Logic
            # 'gemini-1.5-flash' standard name hai latest library ke liye
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                # Test call to check if model exists
                model.get_model("models/gemini-1.5-flash") 
            except Exception:
                # Fallback to older model names if flash is not found
                model = genai.GenerativeModel("gemini-pro")

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
                st.markdown(response.text) # Use markdown for better formatting

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("💡 Solution: Terminal mein ye command run karo: \n`pip install --upgrade google-generativeai`")
    else:
        st.warning("⚠️ Please provide API Key, upload resume, and paste job description.")
