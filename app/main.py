import streamlit as st
import os
from app.parser import parse_resume
from app.utils import extract_details, highlight_skills_in_text
from app.matcher import match_resume_to_jd
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Resume Analyzer Pro", layout="wide")
st.title("🧪 Resume Analyzer Pro - Phase 5")

# --- Form UI ---
with st.form("analyze_form"):
    jd_text = st.text_area("📄 Paste Job Description", height=200)
    uploaded_files = st.file_uploader("📂 Upload Resumes (PDF/DOCX)", type=["pdf", "docx"], accept_multiple_files=True)
    submitted = st.form_submit_button("🔍 Analyze")

if submitted:
    if not jd_text or not uploaded_files:
        st.warning("Please upload resumes and paste a job description.")
    else:
        os.makedirs("resumes", exist_ok=True)
        results = []
        skill_freq = {}
        progress = st.progress(0)

        for i, resume in enumerate(uploaded_files):
            file_path = os.path.join("resumes", resume.name)
            with open(file_path, "wb") as f:
                f.write(resume.getbuffer())

            resume_text = parse_resume(resume)
            details = extract_details(resume_text)
            match_score = match_resume_to_jd(resume_text, jd_text)

            # Count skills
            skill_list = details["Skills"].split(", ")
            for skill in skill_list:
                if skill:
                    skill_freq[skill.lower()] = skill_freq.get(skill.lower(), 0) + 1

            details["Filename"] = resume.name
            details["Match %"] = round(match_score, 2)
            details["Text"] = resume_text
            results.append(details)

            progress.progress((i + 1) / len(uploaded_files))

        df = pd.DataFrame(results).sort_values("Match %", ascending=False)

        st.subheader("📈 Match Results with Highlights")
        def highlight_row(row):
            color = "background-color: "
            if row["Match %"] >= 75:
                return [color + "#c6f6d5"] * len(row)
            elif row["Match %"] >= 50:
                return [color + "#fefcbf"] * len(row)
            else:
                return [color + "#fed7d7"] * len(row)

        st.dataframe(df.drop(columns=["Text"]).style.apply(highlight_row, axis=1), use_container_width=True)

        # 📥 Download CSV
        csv = df.drop(columns=["Text"]).to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Results", csv, "resume_analysis.csv", "text/csv")

        # 📄 Preview Highlighted Text
        st.subheader("📃 Resume Viewer with Matched Skill Highlights")
        for i, row in df.iterrows():
            with st.expander(f"📝 {row['Filename']} — {row['Match %']}% match"):
                highlighted = highlight_skills_in_text(row["Text"], row["Skills"].split(", "))
                st.markdown(highlighted)

        # 📊 Visualization
        if skill_freq:
            st.subheader("📊 Top Matched Skills")
            skill_df = pd.DataFrame(sorted(skill_freq.items(), key=lambda x: x[1], reverse=True), columns=["Skill", "Frequency"])
            st.plotly_chart(px.bar(skill_df, x="Skill", y="Frequency", title="Top Skills"))

        # 📈 Score Distribution
        bins = ["0-50%", "51-75%", "76-100%"]
        counts = [len(df[df["Match %"] <= 50]),
                  len(df[(df["Match %"] > 50) & (df["Match %"] <= 75)]),
                  len(df[df["Match %"] > 75])]
        pie = px.pie(values=counts, names=bins, title="Match Score Breakdown")
        st.plotly_chart(pie)
