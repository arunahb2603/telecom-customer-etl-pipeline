import pandas as pd
import logging
import time
from config import INPUT_PATH, OUTPUT_PATH, DB_USER, DB_PASSWORD,DB_HOST, DB_PORT, DB_NAME, ENVIRONMENT
from datetime import datetime
from sqlalchemy import create_engine
logging.basicConfig(
    filename="../logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
) 
logging.info(f"Running pipeline in {ENVIRONMENT} environment") 

 #read csv file 
  
try:
    def extract_data():
        print("Starting ETL pipeline...")
        #print("Reading CSV input file...")
        logging.info("Reading CSV input file")
        df= pd.read_csv(INPUT_PATH)
        return df

    # ----- STEP 1 -----Basic Data cleaning -----
    #remove duplicate rows
    def clean_data(df):
        logging.info("Cleaning data...")
        #Track duplicate data removed
        initial_count = len(df)
        df=df.drop_duplicates()
        final_count=len(df)
        logging.info(f"Removed {initial_count-final_count} duplicate rows")
        #remove rows with null values
        df=df.dropna()
        #restructure column names with lowercase and replace space with underscore
        df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
        #print top 5 rows
        #print(df.head())
        #check dataset shape
        #print("\n Dataset shape:")
        #print(df.shape)
        #prints column in index
        #print(df.columns)

        #Data Validation checks
        if df.empty:
            raise ValueError("input dataframe is empty")
        if "customer_id" not in df.columns:
            raise ValueError("Customer_id column is missing")
        return df

    # ----- STEP 2 -----ADD transformation logic-----

    #convert date registration to datetime registration
    def transform_data(df):
        df["pipeline_runtime"] = datetime.now()
        logging.info("Applying transformations...")
        df["date_of_registration"] = pd.to_datetime(df["date_of_registration"])

        #alert flag for high data usage

        df["high_data_user"] = df["data_used"] >5000

        #age group categorisation

        df["age_group"] = pd.cut(
            df["age"],
            bins = [0,18,30,50,100],
            labels = ["Teen", "Young adult", "Adult", "Senior"]
        )

        #data usage group

        df["data_usage_type"] = pd.cut(
            df["data_used"],
            bins = [float('-inf'), 0, 1000,5000, 10000, float('inf')],
            labels = ["Invalid usage", "Low usage","Medium usage", "Heavy usage", "Very high usage"]
        )
        #print(df[["data_used","data_usage_type"]].head(10)) -- top 10
        logging.info(f"Total rows processed: {len(df)}")
        logging.info(f"Total columns processed: {len(df.columns)}")
        logging.info(f"Churn customers: {df['churn'].value_counts().to_dict()}")
        df = df.drop_duplicates(subset=["customer_id"])
        return df
    #save output 
    def load_data(df):
        logging.info("Saving transformed data...")
        df.to_csv(OUTPUT_PATH,index = False)
        
    #ETL_DB connectivity and sample output
        query = "SELECT * FROM telecom_customers LIMIT 5"
        sample_df = pd.read_sql (query, engine)
        print(sample_df)
    #row count verification
        row_count_query = "SELECT * FROM telecom_customers"
        count_df = pd.read_sql(row_count_query, engine)
        print(count_df)
        return df
    def load_to_postgres(df):
        logging.info("Loading data into PostgreSQL...")
        df.to_sql(
            name="telecom_customers",
            con=engine,
            if_exists="replace",
            index=False)
        logging.info("Data loaded to SQL successfully")
  #-----------main------------------
    def main():
        df=extract_data()
        df=clean_data(df)
        df=transform_data(df)
        logging.info(df.describe().to_string())
        load_data(df)
        load_to_postgres(df)
        print("ETL pipeline completed successfully...")
        
    if __name__ == "__main__":
        print("Script started")
        start_time = time.time()
        main()
        end_time = time.time()
        logging.info(f"Pipeline execution time: {end_time - start_time} seconds")
        
        
except Exception as e:
    print(f"Pipeline failed due to error: {e}")

