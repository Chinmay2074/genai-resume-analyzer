import streamlit as st
import PyPDF2
import re

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

st.title("📄 AI Resume Analyzer")
st.write("Upload resume and compare it with job description")

uploaded_file = st.file_uploader("Upload Resume PDF", type="pdf")
job_description = st.text_area("Paste Job Description")

# Common skills list
skills_db = [
    "python","excel","sql","communication","leadership","recruitment",
    "data analysis","machine learning","hr","talent acquisition",
    "screening","sourcing","interview","management","training"
]

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

        # Skill detection
        detected_skills = [skill for skill in skills_db if skill in resume_text.lower()]

        st.subheader("🧠 Detected Skills")

        if detected_skills:
            for skill in detected_skills:
                st.write("✔️", skill)
        else:
            st.write("No skills detected")

        st.subheader("✅ Matching Keywords")

        for word in list(matches)[:10]:
            st.write("•", word)

        st.subheader("❌ Missing Keywords")

        for word in list(missing)[:10]:
            st.write("•", word)

    else:
        st.warning("Upload resume and paste job description")
