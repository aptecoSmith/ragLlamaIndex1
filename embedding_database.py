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


class EmbeddingDatabasePgVector:
    def __init__(self):
        self.connect_db()

    def connect_db(self):
        self.connection = psycopg2.connect(dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD,
                                           host=config.DB_HOST, port=config.DB_PORT)
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()

    def create_db(self, db_name):
        try:
            self.cursor.execute(f"CREATE EXTENSION IF NOT EXISTS vector;")
            self.cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
            self.cursor.execute(f"CREATE DATABASE {db_name}")
        except Exception as e:
            print(e)


