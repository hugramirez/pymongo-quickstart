from __future__ import annotations
import os
import time
import logging
from typing import List
from batch_ecobici import EcobiciDataDownloader, CsvFileInfo, Config, generate_report, setup_logging

def main() -> None:
    """Main script function."""
    setup_logging()
    config = Config()

    try:
        with EcobiciDataDownloader(config) as downloader:
            start_time = time.monotonic()

            if not os.path.exists(config.root_folder):
                os.makedirs(config.root_folder)

            urls = downloader.get_csv_urls()
            if not urls:
                logging.warning("No CSV files found.")
                return

            files: List[CsvFileInfo] = []
            for url in urls:
                normalized_date = downloader.extract_date_from_url(url)
                year = normalized_date[:4]
                month = normalized_date[5:7]
                files.append(CsvFileInfo(url, normalized_date, year, month))

            for year in set(f.year for f in files):
                downloader.create_folder(os.path.join(config.root_folder, year))

            for file_info in files:
                downloader.download_csv(file_info)

            generate_report(files, config.root_folder)

            elapsed = time.monotonic() - start_time
            logging.info(f"Process completed in {elapsed:.2f} seconds")

    except Exception as e:
        logging.critical(f"Fatal error: {str(e)}", exc_info=True)
        raise SystemExit(1) from e

if __name__ == "__main__":
    main()