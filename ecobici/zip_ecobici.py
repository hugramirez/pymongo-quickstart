import os
import zipfile
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

def zip_ecobici_by_year(base_dir='ecobici_historic_csv', output_dir='ecobici_zips'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for year in os.listdir(base_dir):
        year_path = os.path.join(base_dir, year)
        if os.path.isdir(year_path):
            zip_path = os.path.join(output_dir, f"{year}.zip")

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(year_path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        arcname = os.path.relpath(full_path, base_dir)
                        zipf.write(full_path, arcname)
            logging.info(f"Created zip for year {year}: {zip_path}")

if __name__ == "__main__":
    logging.info("Starting zipping process...")
    zip_ecobici_by_year()
    logging.info("Zipping process completed.")