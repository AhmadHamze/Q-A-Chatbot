from datasets import load_dataset
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EMBEDDINGS_PATH = os.path.join(BASE_DIR, "question_embeddings_gpu.npy")

ds = load_dataset("ruslanmv/ai-medical-chatbot")

# TODO: use another dataset alongside this one
# Login using e.g. `huggingface-cli login` to access this dataset
# ds = load_dataset("FreedomIntelligence/medical-o1-reasoning-SFT", "en")

qa_pairs = [(entry["Patient"], entry["Doctor"]) for entry in ds["train"]]
questions, answers = zip(*qa_pairs)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
question_embeddings = np.load(EMBEDDINGS_PATH)

# Store embeddings in FAISS for fast retrieval
dimension = question_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(question_embeddings)

def retrieve_context(user_query, top_k=3):
    """Finds the most relevant stored questions and their answers"""
    query_embedding = embed_model.encode([user_query], convert_to_numpy=True)
    _, indices = index.search(query_embedding, top_k)
    
    retrieved_context = "\n\n".join([f"Patient: {questions[i]}\nDoctor: {answers[i]}" for i in indices[0]])
    return retrieved_context
