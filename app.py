import streamlit as st
import PyPDF2
import re

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and compare it with the job description")

uploaded_file = st.file_uploader("Upload Resume PDF", type="pdf")
job_description = st.text_area("Paste Job Description")


def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


def clean_words(text):
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    return set(words)


if st.button("Analyze Resume"):

    if uploaded_file and job_description:

        resume_text = extract_text(uploaded_file)

        resume_words = clean_words(resume_text)
        jd_words = clean_words(job_description)

        matches = resume_words.intersection(jd_words)
        missing = jd_words - resume_words

        score = int((len(matches) / len(jd_words)) * 100)

        st.subheader("📊 Resume Analysis Result")

        st.progress(score / 100)
        st.metric("Match Score", f"{score}%")

        if score >= 70:
            st.success("Strong match for this job role")
        elif score >= 40:
            st.warning("Moderate match – candidate may need improvement")
        else:
            st.error("Low match – resume may not fit this role")

        st.subheader("✅ Matching Keywords")

        cols = st.columns(2)
        for i, word in enumerate(list(matches)[:10]):
            cols[i % 2].write("✔️ " + word)

        st.subheader("❌ Missing Keywords")

        cols2 = st.columns(2)
        for i, word in enumerate(list(missing)[:10]):
            cols2[i % 2].write("❌ " + word)

    else:
        st.warning("Please upload resume and paste job description")
