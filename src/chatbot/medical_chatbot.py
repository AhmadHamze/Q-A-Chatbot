import os
from openai import OpenAI
from src.data.dataset import retrieve_context
from dotenv import load_dotenv

load_dotenv("../../.env")

GPT_4o_MODEL = "openai/gpt-4o-mini"
client_4o = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["GPT_4o_API_KEY"])

def medical_chatbot(user_query):
    """Uses OpenAI's GPT-4 to generate a response with retrieved context"""
    retrieved_info = retrieve_context(user_query)
    prompt = f"""
    You are a helpful and professional medical chatbot. Below is past conversation data:

    {retrieved_info}

    Now answer the following question in a helpful and concise manner:
    Patient: {user_query}
    Doctor:
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

def main():
  print("Welcome to the medical chatbot! Type 'exit' to quit.")
  while True:
    user_input = input("Ask anything: ")
    if user_input.lower() == "exit":
      break
    response = medical_chatbot(user_input)
   
    print("Medical Bot:", response)

if __name__ == "__main__":
  main()
