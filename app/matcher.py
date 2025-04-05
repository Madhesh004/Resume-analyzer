from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load once (global)
model = SentenceTransformer('all-MiniLM-L6-v2')

def match_resume_to_jd(resume_text: str, jd_text: str) -> float:
    resume_embedding = model.encode([resume_text])[0]
    jd_embedding = model.encode([jd_text])[0]
    similarity = cosine_similarity([resume_embedding], [jd_embedding])[0][0]
    return similarity * 100  # Return as percentage
