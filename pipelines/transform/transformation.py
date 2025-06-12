import os
from dotenv import load_dotenv
from typing import List, Dict, Any
import pandas as pd
from pathlib import Path


load_dotenv()

import re

class EcobiciDataTransformer:

    def __init__(self):
        pass

    @staticmethod
    def extract_hour_minute_vectorized(series: pd.Series) -> pd.Series:
        if pd.api.types.is_datetime64_any_dtype(series):
            return series.dt.strftime('%H:%M')
        return series.astype(str).str.extract(r'(\d{1,2}:\d{2})')[0]

    def transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        dataset = df.copy()
        dataset = (
            dataset
            .rename(columns={
                'genero_usuario': 'gender',
                'edad_usuario': 'age',
                'fecha_retiro': 'start_date',
                'fecha_arribo': 'end_date',
                'hora_retiro': 'start_time',
                'hora_arribo': 'end_time',
                'ciclo_estacion_retiro': 'start_station_id',
                'ciclo_estacion_arribo': 'end_station_id',
                'bici': 'bike_id',
            })
        )
       
        dataset['start_date'] = pd.to_datetime(dataset['start_date'], errors='coerce').dt.date
        dataset['end_date'] = pd.to_datetime(dataset['end_date'], errors='coerce').dt.date

        if 'start_time' in dataset.columns:
            dataset['start_time'] = self.extract_hour_minute_vectorized(dataset['start_time'])
        if 'end_time' in dataset.columns:
            dataset['end_time'] = self.extract_hour_minute_vectorized(dataset['end_time'])

        if 'age' in dataset.columns:
            dataset['age'] = pd.to_numeric(dataset['age'], errors='coerce').astype('Int64')
        if 'gender' in dataset.columns:
            dataset['gender'] = dataset['gender'].astype('category')
        for col in ['bike_id', 'start_station_id', 'end_station_id']:
            if col in dataset.columns:
                dataset[col] = pd.to_numeric(dataset[col], errors='coerce').astype('Int64')
        
        dataset['start_date'] = pd.to_datetime(dataset['start_date'], errors='coerce').dt.strftime('%Y-%m-%d')
        dataset['end_date'] = pd.to_datetime(dataset['end_date'], errors='coerce').dt.strftime('%Y-%m-%d')
        
        return dataset