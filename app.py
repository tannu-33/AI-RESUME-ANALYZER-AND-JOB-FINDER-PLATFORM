import streamlit as st
from streamlit_option_menu import option_menu

from utils.parser import extract_text
from utils.scoring import (
    semantic_score,
    extract_required_skills,
    skill_coverage_score,
    ats_score,
    quality_score,
    final_score,
    performance_label
)
from utils.skills import load_roles, learning_resources
from utils.bullet_analyzer import extract_bullets, weak_bullets, fallback_bullets
from utils.llm_engine import improve_bullets
from utils.report_generator import generate_report
from services.job_scraper import fetch_jobs


st.set_page_config(page_title="Resume Intelligence System", layout="wide")

# -----------------------------
# Sidebar Navigation
# -----------------------------
with st.sidebar:
    selected_page = option_menu(
        "Navigation",
        ["AI Resume Analyzer", "Job / Internship Finder"],
        icons=["file-earmark-text", "briefcase"],
        menu_icon="cast",
        default_index=0
    )

roles_data = load_roles()
role_options = list(roles_data.keys())

# ==========================================================
# PAGE 1 — AI RESUME ANALYZER
# ==========================================================
if selected_page == "AI Resume Analyzer":

    st.title("🧠 AI Resume Analyzer")

    uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
    selected_role = st.selectbox("Select Target Job Role", role_options)

    if uploaded_file and selected_role:

        # -----------------------------
        # Extract Resume Text
        # -----------------------------
        resume_text = extract_text(uploaded_file)

        # -----------------------------
        # Job Role Skills
        # -----------------------------
        job_text = " ".join(roles_data[selected_role]["skills"])
        required_skills = extract_required_skills(job_text)

        # -----------------------------
        # Scores
        # -----------------------------
        semantic = semantic_score(resume_text, job_text)

        coverage, matched_skills, missing_skills = skill_coverage_score(
            resume_text,
            required_skills
        )

        ats = ats_score(resume_text, job_text, coverage)
        quality = quality_score(resume_text)
        final = final_score(semantic, ats, coverage, quality)
        label = performance_label(final)

        # =====================================================
        # DISPLAY RESULTS
        # =====================================================
        st.subheader("📊 Score Breakdown")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("🧠 Semantic Match", f"{semantic}%")
            st.metric("🤖 ATS Match", f"{ats}%")
            st.caption("⚡ This ATS score is generated using our Intelligent Resume Intelligence Model combining semantic AI, skill coverage, keyword matching, and resume quality analysis. It is NOT a basic keyword-based ATS.")

        with col2:
            st.metric("🎯 Skill Coverage", f"{coverage}%")
            st.metric("📄 Resume Quality", f"{quality}%")

        st.success(f"🏆 Final Match Score: {final}%")
        st.info(f"📌 Resume Strength: {label}")

        # -----------------------------
        # Matched Skills
        # -----------------------------
        st.subheader("✅ Matched Skills")

        if matched_skills:
            for skill in matched_skills:
                st.write(f"- {skill}")
        else:
            st.write("No matched skills found.")

        # -----------------------------
        # Missing Skills + Resources
        # -----------------------------
        st.subheader("📚 Missing Skills + Resources")

        if missing_skills:
            for skill in missing_skills:
                st.markdown(f"### {skill}")
                resources = learning_resources(skill)
                for name, link in resources.items():
                    st.markdown(f"- [{name}]({link})")
        else:
            st.success("🎉 No major missing skills detected for this role!")

        # -----------------------------
        # Bullet Optimization
        # -----------------------------
        st.subheader("🔥 Bullet Optimization")

        bullets = extract_bullets(resume_text)

        if not bullets:
            st.warning("""
⚠ No clear bullet points detected.

For better ATS readability:
• Use '-' or '•' consistently  
• Start with strong action verbs  
• Quantify results with numbers (%)  
• Keep each point concise (1–2 lines)

Example:
- Improved system efficiency by 30% by optimizing backend APIs  
- Built ML model achieving 92% accuracy  
""")
        else:
            weak = weak_bullets(bullets)

            if len(weak) < 2:
                weak = fallback_bullets(bullets)

            if weak:
                st.subheader("✨ Suggested Improvements")
                improved = improve_bullets(weak)
                st.write(improved)
            else:
                st.success("✅ Your bullet points are well-written and ATS-friendly.")

        # -----------------------------
        # Role-Based Resume Tips
        # -----------------------------
        st.subheader("📌 Role-Based Resume Tips")

        if "Engineer" in selected_role:
            st.markdown("""
- Add measurable performance improvements
- Show scalability impact
- Mention system design exposure
- Quantify optimization
""")
        elif "Data" in selected_role:
            st.markdown("""
- Mention dataset size
- Quantify insights
- Show business impact
- Include dashboards or models
""")
        else:
            st.markdown("""
- Use strong action verbs
- Quantify achievements
- Tailor resume to job role
- Avoid generic phrases
""")

        # -----------------------------
        # Downloadable Report
        # -----------------------------
        if st.button("Generate Downloadable Report"):

            report_data = {
                "Role": selected_role,
                "Semantic Score": semantic,
                "ATS Score": ats,
                "Skill Coverage": coverage,
                "Quality Score": quality,
                "Final Score": final,
                "Matched Skills": ", ".join(matched_skills),
                "Missing Skills": ", ".join(missing_skills)
            }

            filepath = generate_report(report_data)

            with open(filepath, "rb") as f:
                st.download_button(
                    "Download Report",
                    f,
                    "resume_report.pdf",
                    "application/pdf"
                )

# ==========================================================
# PAGE 2 — JOB FINDER
# ==========================================================
elif selected_page == "Job / Internship Finder":

    st.title("💼 Live Job Finder")

    
    job_type = st.selectbox(
    "Select Opportunity Type",
    ["Full-Time Jobs", "Internships"]
)
    selected_role = st.selectbox("Select Role", role_options)

    if st.button("🔎 Find Opportunities"):

        jobs = fetch_jobs(selected_role,job_type)

        if jobs:
            for job in jobs:
                st.markdown(f"""
### {job['title']}
**Company:** {job['company']}  
**Location:** {job['location']}  
**Salary:** {job['salary'] if job['salary'] else "Not Disclosed"}  
[Apply Here]({job['link']})
---
""")
                if not jobs:
                    st.warning("No API jobs found. Explore below platforms:")

    st.markdown("- [LinkedIn India Jobs](https://www.linkedin.com/jobs)")
    st.markdown("- [Indeed India](https://in.indeed.com)")
else:
    st.warning("No live jobs found. Try again.")