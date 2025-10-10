# utils/matcher.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def preprocess(text):
    """
    Preprocess skill or keyword:
    - Lowercase
    - Remove articles (a, an, the)
    - Strip extra spaces
    """
    text = text.lower()
    text = re.sub(r'\b(a|an|the)\b', '', text)
    text = re.sub(r'\s+', ' ', text)  # remove extra spaces
    return text.strip()

def hybrid_match(resume_skills, jd_keywords, similarity_threshold=0.65):
    """
    Hybrid skill matcher using cosine similarity with preprocessing.
    - resume_skills: list of skills from resume
    - jd_keywords: list of keywords from job description
    - similarity_threshold: float (0-1), higher = stricter matching
    Returns: dict with common_skills, missing_skills, match_score
    """
    if not resume_skills or not jd_keywords:
        return {
            "common_skills": [],
            "missing_skills": jd_keywords or [],
            "match_score": 0
        }

    # Preprocess skills
    resume_skills_clean = [preprocess(skill) for skill in resume_skills]
    jd_keywords_clean = [preprocess(jd) for jd in jd_keywords]

    # Prepare text for TF-IDF
    all_texts = resume_skills_clean + jd_keywords_clean
    vectorizer = TfidfVectorizer().fit_transform(all_texts)

    # Cosine similarity between resume skills and JD keywords
    similarity_matrix = cosine_similarity(vectorizer[:len(resume_skills_clean)],
                                         vectorizer[len(resume_skills_clean):])

    common_skills = []
    matched_jd_indices = set()

    for i, skill in enumerate(resume_skills_clean):
        for j, jd in enumerate(jd_keywords_clean):
            if j in matched_jd_indices:
                continue  # skip already matched JD keywords
            if similarity_matrix[i][j] >= similarity_threshold:
                common_skills.append(resume_skills[i])  # use original resume skill
                matched_jd_indices.add(j)

    # Identify missing skills
    missing_skills = [jd_keywords[idx] for idx in range(len(jd_keywords)) if idx not in matched_jd_indices]

    # Calculate match score
    match_score = (len(common_skills) / len(jd_keywords)) * 100 if jd_keywords else 0

    return {
        "common_skills": list(set(common_skills)),
        "missing_skills": missing_skills,
        "match_score": round(match_score, 2)
    }
