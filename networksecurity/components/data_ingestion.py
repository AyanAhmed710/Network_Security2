from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import get_logger
import os
import pymongo 
from sklearn.model_selection import train_test_split
import pandas as pd
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
from dotenv import load_dotenv
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import sys

load_dotenv()



data_ingestion_logger = get_logger("DataIngestion")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config


    def mongo_db_to_dataframe(self):
        try:
            data_ingestion_logger.info("Connecting to MongoDB and fetching data.")
            client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
            db = client[self.data_ingestion_config.database_name]
            collection = db[self.data_ingestion_config.collection_name]
            data = list(collection.find())
            df = pd.DataFrame(data)

            if "_id" in df.columns:
                df.drop("_id", axis=1, inplace=True)

            data_ingestion_logger.info("Data fetched from MongoDB successfully.")
            return df
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def store_data_in_feature_store(self, df: pd.DataFrame):
        try:
            data_ingestion_logger.info("Storing data in feature store.")
            os.makedirs(os.path.dirname(self.data_ingestion_config.raw_data_file_path), exist_ok=True) #Here os.path.dirname is used to get the directory path from the file path and os.makedirs is used to create the directory if it does not exist.
            df.to_csv(self.data_ingestion_config.raw_data_file_path, index=False)
            data_ingestion_logger.info("Data stored in feature store successfully.")
        except Exception as e:
            raise NetworkSecurityException(e , sys)
        
    def split_data_as_train_test(self, df: pd.DataFrame):
        try:
            data_ingestion_logger.info("Splitting data into train and test sets.")
            train_df, test_df = train_test_split(df, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=self.data_ingestion_config.random_state)
            os.makedirs(self.data_ingestion_config.ingested_dir, exist_ok=True)
            train_df.to_csv(self.data_ingestion_config.train_file_path, index=False)
            test_df.to_csv(self.data_ingestion_config.test_file_path, index=False)
            data_ingestion_logger.info("Data split into train and test sets successfully.")
        except Exception as e:
            raise NetworkSecurityException(e ,sys)



    def initiate_data_ingestion(self):
        try:
            data_ingestion_logger.info("Starting data ingestion process.")

            df = self.mongo_db_to_dataframe()

            self.store_data_in_feature_store(df)

            self.split_data_as_train_test(df)

            self.data_ingestion_artifact = DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.raw_data_file_path,
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path
            )

            data_ingestion_logger.info("Data ingestion process completed successfully.")

            return self.data_ingestion_artifact


            
            
           
           
            
        except Exception as e:
            raise NetworkSecurityException(e , sys)