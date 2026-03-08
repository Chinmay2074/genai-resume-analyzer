import streamlit as st
import PyPDF2

st.set_page_config(page_title="Smart Resume Analyzer", page_icon="🤖")

st.title("🤖 Smart Resume Analyzer")
st.write("Upload your resume and analyze it against a job description.")

uploaded_file = st.file_uploader("Upload Resume PDF", type="pdf")
job_description = st.text_area("Paste Job Description")

skills_db = [
    "python","excel","sql","communication","leadership",
    "recruitment","hr","talent acquisition","training",
    "management","data analysis","analytics","sourcing",
    "screening","interview","payroll","labor law",
    "employee engagement","hr analytics"
]

def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()


if st.button("Analyze Resume"):

    if uploaded_file and job_description:

        resume_text = extract_text(uploaded_file)
        jd_text = job_description.lower()

        resume_skills = [s for s in skills_db if s in resume_text]
        jd_skills = [s for s in skills_db if s in jd_text]

        matched = list(set(resume_skills) & set(jd_skills))
        missing = list(set(jd_skills) - set(resume_skills))

        score = int((len(matched) / len(jd_skills)) * 100) if jd_skills else 0

        st.subheader("📊 Resume Match Score")
        st.progress(score/100)
        st.metric("Match Score", f"{score}%")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Matched Skills")
            if matched:
                for s in matched:
                    st.success(s)
            else:
                st.write("No matched skills found")

        with col2:
            st.subheader("❌ Missing Skills")
            if missing:
                for s in missing:
                    st.error(s)
            else:
                st.write("No missing skills")

        st.divider()

        st.subheader("💡 Resume Improvement Suggestions")

        if score < 40:
            st.write("• Add more role-specific skills from the job description.")
            st.write("• Include measurable achievements in your experience.")
            st.write("• Highlight projects related to the role.")
        elif score < 70:
            st.write("• Improve resume by adding the missing skills.")
            st.write("• Add keywords used in the job description.")
        else:
            st.write("• Resume looks strong for this role.")
            st.write("• Focus on preparing for interview questions.")

        st.divider()

        st.subheader("🧠 Recruiter Insight")

        if score >= 70:
            st.success("Candidate is a strong match for the role.")
        elif score >= 40:
            st.warning("Candidate is moderately suitable.")
        else:
            st.error("Candidate is not strongly aligned with the role.")

    else:
        st.warning("Please upload a resume and paste job description.")
