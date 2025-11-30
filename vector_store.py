from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import pandas as pd
import os

def load_documents_from_paths(file_paths: list) -> list:
    """Load .csv, .txt, and .pdf files into LangChain Documents."""
    documents = []
    
    for path in file_paths:
        ext = os.path.splitext(path)[1].lower()

        # Handle TXT/MD
        if ext in [".txt", ".md"]:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            documents.append(Document(page_content=text, metadata={"source": path}))

        # Handle CSV
        elif ext == ".csv":
            df = pd.read_csv(path)
            for idx, row in df.iterrows():
                # Turn each row into readable text
                content = " | ".join(f"{col}: {val}" for col, val in row.items())
                documents.append(Document(
                    page_content=content,
                    metadata={"source": path, "row": idx}
                ))

        # Handle PDF
        elif ext == ".pdf":
            from langchain_community.document_loaders import PyPDFLoader
            loader = PyPDFLoader(path)
            documents.extend(loader.load())  # returns list of Documents

    return documents


def create_retriever_from_files(file_paths: list, k: int = 5):
    """Create an in-memory retriever from uploaded files."""
    docs = load_documents_from_paths(file_paths)
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    vectorstore = Chroma.from_documents(documents=docs, embedding=embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": k})