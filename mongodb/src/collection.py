from typing import Any, List, Optional
from pymongo import MongoClient, collection
from pymongo.errors import PyMongoError
from settings import MONGODB_URI, MONGODB_DBNAME
import logging

def setup_logging() -> None:
    """Configures logging for the downloader."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('mongodb.log'),
            logging.StreamHandler()
        ]
    )
class MongoCollectionManager:
    """Class to manage MongoDB collections using PyMongo.

    Provides methods to create, delete, list, and use collections.
    """

    def __init__(self, uri: str, db_name: str) -> None:
        """Initializes the MongoCollectionManager.

        Args:
            uri (str): MongoDB connection URI.
            db_name (str): Name of the database to use.
        """
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def list_collections(self) -> List[str]:
        """Lists all collection names in the database.

        Returns:
            List[str]: List of collection names.
        """
        return self.db.list_collection_names()

    def create_collection(self, name: str) -> Optional[collection.Collection]:
        """Creates a new collection.

        Args:
            name (str): Name of the collection to create.

        Returns:
            Collection or None: The created collection or None if it exists.
        """
        if name in self.db.list_collection_names():
            return None
        try:
            return self.db.create_collection(name)
        except PyMongoError as e:
            print(f"Error creating collection: {e}")
            return None

    def drop_collection(self, name: str) -> bool:
        """Drops a collection.

        Args:
            name (str): Name of the collection to drop.

        Returns:
            bool: True if dropped, False otherwise.
        """
        if name not in self.db.list_collection_names():
            return False
        try:
            self.db.drop_collection(name)
            return True
        except PyMongoError as e:
            print(f"Error dropping collection: {e}")
            return False

    def get_collection(self, name: str) -> Optional[collection.Collection]:
        """Gets a collection by name.

        Args:
            name (str): Name of the collection.

        Returns:
            Collection or None: The collection object or None if not found.
        """
        if name in self.db.list_collection_names():
            return self.db[name]
        return None

    def insert_one(self, collection_name: str, document: dict) -> Optional[Any]:
        """Inserts a single document into a collection.

        Args:
            collection_name (str): Name of the collection.
            document (dict): Document to insert.

        Returns:
            InsertOneResult or None: The result of the insert operation.
        """
        coll = self.get_collection(collection_name)
        if coll is not None:
            try:
                return coll.insert_one(document)
            except PyMongoError as e:
                print(f"Error inserting document: {e}")
        return None
    
    def insert_many(self, collection_name: str, documents: List[dict]) -> Optional[Any]:
        """Inserts multiple documents into a collection.

        Args:
            collection_name (str): Name of the collection.
            documents (List[dict]): List of documents to insert.

        Returns:
            InsertManyResult or None: The result of the insert operation.
        """
        coll = self.get_collection(collection_name)
        if coll is not None:
            try:
                return coll.insert_many(documents)
            except PyMongoError as e:
                print(f"Error inserting documents: {e}")
        return None

    def find(self, collection_name: str, query: dict = {}) -> List[dict]:
        """Finds documents in a collection.

        Args:
            collection_name (str): Name of the collection.
            query (dict, optional): Query filter. Defaults to {}.

        Returns:
            List[dict]: List of documents found.
        """
        coll = self.get_collection(collection_name)
        if coll is not None:
            try:
                return list(coll.find(query))
            except PyMongoError as e:
                print(f"Error finding documents: {e}")
        return []

