import logging
import os
import zipfile
from typing import Optional

def setup_logging() -> None:
    """Configura el sistema de logging para el proceso de zipeado."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

def zip_ecobici_by_year(base_dir: str = 'ecobici_historic_csv', output_dir: str = 'ecobici_zips') -> None:
    """Crea archivos ZIP por año a partir de carpetas de datos Ecobici.

    Args:
        base_dir (str): Directorio base donde están los datos por año.
        output_dir (str): Directorio donde se guardarán los ZIPs.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for year in os.listdir(base_dir):
        year_path = os.path.join(base_dir, year)
        if os.path.isdir(year_path):
            zip_path = os.path.join(output_dir, f"{year}.zip")
            try:
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, _, files in os.walk(year_path):
                        for file in files:
                            full_path = os.path.join(root, file)
                            arcname = os.path.relpath(full_path, base_dir)
                            zipf.write(full_path, arcname)
                logging.info(f"Created zip for year {year}: {zip_path}")
            except Exception as e:
                logging.error(f"Error creating zip for year {year}: {e}")

if __name__ == "__main__":
    setup_logging()
    logging.info("Starting zipping process...")
    zip_ecobici_by_year()
    logging.info("Zipping process completed.")