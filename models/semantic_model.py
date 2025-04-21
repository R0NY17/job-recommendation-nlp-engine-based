from sentence_transformers import SentenceTransformer

semantic_model = SentenceTransformer("all-MiniLM-L6-v2")

def encode_texts(texts):
    return semantic_model.encode(texts, convert_to_tensor=True)