🧠 Resume Skill Matcher

An AI-powered tool that analyzes resumes against job descriptions to identify matched and missing skills — helping candidates tailor their resumes for specific roles.

🚀 Features

✅ Resume–JD Skill Matching — Upload your resume and paste a job description to get an instant skill comparison.
✅ Smart Matching Engine — Uses NLP (spaCy) and fuzzy matching to find relevant skills even if worded differently.
✅ CSV Skill Dictionary — Reads from a curated list of skills to filter only relevant keywords.
✅ Beautiful UI — Built with Streamlit, featuring a sticky navbar, glass-style overlay, and PDF report download.
✅ Downloadable Reports — Export results as a professional PDF summary.
✅ Modular Codebase — Separate utils for parsing resumes, job descriptions, and matching logic.

🏗️ Tech Stack

Frontend:

Streamlit

Python Requests

ReportLab (for PDF generation)

Backend:

Flask

spaCy (NLP)

FuzzyWuzzy / RapidFuzz

Pandas

Custom CSV-based skill dictionary

Other Tools:

GitHub for collaboration

Virtual environment (venv)

JSON-based API communication

📁 Project Structure
resume-skill-matcher/
│
├── backend/
│   ├── app.py                   # Flask backend (API)
│   ├── utils/
│   │   ├── resume_parser.py     # Extracts text from PDF
│   │   ├── jd_parser.py         # Extracts keywords from JD
│   │   ├── matcher.py           # Hybrid skill matching logic
│   │   └── skills.csv           # Skill dictionary
│   └── requirements.txt
│
├── frontend/
│   ├── app.py                   # Streamlit frontend
│   ├── assets/                  # Optional images, icons, etc.
│   └── requirements.txt
│
└── README.md

⚙️ Installation & Setup
1. Clone the Repository
git clone https://github.com/TeamCatalyst/resume-skill-matcher.git
cd resume-skill-matcher

2. Create Virtual Environment
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

3. Install Requirements

Install dependencies for both backend and frontend:

pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

🧩 Running the Project
Start Backend (Flask)
cd backend
python app.py


Backend will start at http://127.0.0.1:5000

Start Frontend (Streamlit)

Open a new terminal:

cd frontend
streamlit run app.py


Frontend runs at http://localhost:8501

🧮 How It Works

Upload your Resume (PDF or TXT).

Paste the Job Description.

Streamlit sends both to the Flask API.

Flask:

Extracts skills using NLP + CSV keywords.

Finds common & missing skills with fuzzy matching.

Calculates a match percentage.

Results are displayed beautifully and can be downloaded as a PDF report.

🧰 Example Output

Match Score: 76%
Matched Skills: Python, Pandas, Excel
Missing Skills: SQL, Power BI, Data Visualization

🧑‍💻 Team Catalyst
Name	Role	Email
Abhishek Kumar	Backend Lead	abhishek.pravat@gmail.com

Krishna Kumar	Frontend Lead	krishnakumar.s9475@gmail.com

Rithesh H B	UX / Research	rithuu20077@gmail.com

Akash K N	Documentation	akashnagaraju91@gmail.com


