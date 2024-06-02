from flask import jsonify
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from flask import current_app

def handle_question(request):
    """
    Processes a user's question by invoking a retrieval-augmented generation (RAG) chain.
    The function initializes the necessary components to retrieve relevant documents from
    a vector database and generate a response to the question using a language model.

    Args:
    request: The Flask request object containing the JSON payload with the 'question'
    and 'collection_name' parameters.

    Returns:
    A Flask response object with a JSON payload containing the answer.
    """

    # Extract the question and collection name from the request
    content = request.json
    question = content['question']
    collection_name = content['collection_name']
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']

    if not question:
        return jsonify(error="Invalid or missing 'question' parameter."), 400

    if not collection_name:
        return jsonify(error="Invalid or missing 'collection_name' parameter."), 400

    # Initialize the vector database with the specified collection
    vector_db = Chroma(
        persist_directory=UPLOAD_FOLDER, 
        collection_name=collection_name, 
        embedding_function=OllamaEmbeddings(model="nomic-embed-text",show_progress=True)
    )

    # Initialize the language model from Ollama with the specified model
    llm = ChatOllama(model="llama3")

    # Define the query prompt template for the retriever
    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""You are an AI language model assistant. Your task is to generate five
        different versions of the given user question to retrieve relevant documents from
        a vector database. By generating multiple perspectives on the user question, your
        goal is to help the user overcome some of the limitations of the distance-based
        similarity search. Provide these alternative questions separated by newlines.
        Original question: {question}""",
    )

    # Initialize the retriever with the query prompt template
    retriever = MultiQueryRetriever.from_llm(
        vector_db.as_retriever(),
        llm,
        prompt=QUERY_PROMPT
    )

    template = """Answer the question based ONLY on the following context:
    {context}
    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)


    # Create the chain for the retrieval-augmented generation
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Invoke the chain with the user's question and retrieve the response
    response = chain.invoke(question)

    print(response)
    # Return the response in a JSON format
    return jsonify(answer=response), 200
