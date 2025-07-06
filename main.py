from fastapi import FastAPI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Initialize Qdrant Client
# For simplicity, using an in-memory client. For production, use a persistent client.
client = QdrantClient(":memory:")

# Create a collection in Qdrant
collection_name = "my_rag_collection"
client.recreate_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

# Initialize LlamaIndex Settings
# Ensure you have an OpenAI API key set as an environment variable (OPENAI_API_KEY)
# Settings.llm = OpenAI(model="gpt-3.5-turbo") # Uncomment and configure if needed
# Settings.embed_model = OpenAIEmbedding() # Uncomment and configure if needed

# Load documents and create index
@app.on_event("startup")
async def startup_event():
    # Create a dummy data directory and file for demonstration
    if not os.path.exists("data"):
        os.makedirs("data")
    with open("data/policy.txt", "w") as f:
        f.write("The quick brown fox jumps over the lazy dog. This is a policy document.")

    documents = SimpleDirectoryReader("data").load_data()
    vector_store = QdrantVectorStore(client=client, collection_name=collection_name)
    # The service context is deprecated, use Settings instead
    # index = VectorStoreIndex.from_documents(documents, vector_store=vector_store, service_context=Settings)
    index = VectorStoreIndex.from_documents(documents, vector_store=vector_store)
    app.state.query_engine = index.as_query_engine()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the LlamaIndex RAG API!"}

@app.post("/query")
async def query_rag(query: str):
    response = app.state.query_engine.query(query)
    return {"response": str(response)}