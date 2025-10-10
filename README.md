# 💼 Resume Skill Matcher – AI-Powered JobFit Analyzer

> 🚀 **Built with Flask | NLP | spaCy | Pandas**

CodeRift 2025 Submission — *Unleash. Build. Disrupt.*

---

## 🧠 Overview

**Resume Skill Matcher** is an intelligent backend application that analyzes resumes and job descriptions using NLP to find how well a candidate’s skills match the role requirements.

It automatically:
- Extracts key skills from resumes (PDF/DOCX)
- Identifies required skills from the job description
- Calculates a **match score**
- Highlights **common** and **missing** skills

---

## ⚙️ Tech Stack

| Component | Technology |
|------------|-------------|
| Backend Framework | 🐍 Flask |
| NLP Engine | 🧩 spaCy (hybrid NLP model) |
| Data Processing | 🧮 Pandas, NumPy |
| File Parsing | 📄 pdfplumber / python-docx |
| Language Model | `en_core_web_sm` |
| API Testing | 🧰 Postman |

---

## 🧩 Features

✅ Extracts skills automatically from resumes  
✅ Keyword-based and NLP-based matching  
✅ JSON response with match score and insights  
✅ Lightweight Flask API – deploy anywhere  
✅ Easy integration with web or mobile front-ends  

---

## 📁 Project Structure

ResumeSkillMatcher/
│
├── app.py # Flask app (API endpoints)
├── matcher.py # Core NLP + matching logic
├── skills_list.csv # List of top industry skills
├── requirements.txt # Dependencies
├── uploads/ # Folder for uploaded resumes
└── README.md # You are here 😎


---

## ⚡ How to Run Locally

### 1️⃣ Clone the repo
```bash
git clone https://github.com/<your-username>/resume-skill-matcher.git
cd resume-skill-matcher

2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate   # (Windows)
# or
source venv/bin/activate  # (Mac/Linux)

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Download spaCy model
python -m spacy download en_core_web_sm

5️⃣ Run Flask app
python app.py


App will start at:
👉 http://127.0.0.1:5000/



🏆 Built For

CodeRift 2025 — National Level Hackathon

Unleash. Build. Disrupt.

👨‍💻 Team: Abhishek & Team
📍 Mode: 100% Online
🕒 Duration: 24-Hour Hackathon


📜 License

This project is open-source under the MIT License.

⭐ Don’t forget to star the repo if you like it!