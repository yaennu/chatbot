from fastapi import FastAPI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
import os
from dotenv import load_dotenv
from logging import getLogger
from typing import List, Union, Generator, Iterator
from pydantic import BaseModel, Field
from fastapi import FastAPI
from dotenv import load_dotenv

logger = getLogger(__name__)
logger.setLevel("DEBUG")

# Load environment variables from .env file
load_dotenv()

# Settings
pipeline_name = "Heiniger Kabelfinder"
phoenix_project = "heiniger-pipe" # This will be removed later if Phoenix is not integrated

class Pipeline:
    class Valves(BaseModel):
        QDRANT_COLLECTION: str = Field(
            default="heiniger",
            description="Name of the Qdrant collection",
        )
        RETRIEVER_TOP_K: str = Field(
            default="5",
            description="Number of top documents to retrieve",
        )
        SIMILARITY_CUTOFF: str = Field(
            default="0.7",
            description="Minimum similarity score for retrieved documents",
        )

    def __init__(self):
        self.name = pipeline_name
        self.index = None

        # Initialize valve paramaters
        self.valves = self.Valves(
            **{k: os.getenv(k, v.default) for k, v in self.Valves.model_fields.items()}
        )

    async def on_startup(self):
        from llama_index.core import VectorStoreIndex, Settings
        import qdrant_client
        from llama_index.vector_stores.qdrant import QdrantVectorStore
        from llama_index.llms.azure_openai import AzureOpenAI
        from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
        from llama_index.core import SimpleDirectoryReader

        # Load environment variables - these will be checked by the Pipeline class
        # For now, we'll just check the ones directly used in this method
        if not os.getenv("QDRANT_API_KEY"):
            raise KeyError("QDRANT_API_KEY environment variable is not set.")
        if not os.getenv("QDRANT_URI"):
            raise KeyError("QDRANT_URI environment variable is not set.")
        if not os.getenv("AZURE_LLM_MODEL"):
            raise KeyError("AZURE_LLM_MODEL environment variable is not set.")
        if not os.getenv("AZURE_LLM_DEPLOYMENT_NAME"):
            raise KeyError("AZURE_LLM_DEPLOYMENT_NAME environment variable is not set.")
        if not os.getenv("AZURE_LLM_API_KEY"):
            raise KeyError("AZURE_LLM_API_KEY environment variable is not set.")
        if not os.getenv("AZURE_LLM_ENDPOINT"):
            raise KeyError("AZURE_LLM_ENDPOINT environment variable is not set.")
        if not os.getenv("AZURE_LLM_API_VERSION"):
            raise KeyError("AZURE_LLM_API_VERSION environment variable is not set.")
        if not os.getenv("AZURE_EMBEDDER_MODEL"):
            raise KeyError("AZURE_EMBEDDER_MODEL environment variable is not set.")
        if not os.getenv("AZURE_EMBEDDER_DEPLOYMENT_NAME"):
            raise KeyError(
                "AZURE_EMBEDDER_DEPLOYMENT_NAME environment variable is not set."
            )
        if not os.getenv("AZURE_EMBEDDER_API_KEY"):
            raise KeyError("AZURE_EMBEDDER_API_KEY environment variable is not set.")
        if not os.getenv("AZURE_EMBEDDER_ENDPOINT"):
            raise KeyError("AZURE_EMBEDDER_ENDPOINT environment variable is not set.")
        if not os.getenv("AZURE_EMBEDDER_API_VERSION"):
            raise KeyError(
                "AZURE_EMBEDDER_API_VERSION environment variable is not set."
            )

        try:
            # LLM
            self.llm = AzureOpenAI(
                model=os.environ["AZURE_LLM_MODEL"],
                deployment_name=os.environ["AZURE_LLM_DEPLOYMENT_NAME"],
                api_key=os.environ["AZURE_LLM_API_KEY"],
                azure_endpoint=os.environ["AZURE_LLM_ENDPOINT"],
                api_version=os.environ["AZURE_LLM_API_VERSION"],
                temperature=0.1,
            )
            Settings.llm = self.llm
        except Exception as e:
            logger.error("Failed to initialize LLM: %s", e)

        try:
            # Embedding model
            self.embed_model = AzureOpenAIEmbedding(
                model=os.environ["AZURE_EMBEDDER_MODEL"],
                deployment_name=os.environ["AZURE_EMBEDDER_DEPLOYMENT_NAME"],
                api_key=os.environ["AZURE_EMBEDDER_API_KEY"],
                azure_endpoint=os.environ["AZURE_EMBEDDER_ENDPOINT"],
                api_version=os.environ["AZURE_EMBEDDER_API_VERSION"],
            )
            Settings.embed_model = self.embed_model
        except Exception as e:
            logger.error("Failed to initialize embedding model: %s", e)

        try:
            # Initialize Qdrant client
            client = qdrant_client.QdrantClient(
                url=os.getenv("QDRANT_URI"),
                api_key=os.getenv("QDRANT_API_KEY"),
            )

            # Vector store
            vector_store = QdrantVectorStore(
                collection_name=self.valves.QDRANT_COLLECTION,
                client=client,
            )

            # Create a dummy data directory and file for demonstration
            if not os.path.exists("data"):
                os.makedirs("data")
            with open("data/policy.txt", "w") as f:
                f.write("The quick brown fox jumps over the lazy dog. This is a policy document.")

            documents = SimpleDirectoryReader("data").load_data()

            self.index = VectorStoreIndex.from_documents(
                documents,
                vector_store=vector_store,
                embed_model=self.embed_model,
            )
        except Exception as e:
            logger.error("Failed to initialize Qdrant: %s", e)

        logger.debug("on_startup:%s", self.name)

    async def on_shutdown(self):
        logger.debug("on_shutdown:%s", self.name)

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        from llama_index.core.schema import QueryBundle
        from llama_index.core import get_response_synthesizer
        from llama_index.core.query_engine import RetrieverQueryEngine
        from llama_index.core.postprocessor import SimilarityPostprocessor
        from llama_index.core import PromptTemplate
        from llama_index.core.retrievers import VectorIndexRetriever

        print(messages)
        print(user_message)

        retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=int(self.valves.RETRIEVER_TOP_K),
            embed_model=self.embed_model,
        )

        # Prompt template
        qa_prompt_tmpl = """
# Aufgabe
Sie sind eine hilfreiche Fachexpertin. Für die Beantwortung der Fragen dürfen Sie ausschliesslich Informationen verwenden, die Ihnen im Kontext zwischen <context> und </context> bereitgestellt werden. Prüfen Sie zuerst sorgfältig den Kontext, der die Informationen enthält, die Sie in Ihren Antworten verwenden dürfen.
<context>
{context_str}
</context>

# Antwort
Bitte beantworten Sie nun die folgende Frage des Benutzers:
<user_query>
{query_str}
</user_query>
        """
        qa_prompt = PromptTemplate(qa_prompt_tmpl)

        # Query
        response_synthesizer = get_response_synthesizer(
            response_mode="compact",
            text_qa_template=qa_prompt,
            use_async=False,
            streaming=True,
            llm=self.llm,
        )

        postprocessor = SimilarityPostprocessor(
            similarity_cutoff=float(self.valves.SIMILARITY_CUTOFF),
        )

        query_engine = RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer,
            node_postprocessors=[postprocessor],
        )

        # Response
        query_bundle = QueryBundle(
            query_str=user_message,
        )
        response = query_engine.query(query_bundle)

        return response.response_gen

app = FastAPI()
pipeline = Pipeline()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await pipeline.on_startup()

@app.on_event("shutdown")
async def shutdown_event():
    await pipeline.on_shutdown()

@app.post("/query")
async def query_rag(query: str):
    response_generator = pipeline.pipe(user_message=query, model_id="", messages=[], body={})
    # Assuming response_generator yields strings
    full_response = "".join(list(response_generator))
    return {"response": full_response}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the LlamaIndex RAG API!"}