import chromadb
from chromadb.config import Settings
import os
import logging
from pathlib import Path
from typing import Dict
import traceback


logger = logging.getLogger(__name__)


class ChromaDBManager:
    def __init__(self, persist_directory="processed_documents/chroma_db"):
        """
        Initialize ChromaDB with persistent storage
        
        Args:
            persist_directory: Directory to store the database
        """
        # self.persist_directory = persist_directory
        # Convert to absolute path and make sure it exists
        self.persist_directory = str(Path(persist_directory).resolve())
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize ChromaDB client with persistent storage
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # Create or get the collection
        self.collection = self.client.get_or_create_collection(
            name="conversation_embeddings",
            metadata={"description": "Processed conversation embeddings and feedback"}
        )
        
        # Verify collection
        logger.info(f"ChromaDB collection initialized at: {persist_directory}")
        logger.info(f"Collection name: {self.collection.name}")
        logger.info(f"Collection count: {self.collection.count()}")
    
    def add_documents(self, documents, metadatas=None, ids=None, embeddings=None):
        """
        Add documents to the collection
        
        Args:
            documents: List of text documents
            metadatas: List of metadata dictionaries
            ids: List of document IDs
            embeddings: List of embeddings
        """
        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids,
                embeddings=embeddings
            )
            logger.info(f"Added {len(documents)} documents to collection")
            logger.info(f"New collection count: {self.collection.count()}")
        except Exception as e:
            logger.error(f"Error adding documents to collection: {str(e)}")
            raise
    
    def query(self, query_text, n_results=5):
        """
        Query the collection
        
        Args:
            query_text: Text to search for
            n_results: Number of results to return
            
        Returns:
            Dictionary containing results
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results
    
    def get_context(self, query_text: str, n_results: int = 3) -> Dict:
        """
        Retrieve context from ChromaDB for RAG.

        Args:
            query_text: Text to search for
            n_results: Number of results to return
            
        Returns:
            Dictionary containing results
        """
        logger.info(f"ChromaDB: Retrieving context for query: '{query_text[:100]}...'")
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            # Logging how many documents were actually found for this query
            num_found = len(results.get('documents', [[]])[0]) if results.get('documents') else 0
            logger.info(f"ChromaDB: Found {num_found} documents for RAG context.")
            return results
        except Exception as e:
            logger.error(f"ChromaDB: Error during context retrieval: {str(e)}\n{traceback.format_exc()}")
            # Returns a structure that won't break downstream processing
            return {"documents": [[]], "metadatas": [[]], "distances": [[]], "ids": [[]]}
    
    def get_all_documents(self):
        """
        Get all documents from the collection
        
        Returns:
            Dictionary containing all documents and their metadata
        """
        return self.collection.get(
            include=["documents", "embeddings", "metadatas"]
        )
