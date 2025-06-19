import sys
import os
os.environ["ANONYMIZED_TELEMETRY"] = "false"

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.chains import ConversationalRetrievalChain
from langchain_chroma import Chroma
from langchain.memory import ConversationBufferMemory

# Page configuration
st.set_page_config(page_title="Chat Application")
st.header("Chat :blue[Application]")

# Add a sidebar for configuration
st.sidebar.title("Configuration")
model_option = st.sidebar.selectbox(
    "Select Language Model",
    ["tinyllama", "llama2", "mistral", "gemma"],
    index=0
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "ai", "content": "Hello!! Welcome to your private Gen AI Bot"}]

# Display chat history
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# Get user input
prompt = st.chat_input("Add your prompt here")

# Initialize LLM with selected model
ollama = OllamaLLM(base_url='http://localhost:11434', model=model_option)

# Initialize vector database
vector_db = Chroma(
    persist_directory="./chromadb",
    embedding_function=OllamaEmbeddings(model="nomic-embed-text"),
    collection_name="jay-rag2"
)

# Add memory to your chain
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)

# Create QA chain with memory
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=ollama,
    retriever=vector_db.as_retriever(),
    memory=memory,
    return_source_documents=True
)

# Process user input and generate response
if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Thinking..."):
        output = qa_chain.invoke({"question": prompt})
        answer = output["answer"]

    st.chat_message("ai").write(answer)
    st.session_state.messages.append({"role": "ai", "content": answer})

    # Show sources
    with st.expander("Sources"):
        for i, doc in enumerate(output["source_documents"]):
            st.markdown(f"**Source {i+1}**")
            st.markdown(f"Page: {doc.metadata.get('page', 'Unknown')}")
            st.markdown(f"Source: {doc.metadata.get('source', 'Unknown')}")
            st.text(doc.page_content[:200] + "...")
