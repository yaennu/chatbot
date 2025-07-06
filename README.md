# RAG Chatbot with Modern Frontend

A production-ready RAG (Retrieval-Augmented Generation) chatbot with a FastAPI backend and a modern Next.js frontend.

## Architecture

### Backend
- FastAPI for the API framework
- LlamaIndex for the RAG implementation
- Qdrant for vector storage
- Azure OpenAI for LLM integration

### Frontend
- Next.js for the React framework
- TypeScript for type safety
- Tailwind CSS for styling

## Project Structure

```
├── backend (Root directory)
│   ├── main.py           # FastAPI application
│   ├── pyproject.toml    # Poetry dependencies
│   ├── .env              # Environment variables
│   └── data/             # Document data for RAG system
│
└── frontend/
    └── chatbot-frontend/ # Next.js application
        ├── src/
        │   ├── app/      # Next.js app directory
        │   ├── components/# React components
        │   └── services/  # API services
        └── package.json   # Node dependencies
```

## Getting Started

### Backend Setup

1. Install dependencies:
   ```
   poetry install
   ```

2. Set up environment variables in `.env`

3. Start the backend server:
   ```
   poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend/chatbot-frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Usage

1. Start both the backend and frontend servers
2. Open the web interface at http://localhost:3000
3. Start asking questions in the chat interface
4. The system will process your query using the RAG system and return relevant answers

## Development

### Adding Documents to the RAG System

Place document files in the `data/` directory. The system will automatically index these on startup.

### Environment Variables

Key variables that need to be configured in `.env`:
- `OPENAI_API_KEY`: Your Azure OpenAI API key
- `QDRANT_COLLECTION_NAME`: Collection name for Qdrant vector store
