import re
from sentence_transformers import SentenceTransformer, util
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


# ===============================
# SEMANTIC MATCH
# ===============================
def semantic_score(resume_text, job_text):
    embeddings = model.encode([resume_text, job_text], convert_to_tensor=True)
    score = util.cos_sim(embeddings[0], embeddings[1])
    return round(float(score) * 100, 2)


# ===============================
# EXTRACT REQUIRED SKILLS
# ===============================
def extract_required_skills(job_text):
    words = job_text.split()
    return list(set(words))


# ===============================
# SKILL COVERAGE
# ===============================
def skill_coverage_score(resume_text, required_skills):

    resume_text = resume_text.lower()

    matched = [
        skill for skill in required_skills
        if skill.lower() in resume_text
    ]

    missing = [
        skill for skill in required_skills
        if skill.lower() not in resume_text
    ]

    if not required_skills:
        return 0, [], []

    coverage = (len(matched) / len(required_skills)) * 100

    return round(coverage, 2), matched, missing


# ===============================
# QUALITY SCORE
# ===============================
def quality_score(resume_text):

    score = 0

    sections = ["education", "experience", "projects", "skills"]
    found = sum(1 for sec in sections if sec in resume_text.lower())
    score += (found / len(sections)) * 50

    bullets = re.findall(r"^\s*[-•]", resume_text, re.MULTILINE)
    if len(bullets) >= 5:
        score += 25

    numbers = re.findall(r"\d+%?|\$\d+|\d+x", resume_text)
    if len(numbers) >= 5:
        score += 25

    return round(score, 2)


# ===============================
# IMPROVED INTELLIGENT ATS SCORE
# ===============================
def ats_score(resume_text, job_text, coverage):

    semantic = semantic_score(resume_text, job_text)

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform([resume_text, job_text])
    keyword_similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])
    keyword = float(keyword_similarity) * 100

    quality = quality_score(resume_text)

    # 🔥 NEW BALANCED ATS FORMULA
    raw_ats = (
        0.40 * coverage +
        0.25 * semantic +
        0.15 * keyword +
        0.20 * quality
    )

    # Smooth scaling
    ats = raw_ats * 1.15

    # Avoid unrealistic low score for decent resumes
    if ats < 35 and coverage > 30:
        ats = 45

    return round(min(95, ats), 2)


# ===============================
# FINAL SCORE
# ===============================
def final_score(semantic, ats, coverage, quality):

    final = (
        0.30 * ats +
        0.25 * semantic +
        0.25 * coverage +
        0.20 * quality
    )

    final = min(97, final + 3)

    return round(final, 2)


# ===============================
# PERFORMANCE LABEL
# ===============================
def performance_label(score):

    if score < 45:
        return "Needs Strong Improvement 🔴"
    elif score < 65:
        return "Moderate Alignment 🟡"
    elif score < 80:
        return "Strong Profile 🟢"
    else:
        return "Highly Competitive 🚀"