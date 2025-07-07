"""
Base project class for handling different types of RAG projects
"""
import os
import pandas as pd
from abc import ABC, abstractmethod
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
import shutil


class BaseProject(ABC):
    """Base class for all project types"""
    
    def __init__(self, project_name: str, project_dir: str):
        self.project_name = project_name
        self.project_dir = project_dir
        self.csv_file = os.path.join(project_dir, "data.csv")
        self.prompt_file = os.path.join(project_dir, "prompt.txt")
        self.db_location = f"./chrome_langchain_db_{project_name}"
        self.embeddings = OllamaEmbeddings(model="mxbai-embed-large")
        
    @abstractmethod
    def process_row(self, row: pd.Series, index: int) -> Document:
        """Process a single CSV row into a Document object"""
        pass
    
    @abstractmethod
    def get_prompt_template(self) -> ChatPromptTemplate:
        """Return the chat prompt template for this project"""
        pass
    
    def create_vector_store(self, force_refresh: bool = False):
        """Create vector store from CSV data"""
        if not os.path.exists(self.csv_file):
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")
            
        df = pd.read_csv(self.csv_file)
        
        # Delete existing vector store if force_refresh is True
        if force_refresh and os.path.exists(self.db_location):
            print(f"Deleting existing vector store: {self.db_location}")
            shutil.rmtree(self.db_location)

        add_documents = not os.path.exists(self.db_location)
        
        if add_documents:
            documents = []
            ids = []
            
            for i, row in df.iterrows():
                doc = self.process_row(row, i)
                documents.append(doc)
                ids.append(str(i))
            
            # Initialize vector store
            vector_store = Chroma(
                collection_name=self.project_name,
                persist_directory=self.db_location,
                embedding_function=self.embeddings
            )
            
            # Batch insertion for large datasets
            batch_size = self.get_batch_size()
            for start in range(0, len(documents), batch_size):
                end = start + batch_size
                batch_docs = documents[start:end]
                batch_ids = ids[start:end]
                vector_store.add_documents(documents=batch_docs, ids=batch_ids)
        else:
            vector_store = Chroma(
                collection_name=self.project_name,
                persist_directory=self.db_location,
                embedding_function=self.embeddings
            )
        
        return vector_store.as_retriever(search_kwargs={"k": 5})
    
    def get_batch_size(self) -> int:
        """Override in subclasses if different batch size needed"""
        return 1000
