from langchain_community.document_loaders import DirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant

def template_retriever(directory_path: str, search_k: int = 1):
    """
    This function retrieves templates from a given directory path using specified embedding models 
    and returns a retriever object.

    Args:
        path (str): The path to the directory containing templates.
        model_name (str, optional): The name of the HuggingFace embedding model to use. Default is "sentence-transformers/all-mpnet-base-v2".
        search_k (int, optional): The number of top-k similar items to retrieve. Default is 1.

    Returns:
        retriever: The retriever object for retrieving similar templates.
    """
    loader = DirectoryLoader(path=directory_path)
    load_applications = loader.load()

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        encode_kwargs={'normalize_embeddings': False}
    )

    vectorstore = Qdrant.from_documents(
        documents=load_applications,
        embedding=embedding_model,
        location=":memory:"
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={'k': search_k}
    )
    
    return retriever
