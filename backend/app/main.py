from fastapi import FastAPI
from backend.app.api import chat, health, admin
from backend.app.database.postgres import engine, Base
from backend.app.models.chat import ChatHistory
from backend.app.models.document import Document

# for the postgres db
Base.metadata.create_all(bind=engine)

app = FastAPI(title="RAGbot API")

app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(health.router, prefix="/api/health", tags=["Health"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {"message": "Welcome to RAGbot API"}
