from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.conversation import Conversation
from app.models.message import Message
from app.services.llm_service import call_llm
from app.services.context_builder import build_context
from app.services.rag_service import get_mock_context
from app.schemas.conversation import StartConversationRequest, ConversationWithMessagesResponse, ConversationListResponse, ConversationWithMessagesResponsePost, ConversationResponse, MessageRequest

router = APIRouter(prefix="/conversations", tags=["Conversations"])

#Start a new conversation with a user and first message
@router.post("/", response_model=ConversationResponse)
async def start_conversation(payload: StartConversationRequest, db: Session = Depends(get_db)):
    # Create conversation
    conversation = Conversation(user_id=payload.user_id, title=payload.message[:50], mode=payload.mode)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    # Save user message
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=payload.message,
        sequence_number=1
    )
    db.add(user_message)
    db.commit()
    if conversation.mode == "rag":
        retrieved_context = get_mock_context(conversation.id)
    else:
        retrieved_context = None
    # Call LLM
    context = build_context([], payload.message, retrieved_context)
    assistant_reply = await call_llm(context)

    # Save assistant reply
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=assistant_reply,
        sequence_number=2
    )
    db.add(assistant_message)
    db.commit()

    return {
        "conversation_id": conversation.id,
        "title": conversation.title,
        "created_at": conversation.created_at,
        "assistant_reply": assistant_reply,
    }


# List all conversations for a user
@router.get("/", response_model=List[ConversationListResponse])
def list_conversations(user_id: int, db: Session = Depends(get_db)):
    conversations = db.query(Conversation).filter(Conversation.user_id == user_id).all()

    if not conversations:
        raise HTTPException(status_code=404, detail="No conversations found")

    result = []

    for conv in conversations:
        messages = (
            db.query(Message)
            .filter(Message.conversation_id == conv.id)
            .order_by(Message.sequence_number)
            .all()
        )

        if not messages:
            continue

        # Use first user message as the title
        title = next((m.content for m in messages if m.role == "user"), messages[0].content)

        result.append({
            "conversation_id": conv.id,
            "title": title,
            "created_at": conv.created_at
        })

    return result
# ------------------------------------------------------------------------------------------------

#Get full conversation history by Conversation ID
@router.get("/{conversation_id}", response_model=ConversationWithMessagesResponse)
def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conversation = db.query(Conversation)\
        .filter(Conversation.id == conversation_id)\
        .first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.sequence_number)
        .all()
    )
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found in this conversation")
    return {
        "conversation_id": conversation.id,
        "messages": [
            {
                "role": m.role,
                "content": m.content,
                "sequence_number": m.sequence_number
            }
            for m in messages
        ]
    }

# ------------------------------------------------------------------------------------------------

# Add a new message to existing conversation
@router.post("/{conversation_id}/messages", response_model=ConversationWithMessagesResponsePost)
async def add_message(conversation_id: int, payload: MessageRequest, db: Session = Depends(get_db)):
    # 1. Find conversation
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # 2. Determine next sequence number
    last_message = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.sequence_number.desc()).first()
    next_seq = last_message.sequence_number + 1 if last_message else 1

    # 3. Save user message
    try:
        user_message = Message(
            conversation_id=conversation_id,
            role="user",
            content=payload.message,
            sequence_number=next_seq
        )
        db.add(user_message)
        db.commit()
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Failed to save user message: {e}")

    # 4️. Build context for LLM (all previous messages + new user message)
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.sequence_number).all()
    context_text = "\n".join([m.content for m in messages])
    assistant_reply = await call_llm([context_text])

    # 5. Save assistant reply
    try:
        assistant_message = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=assistant_reply,
            sequence_number=next_seq + 1
        )
        db.add(assistant_message)
        db.commit()
    except Exception as e:
        db.rollback()
        raise RuntimeError(f"Failed to save assistant message: {e}")

    # 6. Return full conversation history
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.sequence_number).all()

    # return {
    #     "conversation_id": conversation_id,
    #     "assistant_reply": assistant_reply,  # latest LLM reply
    #     "messages": history  # full memory
    # }
    return {
    "conversation_id": conversation.id,
    "title": conversation.title,
    "created_at": conversation.created_at,
    "assistant_reply": assistant_reply,
    "messages": [
        {"role": m.role, "content": m.content, "sequence_number": m.sequence_number}
        for m in messages
    ]
}


# 5️. Delete a conversation and its messages
@router.delete("/{conversation_id}")
def delete_conversation(conversation_id: int, db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Delete messages first
    db.query(Message).filter(Message.conversation_id == conversation_id).delete()
    db.delete(conversation)
    db.commit()

    return {"detail": f"Conversation {conversation_id} deleted successfully"}
