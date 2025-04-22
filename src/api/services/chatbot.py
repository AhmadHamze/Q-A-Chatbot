from qdrant_chatbot import medical_chatbot

def get_chatbot_response(query: str, chat_history=None):
    """
    Process a user query through the medical chatbot
    
    Args:
        query: The user's question
        chat_history: Optional chat history
        
    Returns:
        The chatbot's response as a string
    """
    if chat_history is None:
        chat_history = []
        
    response = medical_chatbot(query, chat_history)
    return response