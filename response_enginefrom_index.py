import hashlib
import os
from pathlib import Path

import psycopg2
from llama_index.core import StorageContext, VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.chat_engine.types import ChatMode
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.vector_stores.postgres import PGVectorStore
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from tqdm import tqdm
import config
from agent_tools import AgentSetup
from prompt_custom import react_system_prompt
from query_engine_setup import QueryEngineSetup


class ResponseEngine:
    def create_index(self, db_name, documents, embed_size):

        vector_store = PGVectorStore.from_params(
            database=db_name,
            host=config.DB_HOST,
            password=config.DB_PASSWORD_url,
            port=config.DB_PORT,
            user=config.DB_USER,
            table_name="embeddings",
            embed_dim=embed_size,
        )

        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context, show_progress=True
        )
        query_engine = index.as_query_engine(similarity_top_k=5)

        return query_engine

    def load_index(selfself, db_name, embed_size):
        print('Loading index')
        vector_store = PGVectorStore.from_params(
            database=db_name,
            host=config.DB_HOST,
            password=config.DB_PASSWORD_url,
            port=config.DB_PORT,
            user=config.DB_USER,
            table_name="embeddings",
            embed_dim=embed_size,  # openai embedding dimension
        )

        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        query_engine = index.as_query_engine(similarity_top_k=5)

        return query_engine

    def update_vector_db(self, db_name):
        # delete processed_files.txt in root to redo all files
        # this whole section needs to record to the db rather than a damn text file.
        processed_files_record = "processed_files.txt"
        processed_files = set()
        # Load record of processed files if exists
        if os.path.exists(processed_files_record):
            with open(processed_files_record, "r") as file:
                processed_files = set(file.read().splitlines())
        # Scan /markdowns directory and subdirectories for new or updated markdown files
        markdowns_path = Path("markdowns")
        for markdown_file in tqdm(markdowns_path.rglob('*.md')):
            # Create a hash of the file content to detect changes
            # print(f'Hashing file: {markdown_file}')
            file_hash = hashlib.md5(open(markdown_file, "rb").read()).hexdigest()
            record_entry = f"{markdown_file}:{file_hash}"

            if record_entry not in processed_files:
                print(f'\t\tProcessing file: {markdown_file}\n')
                # Process new or updated file
                abc = markdown_file
                # print(f'\nmarkdown_file:{abc}')
                defg = markdown_file.absolute()
                # print(f'\nmarkdown_file.parent:{defg}')
                documents = SimpleDirectoryReader(input_files=[markdown_file.absolute()]).load_data()
                self.create_index(db_name, documents, 1024)  # Or update_index if it exists

                # Add to the set of processed files
                processed_files.add(record_entry)
        # Update the record of processed files
        with open(processed_files_record, "w") as file:
            for record in processed_files:
                file.write(record + "\n")

    def load_index_for_chat(self, db_name, embed_size, llm):
        print('Loading index')
        vector_store = PGVectorStore.from_params(
            database=db_name,
            host=config.DB_HOST,
            password=config.DB_PASSWORD_url,
            port=config.DB_PORT,
            user=config.DB_USER,
            table_name="embeddings",
            embed_dim=embed_size,  # openai embedding dimension
        )

        sys_prompt = ("You are a chatbot, specifically designed to "
                      "advise on how to use the Apteco Orbit platform.  Your answers should only ever be about using "
                      "Apteco software, and most answers can be found from the database. "
                      "An 'Audience', sometimes called a 'Selection' or 'Segment' is created using the Orbit Audiences tool."
                      "Audience, selection and segment are keywords that indicate we should be using Orbit Audiences.Here are the relevant documents for the context:\n"
                      "{context_str}"
                      "\nInstruction: Use the previous chat history, or the context above, to interact and help the user.  Where possible do not repeat earlier answers.")

        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        memory = ChatMemoryBuffer.from_defaults(token_limit=4000)
        chat_engine = index.as_chat_engine(usingOpenAi=False, llm=llm, chat_mode='condense_plus_context',
                                           memory=memory,
                                           system_prompt=sys_prompt, similarity_top_k=5)

        return chat_engine

    def load_index_for_chat_with_react(self, db_name, embed_size, llm):
        print('Loading index')
        vector_store = PGVectorStore.from_params(
            database=db_name,
            host=config.DB_HOST,
            password=config.DB_PASSWORD_url,
            port=config.DB_PORT,
            user=config.DB_USER,
            table_name="embeddings",
            embed_dim=embed_size,  # openai embedding dimension
        )

        sys_prompt = ("You are a chatbot, specifically designed to "
                      "advise on how to use the Apteco Orbit platform.  Your answers should only ever be about using "
                      "Apteco software, and most answers can be found from the database. "
                      "An 'Audience', sometimes called a 'Selection' or 'Segment' is created using the Orbit Audiences tool."
                      "Audience, selection and segment are keywords that indicate we should be using Orbit Audiences.Here are the relevant documents for the context:\n"
                      "{context_str}"
                      "\nInstruction: Use the previous chat history, or the context above, to interact and help the user.  Where possible do not repeat earlier answers.")

        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        memory = ChatMemoryBuffer.from_defaults(token_limit=4000)
        chat_engine = index.as_chat_engine(usingOpenAi=False, llm=llm, chat_mode='react',
                                           memory=memory,
                                           system_prompt=sys_prompt, similarity_top_k=5)

        return chat_engine

    def load_index_for_chat_react_with_functions(self, db_name, embed_size, llm):
        print('Loading index')
        vector_store = PGVectorStore.from_params(
            database=db_name,
            host=config.DB_HOST,
            password=config.DB_PASSWORD_url,
            port=config.DB_PORT,
            user=config.DB_USER,
            table_name="embeddings",
            embed_dim=embed_size,  # openai embedding dimension
        )

#

        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        memory = ChatMemoryBuffer.from_defaults(token_limit=4000)

        # response_engine = index.as_chat_engine(usingOpenAi=False, llm=llm, chat_mode='react', memory=memory,
        #                                        system_prompt=sys_prompt, similarity_top_k=5, verbose=True)

        db_engine = index.as_query_engine(similarity_top_k=10)
        agent_setup = AgentSetup(llm, db_name)
        query_engine_tools = self.get_query_engine_array(llm, db_name, db_engine)
        agent = agent_setup.return_agent(memory, query_engine_tools)

        # agent.update_prompts({"agent_worker:system_prompt": react_system_prompt})
        #
        # abc = agent.agent_worker



        return agent

    def get_query_engine_array(self, llm, db_name, response_engine):

        qes = QueryEngineSetup(llm)
        query_engine_tools = qes.get_query_engine_array(db_name, response_engine)
        return query_engine_tools
