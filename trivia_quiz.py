import requests
from openai import OpenAI
from project_secrets import GPT_4o_API_KEY

# * This is a simple trivia quiz game that uses the Open Trivia Database API to get random trivia questions.
# * GPT-4o is used to ask the user a random trivia question using the model's tools to get the question from the Open Trivia Database.

GPT_4o_MODEL = "openai/gpt-4o-mini"

TRIVIA_URL = "https://opentdb.com/api.php?amount=1&category=9&difficulty=medium&type=boolean"
client_4o = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=GPT_4o_API_KEY)

tools = [{
    "type": "function",
    "function": {
        "name": "get_trivia_question",
        "description": "Get a random trivia question from the Open Trivia Database",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        },
    }
}]

def get_trivia_question():
    """Get a random trivia question from the Open Trivia Database"""
    response = requests.get(TRIVIA_URL)
    response.raise_for_status()
    data = response.json()
    return data["results"][0]

def start_trivia_game():
    messages = [
        {"role": "system", 
        "content": (
            "You are a gameshow host, you are asking the user a random trivia question,"
            "ask the question immediately"
            )
        }
    ]
    
    question_response = client_4o.chat.completions.create(
        model=GPT_4o_MODEL,
        messages=messages,
        tools=tools,
        parallel_tool_calls=False
    )
    if not question_response.choices[0].message.tool_calls:
        print("No tools were used")
        return

    if question_response.choices[0].message.tool_calls[0].function.name == "get_trivia_question":
        try:
            function_response = get_trivia_question()
        except Exception as e:
            function_response = {'error': str(e)}
    else:
        print("get_trivia_question is not found!")
        return

    question = function_response["question"]
    answer = function_response["correct_answer"]
    print(question)
    user_input = input("What is your answer?")
    if user_input.lower() == answer.lower():
        print("Correct!")
    else:
        print("Incorrect!")
    return

if __name__ == "__main__":
    start_trivia_game()
