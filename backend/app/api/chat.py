from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from backend.app.database.postgres import get_db
from backend.app.models.chat import ChatHistory
from backend.app.services.llm import LLMService
from backend.app.rag.pipeline import RAGPipeline
from pydantic import BaseModel
import json
import asyncio

router = APIRouter()
llm_service = LLMService()
rag_pipeline = RAGPipeline()

class ChatRequest(BaseModel):
    message: str

@router.post("/")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    # 1. Get context from RAG pipeline
    context = rag_pipeline.get_relevant_context(request.message)
    
    # 2. Augmented prompt
    augmented_message = f"Context:\n{context}\n\nQuestion: {request.message}"

    async def event_generator():
        full_response = ""
        try:
            async for token in llm_service.get_streaming_response(augmented_message):
                full_response += token
                yield f"data: {json.dumps({'token': token})}\n\n"
            
            new_chat = ChatHistory(question=request.message, answer=full_response)
            db.add(new_chat)
            db.commit()
            
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/history")
async def get_history(db: Session = Depends(get_db)):
    history = db.query(ChatHistory).order_by(ChatHistory.timestamp.desc()).all()
    return history

@router.delete("/history")
async def clear_history(db: Session = Depends(get_db)):
    try:
        db.query(ChatHistory).delete()
        db.commit()
        return {"message": "Chat history cleared successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to clear chat history: {str(e)}")
