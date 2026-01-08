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
- **SQLite** – Local database (can be replaced with PostgreSQL for production grade.)  
- **Groq SDK** – LLM integration (OpenAI GPT-OSS 120B model)  
- **Pydantic** – Data validation and serialization  
- **Dotenv** – Environment variable management  

**-----------------------------------------------------------------------------**

## Features

- Continuous turn-based chat with memory  
- **Open Chat Mode:** General chat without context  
- **RAG Mode:** Grounded chat using documents (implemented at very basic level)  
- Persistent conversation history for each user  
- Conversation titles (auto-generated from first user message)  
- Supports multiple messages per conversation with proper sequence numbers  
- Error handling for database & LLM calls
- Listing all conversation as a tile view for a user.
- Listing all the conversation in a particular conversation using its id.
- Delete the entire conversation.
- Add the message in the current conversation from the context.

**-----------------------------------------------------------------------------**
## Setup & Installation

1. **Clone the repository**

git clone https://github.com/amanman15/bot-gpt-backend.git
cd bot-gpt-backend

*Note: As of now everything was pushed directly to main branch as no team collaboration is here.*


2. **Create virtual environment & install dependencies**
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
pip install -r requirements.txt

3. **Set environment variables**
Go to: https://console.groq.com/playground?model=openai/gpt-oss-120b and create a free tier API Key
Create a .env file:
GROQ_API_KEY=YOUR_GROQ_API_KEY

4. **Run the application**
uvicorn app.main:app --reload
Visit http://127.0.0.1:8000/ for the health check

Visit http://127.0.0.1:8000/docs for swagger.

**---------------------------------------------------------------------------------**
## API Endpoints

1. **Start Conversation with a first message and mode**
POST /conversations/
Request Body
{
  "user_id": 1,
  "message": "Hello, who is Elon Musk?",
  "mode": open(default) [open|rag]
}

Response:
{
  "conversation_id": 1,
  "title": "Hello, who is Elon Musk?",
  "created_at": "2026-01-07T12:00:00Z",
  "assistant_reply": "Elon Musk is the CEO of Tesla and SpaceX..."
}

2. **Add Message to Existing Conversation**
In this route we use sliding window, hardcoded as of now. This will set the context for the next message.
POST /conversations/{conversation_id}/messages
conversation_id- as parameter
Request Body
{
  "message": "Tell me more about SpaceX."
}

Response:
{
  "conversation_id": 1,
  "title": "Tell me more about SpaceX",
  "created_at": "2026-01-07T07:22:35.552194",
  "assistant_reply": "SpaceX is an aerospace manufacturer and space transport company...",
  "messages": [
    {"role": "user", "content": "Hello, who is Elon Musk?", "sequence_number": 1},
    {"role": "assistant", "content": "...", "sequence_number": 2},
    {"role": "user", "content": "Tell me more about SpaceX.", "sequence_number": 3},
    {"role": "assistant", "content": "...", "sequence_number": 4}
  ]
}

3. **Get Conversation by conversation ID**
GET /conversations/{conversation_id}
conversation_id---->parameter
Response
{
  "conversation_id": 1,
  "messages": [
    {"role": "user", "content": "Hello, who is Elon Musk?", "sequence_number": 1},
    {"role": "assistant", "content": "Elon Musk is the CEO of Tesla and SpaceX...", "sequence_number": 2},
    {"role": "user", "content": "Tell me more about SpaceX.", "sequence_number": 3},
    {"role": "assistant", "content": "...", "sequence_number": 4}
  ]
}

4. **List All Conversations for a User(list view)**
GET /conversations/?user_id={user_id}
user_id-parameter
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
conversation_id---->paramter
Response
{
  "detail": "Conversation 1 deleted successfully"
}

**--------------------------------------------------------------------------------------------**

**Database Models**

1. **User**

id

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
created_at

**------------------------------------------------------------------------------**

**UNIT TESTING**
Unit tests are written using pytest and FastAPI TestClient.
A separate SQLite database is used for test isolation.
Run tests using: pytest -v (for verbose mode) and pytest (for direct)

**------------------------------------------------------------------------------**

**Usage Notes**

Conversations retain full history for a continuous chat experience.
Sequence numbers ensure proper ordering of messages.
Titles are auto-generated from the first user message.
Rag mode is implemented at a basic level for understanding the context, can be extended to future ready version.