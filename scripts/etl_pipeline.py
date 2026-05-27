import pandas as pd
import logging
from config import INPUT_PATH, OUTPUT_PATH
from datetime import datetime
logging.basicConfig(
    filename="../logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
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
        return df
    #save output 
    def load_data(df):
        logging.info("Saving transformed data...")
        df.to_csv(OUTPUT_PATH,index = False)
        return df
  #-----------main------------------
    def main():
        df=extract_data()
        df=clean_data(df)
        df=transform_data(df)
        load_data(df)
        print("ETL pipeline completed successfully...")
    if __name__ == "__main__":
        print("Script started")
        main()
except Exception as e:
    print(f"Pipeline failed due to error: {e}")

