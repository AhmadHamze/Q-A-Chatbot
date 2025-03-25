import requests
from openai import OpenAI
import os
import html
from dotenv import load_dotenv


# * This is a simple trivia quiz game that uses the Open Trivia Database API to get random trivia questions.
# * DeepSeek V3 is used to ask the user a random trivia question using the model's tools to get the question from the Open Trivia Database.

load_dotenv(".env")

DEEP_SEEK_V3_MODEL = "deepseek/deepseek-chat:free"

TRIVIA_URL = "https://opentdb.com/api.php?amount=1&category=9&difficulty=medium&type=boolean"
client_v3 = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ["V3_API_KEY"])

def get_trivia():
    """Get a random trivia question from the Open Trivia Database"""
    response = requests.get(TRIVIA_URL)
    response.raise_for_status()
    data = response.json()
    return data["results"][0]

def get_explanation(question, correct_answer, user_answer):
    """Get an explanation from DeepSeek V3 about the trivia question and answer"""
    
    # Decode HTML entities in the question
    clean_question = html.unescape(question)
    
    prompt = f"""
            You are a robot explaining a trivia question to a human.
            Question: {clean_question}
            Correct answer: {correct_answer}
            User's answer: {user_answer}

            Please provide a brief explanation about this question {correct_answer}. 
            Include some interesting facts related to this trivia.
            """
    
    response = client_v3.chat.completions.create(
        model=DEEP_SEEK_V3_MODEL,
        messages=[
            {
                "role": "user", "content": prompt
            }
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content

def start_trivia_game():
    trivia = get_trivia()
    question = trivia["question"]
    answer = trivia["correct_answer"]
    print(html.unescape(question))
    user_input = input("What is your answer? (true/false)")
    if user_input.lower() == "exit":
        print("Goodbye!")
        exit()
    if user_input.lower() == answer.lower():
        print("Correct!")
    else:
        print("Incorrect!")
    
    # Get explanation from V3
    print("\nGetting some context about this question...")
    explanation = get_explanation(question, answer, user_input)
    
    print("\n----- EXPLANATION -----")
    print(explanation)
    print("-----------------------\n")
    
    return

if __name__ == "__main__":
    print("Welcome to Trivia Quiz with AI Explanations!")
    print("Type 'exit' to quit the game.")
    print("-------------------------------------")

    while True:
        start_trivia_game()
        print("\nNext question coming up...\n")
