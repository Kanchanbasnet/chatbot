# RAG Chatbot

A chatbot you can talk to normally, ask about your own documents, or use to search the web. Answers stream in live, word by word, and every conversation is saved.

## Features

- Streaming answers
- Chat history saved in a database
- Upload a document (PDF, DOCX, PPTX, TXT) and ask questions about it
- Web search for current information
- Read a web page when you share a link

## Model

- **LLM:** `openai/gpt-oss-20b`
- **Provider:** Groq (via `langchain-groq`)

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy
- **AI agent:** LangChain (`create_agent`) with tools
- **Frontend:** Streamlit

## Agent Tools

| Tool | What it does |
|---|---|
| `search_documents` | Searches the uploaded document (RAG) |
| `web_search` | Searches the web for latest information |
| `fetch_url` | Reads the text of one web page |

## API

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/chat` | Send a question and get a streamed answer. Body: `question`, `conversation_id`, `document_id`. The conversation id is returned in the `X-Conversation-Id` response header. |
| `POST` | `/chat/upload` | Upload a file. Returns the `document_id`. |
| `GET` | `/conversations` | List all conversations |
| `GET` | `/conversations/{id}/messages` | Get the messages of one conversation |
| `DELETE` | `/conversations?conversation_id=ID` | Delete a conversation |

## Setup

1. Install the dependencies:

   ```bash
   uv sync
   ```

2. Create a `.env` file:

   ```
   GROQ_API_KEY=your_groq_api_key
   BACKEND_URL=http://localhost:8000
   ```

3. Start the backend:

   ```bash
   uv run uvicorn backend.main:app --reload
   ```

4. Start the frontend:

   ```bash
   uv run streamlit run frontend/app.py
   ```

## How It Works

1. The user sends a question (and optionally a document).
2. The agent decides whether to answer directly or use a tool.
3. The answer streams back to the Streamlit app.
4. The question and answer are saved in the database.