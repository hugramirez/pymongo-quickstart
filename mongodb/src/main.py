import logging
from typing import Any

from settings import MONGODB_URI, MONGODB_DBNAME
from collection import MongoCollectionManager

import pandas as pd

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

def main() -> None:
    """Main function to manage MongoDB collections."""
    setup_logging()
    logging.info("Starting MongoDB collection manager...")

    manager = MongoCollectionManager(MONGODB_URI, MONGODB_DBNAME)

    # Create a sample collection
    # collection_name = "ecobici_test"
    # created = manager.create_collection(collection_name)
    # if created is not None:
    #     logging.info(f"Collection created: {collection_name}")
    # else:
    #     logging.info(f"The collection already exists: {collection_name}")

    # Insert a sample document
    # doc = {"name": "Ecobici", "year": 2025}
    # result = manager.insert_one(collection_name, doc)
    # if result is not None:
    #     logging.info(f"Document inserted with _id: {result.inserted_id}")

    # Insert multiple documents
    collection_name = "logs"
    base_path = "/Users/psf/Github/pymongo-quickstart/ecobici_data/"
    docs_many = pd.read_csv(f"{base_path}ecobici_download_report.csv").to_dict(orient='records')
    result_many = manager.insert_many(collection_name, docs_many)
    if result_many is not None:
        logging.info(f"Number of documents inserted: {len(result_many.inserted_ids)}")
        # logging.info(f"Documents inserted with _ids: {result_many.inserted_ids}")


    # List collections
    collections = manager.list_collections()
    logging.info(f"Collections in the database: {collections}")

    # Find documents
    docs = manager.find(collection_name, {"name": "Ecobici"})
    logging.info(f"Documents found: {docs}")

    # Delete the sample collection
    # if manager.drop_collection(collection_name):
    #     logging.info(f"Collection deleted: {collection_name}")
    # else:
    #     logging.info(f"Could not delete the collection: {collection_name}")

    # logging.info("MongoDB collection manager finished.")

if __name__ == "__main__":
    main()
