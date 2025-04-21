import json
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.text_utils import clean_text

def load_job_descriptions(filepath: str) -> List[Dict]:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
    
def match_resume_to_jobs(parsed_resume: Dict[str, List[str]], job_descriptions: List[Dict], top_n: int = 3) -> List[Dict]:
    resume_summary = " ".join(parsed_resume.get("skills", []) + parsed_resume.get("experience", [])).lower()
    
    job_docs = [clean_text(job["description"]) for job in job_descriptions]
    
    docs = [resume_summary] + job_docs

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(docs)

    resume_vec = tfidf_matrix[0]
    job_vecs = tfidf_matrix[1:]

    similarities = cosine_similarity(resume_vec, job_vecs).flatten()
    ranked_jobs = sorted(zip(job_descriptions, similarities), key=lambda x: x[1], reverse=True)

    return [
        {"job_id": job["id"], "title": job["title"], "similarity": round(score, 2)}
        for job, score in ranked_jobs[:top_n]
    ]