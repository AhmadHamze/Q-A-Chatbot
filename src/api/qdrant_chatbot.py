from openai import OpenAI
import json
import boto3
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

def get_secret(secret_name, region_name="eu-north-1"):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name
    )
    try:
        response = client.get_secret_value(SecretId=secret_name)
        if "SecretString" in response:
            return json.loads(response["SecretString"])
        else:
            # Binary secrets handling if needed
            return json.loads(response["SecretBinary"].decode("utf-8"))
    except Exception as e:
        print(f"Error retrieving secret {secret_name}: {e}")
        raise

# Get secrets from AWS Secrets Manager
# You can store all related secrets in one secret with multiple key-value pairs
secrets = get_secret("qdrant-medical-chatbot-secrets")

GPT_4o_MODEL = "openai/gpt-4o-mini"
client_4o = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=secrets["GPT_4o_API_KEY"])

QDRANT_HOST = secrets["QDRANT_HOST"]
QDRANT_API_KEY = secrets["QDRANT_API_KEY"]
COLLECTION_NAME="ruslanmv-ai-medical-chatbot"

client = QdrantClient(
    url=QDRANT_HOST,
    api_key=QDRANT_API_KEY,
)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_context(query: str) -> str:
    # Input validation
    if not isinstance(query, str):
        raise TypeError("Query must be a string")
    if not query.strip() or len(query) > 2000:
        raise ValueError("Query must be non-empty and reasonably sized")
    nearest = client.query_points(
        collection_name=COLLECTION_NAME,
        query=embed_model.encode(query),
        limit=3
    )
    if not nearest.points:
        return "No relevant information found."
    return "\n\n".join(
        [
            f"Patient: {question}\nDoctor: {answer}" for question, answer in [(point.payload["question"], point.payload["answer"]) for point in nearest.points]
            ]
        )


def medical_chatbot(user_query, chat_history=[]):
    """Uses OpenAI's GPT-4 to generate a response with retrieved context"""
    retrieved_info = retrieve_context(user_query)
    print("Retrieved info:", retrieved_info)
    prompt = f"""
    You are a helpful and professional medical chatbot, you only answer questions related to medical topics,
    if the user asks a question that is not medical, you should let them know that you can only answer medical questions.
    Below is past conversation data:

    {retrieved_info}

    Now, answer the following question solely based on the context provided above, do not use any other knowledge, even if it is related:
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
