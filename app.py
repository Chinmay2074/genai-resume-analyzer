import streamlit as st
import PyPDF2

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

st.title("🤖 AI Resume Analyzer")
st.write("Analyze resume against job description and get improvement suggestions")

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
    return text


if st.button("Analyze Resume"):

    if uploaded_file and job_description:

        resume_text = extract_text(uploaded_file).lower()
        jd_text = job_description.lower()

        resume_skills = [skill for skill in skills_db if skill in resume_text]
        jd_skills = [skill for skill in skills_db if skill in jd_text]

        matched = set(resume_skills).intersection(jd_skills)
        missing = set(jd_skills) - set(resume_skills)

        if jd_skills:
            score = int((len(matched) / len(jd_skills)) * 100)
        else:
            score = 0

        st.subheader("📊 Resume Match Score")

        st.progress(score / 100)
        st.metric("Match Score", f"{score}%")

        st.subheader("🧠 Skills Detected in Resume")

        for skill in resume_skills:
            st.write("✔️", skill)

        st.subheader("✅ Matched Skills")

        if matched:
            for skill in matched:
                st.write("✔️", skill)
        else:
            st.write("No matching skills found")

        st.subheader("❌ Missing Skills")

        if missing:
            for skill in missing:
                st.write("❌", skill)
        else:
            st.write("No missing skills")

        st.subheader("🤖 AI Resume Improvement Suggestions")

        suggestions = []

        if score < 40:
            suggestions.append("Add more relevant skills from the job description.")
            suggestions.append("Include specific achievements in your resume.")
            suggestions.append("Use strong action verbs like 'managed', 'implemented', 'led'.")
        
        if missing:
            suggestions.append("Consider adding these skills: " + ", ".join(list(missing)[:5]))

        if not suggestions:
            suggestions.append("Your resume matches well with the job description.")

        for tip in suggestions:
            st.write("💡", tip)

        st.subheader("💼 HR Recommendation")

        if score >= 70:
            st.success("Strong candidate – suitable for interview")
        elif score >= 40:
            st.warning("Moderate match – candidate may need some improvements")
        else:
            st.error("Low match – resume may not fit this role")

    else:
        st.warning("Upload resume and paste job description")
