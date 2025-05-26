from typing import Final

BASE_URL: Final[str] = "https://ecobici.cdmx.gob.mx/datos-abiertos/"
ROOT_FOLDER: Final[str] = "ecobici_data" # ecobici_data - ecobici_historic_csv
MONTHS_MAPPING: Final[dict] = {
    'jan': '01', 'feb': '02', 'mar': '03', 
    'apr': '04', 'may': '05', 'jun': '06',
    'jul': '07', 'aug': '08', 'sep': '09',
    'oct': '10', 'nov': '11', 'dec': '12'
}