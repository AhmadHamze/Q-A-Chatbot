import os
from openai import OpenAI
import gradio as gr
from src.data.dataset import retrieve_context
from dotenv import load_dotenv

# Load environment variables from .env file in project root
load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

GPT_4o_MODEL = "openai/gpt-4o-mini"
client_4o = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ.get("GPT_4o_API_KEY"))

# TODO: Use chat_history
# TODO: Show the user the retrieved context
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

if __name__ == "__main__":
    demo = gr.ChatInterface(fn=medical_chatbot, title="Medical Chatbot", description="Ask any medical question.", type="messages")
    demo.launch()
