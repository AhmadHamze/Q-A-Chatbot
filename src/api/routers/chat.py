from fastapi import APIRouter, HTTPException
from ..models import ChatRequest, ChatResponse
from ..services.chatbot import get_chatbot_response

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = get_chatbot_response(request.query, request.chat_history)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")