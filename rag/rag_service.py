import os
import shutil
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
# Migrating to langchain_chroma as per the deprecation warning
from langchain_chroma import Chroma


BASE_DIR = Path(__file__).parent.parent
DOCUMENTS_PATH = BASE_DIR / "documents"
VECTOR_DB_PATH = str(Path(__file__).parent / "chroma_db")


def load_documents():

    documents = []

    for file_path in DOCUMENTS_PATH.glob("*.txt"):
        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )
        documents.extend(loader.load())

    return documents


def create_new_database(embeddings):
    """Deletes existing DB if any, and creates a fresh one."""
    if os.path.exists(VECTOR_DB_PATH):
        try:
            shutil.rmtree(VECTOR_DB_PATH)
        except Exception as e:
            print(f"Warning: Could not remove old vector db path: {e}")

    documents = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )
    
    return vector_db


def get_vector_database():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    if os.path.exists(VECTOR_DB_PATH) and os.listdir(VECTOR_DB_PATH):
        try:
            # Attempt to load the existing database
            vector_db = Chroma(
                persist_directory=VECTOR_DB_PATH,
                embedding_function=embeddings
            )
            # Do a tiny test query to ensure it's not corrupted by rust bindings PanicException
            vector_db.similarity_search("test", k=1)
            return vector_db
        except Exception as e:
            print(f"Detected corrupted or incompatible Chroma database: {e}")
            print("Rebuilding Chroma database from source documents...")
            return create_new_database(embeddings)
    else:
        # Create it for the first time
        return create_new_database(embeddings)


def search_documents(query: str, k: int = 3):

    vector_db = get_vector_database()

    results = vector_db.similarity_search(
        query,
        k=k
    )

    return results
