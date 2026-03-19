import pymongo
import os
from dotenv import load_dotenv
import certifi
from networksecurity.logging.logger import get_logger
from networksecurity.exception.exception import NetworkSecurityException
import pandas as pd
import sys

push_data_logger = get_logger("push_data_logger")

load_dotenv()

class Network_Data_Extract:
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(os.getenv("MONGO_URI"), tlsCAFile=certifi.where())
            push_data_logger.info("MongoDB client initialized successfully.")
        except Exception as e:
            push_data_logger.error(f"Failed to initialize MongoDB client: {e}")
            raise NetworkSecurityException("Failed to initialize MongoDB client", sys) from e

    def data_pusher(self, data_path :str ,database_name :str ,collection_name :str):
        try:
            data = pd.read_csv(data_path)
            data.reset_index(drop=True, inplace=True)
            db=self.client[database_name]
            collection = db[collection_name]
            collection.insert_many(data.to_dict('records'))
            print(len(data))
            push_data_logger.info(f"Data pushed successfully to {database_name}.{collection_name}")
        except Exception as e:
            push_data_logger.error(f"Failed to push data to {database_name}.{collection_name}: {e}")
            raise NetworkSecurityException(f"Failed to push data to {database_name}.{collection_name}", sys) from e


if __name__ == "__main__":
    try:
        FILE_PATH = r"D:\MLOPS\Network_Security2\Network_Security2\Network_Data\phisingData.csv"
        DATABASE_NAME = "Network_Security"
        COLLECTION_NAME = "Data"
        data_extractor = Network_Data_Extract()
        data_extractor.data_pusher(data_path=FILE_PATH, database_name=DATABASE_NAME, collection_name=COLLECTION_NAME)
    except NetworkSecurityException as e:
        ra
        push_data_logger.error(f"An error occurred: {e}")

