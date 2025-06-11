import logging
import os
import re
import time
from dataclasses import dataclass, field
from typing import List, Optional
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup # type: ignore

from settings import BASE_URL, ROOT_FOLDER, MONTHS_MAPPING

def setup_logging() -> None:
    """Configures logging for the downloader."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('ecobici.log'),
            logging.StreamHandler()
        ]
    )
    
@dataclass
class CsvFileInfo:
    """Stores information about a CSV file to download.

    Attributes:
        url (str): Full URL of the CSV file.
        normalized_date (str): Normalized date in YYYY-MM format.
        year (str): Year extracted from the date.
        month (str): Month extracted from the date.
        downloaded (bool): Download status (default False).
    """
    url: str
    normalized_date: str
    year: str
    month: str
    downloaded: bool = field(default=False)

class Config:
    """Handles application configuration."""
    def __init__(self) -> None:
        self.base_url: str = BASE_URL
        self.root_folder: str = ROOT_FOLDER
        self.timeout: int = 10
        self.max_retries: int = 3
        self.retry_delay: int = 2

class EcobiciDataDownloader:
    """Main class for downloading Ecobici data."""

    DATE_PATTERNS = [
        re.compile(r'(\d{4})[_-](\d{1,2})$'),  # YYYY_MM o YYYY-MM
        re.compile(r'(\d{4})[_-]([a-záéíóú]+)$', re.IGNORECASE),  # YYYY_Mon (al final)
        re.compile(r'(\d{4})[-_](\d{2})[-_](\w+)$'),  # YYYY-MM-DD_suffix
        re.compile(r'(\d{4})(\d{2})$'),  # YYYYMM
        re.compile(r'(\d{4})[_-](\d{2})'),  # YYYY_MM (más flexible)
        re.compile(r'(\d{4})[_-]([a-záéíóú]+)', re.IGNORECASE),  # YYYY_Mon en cualquier parte
    ]

    def __init__(self, config: Config) -> None:
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'EcobiciDataDownloader/1.0'})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def get_csv_urls(self) -> List[str]:
        """Gets all CSV file URLs from the base page.

        Returns:
            List[str]: List of absolute CSV file URLs found.

        Raises:
            requests.RequestException: If the HTTP request fails.
        """
        try:
            response = self.session.get(self.config.base_url, timeout=self.config.timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            urls: List[str] = []
            for url in soup.find_all("a", href=True):
                href = url["href"]
                if href.endswith(".csv"):
                    urls.append(urljoin(self.config.base_url, href))
            return urls
        except requests.RequestException as e:
            logging.error(f"Error getting urls: {e}")
            return []

    def extract_date_from_url(self, url: str) -> str:
        """Extracts and normalizes the date from the filename in the URL.

        Tries several patterns to support filenames like:
        - 202209
        - datos_abiertos_2024_03-1-1
        - 2024-03
        - 2024_mar
        - 2024-03-01_extra
        """
        filename = os.path.splitext(os.path.basename(url))[0].lower()
        for pattern in self.DATE_PATTERNS:
            match = pattern.search(filename)
            if match:
                if pattern == self.DATE_PATTERNS[1]:
                    month = MONTHS_MAPPING.get(match.group(2)[:3], '00')
                    return f"{match.group(1)}-{month}"
                return f"{match.group(1)}-{match.group(2).zfill(2)}"
        logging.warning(f"Could not extract date from: {filename}")
        return None

    def create_folder(self, folder_name: str) -> None:
        """Creates a folder if it does not exist."""
        os.makedirs(folder_name, exist_ok=True)
        logging.debug(f"Ensured folder exists: {folder_name}")

    def download_csv(self, file_info: CsvFileInfo) -> None:
        """Downloads a CSV file and saves it locally.

        Args:
            file_info (CsvFileInfo): Information about the file to download.

        Raises:
            requests.RequestException: If the download fails.
            OSError: If there are problems writing the file.
        """
        if file_info.year == '0000':
            logging.warning(f"Skipping invalid year: {file_info.year} for URL: {file_info.url}")
            return

        folder_path = os.path.join(self.config.root_folder, file_info.year)
        filename = f"{file_info.normalized_date}.csv"
        file_path = os.path.join(folder_path, filename)

        try:
            if os.path.exists(file_path):
                logging.debug(f"File already exists: {file_path}")
                file_info.downloaded = True
                return

            os.makedirs(folder_path, exist_ok=True)
            response = self.session.get(file_info.url, timeout=self.config.timeout)
            response.raise_for_status()

            with open(file_path, 'wb') as f:
                f.write(response.content)
                file_info.downloaded = True
                logging.info(f"Downloaded: {file_path}")

        except requests.RequestException as e:
            logging.error(f"Download failed for {file_info.url}: {str(e)}")
        except OSError as e:
            logging.error(f"File write error for {file_path}: {str(e)}")

def generate_report(files: List[CsvFileInfo], root_folder: str) -> None:
    """Generates a CSV report of the download process."""
    df_report = pd.DataFrame([f.__dict__ for f in files])
    df_report.to_csv(os.path.join(root_folder, "ecobici_download_report.csv"), index=False)

