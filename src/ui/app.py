import gradio as gr
import requests
import os

# Replace with your actual API endpoint
API_URL = os.getenv("API_URL", "http://chatbot-api:8000/chat")

def chat_with_api(query):
    try:
        response = requests.post(API_URL, json={"query": query})
        response.raise_for_status()
        return response.json().get("response", "No response key found.")
    except Exception as e:
        return f"Error: {e}"

iface = gr.Interface(
    fn=chat_with_api,
    inputs=gr.Textbox(label="Ваш вопрос"),
    outputs=gr.Textbox(label="Ответ бота"),
    title="Медицинский чат-бот",
    description="Введите ваш вопрос"
)

if __name__ == "__main__":
    iface.launch()
