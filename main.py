from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the LlamaIndex RAG API!"}

# TODO: Implement LlamaIndex RAG process here
