from PyPDF2 import PdfReader
import re
import pandas as pd

def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text() + " "
    return text.lower()

def extract_skills_from_text(text, skill_csv_path="data/skills_list.csv"):
    skills_df = pd.read_csv(skill_csv_path)
    skill_list = skills_df['skill'].str.lower().tolist()
    found_skills = []
    for skill in skill_list:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found_skills.append(skill)
    return list(set(found_skills))
