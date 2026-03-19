from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from networksecurity.logging.logger import get_logger
from networksecurity.exception.exception import NetworkSecurityException
import sys

main_logger = get_logger("Main")

if __name__ == "__main__":
    try :
        data_ingestion_config = DataIngestionConfig(TrainingPipelineConfig())
        data_ingestion =DataIngestion(data_ingestion_config)
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        main_logger.info("Data ingestion completed successfully.")



    except Exception as e:        
        main_logger.error(f"An error occurred: {e}")
        raise NetworkSecurityException(e,sys)

