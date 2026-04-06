import os
from typing import List, Optional
import pandas as pd
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from src.config import CHROMA_PERSIST_DIR, CHROMA_PERSIST_DIR_RAG


def create_embeddings(model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    """
    Create a HuggingFace embeddings model.
    
    Args:
        model_name: Name of the sentence transformer model
        
    Returns:
        HuggingFaceEmbeddings instance
    """
    embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return embeddings


def create_documents_from_dataframe(
    df: pd.DataFrame,
    content_column: str = "combined_text",
    metadata_columns: Optional[List[str]] = None
) -> List[Document]:
    """
    Create LangChain Document objects from a DataFrame.
    
    Args:
        df: Input DataFrame
        content_column: Column name to use as document content
        metadata_columns: List of column names to include as metadata
        
    Returns:
        List of Document objects
    """
    documents = []
    
    if content_column not in df.columns:
        raise ValueError(f"Column '{content_column}' not found in DataFrame")
    
    if metadata_columns is None:
        metadata_columns = []
    
    for idx, row in df.iterrows():
        content = str(row[content_column])
        
        # Skip empty content
        if not content or content.strip() == "":
            continue
        
        metadata = {}
        for col in metadata_columns:
            if col in df.columns:
                metadata[col] = str(row[col])
        
        metadata['source_index'] = idx
        
        doc = Document(page_content=content, metadata=metadata)
        documents.append(doc)
    
    return documents


def create_vectorstore(
    documents: List[Document],
    embeddings,
    persist_directory: str = CHROMA_PERSIST_DIR,
    collection_name: str = "financial_docs"
):
    """
    Create a Chroma vectorstore from documents.
    
    Args:
        documents: List of Document objects
        embeddings: Embeddings model
        persist_directory: Directory to persist the vectorstore
        collection_name: Name of the collection
        
    Returns:
        Chroma vectorstore instance
    """
    # Create persist directory if it doesn't exist
    os.makedirs(persist_directory, exist_ok=True)
    
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name
    )
    
    return vectorstore


def load_vectorstore(
    embeddings,
    persist_directory: str = CHROMA_PERSIST_DIR,
    collection_name: str = "financial_docs"
):
    """
    Load an existing Chroma vectorstore.
    
    Args:
        embeddings: Embeddings model
        persist_directory: Directory where the vectorstore is persisted
        collection_name: Name of the collection
        
    Returns:
        Chroma vectorstore instance or None if not found
    """
    if not os.path.exists(persist_directory):
        return None
    
    try:
        vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings,
            collection_name=collection_name
        )
        return vectorstore
    except Exception as e:
        print(f"Error loading vectorstore: {e}")
        return None


def add_documents_to_vectorstore(
    vectorstore,
    documents: List[Document],
    embeddings
):
    """
    Add new documents to an existing vectorstore.
    
    Args:
        vectorstore: Existing Chroma vectorstore
        documents: List of new Document objects
        embeddings: Embeddings model
        
    Returns:
        Updated vectorstore
    """
    vectorstore.add_documents(documents)
    return vectorstore


def build_vectorstore_from_dataframe(
    df: pd.DataFrame,
    content_column: str = "combined_text",
    metadata_columns: Optional[List[str]] = None,
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    persist_directory: str = CHROMA_PERSIST_DIR,
    collection_name: str = "financial_docs"
):
    """
    Complete pipeline to build a vectorstore from a DataFrame.
    
    Args:
        df: Input DataFrame
        content_column: Column name to use as document content
        metadata_columns: List of column names to include as metadata
        model_name: Name of the sentence transformer model
        persist_directory: Directory to persist the vectorstore
        collection_name: Name of the collection
        
    Returns:
        Tuple of (vectorstore, embeddings)
    """
    # Create embeddings
    embeddings = create_embeddings(model_name)
    
    # Create documents
    documents = create_documents_from_dataframe(
        df,
        content_column=content_column,
        metadata_columns=metadata_columns
    )
    
    if not documents:
        raise ValueError("No documents created from DataFrame")
    
    # Create vectorstore
    vectorstore = create_vectorstore(
        documents=documents,
        embeddings=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name
    )
    
    return vectorstore, embeddings
