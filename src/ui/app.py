import gradio as gr
import requests
import os

API_URL = os.environ.get("CHATBOT_API_URL_RENDER", "http://localhost:8000/chat/")

def chat_with_api(query):
    try:
        response = requests.post(API_URL, json={"query": query})
        response.raise_for_status()
        return response.json().get("response", "No response key found.")
    except Exception as e:
        return f"Error: {e}"

iface = gr.Interface(
    fn=chat_with_api,
    inputs=gr.Textbox(label="Your Question"),
    outputs=gr.Textbox(label="Bot's Answer"),
    title="Medical Chatbot",
    description="Enter your question"
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    iface.launch(server_name="0.0.0.0", server_port=port)
