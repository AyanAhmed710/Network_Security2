from networksecurity.entity.artifact_entity import DataIngestionArtifact ,DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig, TrainingPipelineConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import get_logger
import os
import sys
from scipy.stats import ks_2samp
from networksecurity.constants import training_pipeline
from networksecurity.utils import read_yaml_file ,write_yaml_file
import pandas as pd
data_validation_logger = get_logger("DataValidation")

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        self.data_validation_config = data_validation_config
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_schma=read_yaml_file(training_pipeline.SCHEMA_FILE_PATH)


    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            data = pd.read_csv(file_path)
            return data
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def validate_schema(self, df: pd.DataFrame, dataset_name: str) -> bool:
        try:
            data_validation_logger.info(f"Validating schema for {dataset_name} dataset")
            expected_columns = self.data_schma["columns"]
            missing_columns = [col for col in expected_columns if col not in df.columns]
            if missing_columns:
                raise NetworkSecurityException(f"{dataset_name} dataset is missing columns: {missing_columns}", sys)
            
            expected_numerical_columns = self.data_schma["numerical_columns"]
            for col in expected_numerical_columns:
                if col in df.columns:
                    if not pd.api.types.is_numeric_dtype(df[col]):
                        raise NetworkSecurityException(f"{dataset_name} dataset column '{col}' is expected to be numerical", sys)
                else:
                    raise NetworkSecurityException(f"{dataset_name} dataset is missing expected numerical column: '{col}'", sys)
            data_validation_logger.info(f"{dataset_name} dataset schema validation successful")
            return True
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    
        

    def validate_data_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame ,threshold=0.05) -> bool:
        try:
            data_validation_logger.info("Validating data drift between training and testing datasets")
            base_columns = base_df.columns
            status= True

            report={}
            
            for column in base_columns:
                base_column = base_df[column]
                current_column = current_df[column]

                p_value = float(ks_2samp(base_column, current_column).pvalue)

                if p_value <= threshold:
                    is_found=True
                    status =False
                    data_validation_logger.warning(f"Data drift detected in column '{column}' with p-value: {p_value}")

                else:
                    is_found=False
                    

                report.update({
                    column: {
                        "p_value": p_value,
                        "is_found": is_found
                    }
                })

            os.makedirs(self.data_validation_config.drift_report_dir, exist_ok=True)

            write_yaml_file(self.data_validation_config.drift_report_file_path, report)



            
            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    



    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            data_validation_logger.info("Starting data validation")
            # Load the training and testing datasets
            train_df = self.read_data(self.data_ingestion_artifact.train_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.test_file_path)

            # Validate the datasets against the schema
            status =None
            if not self.validate_schema(train_df, "train"):
                return (f"There is some issue with the train dataset schema validation")
            if not self.validate_schema(test_df, "test"):
                return (f"There is some issue with the test dataset schema validation")
            
            # Validate data drift between training and testing datasets
            status = self.validate_data_drift(train_df, test_df)

            os.makedirs(self.data_validation_config.valid_dir, exist_ok=True)
            os.makedirs(self.data_validation_config.invalid_dir, exist_ok=True)

            if status == True:
                train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False)
                test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False)
                data_validation_logger.info("Data validation successful. Valid datasets saved.")

            else:
                train_df.to_csv(self.data_validation_config.invalid_train_file_path, index=False)
                test_df.to_csv(self.data_validation_config.invalid_test_file_path, index=False)
                data_validation_logger.warning("Data validation failed. Invalid datasets saved.")


            return DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
                
            


            

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        