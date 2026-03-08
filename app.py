import streamlit as st
import PyPDF2

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and analyze it against the job description.")

uploaded_file = st.file_uploader("Upload Resume PDF", type="pdf")
job_description = st.text_area("Paste Job Description")

skills_db = [
"python","excel","sql","communication","leadership","recruitment",
"hr","talent acquisition","training","management","analytics",
"data analysis","sourcing","screening","interview","payroll",
"labor law","employee engagement","hr analytics","performance management"
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

        st.subheader("📊 ATS Score")
        st.progress(score/100)
        st.metric("Resume Match", f"{score}%")

        st.divider()

        # Resume summary
        st.subheader("📄 Resume Summary")

        if resume_skills:
            summary = f"This candidate demonstrates experience in {', '.join(resume_skills[:4])}."
        else:
            summary = "Limited recognizable skills found in the resume."

        st.write(summary)

        st.divider()

        # Top skills
        st.subheader("🧠 Top Skills Found")

        if resume_skills:
            for skill in resume_skills[:6]:
                st.success(skill)
        else:
            st.write("No major skills detected")

        st.divider()

        # Strengths
        st.subheader("💪 Strengths")

        if matched:
            for skill in matched:
                st.write(f"• Strong alignment with **{skill}**")
        else:
            st.write("No strong alignment with job description")

        st.divider()

        # Improvements
        st.subheader("⚠ Areas to Improve")

        if missing:
            for skill in missing[:5]:
                st.write(f"• Consider adding **{skill}** to your resume")
        else:
            st.success("No major skill gaps detected")

        st.divider()

        # Resume length check
        st.subheader("📏 Resume Length Check")

        word_count = len(resume_text.split())

        if word_count < 200:
            st.warning("Resume may be too short. Consider adding more details.")
        elif word_count > 1000:
            st.warning("Resume may be too long. Try to keep it concise.")
        else:
            st.success("Good resume length detected.")

        st.divider()

        # Keyword coverage
        st.subheader("🔍 Keyword Coverage")

        st.write(f"{len(matched)} out of {len(jd_skills)} job keywords found in the resume.")

        st.divider()

        # Interview questions
        st.subheader("🎯 Possible Interview Questions")

        for skill in matched[:3]:
            st.write(f"• Tell me about your experience with **{skill}**.")

        st.divider()

        # Recruiter insight
        st.subheader("🧠 Recruiter Insight")

        if score >= 70:
            st.success("Strong candidate match for the role.")
        elif score >= 40:
            st.warning("Moderate alignment with job requirements.")
        else:
            st.error("Resume needs improvement for this role.")

    else:
        st.warning("Please upload resume and paste job description.")
