import pandas as pd
 #read csv file 
  
try:
    print("Starting ETL pipeline...")
    print("Reading CSV input file...")
    df= pd.read_csv("data/telecom_churn.csv")

    # ----- STEP 1 -----Basic Data cleaning -----
    #remove duplicate rows
    print("Cleaning data...")
    df=df.drop_duplicates()
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

    # ----- STEP 2 -----ADD transformation logic-----

    #convert date registration to datetime registration
    print("Applying transformations...")
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
    #save output 
    print("Saving transformed data...")
    df.to_csv("output/processed_telecom_data.csv", index=False)
    print("ETL pipeline completed successfully...")

except Exception as e:
    print(f"Pipeline failed due to error: {e}")
    