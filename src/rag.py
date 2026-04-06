from typing import Optional
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFacePipeline
from langchain.llms.base import LLM
from transformers import pipeline
import torch
from src.config import HUGGINGFACEHUB_API_TOKEN, CHROMA_PERSIST_DIR_RAG
from src.embeddings import load_vectorstore, create_embeddings


class MockLLM(LLM):
    """Mock LLM for testing when model loading fails."""
    
    @property
    def _llm_type(self) -> str:
        return "mock"
    
    def _call(self, prompt: str, stop=None, **kwargs) -> str:
        """Generate a mock response based on the prompt."""
        if "price" in prompt.lower():
            return "Based on the financial data, the current price is around $150."
        elif "news" in prompt.lower():
            return "Recent news shows positive sentiment with strong earnings reports."
        elif "market cap" in prompt.lower():
            return "The market cap indicates a strong valuation of approximately $2.4 trillion."
        else:
            return "This is a relevant response to your question about the financial data."


def create_mock_llm():
    """Create a mock LLM for demo purposes."""
    return MockLLM()


def create_llm(
    model_id: str = "mistralai/Mistral-7B-Instruct-v0.1",
    temperature: float = 0.3,
    max_length: int = 512
):
    """
    Create a HuggingFace LLM instance using local pipeline.
    
    Args:
        model_id: HuggingFace model ID
        temperature: Temperature for generation (0.0-1.0)
        max_length: Maximum length of generated text
        
    Returns:
        HuggingFacePipeline LLM instance or MockLLM if loading fails
    """
    print(f"  Loading model {model_id}... (this may take a moment)")
    
    try:
        # Determine device
        try:
            device = 0 if torch.cuda.is_available() else -1
        except:
            device = -1
        
        # Create text generation pipeline
        hf_pipeline = pipeline(
            "text-generation",
            model=model_id,
            device=device,
            max_new_tokens=max_length,
            temperature=temperature,
            top_p=0.95
        )
        
        llm = HuggingFacePipeline(
            model=hf_pipeline,
            model_kwargs={
                "temperature": temperature,
                "max_length": max_length
            }
        )
        
        return llm
    except Exception as e:
        print(f"  ⚠️  Could not load transformer model: {str(e)[:100]}")
        print(f"  Using mock LLM for demo purposes...")
        return create_mock_llm()


def build_rag_chain(
    vectorstore,
    model_id: str = "mistralai/Mistral-7B-Instruct-v0.1",
    chain_type: str = "stuff",
    temperature: float = 0.3,
    max_length: int = 512,
    k: int = 4
):
    """
    Build a RetrievalQA chain.
    
    Args:
        vectorstore: Chroma vectorstore
        model_id: HuggingFace model ID
        chain_type: Type of chain (stuff, map_reduce, refine, map_rerank)
        temperature: Temperature for generation
        max_length: Maximum length of generated text
        k: Number of documents to retrieve
        
    Returns:
        RetrievalQA chain instance
    """
    # Create LLM
    llm = create_llm(
        model_id=model_id,
        temperature=temperature,
        max_length=max_length
    )
    
    # Create retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )
    
    # Create RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type=chain_type,
        retriever=retriever,
        return_source_documents=True,
        verbose=False
    )
    
    return qa_chain


def query_rag(qa_chain, query: str) -> dict:
    """
    Query the RAG chain.
    
    Args:
        qa_chain: RetrievalQA chain instance
        query: User query string
        
    Returns:
        Dictionary with 'answer' and 'source_documents' keys
    """
    result = qa_chain({"query": query})
    return result


def load_and_query(
    query: str,
    model_id: str = "mistralai/Mistral-7B-Instruct-v0.1",
    persist_directory: str = CHROMA_PERSIST_DIR_RAG,
    collection_name: str = "financial_docs",
    temperature: float = 0.3,
    max_length: int = 512,
    k: int = 4
) -> dict:
    """
    Complete pipeline: load vectorstore, build RAG chain, and query.
    
    Args:
        query: User query string
        model_id: HuggingFace model ID
        persist_directory: Directory where vectorstore is persisted
        collection_name: Name of the collection
        temperature: Temperature for generation
        max_length: Maximum length of generated text
        k: Number of documents to retrieve
        
    Returns:
        Dictionary with 'answer' and 'source_documents' keys
    """
    # Load embeddings
    embeddings = create_embeddings()
    
    # Load vectorstore
    vectorstore = load_vectorstore(
        embeddings=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name
    )
    
    if vectorstore is None:
        raise ValueError(f"Vectorstore not found at {persist_directory}")
    
    # Build RAG chain
    qa_chain = build_rag_chain(
        vectorstore=vectorstore,
        model_id=model_id,
        temperature=temperature,
        max_length=max_length,
        k=k
    )
    
    # Query
    result = query_rag(qa_chain, query)
    
    return result


def format_result(result: dict) -> str:
    """
    Format the RAG result for display.
    
    Args:
        result: Result dictionary from RAG chain
        
    Returns:
        Formatted string
    """
    output = "Answer:\n"
    output += "-" * 50 + "\n"
    output += result.get("result", "No answer found") + "\n"
    output += "-" * 50 + "\n"
    
    if "source_documents" in result:
        output += f"\nSource Documents ({len(result['source_documents'])}):\n"
        for i, doc in enumerate(result["source_documents"], 1):
            output += f"\n{i}. {doc.page_content[:200]}...\n"
            if doc.metadata:
                output += f"   Metadata: {doc.metadata}\n"
    
    return output
