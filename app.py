import streamlit as st

st.title("GenAI Resume Analyzer")

resume = st.text_area("Paste Resume")
jd = st.text_area("Paste Job Description")

if st.button("Analyze"):
    st.write("Analysis result will appear here")