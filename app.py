import streamlit as st
import PyPDF2
import pandas as pd

st.set_page_config(page_title="AI Resume Analyzer", page_icon="🤖")

st.title("🤖 AI Resume Analyzer")
st.write("Analyze your resume against a job description and get insights.")

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
                st.write("No matched skills")

        with col2:
            st.subheader("❌ Missing Skills")
            if missing:
                for s in missing:
                    st.error(s)
            else:
                st.write("No missing skills")

        st.divider()

        st.subheader("📈 Skill Comparison Chart")

        data = {
            "Category":["Matched Skills","Missing Skills"],
            "Count":[len(matched),len(missing)]
        }

        df = pd.DataFrame(data)

        st.bar_chart(df.set_index("Category"))

        st.divider()

        st.subheader("💡 Resume Improvement Suggestions")

        if missing:
            st.write("• Add these skills if relevant:")
            for s in missing[:5]:
                st.write(f"  - {s}")

        st.write("• Add measurable achievements in work experience.")
        st.write("• Use strong action verbs like *managed, led, implemented*.")

        st.divider()

        st.subheader("🎯 Possible Interview Questions")

        for skill in matched[:3]:
            st.write(f"• Can you describe your experience with {skill}?")

        st.divider()

        st.subheader("🧠 Recruiter Insight")

        if score >= 70:
            st.success("Strong candidate match for this role.")
        elif score >= 40:
            st.warning("Moderate candidate match.")
        else:
            st.error("Low alignment with job requirements.")

    else:
        st.warning("Upload resume and paste job description.")
