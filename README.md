# Local RAG Document Assistant

A simple, offline desktop app that lets you **ask questions about your own documents** — no internet, no cloud.

Upload PDFs, text files, or CSVs. Ask stuff like:  
> _“What’s in my notes about Llama 3.2?”_

It’ll read your files, find the most relevant parts, and give you a clear answer — all running on your system.

---

## Why I built this

As I dive deeper into AI, I’ve been exploring tools like Ollama, RAG, and local AI agents. Instead of just reading about them, I wanted to build something so I created my own personal AI assistant that runs entirely on my system, with full control over the data and logic.

---

## What it does

- ✅ Accepts **PDF, TXT, and CSV** files (drag & drop in the browser)
- ✅ Embeds content locally using **Ollama’s `mxbai-embed-large`**
- ✅ Stores everything in an in-memory **ChromaDB** (no leftover files)
- ✅ Answers questions using **Llama 3.2** — Meta’s lightweight, multilingual Large Language model(LLM)
- ✅ Runs 100% on your local system

## Quickstart
 
 To get started with the Local RAG Document Assistant, follow these steps:
 
 1. Install the required Python libraries listed in `requirements.txt`.
 2. Download the `llama3.2` and `mxbai-embed-large` models from ollama.
 3. Run the application and upload your documents.
 
 ## File Descriptions

- `main.py` — Streamlit app: handles file uploads, saves uploaded files to a temporary folder, creates the retriever, and runs the RAG chain that queries the Ollama LLM.
- `vector_store.py` — Document loader and vector store helper: converts `txt`/`csv`/`pdf` files into `langchain_core.documents.Document` objects, creates embeddings with `OllamaEmbeddings`, and builds an in-memory `Chroma` retriever.
- `requirements.txt` — Contains all the necessary Python libraries for the application.

---

## Models

- `mxbai-embed-large` — embedding model used by `OllamaEmbeddings` to encode document text and queries.
- `llama3.2` — LLM used by `OllamaLLM` to generate answers from the retrieved context.

These model names are the defaults used in `vector_store.py` and `main.py`. If you prefer other models, update the `model=` arguments in those files.

---

## Detailed Quickstart

1. (Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Install and run Ollama (run locally). Follow the official docs: `https://ollama.com/docs`.

4. Pull the models into Ollama (example):

```bash
ollama pull mxbai-embed-large
ollama pull llama3.2
ollama list   # verify installed models
```

5. Start the Streamlit app:

```bash
streamlit run main.py
```

6. In the browser UI, upload one or more `pdf`, `txt`, or `csv` files, type a question, and click **Get Answer**.


 ## Configuration
 
 Ensure that you have the correct model files in the designated directory before running the application.
 
 ## Troubleshooting
 
 If you encounter issues, check the following:
 - Ensure all model files are correctly downloaded.
 - Verify that all required libraries are installed.
 

