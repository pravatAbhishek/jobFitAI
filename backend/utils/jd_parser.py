# utils/jd_parser.py

import re
import spacy
import pandas as pd
from pathlib import Path

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load predefined skills list from CSV
SKILLS_PATH = Path(__file__).resolve().parent.parent / "data" / "skills_list.csv"

try:
    df = pd.read_csv(SKILLS_PATH, header=None)
    SKILL_LIST = [s.strip().lower() for s in df[0].tolist() if isinstance(s, str)]
except Exception as e:
    print(f"⚠️ Error loading skills.csv: {e}")
    SKILL_LIST = []

def extract_keywords_from_jd(jd_text):
    """
    Extract only real, skill-based keywords from job description text
    using the preloaded CSV skill list.
    """
    jd_text = jd_text.lower()

    # Tokenize with spaCy
    doc = nlp(jd_text)

    # Collect candidate words and phrases
    tokens = set()
    for token in doc:
        if not token.is_stop and token.is_alpha and len(token.text) > 2:
            tokens.add(token.text)

    # Match against known skills
    matched_skills = []
    for skill in SKILL_LIST:
        # Match exact or fuzzy pattern (allow partial phrases)
        if re.search(rf"\b{re.escape(skill)}\b", jd_text):
            matched_skills.append(skill)
        else:
            # Partial match for compound skills like 'machine learning'
            if any(word in tokens for word in skill.split()):
                matched_skills.append(skill)

    # Remove duplicates & sort
    matched_skills = sorted(list(set(matched_skills)))

    return matched_skills
