INPUT_PATH = "../data/telecom_churn.csv"
OUTPUT_PATH = "../output/processed_telecom_churn.csv"
DB_USER = "postgres"
DB_PASSWORD = "postgres123"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "telecom_etl_db"
ENVIRONMENT = "local"

from dotenv import load_dotenv
import os 
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSOWRD = os.getenv("DB_PASSOWRD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
