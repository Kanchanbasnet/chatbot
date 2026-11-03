
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    
vector_store = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory="./vectorstores",
)


def ingestion_pipeline(text: str, document_id: int, conversation_id: int, filename: str):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    metadatas = [
        {
            "document_id": document_id,
            "conversation_id": conversation_id,
            "filename": filename,
        }
        for _ in chunks
    ]
    
    
    vector_store.add_texts(texts=chunks, metadatas=metadatas)
    
    
    
    
    