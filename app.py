import streamlit as st
import PyPDF2

st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader("Upload Resume PDF", type="pdf")

job_description = st.text_area("Paste Job Description")


def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


if st.button("Analyze Resume"):

    if uploaded_file and job_description:

        resume_text = extract_text(uploaded_file)

        resume_words = set(resume_text.lower().split())
        jd_words = set(job_description.lower().split())

        matching = resume_words.intersection(jd_words)

        score = int((len(matching) / len(jd_words)) * 100)

        st.subheader("Analysis Result")

        st.write("Match Score:", score, "%")

        st.write("Matching Keywords:")
        st.write(list(matching)[:10])

    else:
        st.warning("Upload resume and paste job description")
