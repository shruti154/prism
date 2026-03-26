import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import chromadb
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.anthropic import Anthropic
from config import (
    ANTHROPIC_API_KEY, CHROMA_PERSIST_DIR, DOCUMENTS_DIR,
    EMBED_MODEL, LLM_MODEL, CHUNK_SIZE, CHUNK_OVERLAP
)

def setup_settings():
    print("Loading embedding model and Claude...")
    embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL)
    llm = Anthropic(model=LLM_MODEL, api_key=ANTHROPIC_API_KEY)
    Settings.embed_model = embed_model
    Settings.llm = llm
    Settings.chunk_size = CHUNK_SIZE
    Settings.chunk_overlap = CHUNK_OVERLAP
    print("Models ready.")
    return embed_model, llm

def ingest_documents():
    setup_settings()

    print(f"Reading documents from {DOCUMENTS_DIR}...")
    reader = SimpleDirectoryReader(DOCUMENTS_DIR, recursive=True)
    documents = reader.load_data()
    print(f"Loaded {len(documents)} document chunks.")

    print("Connecting to ChromaDB...")
    chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    chroma_collection = chroma_client.get_or_create_collection("prism_fintech")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    print("Embedding documents — this will take a few minutes...")
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True
    )
    print("Done! Prism's knowledge base is ready.")
    return index

if __name__ == "__main__":
    ingest_documents()