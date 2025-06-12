#░█▀▀░█░█░▀█▀░█▀▄░█▀█░█▀▀░▀█▀░▀█▀░█▀█░█▀█░░░█▄█░█▀█░█▀▄░█░█░█░░░█▀▀
#░█▀▀░▄▀▄░░█░░█▀▄░█▀█░█░░░░█░░░█░░█░█░█░█░░░█░█░█░█░█░█░█░█░█░░░█▀▀
#░▀▀▀░▀░▀░░▀░░▀░▀░▀░▀░▀▀▀░░▀░░▀▀▀░▀▀▀░▀░▀░░░▀░▀░▀▀▀░▀▀░░▀▀▀░▀▀▀░▀▀▀

from typing import List, Dict, Any
import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from config.settings import COLUMN_MAPPING
from concurrent.futures import ThreadPoolExecutor
import time


load_dotenv()

class EcobiciDataExtractor:
    
    def __init__(self, source: str, subfolder: str = "ecobici/ecobici_data"):
        self.source = source
        self.subfolder = subfolder

    def list_csv_files(self) -> List[Path]:

        if not self.source:
            raise ValueError("The environment variable BASE_PATH is not defined.")
        
        folder = Path(self.source) / self.subfolder
        if not folder.exists():
            raise FileNotFoundError(f"The folder {folder} does not exist.")
        
        year_dirs = [f for f in folder.iterdir() if f.is_dir() and f.name.isdigit() and len(f.name) == 4]
        file_paths = []
        for year_dir in year_dirs:
            file_paths.extend([file for file in year_dir.glob("*.csv")])

        return file_paths

    def standardize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]
        df = df.rename(columns=COLUMN_MAPPING)
        df = df.loc[:, ~df.columns.str.contains('^unnamed', case=False)]
        df = df.loc[:, ~df.columns.duplicated()]
        return df

    def read_file_pandas(self, file_path: Path) -> pd.DataFrame:
        if file_path.suffix == ".csv":
            chunks = pd.read_csv(file_path, chunksize=100_000, low_memory=False)
            df = pd.concat((self.standardize_columns(chunk) for chunk in chunks), ignore_index=True)
        else:
            raise ValueError(f"Unsupported format: {file_path.suffix}")
        return df
    
    def safe_read_file(self, file_path: Path):
        try:
            return self.read_file_pandas(file_path)
        except Exception as e:
            print(f"Error al leer {file_path.name}: {e}")
            return pd.DataFrame()

    def read_files_in_parallel_pandas(self, file_paths, max_workers=4) -> pd.DataFrame:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = list(executor.map(self.safe_read_file, file_paths))
        results = [df for df in results if not df.empty]
        return pd.concat(results, ignore_index=True)


# def main():
#     source = os.getenv('BASE_PATH')
#     max_workers = int(os.getenv('MAX_WORKERS', 4))
#     extractor = EcobiciDataExtractor(source)
#     try:
#         start_time = time.time()
#         file_paths = extractor.list_csv_files()
#         if file_paths:
#             df = extractor.read_files_in_parallel_pandas(file_paths, max_workers=max_workers)
#             # df.to_csv("ecobici_data.csv", index=False)
#             print(df.info())
#         end_time = time.time()
#         print(f"{end_time - start_time:.2f} seconds elapsed.")
#     except FileNotFoundError as e:
#         print(e)

# if __name__ == "__main__":
#     main()