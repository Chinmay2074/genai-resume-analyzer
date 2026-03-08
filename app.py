import streamlit as st

st.title("GenAI Resume Analyzer")

resume = st.text_area("Paste Resume")
jd = st.text_area("Paste Job Description")

if st.button("Analyze"):

    if resume and jd:

        resume_words = set(resume.lower().split())
        jd_words = set(jd.lower().split())

        match = resume_words.intersection(jd_words)

        score = int((len(match) / len(jd_words)) * 100)

        st.subheader("Analysis Result")

        st.write("Match Score:", score, "%")

        st.write("Matching Keywords:")
        st.write(list(match)[:10])

    else:
        st.write("Please paste resume and job description")
