import streamlit as st
import tempfile
import os
from vector_store import create_retriever_from_files
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Title
st.title(" Local RAG Document Assistant")
st.write("Upload **PDF, TXT, or CSV** files. Ask questions — answers come ONLY from your documents.")

# File uploader
uploaded_files = st.file_uploader(
    "Upload your documents", 
    accept_multiple_files=True,
    type=["pdf", "txt", "csv"]
)

# Save uploaded files temporarily
def save_uploaded_files(uploaded_files):
    temp_dir = tempfile.mkdtemp()
    saved_paths = []
    for file in uploaded_files:
        file_path = os.path.join(temp_dir, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        saved_paths.append(file_path)
    return saved_paths

# Only process if files are uploaded
if uploaded_files:
    temp_file_paths = save_uploaded_files(uploaded_files)
    
    # Create retriever from vector_store.py
    with st.spinner("Embedding your documents..."):
        retriever = create_retriever_from_files(temp_file_paths)

    # Build RAG chain
    llm = OllamaLLM(model="llama3.2") 
    prompt = ChatPromptTemplate.from_template(
        "Use ONLY the following context to answer the question. "
        "If the answer isn't in the context, say: 'I don't know based on the provided documents.'\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}"
    )

    def format_docs(docs):
        return "\n\n".join(d.page_content for d in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # User question
    question = st.text_input("Ask a question about your documents:")
    if st.button("Get Answer") and question:
        with st.spinner("Thinking..."):
            answer = rag_chain.invoke(question)
        st.subheader("Answer")
        st.write(answer)