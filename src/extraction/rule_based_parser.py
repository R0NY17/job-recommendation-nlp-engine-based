import re
from typing import List, Dict

# Simple sample lists for now
SKILL_KEYWORDS = [
    "python", "java", "sql", "excel", "machine learning",
    "data analysis", "tensorflow", "pandas", "numpy", "c++"
]

DEGREE_KEYWORDS = [
    "bachelor", "master", "b.tech", "m.tech", "b.sc", "m.sc",
    "bachelor of science", "master of science", "engineering"
]

JOB_TITLE_KEYWORDS = [
    "software engineer", "data analyst", "intern", "developer",
    "research assistant", "consultant", "project manager"
]

def extract_skills(text: str) -> List[str]:
    text = text.lower()
    return list({skill for skill in SKILL_KEYWORDS if skill in text})

def extract_education(text: str) -> List[str]:
    text = text.lower()
    return re.findall(r"(?i)(" + "|".join(DEGREE_KEYWORDS) + r")", text)

def extract_experience(text: str) -> List[str]:
    text = text.lower()
    return re.findall(r"(?i)(" + "|".join(JOB_TITLE_KEYWORDS) + r")", text)

def parse_resume(text: str) -> Dict[str, List[str]]:
    return {
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text)
    }
