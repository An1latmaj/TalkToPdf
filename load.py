import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# Disable Telemetry Posting for Chroma
os.environ["ANONYMIZED_TELEMETRY"] = "false"

# Check if the './pdf-docs' directory exists
if not os.path.exists("./pdf-docs"):
    raise FileNotFoundError("The './pdf-docs' directory does not exist. Please create it and add PDF files.")
pdf_loader = PyPDFDirectoryLoader("./pdf-docs")
documents = pdf_loader.load()

if not documents:
    raise ValueError("No documents found. Ensure the './pdf-docs' directory contains valid PDF files.")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
all_documents = text_splitter.split_documents(documents)
print(f"Total number of documents: {len(all_documents)}")
vector_db = Chroma.from_documents(
    persist_directory="./chromadb",
    documents=all_documents,
    embedding=OllamaEmbeddings(model="nomic-embed-text"),
    collection_name="jay-rag2")

print("Vector database created and persisted successfully.")