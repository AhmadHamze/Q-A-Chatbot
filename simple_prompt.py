from openai import OpenAI
from project_secrets import R1_API_KEY

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=R1_API_KEY,
)

def ask_model(input):
  result = client.chat.completions.create(
    # * The model used for the completion, make sure to use the correct version associated with the API key
    model="deepseek/deepseek-r1:free",
    messages=[
      {
        "role": "user",
        "content": input
      }
    ]
  )
  try:
    return (result, result.choices[0].message.content)
  except Exception as e:
    return f"Something went wrong. Please try again: {e}"

def main():
  print("Welcome to Simple Prompt! Type 'exit' to quit.")
  while True:
    user_input = input("Ask anything: ")
    if user_input.lower() == "exit":
      break
    _, response = ask_model(user_input)
   
    print("Bot:", response)

if __name__ == "__main__":
  main()