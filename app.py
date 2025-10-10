# app.py

from flask import Flask, request, jsonify
from utils.resume_parser import extract_text_from_pdf, extract_skills_from_text
from utils.jd_parser import extract_keywords_from_jd
from utils.matcher import hybrid_match
import spacy
from spacy.cli import download as spacy_download

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

        # 4️⃣ Extract skills from resume
        resume_skills = extract_skills_from_text(resume_text)

        # 5️⃣ Extract keywords from JD using spaCy
        jd_keywords = extract_keywords_from_jd(jd_text)

        # 6️⃣ Run hybrid matcher (with stricter threshold)
        result = hybrid_match(resume_skills, jd_keywords, similarity_threshold=0.65)

        # 7️⃣ Return JSON response
        return jsonify({
            "resume_skills": resume_skills,
            "jd_keywords": jd_keywords,
            "common_skills": result["common_skills"],
            "missing_skills": result["missing_skills"],
            "match_score": result["match_score"]
        })

    except Exception as e:
        # Always return JSON on error
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
