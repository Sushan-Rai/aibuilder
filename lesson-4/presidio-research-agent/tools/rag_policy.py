import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.tools import create_retriever_tool

def create_hr_rag_tool():
    """Builds an on-the-fly VectorDB store over corporate HR files and presents it as a tool."""
    pdf_path = "data/hr_policies.pdf"
    
    if not os.path.exists(pdf_path):
        os.makedirs("data", exist_ok=True)
        with open(pdf_path, "w") as f:
            f.write("Placeholder compliance text: AI data handling rules dictate all models must protect PII.")

    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    splits = text_splitter.split_documents(docs)
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
    
    rag_tool = create_retriever_tool(
        retriever,
        name="search_hr_policies",
        description="Searches internal HR policy, data management compliance, and hiring rules documents."
    )
    return rag_tool