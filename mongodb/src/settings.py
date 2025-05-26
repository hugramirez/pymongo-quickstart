import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB connection string from environment variables
MONGODB_URI = os.getenv("MONGODB_URI")
print(f"MongoDB connection string: {MONGODB_URI}")
