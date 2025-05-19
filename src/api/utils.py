from openai import OpenAI
import json

GPT_4o_MODEL = "openai/gpt-4o-mini"

def translate_to_english(text: str, language: str) -> str:
    """Translate text to English if it's in a different language."""
    return text

def translate_function_call(client: OpenAI, query: str) -> str:
        # Step 1: Translate the query to English (using OpenAI function calling)
    tools = [
        {
            "type": "function",
            "function": {
            "name": "translate_to_english",
            "description": "Translate non-English input into English and detect the language",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The translated version of the user's input in English."
                    },
                    "language": {
                        "type": "string",
                        "description": "The language code of the user's original query (e.g. 'ru', 'fr', 'ar')."
                    }
                },
                "required": ["text", "language"]
            }}
        }
    ]

    messages = [
        {"role": "system", "content": "You are a translation assistant. Only call the function if the input is not in English."},
        {"role": "user", "content": query}
    ]
    print("Hello World")
    try:
        response = client.chat.completions.create(
            model=GPT_4o_MODEL,
            messages=messages,
            tools=tools,
            function_call="auto"
        )
    except Exception as e:
        print("Error during function call:", e)
        return query, "en"

    # Use translated text if function was called
    if response.choices[0].finish_reason == "tool_calls":
        # Access the first tool call (which is your translation function)
        tool_call = response.choices[0].message.tool_calls[0]
        # Parse the arguments JSON
        args = json.loads(tool_call.function.arguments)
        return args["text"], args["language"]
    return query, "en"
