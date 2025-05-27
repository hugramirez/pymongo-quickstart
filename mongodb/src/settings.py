import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB connection string from environment variables
MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    print("Error: MONGODB_URI environment variable is not set.")
    sys.exit(1)

MONGODB_DBNAME = os.getenv("MONGODB_DBNAME")
if not MONGODB_DBNAME:
    print("Error: MONGODB_DBNAME environment variable is not set.")
    sys.exit(1)
