import os
import dagshub
import sys


load_dotenv()

# Only set if not already defined in the environment (EC2 will have these pre-set)
if os.environ.get("DAGSHUB_USERNAME") and os.environ.get("DAGSHUB_TOKEN"):
    os.environ["MLFLOW_TRACKING_USERNAME"] = os.environ["DAGSHUB_USERNAME"]
    os.environ["MLFLOW_TRACKING_PASSWORD"] = os.environ["DAGSHUB_TOKEN"]

dagshub.init(repo_owner='sheikhayanahmad710', repo_name='Network_Security2', mlflow=True)
import io

# Fix Windows cp1252 encoding issue with MLflow emoji output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig ,DataValidationConfig ,DataTransformationConfig ,ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.logging.logger import get_logger
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from dotenv import load_dotenv
import sys
import os




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

        main_logger.info("Starting Data transformation process.")
        DataTransformationConfig = DataTransformationConfig(TrainingPipelineConfig())
        data_transformation = DataTransformation(DataTransformationConfig, data_validation_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        main_logger.info("Data transformation completed successfully.")


        main_logger.info("Starting model trainer process.")
        model_trainer_config = ModelTrainerConfig(TrainingPipelineConfig())
        model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        main_logger.info("Model trainer completed successfully.")



    except Exception as e:        
        main_logger.error(f"An error occurred: {e}")
        raise NetworkSecurityException(e,sys)

