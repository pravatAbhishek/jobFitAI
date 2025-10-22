# app.py

from flask import Flask, request, jsonify
from utils.resume_parser import extract_text_from_pdf, extract_skills_from_text
from utils.jd_parser import extract_keywords_from_jd
import spacy
from spacy.cli import download as spacy_download
from fuzzywuzzy import fuzz

# Initialize Flask
app = Flask(__name__)

# Load spaCy model safely
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy_download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


# Health check route
@app.route('/')
def index():
    return jsonify({"message": "Resume Skill Matcher API is running"})


# POST endpoint for matching resume with JD
@app.route('/match', methods=['POST'])
def match_resume():
    try:
        # 1️⃣ Check resume file
        if 'resume' not in request.files:
            return jsonify({"error": "No resume file provided"}), 400
        resume_file = request.files['resume']

        # 2️⃣ Check job description
        jd_text = request.form.get('job_description', "").strip()
        if not jd_text:
            return jsonify({"error": "No job description provided"}), 400

        # 3️⃣ Extract text from resume
        resume_text = extract_text_from_pdf(resume_file)
        if not resume_text:
            return jsonify({"error": "Failed to extract text from resume"}), 500

        # 4️⃣ Extract skills from resume using your parser
        resume_skills = extract_skills_from_text(resume_text)

        # 5️⃣ Extract keywords from JD
        jd_keywords = extract_keywords_from_jd(jd_text)

        # 6️⃣ Hybrid Fuzzy + Keyword Matching
        matched = []
        for r_skill in resume_skills:
            for j_skill in jd_keywords:
                if fuzz.partial_ratio(r_skill.lower(), j_skill.lower()) >= 75:
                    matched.append(r_skill)
                    break

        matched = list(set(matched))
        missing = [kw for kw in jd_keywords if kw.lower() not in [m.lower() for m in matched]]

        # Match Score Calculation
        total_skills = len(set(jd_keywords))
        match_score = round((len(matched) / total_skills * 100), 2) if total_skills > 0 else 0

        # 7️⃣ Return JSON Response
        return jsonify({
            "resume_skills": resume_skills,
            "jd_keywords": jd_keywords,
            "common_skills": matched,
            "missing_skills": missing,
            "match_score": match_score
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
