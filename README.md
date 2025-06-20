# TalkToPDF

A local Retrieval-Augmented Generation (RAG) application that allows you to chat with your PDF documents using Ollama and LangChain.

## Overview

TalkToPDF enables you to:
- Upload PDF documents to your personal knowledge base
- Ask questions about your documents in natural language
- Receive accurate answers based on the content of your PDFs
- Keep all data processing local for privacy

## Prerequisites

### For Linux Users
- Python 3.12 or higher
- [Ollama](https://ollama.com) installed

### For Windows Users
- Python 3.12 or higher
- [Ollama for Windows](https://ollama.com/download/windows)
- Git Bash or WSL (Windows Subsystem for Linux) recommended for command execution

## Installation

### Step 1: Clone or Download Project

```bash
git clone <repository-url>
# OR
mkdir TalkToPDF
cd TalkToPDF
# Then copy the project files
```

### Step 2: Set Up Python Environment

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# Linux/macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install streamlit langchain-core langchain-community chromadb pypdf langchain-ollama langchain-chroma
```

Alternatively, use the requirements.txt file:
```bash
pip install -r requirements.txt
```

### Step 4: Install and Configure Ollama

#### Linux Users:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Windows Users:
1. Download and install Ollama from [ollama.com/download/windows](https://ollama.com/download/windows)
2. After installation, run Ollama from the Start menu
3. Verify Ollama is running by checking if it appears in your system tray

### Step 5: Download Required Models

Open a terminal/command prompt and run:
```bash
# Download language models for answering questions
ollama pull tinyllama
ollama pull llama2
ollama pull mistral
ollama pull gemma 

# Download embedding model for document indexing
ollama pull nomic-embed-text
```

## Project Setup

### Step 1: Organize Your Documents

1. Create a directory for your PDF documents:
```bash
mkdir pdf-docs
```

2. Add your PDF files to the `pdf-docs` directory
   - You can use documents directly related to your topic of interest
   - The system works best with text-based PDFs (not scanned images)

### Step 2: Create Vector Database

Run the loading script to process your PDFs and create the vector database:

```bash
python load.py
```

This script will:
- Validate your `pdf-docs` directory
- Load all PDFs from this directory
- Split documents into manageable chunks
- Create embeddings for each chunk
- Store everything in a ChromaDB vector database

You should see a confirmation message when the process completes successfully.

### Step 3: Launch the Application

Start the Streamlit web interface:

```bash
streamlit run app.py
```

The application will open in your default web browser (typically at http://localhost:8501).

## Using TalkToPDF

1. When the application loads, you'll see a chat interface
2. Type your question about the content of your PDFs in the input field
3. Press Enter to submit your query
4. The system will:
   - Search for relevant passages in your documents
   - Use the language model to generate a response based on those passages
   - Display the answer in the chat window

## Project Structure

```
TalkToPDF/
├── app.py              # Streamlit chat application
├── load.py             # PDF processing and database creation
├── pdf-docs/           # Directory for your PDF files
├── chromadb/           # Vector database storage (created automatically)
├── requirements.txt    # Package dependencies
└── README.md           # This documentation file
```

## Troubleshooting

### Common Issues on Linux

- **Permission denied errors**: 
  ```bash
  sudo chown -R $(whoami) ./chromadb
  ```

- **Model not found errors**:
  ```bash
  ollama list  # Check if models are installed
  ollama pull tinyllama  # Pull missing models
  ollama pull mistral
  ollama pull gemma
  ollama pull llama2
  ollama pull nomic-embed-text
  ```

### Common Issues on Windows

- **Ollama connection errors**:
  - Ensure Ollama is running (check system tray)
  - Verify in Task Manager that the Ollama service is active
  - Try restarting Ollama

- **Path issues**:
  - Use forward slashes `/` in paths
  - Avoid spaces in directory names

- **Python environment issues**:
  - Use `python -m pip install` instead of just `pip install`
  - Ensure your PATH includes Python and the virtual environment

## How It Works

1. **Document Processing**:
   - PDFs are loaded and split into smaller chunks
   - Each chunk is converted into vector embeddings

2. **Query Processing**:
   - When you ask a question, it's converted to the same vector space
   - The system finds the most similar document chunks
   - These relevant chunks provide context to the language model

3. **Response Generation**:
   - The language model (tinyllama) generates an answer based on:
     - Your question
     - The retrieved document context

## Customization

- **Change Chunking Parameters**: Edit `load.py` to modify `chunk_size` and `chunk_overlap` for different document segmentation
- **Switch Language Models**: Edit `app.py` to use different Ollama models
- **Adjust Retrieval Settings**: Modify the retriever parameters in `app.py` for different search behaviors

## Privacy Note

All processing happens locally on your machine. Your documents and queries never leave your computer, making this a privacy-friendly solution for document question-answering.

