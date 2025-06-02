import os
import requests
from openai import OpenAI
from qdrant_client import QdrantClient
from utils import translate_function_call

API_URL = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2/pipeline/feature-extraction"
def get_embedding(text: str):
    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": text}
    )
    return response.json()

# Get secrets from AWS Secrets Manager
# You can store all related secrets in one secret with multiple key-value pairs

GPT_4o_MODEL = "openai/gpt-4o-mini"
client_4o = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("GPT_4o_API_KEY"))

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")
COLLECTION_NAME = "ruslanmv-ai-medical-chatbot"

client = QdrantClient(
    url=QDRANT_HOST,
    api_key=QDRANT_API_KEY,
)

headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}

def retrieve_context(query: str) -> str:
    # Input validation
    if not isinstance(query, str):
        raise TypeError("Query must be a string")
    if not query.strip() or len(query) > 2000:
        raise ValueError("Query must be non-empty and reasonably sized")
    
    translated_text, language_code = translate_function_call(client_4o, query)
    nearest = client.query_points(
        collection_name=COLLECTION_NAME,
        query=get_embedding(translated_text),
        limit=3
    )
    print("nearest", nearest)
    if not nearest.points:
        return "No relevant information found.", language_code
    return "\n\n".join(
        [
            f"Patient: {question}\nDoctor: {answer}" for question, answer in [(point.payload["question"], point.payload["answer"]) for point in nearest.points]
        ]
    ), language_code


def medical_chatbot(user_query, chat_history=[]):
    """Uses OpenAI's GPT-4 to generate a response with retrieved context"""
    retrieved_info, language_code = retrieve_context(user_query)
    print("Retrieved info:", retrieved_info)
    prompt = f"""
    You are a helpful and professional medical chatbot, you only answer questions related to medical topics,
    if the user asks a question that is not medical, you should let them know that you can only answer medical questions.
    
    The user asked their question in the language: {language_code}.
    You must respond in that language, and you must base your answer only on the context provided below, do not use any other knowledge, even if it is related.

    Context:
    {retrieved_info}

    User's question:
    {user_query}
    """
    response = client_4o.chat.completions.create(
        model=GPT_4o_MODEL,
        messages=[
            {
                "role": "system", "content": "You are a medical chatbot."
            },
            {
                "role": "user", "content": prompt
            }
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    # Example usage
    user_query = "What are the symptoms of diabetes?"
    chat_history = []
    response = medical_chatbot(user_query, chat_history)
    print("Chatbot response:", response)
