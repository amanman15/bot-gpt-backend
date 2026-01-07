from fastapi import FastAPI
from app.db.database import Base, engine
from app.api.conversations import router as conversation_router

# Import models so SQLAlchemy registers them
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message

app = FastAPI(title="BOT GPT Backend")

Base.metadata.create_all(bind=engine)

app.include_router(conversation_router)

@app.get("/")
def health_check():
    return {"status": "BOT GPT backend running"}