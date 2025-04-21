from models.semantic_model import encode_texts
from sentence_transformers.util import cos_sim
from typing import List, Dict
from utils.text_utils import clean_text

def match_resume_to_jobs_semantic(parsed_resume: Dict[str, List[str]], job_descriptions: List[Dict], top_n: int = 3) -> List[Dict]:
    resume_summary = " ".join(parsed_resume.get("skills", []) + parsed_resume.get("experience", [])).lower()
    job_texts = [clean_text(job["description"]) for job in job_descriptions]

    resume_embedding = encode_texts([resume_summary])[0]
    job_embeddings = encode_texts(job_texts)

    similarities = cos_sim(resume_embedding, job_embeddings).squeeze().tolist()

    ranked_jobs = sorted(zip(job_descriptions, similarities), key=lambda x: x[1], reverse=True)

    return [
        {"job_id": job["id"], "title": job["title"], "similarity": round(score, 2)}
        for job, score in ranked_jobs[:top_n]
    ]