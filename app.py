import streamlit as st
import PyPDF2

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

st.title("📄 AI Resume Analyzer")
st.write("Upload a resume and compare it with a job description.")

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

        matches = resume_words.intersection(jd_words)

        score = int((len(matches) / len(jd_words)) * 100)

        st.subheader("📊 Resume Analysis Result")

        st.metric("Match Score", f"{score}%")

        if score >= 70:
            st.success("Strong match for the job role")
        elif score >= 40:
            st.warning("Moderate match – candidate may need improvements")
        else:
            st.error("Low match – resume may not fit this role well")

        st.subheader("✅ Matching Keywords")

        for word in list(matches)[:10]:
            st.write("•", word)

        missing = jd_words - resume_words

        st.subheader("❌ Missing Keywords")

        for word in list(missing)[:10]:
            st.write("•", word)

    else:
        st.warning("Please upload a resume and paste job description.")
