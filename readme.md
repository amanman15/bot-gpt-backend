# BOT GPT BACKEND

A Python-based backend application that provides a continuous, turn-based chat experience using LLMs (Groq/OpenAI models). Supports both Open Chat and RAG (Retrieval-Augmented Generation) Chat** modes, with conversation memory and persistence.

--
## Table of Contents

- [Author](#author)  
- [Tech Stack](#tech-stack)  
- [Features](#features)  
- [Setup & Installation](#setup--installation)  
- [API Endpoints](#api-endpoints)  
- [Database Models](#database-models)  
- [Usage Notes](#usage-notes)  

# Author
Aman Jain
Email:<amanjainwork1599@gmail.com>

**-----------------------------------------------------------------------------**

# Tech Stack

- **Python 3.13**  
- **FastAPI** – API framework  
- **SQLAlchemy** – ORM for database interactions  
- **SQLite** – Local database (can be replaced with PostgreSQL)  
- **Groq SDK** – LLM integration (OpenAI GPT-OSS 120B model)  
- **Pydantic** – Data validation and serialization  
- **Dotenv** – Environment variable management  

**-----------------------------------------------------------------------------**

## Features

- Continuous turn-based chat with memory  
- **Open Chat Mode:** General chat without context  
- **RAG Mode:** Grounded chat using documents (planned)  
- Persistent conversation history for each user  
- Conversation titles (auto-generated from first user message)  
- Supports multiple messages per conversation with proper sequence numbers  
- Error handling for database & LLM calls (planned)  

---
**-----------------------------------------------------------------------------**
## Setup & Installation

1. **Clone the repository**

git clone https://github.com/amanman15/bot-gpt-backend.git
cd bot-gpt-backend

2. **Create virtual environment & install dependencies**
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
pip install -r requirements.txt

3. **Set environment variables**
Create a .env file:
GROQ_API_KEY=YOUR_GROQ_API_KEY
4. **Run the application**
uvicorn app.main:app --reload
Visit http://127.0.0.1:8000/ for the health check

Visit http://127.0.0.1:8000/docs/ for swagger.

**---------------------------------------------------------------------------------**
## API Endpoints

1. **Start Conversation**
POST /conversations/
Request Body
{
  "user_id": 1,
  "message": "Hello, who is Elon Musk?"
}

Response:
{
  "conversation_id": 1,
  "title": "Hello, who is Elon Musk?",
  "created_at": "2026-01-07T12:00:00Z",
  "assistant_reply": "Elon Musk is the CEO of Tesla and SpaceX..."
}

2. **Add Message to Existing Conversation**
POST /conversations/{conversation_id}/messages
Request Body
{
  "message": "Tell me more about SpaceX."
}

Response:
{
  "conversation_id": 1,
  "assistant_reply": "SpaceX is an aerospace manufacturer and space transport company...",
  "messages": [
    {"role": "user", "content": "Hello, who is Elon Musk?", "sequence_number": 1},
    {"role": "assistant", "content": "...", "sequence_number": 2},
    {"role": "user", "content": "Tell me more about SpaceX.", "sequence_number": 3},
    {"role": "assistant", "content": "...", "sequence_number": 4}
  ]
}

3. **Get Conversation by ID**
GET /conversations/{conversation_id}
Response
{
  "conversation_id": 1,
  "title": "Hello, who is Elon Musk?",
  "messages": [
    {"role": "user", "content": "Hello, who is Elon Musk?", "sequence_number": 1},
    {"role": "assistant", "content": "Elon Musk is the CEO of Tesla and SpaceX...", "sequence_number": 2},
    {"role": "user", "content": "Tell me more about SpaceX.", "sequence_number": 3},
    {"role": "assistant", "content": "...", "sequence_number": 4}
  ]
}

4. **List All Conversations for a User**
GET /conversations/?user_id={user_id}
Response
[
  {
    "conversation_id": 1,
    "title": "Hello, who is Elon Musk?",
    "created_at": "2026-01-07T12:00:00Z"
  },
  {
    "conversation_id": 2,
    "title": "Hi, tell me about Virat Kohli",
    "created_at": "2026-01-07T12:30:00Z"
  }
]

5. **Delete the conversation**
DELETE /conversations/{conversation_id}
Response
{
  "detail": "Conversation 1 deleted successfully"
}

**--------------------------------------------------------------------------------------------**

**Database Models**

1. **User**

id, name, etc.

2. **Conversation**

id – Conversation ID
user_id – Linked user
title – First message snippet
mode – open or rag
created_at, updated_at – timestamps

3. **Message**

id – Message ID
conversation_id – Linked conversation
role – "user" or "assistant"
content – Text
sequence_number – Order of message

**------------------------------------------------------------------------------**

**Usage Notes**

Conversations retain full history for a continuous chat experience.
Sequence numbers ensure proper ordering of messages.
Titles are auto-generated from the first user message.
Future enhancements include RAG mode (document-grounded chat)