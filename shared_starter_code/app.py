import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq

def get_answer(user_question, chat_history):
    # Setup paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DOCS_FOLDER = os.path.join(BASE_DIR, "../docs")
    CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Load/Create Vector Store
    if os.path.exists(CHROMA_DIR) and os.listdir(CHROMA_DIR):
        vectorstore = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    else:
        docs = []
        for file in os.listdir(DOCS_FOLDER):
            path = os.path.join(DOCS_FOLDER, file)
            if file.endswith(".pdf"): docs.extend(PyPDFLoader(path).load())
            elif file.endswith(".txt"): docs.extend(TextLoader(path).load())
        
        splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
        vectorstore = Chroma.from_documents(documents=splitter.split_documents(docs), 
                                          embedding=embeddings, 
                                          persist_directory=CHROMA_DIR)

    # Retrieval & LLM
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    context_docs = retriever.invoke(user_question)
    context_text = "\n\n".join([d.page_content for d in context_docs])
    
    llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0)
    prompt = f"Context: {context_text}\nQuestion: {user_question}\nAnswer:"
    
    response = llm.invoke(prompt)
    return response.content
