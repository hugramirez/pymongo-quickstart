import os
from dotenv import load_dotenv
import time
from .extract.extraction import EcobiciDataExtractor
from .transform.transformation import EcobiciDataTransformer

load_dotenv()

def main():
    source = os.getenv('BASE_PATH')
    max_workers = int(os.getenv('MAX_WORKERS', 4))
    extractor = EcobiciDataExtractor(source)
    transformer = EcobiciDataTransformer()
    try:
        start_time = time.time()
        extractor.get_station_coordinates()
        file_paths = extractor.list_csv_files()
        if file_paths:
            df = extractor.read_files_in_parallel_pandas(file_paths[:5], max_workers=max_workers)
            # df.to_csv("ecobici_data.csv", index=False)
            # print(df.info())
        transformed_df = transformer.transform_data(df)
        print(transformed_df.info())
        print(transformed_df.head(5)) #.transpose())
        end_time = time.time()
        print(f"{end_time - start_time:.2f} seconds elapsed.")
    except FileNotFoundError as e:
        print(e)

if __name__ == "__main__":
    main()