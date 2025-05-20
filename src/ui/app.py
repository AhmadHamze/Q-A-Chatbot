import gradio as gr
import requests

# Replace with your actual API endpoint
API_URL = "http://localhost:8000/chat"

def chat_with_api(query):
    try:
        response = requests.post(API_URL, json={"query": query})
        response.raise_for_status()
        return response.json().get("response", "No response key found.")
    except Exception as e:
        return f"Error: {e}"

iface = gr.Interface(
    fn=chat_with_api,
    inputs=gr.Textbox(label="Your message"),
    outputs=gr.Textbox(label="Bot response"),
    title="Chatbot Demo",
    description="Enter a message and see the response from the AI API."
)

if __name__ == "__main__":
    iface.launch()
