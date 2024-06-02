import os
from flask import jsonify
from langchain_community.document_loaders import PyPDFLoader, CSVLoader, JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

def add_file_to_vector_db(file_path, file_type, collection_name):
    """
    Adds the contents of the uploaded file to the VectorDB after loading and splitting the text data.

    Args:
    file_path: The path to the saved file.
    file_type: The type of the file (pdf, json, csv).
    collection_name: Rag collection name

    Returns:
    A Flask response object with a JSON payload indicating success or failure.
    """
    # Load the file using the appropriate loader based on file type
    loader = get_loader(file_type, file_path)
    if not loader:
        return jsonify(error="Unsupported file type"), 400

    data = loader.load()

    # Split and chunk the text data
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(data)

    # Initialize the embeddings and vector database
    vector_db = Chroma.from_documents(
        persist_directory=os.path.dirname(file_path),
        documents=chunks,
        embedding=OllamaEmbeddings(model="nomic-embed-text",show_progress=True),
        collection_name=collection_name
    )

    return jsonify(message="File chunks added to VectorDB successfully"), 200

def get_loader(file_type, file_path):
    """
    Returns the appropriate loader for the given file type.

    Args:
    file_type: The type of the file (pdf, json, csv).
    file_path: The path to the saved file.

    Returns:
    An instance of the appropriate loader, or None if the file type is unsupported.
    """
    if file_type == 'pdf':
        return PyPDFLoader(file_path)
    elif file_type == 'csv':
        return CSVLoader(file_path)
    elif file_type == 'json':
        return JSONLoader(file_path)
    else:
        return None