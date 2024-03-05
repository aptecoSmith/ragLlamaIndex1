import hashlib
import os
import textwrap
from time import time
from pathlib import Path

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext, load_index_from_storage
from llama_index.core.embeddings import resolve_embed_model
from llama_index.core.llms import llm
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.llms.ollama import Ollama


import logging
import sys

from embedding_database import EmbeddingDatabasePgVector
from helpers import string_contains_text
from response_enginefrom_index import ResponseEngine


# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


# bge-m3 embedding model
# Settings.embed_model = resolve_embed_model("local:BAAI/bge-small-en-v1.5")

def basic_example():
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    # ollama pull mistral
    Settings.llm = Ollama(model="mistral", request_timeout=90.0)

    # check if storage already exists
    PERSIST_DIR = "./storage"
    if not os.path.exists(PERSIST_DIR):
        # load the documents and create the index
        documents = SimpleDirectoryReader("data").load_data()
        print("Document ID:", documents[0].doc_id)
        index = VectorStoreIndex.from_documents(documents)
        # store it for later
        index.storage_context.persist(persist_dir=PERSIST_DIR)
        print('Index built')

    else:
        # load the existing index
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)
        print('Index Loaded')

    # #check llm is online
    # response = Settings.llm.complete("Who is Laurie Voss?")
    # print('-----------------------------------------------------------------')
    # print(response)
    # print('-----------------------------------------------------------------')
    # looking_for = 'Voss'
    # contains_word = string_contains_text(response, looking_for)
    #
    #
    # print(f'\t\t\tLLM ONLINE - {contains_word}')
    # print('-----------------------------------------------------------------')

    query_engine = index.as_query_engine()
    print('Asking Question')
    response = query_engine.query("What did the author do growing up?")
    print(textwrap.fill(str(response), 100))


def example_with_pg():
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    # ollama
    Settings.llm = Ollama(model="mistral", request_timeout=90.0)

    db_name = 'vector_db'
    db = EmbeddingDatabasePgVector()
    db.create_db(db_name)

    #load documents from data
    documents = SimpleDirectoryReader("data").load_data()
    print("Document ID:", documents[0].doc_id)

    query_engine = db.create_index(db_name,documents,384)

    #ask the question
    response = query_engine.query("What did the author do?")
    #show the response (about 60 seconds on my pc)
    print(textwrap.fill(str(response), 100))

def example_with_different_embedder():
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="WhereIsAI/UAE-Large-V1", embed_batch_size=10
    )

    # ollama
    Settings.llm = Ollama(model="mistral", request_timeout=90.0)

    db_name = 'vector_db'
    db = EmbeddingDatabasePgVector()
    db.create_db(db_name)

    response_engine = ResponseEngine()

    #load documents from data
    documents = SimpleDirectoryReader("data").load_data()
    print("Document ID:", documents[0].doc_id)

    query_engine = response_engine.create_index(db_name,documents,1024)

    #ask the question
    response = query_engine.query("What did the author do?")
    #show the response (about 60 seconds on my pc)
    print(textwrap.fill(str(response), 100))

def example_with_different_embedder_and_not_ollama():
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="WhereIsAI/UAE-Large-V1", embed_batch_size=10
    )

    # ollama
    #Settings.llm = Ollama(model="mistral", request_timeout=90.0)

    Settings.llm = LlamaCPP(
    # You can pass in the URL to a GGML model to download it automatically
    # model_url='https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf',
    #model_url='https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf',
    # optionally, you can set the path to a pre-downloaded model instead of model_url
    model_path=r"C:\models\mistral\mistral-7b-v0.1.Q8_0.gguf",
    temperature=0.1,
    max_new_tokens=256,
    # llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
    context_window=4096,
    # kwargs to pass to __call__()
    generate_kwargs={},
    # kwargs to pass to __init__()
    # set to at least 1 to use GPU
    model_kwargs={"n_gpu_layers": -1},
    # transform inputs into Llama2 format
    # messages_to_prompt=messages_to_prompt,
    # completion_to_prompt=completion_to_prompt,
    verbose=True,
)

    db_name = 'vector_db'
    db = EmbeddingDatabasePgVector()
    db.create_db(db_name)

    response_engine = ResponseEngine()

    #load documents from data
    documents = SimpleDirectoryReader("data").load_data()
    print("Document ID:", documents[0].doc_id)

    query_engine = response_engine.create_index(db_name,documents,1024)

    #ask the question
    response = query_engine.query("What did the author do?")
    #show the response (about 60 seconds on my pc)
    print(textwrap.fill(str(response), 100))

def example_with_different_embedder_reading_markdown():
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="WhereIsAI/UAE-Large-V1", embed_batch_size=10
    )

    # ollama
    Settings.llm = Ollama(model="mistral", request_timeout=90.0)

    db_name = 'vector_db'
    db = EmbeddingDatabasePgVector()
    db.create_db(db_name)

    response_engine = ResponseEngine()

    #load documents from data
    documents = SimpleDirectoryReader("markdowns",recursive=True).load_data()
    print("Document ID:", documents[0].doc_id)

    query_engine = response_engine.create_index(db_name,documents,1024)

    #ask the question
    response = query_engine.query("What channels can be used in the journey builder?")
    #show the response (about 60 seconds on my pc)
    print(textwrap.fill(str(response), 100))

def example_with_different_embedder_loading_already_embedded_markdown_from_db():
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="WhereIsAI/UAE-Large-V1", embed_batch_size=10
    )

    # ollama
    Settings.llm = Ollama(model="mistral", request_timeout=90.0)

    db_name = 'vector_db'
    db = EmbeddingDatabasePgVector()
    #db.create_db(db_name)

    response_engine = ResponseEngine()

    # #load documents from data
    # documents = SimpleDirectoryReader("markdowns/journeybuilder").load_data()
    # print("Document ID:", documents[0].doc_id)
    #query_engine = db.create_index(db_name,documents,1024)

    query_engine = response_engine.load_index(db_name,1024)

    #ask the question
    response = query_engine.query("What channels can be used in the journey builder?")
    #show the response (about 60 seconds on my pc)
    print(textwrap.fill(str(response), 100))


def process_new_markdown_documents():
    # Initialize embedding model, llm and database
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="WhereIsAI/UAE-Large-V1", embed_batch_size=10
    )

    # ollama
    Settings.llm = Ollama(model="mistral", request_timeout=90.0)

    db_name = 'vector_db'
    db = EmbeddingDatabasePgVector()

    response_engine = ResponseEngine()

    # Assuming db.load_index() method loads the existing embeddings index
    query_engine = response_engine.load_index(db_name, 1024)

#this whole section needs to record to the db rather than a damn text file.
    processed_files_record = "processed_files.txt"
    processed_files = set()

    # Load record of processed files if exists
    if os.path.exists(processed_files_record):
        with open(processed_files_record, "r") as file:
            processed_files = set(file.read().splitlines())

    # Scan /markdowns directory and subdirectories for new or updated markdown files
    markdowns_path = Path("markdowns")
    for markdown_file in markdowns_path.rglob('*.md'):
        # Create a hash of the file content to detect changes
        print(f'Hashing file: {markdown_file}')
        file_hash = hashlib.md5(open(markdown_file, "rb").read()).hexdigest()
        record_entry = f"{markdown_file}:{file_hash}"

        if record_entry not in processed_files:
            print(f'Processing file: {markdown_file}')
            # Process new or updated file
            documents = SimpleDirectoryReader(markdown_file.parent).load_data()
            db.create_index(db_name, documents, 1024)  # Or update_index if it exists

            # Add to the set of processed files
            processed_files.add(record_entry)

    # Update the record of processed files
    with open(processed_files_record, "w") as file:
        for record in processed_files:
            file.write(record + "\n")

    # Example usage of the updated database
    response = query_engine.query("How do I get an audience of 100 Ford drivers?")
    print(textwrap.fill(str(response), 100))



def chat_style_process_new_markdown_documents():
    # Initialize embedding model, llm and database
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="WhereIsAI/UAE-Large-V1", embed_batch_size=10
    )

    # ollama
    Settings.llm = Ollama(model="mistral", request_timeout=90.0)

    db_name = 'vector_db'
    db = EmbeddingDatabasePgVector()

    response_engine = ResponseEngine()

    # Assuming db.load_index() method loads the existing embeddings index
    chat_engine = response_engine.load_index_for_chat(db_name, 1024, llm=Settings.llm)

    response_engine.update_vector_db(db, db_name)

    # Example usage of the updated database
    response = chat_engine.chat("How do I get an audience of 100 Ford drivers?")
    print(textwrap.fill(str(response), 100))
    print('\n')

    # Example usage of the updated database
    response = chat_engine.chat("How exactly do I know there is 100?")
    print(textwrap.fill(str(response), 100))
    print('\n')

    # # Example usage of the updated database
    # response = query_engine.query("How can I see other attributes of these people?")
    # print(textwrap.fill(str(response), 100))
    #
    # # Example usage of the updated database
    # response = query_engine.query("Right but I want to check that these people really do drive Fords")
    # print(textwrap.fill(str(response), 100))
    #
    # response = query_engine.query("The people in my audience")
    # print(textwrap.fill(str(response), 100))

def chat_style_process_new_markdown_documents_with_other_models():
    # Initialize embedding model, llm and database
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="WhereIsAI/UAE-Large-V1", embed_batch_size=10
    )

    # ollama
    #mixtral uses much more RAM - 26gb
    #trialling as mistral seems to be hallucinating some details
    #Settings.llm = Ollama(model="mixtral", request_timeout=180.0)

    Settings.llm = Ollama(model="mistral", request_timeout=180.0)

    db_name = 'vector_db'
    db = EmbeddingDatabasePgVector()

    response_engine = ResponseEngine()

    # Assuming db.load_index() method loads the existing embeddings index
    chat_engine = response_engine.load_index_for_chat(db_name, 1024, llm=Settings.llm)

    response_engine.update_vector_db(db, db_name)
    begins = time()
    print(begins)
    # Example usage of the updated database
    print('Asking Question')
    response = chat_engine.chat("How do I get an audience of 100 Ford drivers?")
    print(textwrap.fill(str(response), 100))
    print('\n')

    print('Asking Question')
    # Example usage of the updated database
    response = chat_engine.chat("How exactly do I know there is 100?")
    print(textwrap.fill(str(response), 100))
    print('\n')
    ends = time()
    print(ends)
    duration = ends-begins
    print(duration)

    # # Example usage of the updated database
    # response = query_engine.query("How can I see other attributes of these people?")
    # print(textwrap.fill(str(response), 100))
    #
    # # Example usage of the updated database
    # response = query_engine.query("Right but I want to check that these people really do drive Fords")
    # print(textwrap.fill(str(response), 100))
    #
    # response = query_engine.query("The people in my audience")
    # print(textwrap.fill(str(response), 100))


def react_chat_style_process_new_markdown_documents_with_other_models():
    # Initialize embedding model, llm and database
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="WhereIsAI/UAE-Large-V1", embed_batch_size=10
    )

    # ollama
    #mixtral uses much more RAM - 26gb
    #trialling as mistral seems to be hallucinating some details
    #Settings.llm = Ollama(model="mixtral", request_timeout=180.0)

    Settings.llm = Ollama(model="mistral", request_timeout=180.0)

    db_name = 'vector_db'
    db = EmbeddingDatabasePgVector()

    response_engine = ResponseEngine()

    # Assuming db.load_index() method loads the existing embeddings index
    chat_engine = response_engine.load_index_for_chat_react_with_functions(db_name, 1024, llm=Settings.llm)

    response_engine.update_vector_db(db, db_name)


    question = "How do I get an audience of 100 Ford drivers?"
    print(f'Asking Question:\t {question}')
    response = chat_engine.chat(question)
    print(textwrap.fill(str(response), 100))
    print('\n')

    question = "How exactly do I know there is 100?"
    print(f'Asking Question:\t {question}')
    response = chat_engine.chat(question)
    print(textwrap.fill(str(response), 100))
    print('\n')

    question = "Can you give me exact instructions?"
    print(f'Asking Question:\t {question}')
    # Example usage of the updated database
    response = chat_engine.chat(question)
    print(textwrap.fill(str(response), 100))
    print('\n')
    #
    # # Example usage of the updated database
    # response = query_engine.query("Right but I want to check that these people really do drive Fords")
    # print(textwrap.fill(str(response), 100))
    #
    # response = query_engine.query("The people in my audience")
    # print(textwrap.fill(str(response), 100))


def react_functions_chat_style_process_new_markdown_documents_with_other_models():
    # Initialize embedding model, llm and database
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="WhereIsAI/UAE-Large-V1", embed_batch_size=10
    )

    # ollama
    #mixtral uses much more RAM - 26gb
    #trialling as mistral seems to be hallucinating some details
    #Settings.llm = Ollama(model="mixtral", request_timeout=180.0)

    Settings.llm = Ollama(model="mistral", request_timeout=180.0)

    db_name = 'vector_db'
    db = EmbeddingDatabasePgVector()

    response_engine = ResponseEngine()

    # Assuming db.load_index() method loads the existing embeddings index
    chat_engine = response_engine.load_index_for_chat_react_with_functions(db_name, 1024, llm=Settings.llm)

    response_engine.update_vector_db(db, db_name)


    question = "How do I get an audience of 100 Ford drivers?"
    print(f'Asking Question:\t {question}')
    response = chat_engine.chat(question)
    print(textwrap.fill(str(response), 100))
    print('\n')

    question = "How exactly do I know there is 100?"
    print(f'Asking Question:\t {question}')
    response = chat_engine.chat(question)
    print(textwrap.fill(str(response), 100))
    print('\n')

    question = "Can you give me exact instructions?"
    print(f'Asking Question:\t {question}')
    # Example usage of the updated database
    response = chat_engine.chat(question)
    print(textwrap.fill(str(response), 100))
    print('\n')
    #
    # # Example usage of the updated database
    # response = query_engine.query("Right but I want to check that these people really do drive Fords")
    # print(textwrap.fill(str(response), 100))
    #
    # response = query_engine.query("The people in my audience")
    # print(textwrap.fill(str(response), 100))


def possibly_chat_mode():
    # Initialize embedding model, llm and database
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="WhereIsAI/UAE-Large-V1", embed_batch_size=10
    )

    # ollama
    #mixtral uses much more RAM - 26gb
    #trialling as mistral seems to be hallucinating some details
    #Settings.llm = Ollama(model="mixtral", request_timeout=180.0)

    Settings.llm = Ollama(model="mistral", request_timeout=180.0)

    db_name = 'vector_db'
    db = EmbeddingDatabasePgVector()

    response_engine = ResponseEngine()

    # Assuming db.load_index() method loads the existing embeddings index
    chat_engine = response_engine.load_index_for_chat_react_with_functions(db_name, 1024, llm=Settings.llm)

    response_engine.update_vector_db(db, db_name)

    chat_engine.chat_repl()




#slower as you get more complex!
###
#Persists embeddings to the storage folder
# uses a smaller embedding model
# embeds a single text file in the data dir
#uses ollama
#basic_example()

# Persists embeddings to a postgres vector database
# You need to have setup pgVector
# uses the same smaller embedding model
# embeds a single text file in the data dir
# uses ollama
#example_with_pg()

#uses an embedder from higher in the list.  Note that the embedding dimensions has changed
#https://huggingface.co/spaces/mteb/leaderboard

#example_with_different_embedder()

#whilst the simple examples use ollama, it is suggested that production would use LlamaCpp
#I don't know the particular pros and cons as yet
#example_with_different_embedder_and_not_ollama()


#example_with_different_embedder_reading_markdown()
#result - The Orbit Campaign Journey Builder supports various channel outputs for communication, including
#FTP, file, and email channels.


#much quicker
#example_with_different_embedder_loading_already_embedded_markdown_from_db()

#process_new_markdown_documents()

#chat_style_process_new_markdown_documents()

#ollama pull mixtral

chat_style_process_new_markdown_documents_with_other_models()

#this isn't providing as good an answer as above - something about the thoughts and actions I think I might not have set up enough
#react_chat_style_process_new_markdown_documents_with_other_models()

#possibly_chat_mode()

