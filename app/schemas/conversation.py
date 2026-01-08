from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import datetime

class StartConversationRequest(BaseModel):
    user_id: int
    message: str
    mode: Literal["open", "rag"] = "open"

class MessageItem(BaseModel):
    role: str
    content: str
    sequence_number: int

class ConversationListResponse(BaseModel):
    conversation_id: int
    title: str
    created_at: datetime

class ConversationResponse(BaseModel):
    conversation_id: int
    title: str
    created_at: datetime
    assistant_reply: Optional[str] = None

class ConversationWithMessagesResponse(BaseModel):
    conversation_id: int
    messages: List[MessageItem]

class ConversationWithMessagesResponsePost(BaseModel):
    conversation_id: int
    title: str
    created_at: datetime
    assistant_reply: Optional[str] = None
    messages: List[MessageItem]

class MessageRequest(BaseModel):
    message: str

