from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig ,DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.logging.logger import get_logger
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.components.data_validation import DataValidation
import sys

main_logger = get_logger("Main")

if __name__ == "__main__":
    try :
        # data_ingestion_config = DataIngestionConfig(TrainingPipelineConfig())
        # data_ingestion =DataIngestion(data_ingestion_config)
        # data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        # print(data_ingestion_artifact)
        # main_logger.info("Data ingestion completed successfully.")

        data_ingestion_artifact = DataIngestionArtifact(train_file_path=r"D:\MLOPS\Network_Security2\Network_Security2\Artifacts\2026-03-19-23-53-39\data_ingestion\ingested\train.csv",
                                                        test_file_path=r"D:\MLOPS\Network_Security2\Network_Security2\Artifacts\2026-03-19-23-53-39\data_ingestion\ingested\test.csv",
                                                        feature_store_file_path=r"D:\MLOPS\Network_Security2\Network_Security2\Artifacts\2026-03-19-23-53-39\data_ingestion\feature_store\phisingData.csv")

        main_logger.info("Starting data validation process.")
        data_validation_config = DataValidationConfig(TrainingPipelineConfig())
        data_validation = DataValidation(data_validation_config, data_ingestion_artifact)
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)
        main_logger.info("Data validation completed successfully.")



    except Exception as e:        
        main_logger.error(f"An error occurred: {e}")
        raise NetworkSecurityException(e,sys)

