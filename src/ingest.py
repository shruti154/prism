import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import fitz
import chromadb
from llama_index.core import VectorStoreIndex, StorageContext, Settings, Document
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

def load_documents():
    """Load all documents using PyMuPDF for PDFs and plain text for txt files."""
    documents = []
    
    for filename in os.listdir(DOCUMENTS_DIR):
        filepath = os.path.join(DOCUMENTS_DIR, filename)
        
        if filename.endswith('.pdf'):
            print(f"Reading PDF: {filename}")
            try:
                doc = fitz.open(filepath)
                text = ""
                for page in doc:
                    text += page.get_text()
                doc.close()
                
                if text.strip():
                    documents.append(Document(
                        text=text,
                        metadata={"filename": filename, "type": "pdf"}
                    ))
                    print(f"  ✓ Extracted {len(text)} characters")
                else:
                    print(f"  ✗ No text extracted from {filename}")
            except Exception as e:
                print(f"  ✗ Error reading {filename}: {e}")
                
        elif filename.endswith('.txt') or '.' not in filename:
            print(f"Reading text file: {filename}")
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                if text.strip():
                    documents.append(Document(
                        text=text,
                        metadata={"filename": filename, "type": "text"}
                    ))
                    print(f"  ✓ Extracted {len(text)} characters")
            except Exception as e:
                print(f"  ✗ Error reading {filename}: {e}")
    
    return documents

def ingest_documents():
    setup_settings()
    
    print(f"\nReading documents from {DOCUMENTS_DIR}...")
    documents = load_documents()
    print(f"\nLoaded {len(documents)} documents successfully.")
    
    print("\nConnecting to ChromaDB...")
    chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR)
    
    # Clear existing collection and rebuild
    try:
        chroma_client.delete_collection("prism_fintech")
        print("Cleared existing knowledge base.")
    except:
        pass
    
    chroma_collection = chroma_client.get_or_create_collection("prism_fintech")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    print("\nEmbedding documents — this will take several minutes...")
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True
    )
    print("\nDone! Prism's knowledge base is ready.")
    return index

if __name__ == "__main__":
    ingest_documents()