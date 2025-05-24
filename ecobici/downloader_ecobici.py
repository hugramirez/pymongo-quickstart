import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import re
import pandas as pd
import numpy as np
from settings import *
import time

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class EcobiciDataDownloader:

    def __init__(self, base_url, dest_folder):
        self.base_url = base_url
        self.dest_folder = dest_folder
        # self.create_folder(dest_folder)

    def get_csv_urls(self):
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            urls = []
            for url in soup.find_all("a", href=True):
                href = url["href"]
                if href.endswith(".csv"):
                    urls.append(urljoin(self.base_url, href))
            return urls
        except Exception as e:
            logging.error(f"Error getting urls: {e}")
            return []
        
    def extract_date_from_url(self, url):
        filename = url.split('/')[-1].replace('.csv', '')
        match = re.search(r'(\d{4})[_-](\d{1,2})$', filename)
        if match:
            return f"{match.group(1)}-{int(match.group(2)):02d}"
        match = re.search(r'(\d{4})[_-]([a-z]+)', filename)
        if match:
            mes = months.get(match.group(2).lower())
            if mes:
                return f"{match.group(1)}-{mes}"
        match = re.search(r'(\d{4})[-_](\d{2})[-_](\w+)', filename)
        if match:
            return f"{match.group(1)}-{match.group(2)}"
        return '0000-00'

    def create_folder(self, folder_name):
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            logging.info(f"Created folder: {folder_name}")
        else:
            logging.info(f"Folder already exists: {folder_name}")

    def download_csv(self, df, index, url, normalized_date, year):
        if year == '0000':
            logging.info(f"Skipping invalid year: {year} for URL: {url}")
            return
        
        folder_path = os.path.join(self.dest_folder, year)
        filename = f"{normalized_date}.csv"
        file_path = os.path.join(folder_path, filename)

        if os.path.exists(file_path):
            logging.info(f"File already exists, skipping: {file_path}")
            return
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                f.write(response.content)
                df.at[index, 'downloaded'] = True
                logging.info(f"Downloaded and saved: {file_path}")
        except Exception as e:
            logging.error(f"Failed to download {url}: {e}")

    
    

def main():
    start_time = time.time()
    downloader = EcobiciDataDownloader(BASE_URL, ROOT_FOLDER)
    urls = downloader.get_csv_urls()
    if not urls:
        logging.info("No ecobici csv files found.")
        return
    logging.info(f"Found {len(urls)} ecobici csv files.")

    ecobicis = pd.DataFrame({'url': urls})
    ecobicis['normalized_date'] = ecobicis['url'].apply(downloader.extract_date_from_url)
    ecobicis = ecobicis.sort_values('normalized_date')
    ecobicis.to_csv(os.path.join(ROOT_FOLDER, "ecobici_urls.csv"), index=False)
    ecobicis['year'] = ecobicis['normalized_date'].str[:4]
    ecobicis['month'] = ecobicis['normalized_date'].str[5:7]

    years = ecobicis['year'].unique()
    for year in years:
        year_folder = os.path.join(ROOT_FOLDER, year)
        downloader.create_folder(year_folder)

    ecobicis['downloaded'] = False
    for index, row in ecobicis.iterrows():
        url = row['url']
        normalized_date = row['normalized_date']
        year = row['year']
        downloader.download_csv(ecobicis, index, url, normalized_date, year)

    ecobicis['downloaded'] = ecobicis['downloaded'].replace({False: True})
    ecobicis.to_csv(f"{ROOT_FOLDER}/ecobici_download_report.csv", index=False)

    elapsed_time = time.time() - start_time
    logging.info(f"Execution time: {elapsed_time:.2f} seconds")

    # import ace_tools_open as tools; tools.display_dataframe_to_user(name="Normalized Ecobici URLs", dataframe=ecobicis) # type: ignore


if __name__ == "__main__":
    main()